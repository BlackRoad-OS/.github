"""
BlackRoad Agent Orchestrator

Coordinates multiple AI agents working together on tasks.
"""

import asyncio
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid


class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    ERROR = "error"


@dataclass
class AgentMessage:
    """Message sent between agents"""
    message_id: str
    from_agent: str
    to_agent: str
    content: str
    timestamp: datetime
    conversation_id: Optional[str] = None
    reply_to: Optional[str] = None
    message_type: str = "question"  # question, answer, notification, request


@dataclass
class Agent:
    """Represents an AI agent"""
    agent_id: str
    name: str
    config: Dict
    status: AgentStatus = AgentStatus.IDLE
    current_task: Optional[str] = None
    message_inbox: List[AgentMessage] = field(default_factory=list)
    conversation_history: Dict[str, List[AgentMessage]] = field(default_factory=dict)


class AgentOrchestrator:
    """
    Orchestrates multiple AI agents working together.
    
    Features:
    - Load agent configurations
    - Route tasks to appropriate agents
    - Enable agent collaboration
    - Track agent status and metrics
    - Facilitate agent-to-agent communication
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            # Default to a 'config' directory located alongside this module
            self.config_dir = Path(__file__).parent / "config"
        else:
            self.config_dir = Path(config_dir)
        self.agents: Dict[str, Agent] = {}
        self.conversations: Dict[str, List[AgentMessage]] = {}
        self.message_log: List[AgentMessage] = []
        self.load_agents()
    
    def load_agents(self):
        """Load all agent configurations"""
        if not self.config_dir.exists():
            print(f"⚠️  Config directory not found: {self.config_dir}")
            return
        
        for config_file in self.config_dir.glob("*.yaml"):
            try:
                with open(config_file) as f:
                    config = yaml.safe_load(f)
                
                agent_id = config["agent_id"]
                agent = Agent(
                    agent_id=agent_id,
                    name=config["name"],
                    config=config
                )
                self.agents[agent_id] = agent
                print(f"✅ Loaded agent: {agent.name} ({agent_id})")
            
            except Exception as e:
                print(f"❌ Failed to load {config_file}: {e}")
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get an agent by ID"""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[str]:
        """List all available agents"""
        return list(self.agents.keys())
    
    def route_task(self, task: str) -> str:
        """
        Route a task to the most appropriate agent.
        
        Uses keyword matching to determine which agent should handle the task.
        """
        task_lower = task.lower()
        
        # Coder keywords
        if any(kw in task_lower for kw in [
            "code", "function", "class", "bug", "fix", "refactor",
            "implement", "debug", "test", "python", "javascript"
        ]):
            return "coder"
        
        # Designer keywords
        if any(kw in task_lower for kw in [
            "design", "ui", "ux", "color", "palette", "layout",
            "component", "style", "css", "accessibility"
        ]):
            return "designer"
        
        # Ops keywords
        if any(kw in task_lower for kw in [
            "deploy", "docker", "kubernetes", "ci/cd", "pipeline",
            "infrastructure", "server", "cloud", "monitoring"
        ]):
            return "ops"
        
        # Docs keywords
        if any(kw in task_lower for kw in [
            "document", "readme", "tutorial", "guide", "api doc",
            "documentation", "explain", "write", "changelog"
        ]):
            return "docs"
        
        # Analyst keywords
        if any(kw in task_lower for kw in [
            "analyze", "metrics", "data", "statistics", "report",
            "trend", "anomaly", "performance", "insights"
        ]):
            return "analyst"
        
        # Default to coder for general tasks
        return "coder"
    
    def get_collaborators(self, agent_id: str, task: str) -> List[str]:
        """
        Determine which other agents should collaborate on a task.
        """
        agent = self.get_agent(agent_id)
        if not agent:
            return []
        
        collaborators = []
        
        # Check handoff triggers in agent config
        if "collaboration" in agent.config:
            handoff_triggers = agent.config["collaboration"].get("handoff_triggers", [])
            
            for trigger in handoff_triggers:
                pattern = trigger.get("pattern", "")
                target = trigger.get("target_agent")
                
                if pattern and target and pattern.lower() in task.lower():
                    if target not in collaborators:
                        collaborators.append(target)
        
        return collaborators
    
    async def send_message(
        self,
        from_agent_id: str,
        to_agent_id: str,
        content: str,
        message_type: str = "question",
        conversation_id: Optional[str] = None,
        reply_to: Optional[str] = None
    ) -> AgentMessage:
        """
        Send a message from one agent to another.
        
        Args:
            from_agent_id: ID of the sending agent
            to_agent_id: ID of the receiving agent
            content: Message content
            message_type: Type of message (question, answer, notification, request)
            conversation_id: Optional conversation thread ID
            reply_to: Optional ID of message being replied to
        
        Returns:
            AgentMessage object
        """
        from_agent = self.get_agent(from_agent_id)
        to_agent = self.get_agent(to_agent_id)
        
        if not from_agent or not to_agent:
            raise ValueError(f"Invalid agent IDs: {from_agent_id} or {to_agent_id}")
        
        # Create conversation ID if not provided
        if not conversation_id:
            conversation_id = f"{from_agent_id}-{to_agent_id}-{uuid.uuid4().hex[:8]}"
        
        # Create message
        message = AgentMessage(
            message_id=uuid.uuid4().hex,
            from_agent=from_agent_id,
            to_agent=to_agent_id,
            content=content,
            timestamp=datetime.now(),
            conversation_id=conversation_id,
            reply_to=reply_to,
            message_type=message_type
        )
        
        # Add to recipient's inbox
        to_agent.message_inbox.append(message)
        
        # Update conversation history for both agents
        if conversation_id not in from_agent.conversation_history:
            from_agent.conversation_history[conversation_id] = []
        if conversation_id not in to_agent.conversation_history:
            to_agent.conversation_history[conversation_id] = []
        
        from_agent.conversation_history[conversation_id].append(message)
        to_agent.conversation_history[conversation_id].append(message)
        
        # Track globally
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        self.conversations[conversation_id].append(message)
        self.message_log.append(message)
        
        print(f"💬 {from_agent.name} → {to_agent.name}: {content[:50]}...")
        
        return message
    
    async def ask_agent(
        self,
        asking_agent_id: str,
        target_agent_id: str,
        question: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Have one agent ask another agent a question.
        
        Args:
            asking_agent_id: ID of the agent asking
            target_agent_id: ID of the agent being asked
            question: The question to ask
            context: Optional context about the question
        
        Returns:
            Response from the target agent
        """
        asking_agent = self.get_agent(asking_agent_id)
        target_agent = self.get_agent(target_agent_id)
        
        if not asking_agent or not target_agent:
            return {
                "success": False,
                "error": "Invalid agent IDs"
            }
        
        print(f"\n🤔 {asking_agent.name} asks {target_agent.name}:")
        print(f"   Q: {question}")
        
        # Send question message
        question_msg = await self.send_message(
            from_agent_id=asking_agent_id,
            to_agent_id=target_agent_id,
            content=question,
            message_type="question"
        )
        
        # Have target agent process the question
        # Prepare enriched question with context
        enriched_question = question
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            enriched_question = f"{question}\n\nContext:\n{context_str}"
        
        # Target agent processes the question
        response = await self.execute_task(enriched_question, target_agent_id)
        
        # Send answer back
        answer_msg = await self.send_message(
            from_agent_id=target_agent_id,
            to_agent_id=asking_agent_id,
            content=response.get("response", ""),
            message_type="answer",
            conversation_id=question_msg.conversation_id,
            reply_to=question_msg.message_id
        )
        
        print(f"   A: {response.get('response', '')[:80]}...")
        
        return {
            "success": True,
            "question": question,
            "answer": response.get("response", ""),
            "conversation_id": question_msg.conversation_id,
            "question_message": question_msg,
            "answer_message": answer_msg,
            "target_agent": target_agent.name
        }
    
    def get_conversation(self, conversation_id: str) -> List[AgentMessage]:
        """Get all messages in a conversation"""
        return self.conversations.get(conversation_id, [])
    
    def get_agent_conversations(self, agent_id: str) -> Dict[str, List[AgentMessage]]:
        """Get all conversations for an agent"""
        agent = self.get_agent(agent_id)
        if not agent:
            return {}
        return agent.conversation_history
    
    def get_agent_inbox(self, agent_id: str) -> List[AgentMessage]:
        """Get unread messages for an agent"""
        agent = self.get_agent(agent_id)
        if not agent:
            return []
        return agent.message_inbox
    
    def clear_agent_inbox(self, agent_id: str):
        """Clear an agent's inbox"""
        agent = self.get_agent(agent_id)
        if agent:
            agent.message_inbox.clear()
    
    async def execute_task(
        self,
        task: str,
        agent_id: Optional[str] = None,
        requesting_agent_id: Optional[str] = None
    ) -> Dict:
        """
        Execute a task using the appropriate agent(s).
        
        Args:
            task: The task to execute
            agent_id: Optional specific agent to use
            requesting_agent_id: Optional ID of agent making the request
        """
        # Route to agent if not specified
        if not agent_id:
            agent_id = self.route_task(task)
        
        agent = self.get_agent(agent_id)
        if not agent:
            return {
                "success": False,
                "error": f"Agent not found: {agent_id}"
            }
        
        # Check for collaborators
        collaborators = self.get_collaborators(agent_id, task)
        
        # Show who is working
        if requesting_agent_id:
            requesting_agent = self.get_agent(requesting_agent_id)
            req_name = requesting_agent.name if requesting_agent else requesting_agent_id
            print(f"🤖 {agent.name} (requested by {req_name}): {task[:60]}...")
        else:
            print(f"🤖 {agent.name} is working on: {task}")
        
        if collaborators:
            collab_names = [self.agents[c].name for c in collaborators if c in self.agents]
            print(f"🤝 Collaborating with: {', '.join(collab_names)}")
        
        # Update agent status
        agent.status = AgentStatus.WORKING
        agent.current_task = task
        
        # TODO: Implement actual model inference
        # This requires integration with Ollama API or other model providers.
        # Example implementation:
        #   - Use ollama.chat() to call local models
        #   - Use OpenAI/Anthropic APIs as fallback
        #   - Parse model response and return structured data
        # For now, returning mock response for demonstration
        
        # Build response mentioning agent capabilities
        response_parts = [f"[{agent.name} - Mock Response] Task received and processed."]
        
        # Add note about agent-to-agent communication
        if requesting_agent_id:
            response_parts.append(f"Working on request from {requesting_agent_id}.")
        
        # Mention if consulting other agents
        can_ask = agent.config.get("collaboration", {}).get("can_request_help_from", [])
        if can_ask and any(trigger in task.lower() for trigger in ["help", "ask", "consult", "check"]):
            response_parts.append(f"I can consult with {', '.join(can_ask)} if needed.")
        
        result = {
            "success": True,
            "agent": agent.name,
            "agent_id": agent_id,
            "task": task,
            "collaborators": collaborators,
            "can_request_help_from": can_ask,
            "response": " ".join(response_parts),
            "model": agent.config["models"]["primary"],
            "requesting_agent": requesting_agent_id
        }
        
        # Reset status
        agent.status = AgentStatus.IDLE
        agent.current_task = None
        
        return result
    
    def get_status(self) -> Dict:
        """Get status of all agents"""
        return {
            "total_agents": len(self.agents),
            "total_conversations": len(self.conversations),
            "total_messages": len(self.message_log),
            "agents": {
                agent_id: {
                    "name": agent.name,
                    "status": agent.status.value,
                    "current_task": agent.current_task,
                    "unread_messages": len(agent.message_inbox),
                    "active_conversations": len(agent.conversation_history)
                }
                for agent_id, agent in self.agents.items()
            }
        }


async def main():
    """Example usage"""
    orchestrator = AgentOrchestrator()
    
    print("\n📊 Agent Status:")
    status = orchestrator.get_status()
    print(f"Total Agents: {status['total_agents']}")
    
    print("\n🎯 Available Agents:")
    for agent_id in orchestrator.list_agents():
        agent = orchestrator.get_agent(agent_id)
        print(f"  - {agent.name} ({agent_id})")
    
    # Test task routing
    print("\n🧪 Testing Task Routing:")
    test_tasks = [
        "Write a Python function to calculate fibonacci",
        "Design a color palette for a dashboard",
        "Deploy the app to Cloudflare Workers",
        "Create API documentation for the router",
        "Analyze user engagement metrics"
    ]
    
    for task in test_tasks:
        agent_id = orchestrator.route_task(task)
        agent = orchestrator.get_agent(agent_id)
        print(f"  '{task[:50]}...' → {agent.name}")
    
    # Test task execution
    print("\n🚀 Executing Task:")
    result = await orchestrator.execute_task(
        "Refactor the API router and update its documentation"
    )
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
