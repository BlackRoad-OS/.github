"""
BlackRoad Agent Orchestrator

Coordinates multiple AI agents working together on tasks.
"""

import asyncio
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    ERROR = "error"


@dataclass
class Agent:
    """Represents an AI agent"""
    agent_id: str
    name: str
    config: Dict
    status: AgentStatus = AgentStatus.IDLE
    current_task: Optional[str] = None


class AgentOrchestrator:
    """
    Orchestrates multiple AI agents working together.
    
    Features:
    - Load agent configurations
    - Route tasks to appropriate agents
    - Enable agent collaboration
    - Track agent status and metrics
    """
    
    def __init__(self, config_dir: str = "codespace-agents/config"):
        self.config_dir = Path(config_dir)
        self.agents: Dict[str, Agent] = {}
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
    
    async def execute_task(self, task: str, agent_id: Optional[str] = None) -> Dict:
        """
        Execute a task using the appropriate agent(s).
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
        
        print(f"🤖 {agent.name} is working on: {task}")
        if collaborators:
            collab_names = [self.agents[c].name for c in collaborators if c in self.agents]
            print(f"🤝 Collaborating with: {', '.join(collab_names)}")
        
        # Update agent status
        agent.status = AgentStatus.WORKING
        agent.current_task = task
        
        # TODO: Implement actual model inference
        # For now, return mock response
        result = {
            "success": True,
            "agent": agent.name,
            "agent_id": agent_id,
            "task": task,
            "collaborators": collaborators,
            "response": f"[{agent.name}] Task received and processed.",
            "model": agent.config["models"]["primary"]
        }
        
        # Reset status
        agent.status = AgentStatus.IDLE
        agent.current_task = None
        
        return result
    
    def get_status(self) -> Dict:
        """Get status of all agents"""
        return {
            "total_agents": len(self.agents),
            "agents": {
                agent_id: {
                    "name": agent.name,
                    "status": agent.status.value,
                    "current_task": agent.current_task
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
