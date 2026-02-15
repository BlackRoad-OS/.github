#!/usr/bin/env python3
"""
Example: Building a feature with collaborative agents

This example demonstrates how multiple agents work together to build,
document, and deploy a new feature.
"""

import asyncio
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from codespace_agents.orchestrator import AgentOrchestrator


async def example_feature_development():
    """
    Example: Build a REST API endpoint with multiple agents collaborating
    """
    print("=" * 60)
    print("Example: Building a REST API Feature")
    print("=" * 60)
    print()
    
    orchestrator = AgentOrchestrator()
    
    # Phase 1: Design (Designer Agent)
    print("📐 Phase 1: Design")
    print("-" * 60)
    design_task = "Design an API endpoint for user authentication with JWT tokens"
    result = await orchestrator.execute_task(design_task, "designer")
    print(f"✓ {result['agent']}: {result['response']}")
    print()
    
    # Phase 2: Implementation (Coder Agent)
    print("💻 Phase 2: Implementation")
    print("-" * 60)
    code_task = "Implement the authentication API with FastAPI and JWT tokens"
    result = await orchestrator.execute_task(code_task, "coder")
    print(f"✓ {result['agent']}: {result['response']}")
    print()
    
    # Phase 3: Documentation (Docs Agent)
    print("📝 Phase 3: Documentation")
    print("-" * 60)
    docs_task = "Create API documentation for the authentication endpoint"
    result = await orchestrator.execute_task(docs_task, "docs")
    print(f"✓ {result['agent']}: {result['response']}")
    print()
    
    # Phase 4: Deployment (Ops Agent)
    print("🚀 Phase 4: Deployment")
    print("-" * 60)
    deploy_task = "Deploy the authentication API to Cloudflare Workers"
    result = await orchestrator.execute_task(deploy_task, "ops")
    print(f"✓ {result['agent']}: {result['response']}")
    print()
    
    # Phase 5: Analytics (Analyst Agent)
    print("📊 Phase 5: Analytics")
    print("-" * 60)
    metrics_task = "Set up monitoring for the authentication API"
    result = await orchestrator.execute_task(metrics_task, "analyst")
    print(f"✓ {result['agent']}: {result['response']}")
    print()
    
    print("=" * 60)
    print("✨ Feature Complete!")
    print("All agents collaborated successfully")
    print("=" * 60)


async def example_bug_fix():
    """
    Example: Fix a bug with agent collaboration
    """
    print("\n\n")
    print("=" * 60)
    print("Example: Bug Fix Workflow")
    print("=" * 60)
    print()
    
    orchestrator = AgentOrchestrator()
    
    # Step 1: Analyze
    print("🔍 Step 1: Analyze the issue")
    print("-" * 60)
    analyze_task = "Why is the login endpoint returning 500 errors?"
    result = await orchestrator.execute_task(analyze_task, "analyst")
    print(f"✓ {result['agent']}: {result['response']}")
    print()
    
    # Step 2: Fix
    print("🔧 Step 2: Fix the code")
    print("-" * 60)
    fix_task = "Fix the authentication token validation logic"
    result = await orchestrator.execute_task(fix_task, "coder")
    print(f"✓ {result['agent']}: {result['response']}")
    print()
    
    # Step 3: Update docs
    print("📝 Step 3: Update documentation")
    print("-" * 60)
    docs_task = "Update changelog with bug fix details"
    result = await orchestrator.execute_task(docs_task, "docs")
    print(f"✓ {result['agent']}: {result['response']}")
    print()
    
    print("=" * 60)
    print("✅ Bug Fixed!")
    print("=" * 60)


async def example_auto_routing():
    """
    Example: Let the orchestrator automatically route tasks
    """
    print("\n\n")
    print("=" * 60)
    print("Example: Automatic Task Routing")
    print("=" * 60)
    print()
    
    orchestrator = AgentOrchestrator()
    
    tasks = [
        "Create a color palette for a dashboard",
        "Write unit tests for the user service",
        "Set up CI/CD pipeline for the project",
        "Analyze user engagement metrics",
        "Write a tutorial on API authentication",
    ]
    
    for task in tasks:
        agent_id = orchestrator.route_task(task)
        agent = orchestrator.get_agent(agent_id)
        print(f"📋 Task: {task}")
        print(f"   → Routed to: {agent.name} ({agent_id})")
        print()


async def main():
    """Run all examples"""
    print("\n")
    print("🤖 BlackRoad Agent Collaboration Examples")
    print("=" * 60)
    print()
    print("This demonstrates how agents work together on real tasks.")
    print()
    
    try:
        # Example 1: Feature development
        await example_feature_development()
        
        # Example 2: Bug fix
        await example_bug_fix()
        
        # Example 3: Auto-routing
        await example_auto_routing()
        
        print("\n")
        print("=" * 60)
        print("Examples Complete!")
        print()
        print("Try it yourself:")
        print("  python -m codespace_agents.chat --agent coder")
        print("  python -m codespace_agents.collaborate")
        print("=" * 60)
        print()
        
    except KeyboardInterrupt:
        print("\n\n👋 Examples interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
