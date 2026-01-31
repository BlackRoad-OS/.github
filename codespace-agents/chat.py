"""
BlackRoad Agent Chat Interface

Simple CLI for chatting with specific agents.
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from codespace_agents.orchestrator import AgentOrchestrator


class AgentChat:
    """Interactive chat interface for agents"""
    
    def __init__(self, orchestrator: AgentOrchestrator):
        self.orchestrator = orchestrator
    
    async def chat_with_agent(self, agent_id: str, message: str = None):
        """Chat with a specific agent"""
        agent = self.orchestrator.get_agent(agent_id)
        
        if not agent:
            print(f"❌ Agent not found: {agent_id}")
            print(f"Available agents: {', '.join(self.orchestrator.list_agents())}")
            return
        
        print(f"\n💬 Chatting with {agent.name}")
        print(f"Model: {agent.config['models']['primary']}")
        print(f"Type 'exit' or 'quit' to end chat\n")
        
        # If message provided, use it and exit
        if message:
            print(f"You: {message}")
            result = await self.orchestrator.execute_task(message, agent_id)
            print(f"{agent.name}: {result.get('response', 'No response')}")
            return
        
        # Interactive mode
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print(f"👋 Goodbye from {agent.name}!")
                    break
                
                if not user_input:
                    continue
                
                result = await self.orchestrator.execute_task(user_input, agent_id)
                print(f"{agent.name}: {result.get('response', 'No response')}\n")
                
            except KeyboardInterrupt:
                print(f"\n👋 Goodbye from {agent.name}!")
                break
            except Exception as e:
                print(f"❌ Error: {e}\n")


async def main():
    parser = argparse.ArgumentParser(
        description="Chat with BlackRoad AI agents"
    )
    parser.add_argument(
        "--agent",
        type=str,
        help="Agent to chat with (coder, designer, ops, docs, analyst)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available agents"
    )
    parser.add_argument(
        "message",
        nargs="*",
        help="Message to send (interactive mode if not provided)"
    )
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator()
    
    # List agents if requested
    if args.list:
        print("\n🤖 Available Agents:\n")
        for agent_id in orchestrator.list_agents():
            agent = orchestrator.get_agent(agent_id)
            print(f"  {agent_id:12} - {agent.name:15} ({agent.config['models']['primary']})")
            print(f"               {agent.config['description']}")
            print()
        return
    
    # Determine agent
    if not args.agent:
        # If no agent specified, auto-route based on message
        if args.message:
            message = " ".join(args.message)
            agent_id = orchestrator.route_task(message)
            agent = orchestrator.get_agent(agent_id)
            print(f"🎯 Auto-routing to: {agent.name}")
            result = await orchestrator.execute_task(message, agent_id)
            print(f"\n{agent.name}: {result.get('response', 'No response')}")
        else:
            # Interactive mode - let user choose
            print("\n🤖 Available Agents:")
            agents = orchestrator.list_agents()
            for i, agent_id in enumerate(agents, 1):
                agent = orchestrator.get_agent(agent_id)
                print(f"  {i}. {agent.name} - {agent.config['description']}")
            
            try:
                choice = input("\nSelect agent (1-{}): ".format(len(agents)))
                idx = int(choice) - 1
                if 0 <= idx < len(agents):
                    agent_id = agents[idx]
                else:
                    print("Invalid choice")
                    return
            except (ValueError, KeyboardInterrupt):
                print("\nExiting...")
                return
            
            chat = AgentChat(orchestrator)
            await chat.chat_with_agent(agent_id)
        return
    
    # Chat with specified agent
    message = " ".join(args.message) if args.message else None
    chat = AgentChat(orchestrator)
    await chat.chat_with_agent(args.agent, message)


if __name__ == "__main__":
    asyncio.run(main())
