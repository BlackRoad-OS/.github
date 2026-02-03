"""
BlackRoad Agent Collaboration

Enables multiple agents to work together on complex tasks.
"""

import asyncio
import argparse
import sys
from pathlib import Path
from typing import List
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from codespace_agents.orchestrator import AgentOrchestrator


class CollaborativeSession:
    """A collaborative coding/working session with multiple agents"""
    
    def __init__(self, orchestrator: AgentOrchestrator, agent_ids: List[str]):
        self.orchestrator = orchestrator
        self.agent_ids = agent_ids
        self.session_log = []
        self.start_time = datetime.now()
    
    def log_message(self, agent_id: str, message: str):
        """Log a message in the session"""
        timestamp = datetime.now()
        self.session_log.append({
            "timestamp": timestamp,
            "agent": agent_id,
            "message": message
        })
    
    async def broadcast_task(self, task: str):
        """Broadcast a task to all agents in the session"""
        print(f"\n📢 Broadcasting task to all agents:")
        print(f"   {task}\n")
        
        results = []
        for agent_id in self.agent_ids:
            agent = self.orchestrator.get_agent(agent_id)
            if agent:
                print(f"🤖 {agent.name} is processing...")
                result = await self.orchestrator.execute_task(task, agent_id)
                results.append(result)
                self.log_message(agent_id, result.get("response", ""))
        
        return results
    
    async def sequential_handoff(self, task: str):
        """
        Execute task with sequential agent handoffs.
        Each agent passes work to the next.
        """
        print(f"\n🔄 Sequential handoff for task:")
        print(f"   {task}\n")
        
        current_task = task
        results = []
        
        for i, agent_id in enumerate(self.agent_ids):
            agent = self.orchestrator.get_agent(agent_id)
            if not agent:
                continue
            
            print(f"{'→' * (i + 1)} {agent.name}")
            
            # Execute task
            result = await self.orchestrator.execute_task(current_task, agent_id)
            results.append(result)
            self.log_message(agent_id, result.get("response", ""))
            
            # Check if this agent hands off to next
            collaborators = self.orchestrator.get_collaborators(agent_id, current_task)
            if collaborators and i < len(self.agent_ids) - 1:
                next_agent_id = self.agent_ids[i + 1]
                if next_agent_id in collaborators:
                    current_task = f"Continue from {agent.name}: {current_task}"
        
        return results
    
    async def chat_session(self):
        """Interactive group chat with all agents"""
        print(f"\n💬 Group Chat Session Started")
        print(f"Participants: {', '.join([self.orchestrator.get_agent(a).name for a in self.agent_ids if self.orchestrator.get_agent(a)])}")
        print(f"Type 'exit' to end session\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    self.print_summary()
                    break
                
                if not user_input:
                    continue
                
                # Route to most appropriate agent
                agent_id = self.orchestrator.route_task(user_input)
                
                # But also get input from others if relevant
                primary_agent = self.orchestrator.get_agent(agent_id)
                result = await self.orchestrator.execute_task(user_input, agent_id)
                
                print(f"{primary_agent.name}: {result.get('response', 'No response')}")
                self.log_message(agent_id, result.get("response", ""))
                
                # Check if other agents should chime in
                collaborators = self.orchestrator.get_collaborators(agent_id, user_input)
                for collab_id in collaborators:
                    if collab_id in self.agent_ids and collab_id != agent_id:
                        collab_agent = self.orchestrator.get_agent(collab_id)
                        print(f"{collab_agent.name}: [Would provide input here]")
                
                print()
                
            except KeyboardInterrupt:
                self.print_summary()
                break
            except Exception as e:
                print(f"❌ Error: {e}\n")
    
    def print_summary(self):
        """Print session summary"""
        duration = datetime.now() - self.start_time
        print(f"\n📊 Session Summary")
        print(f"Duration: {duration}")
        print(f"Messages: {len(self.session_log)}")
        print(f"Participants: {len(self.agent_ids)}")
        print(f"\n👋 Session ended")


async def main():
    parser = argparse.ArgumentParser(
        description="Collaborative agent sessions"
    )
    parser.add_argument(
        "--agents",
        type=str,
        help="Comma-separated list of agents (e.g., coder,designer,ops)"
    )
    parser.add_argument(
        "--task",
        type=str,
        help="Task for agents to work on"
    )
    parser.add_argument(
        "--mode",
        choices=["broadcast", "sequential", "chat"],
        default="chat",
        help="Collaboration mode"
    )
    
    args = parser.parse_args()
    
    orchestrator = AgentOrchestrator()
    
    # Determine agents
    if args.agents:
        agent_ids = [a.strip() for a in args.agents.split(",")]
    else:
        # Default to all agents
        agent_ids = orchestrator.list_agents()
    
    # Validate agents exist
    valid_agents = []
    for agent_id in agent_ids:
        if orchestrator.get_agent(agent_id):
            valid_agents.append(agent_id)
        else:
            print(f"⚠️  Agent not found: {agent_id}")
    
    if not valid_agents:
        print("❌ No valid agents specified")
        return
    
    # Create session
    session = CollaborativeSession(orchestrator, valid_agents)
    
    # Execute based on mode
    if args.mode == "broadcast" and args.task:
        await session.broadcast_task(args.task)
    elif args.mode == "sequential" and args.task:
        await session.sequential_handoff(args.task)
    else:
        await session.chat_session()


if __name__ == "__main__":
    asyncio.run(main())
