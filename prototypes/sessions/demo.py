#!/usr/bin/env python3
"""
Demo script for BlackRoad Session Management.

Shows how sessions can discover each other, collaborate, and share memory.
"""

import sys
import time
from pathlib import Path

# Add sessions to path
sys.path.insert(0, str(Path(__file__).parent))

from sessions import (
    SessionRegistry, SessionStatus,
    CollaborationHub, MessageType,
    SharedMemory, MemoryType
)


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_session_discovery():
    """Demo: Register and discover sessions."""
    print_section("DEMO 1: Session Discovery")
    
    registry = SessionRegistry()
    
    # Register Cece (Claude)
    print("\n📝 Registering Cece (Claude)...")
    cece = registry.register(
        session_id="cece-001",
        agent_name="Cece",
        agent_type="Claude",
        human_user="Alexa",
        capabilities=["python", "planning", "review"]
    )
    print(f"   ✅ {cece.agent_name} registered: {cece.session_id}")
    
    # Register another agent (GPT-4)
    print("\n📝 Registering Agent-2 (GPT-4)...")
    agent2 = registry.register(
        session_id="agent-002",
        agent_name="Agent-2",
        agent_type="GPT-4",
        human_user="Alexa",
        capabilities=["javascript", "react", "testing"]
    )
    print(f"   ✅ {agent2.agent_name} registered: {agent2.session_id}")
    
    # List all sessions
    print("\n📋 Listing all active sessions:")
    sessions = registry.list_sessions()
    for session in sessions:
        print(f"   • {session.agent_name} ({session.agent_type}) - {session.status.value}")
        if session.capabilities:
            print(f"     Capabilities: {', '.join(session.capabilities)}")
    
    # Find Python expert
    print("\n🔍 Finding Python experts...")
    python_experts = registry.find_sessions(capability="python")
    for session in python_experts:
        print(f"   • {session.agent_name} can help with Python!")
    
    # Update status
    print("\n⚙️ Cece starts working...")
    registry.update_status("cece-001", SessionStatus.WORKING, "Building collaboration system")
    
    # Show stats
    print("\n📊 Session Statistics:")
    stats = registry.get_stats()
    print(f"   Total: {stats['total_sessions']}")
    print(f"   Active: {stats['active_sessions']}")
    print(f"   By status: {stats['by_status']}")


def demo_collaboration():
    """Demo: Inter-session collaboration."""
    print_section("DEMO 2: Collaboration Messages")
    
    hub = CollaborationHub()
    
    # Ping another session
    print("\n🔔 Cece pings Agent-2...")
    ping = hub.ping_session("cece-001", "agent-002")
    print(f"   {ping.format_signal()}")
    
    # Request help
    print("\n❓ Cece requests help with React...")
    request = hub.send(
        from_session="cece-001",
        to_session="agent-002",
        type=MessageType.REQUEST,
        subject="React component review",
        body="Can you review this React component for me?",
        data={"component": "UserProfile.jsx", "lines": 150}
    )
    print(f"   {request.format_signal()}")
    
    # Agent-2 responds
    print("\n✅ Agent-2 responds...")
    response = hub.reply(
        from_session="agent-002",
        to_message=request,
        body="Sure! I'll review it now. Looks good overall, minor suggestions in comments.",
        data={"approved": True, "suggestions": 3}
    )
    print(f"   {response.format_signal()}")
    
    # Broadcast announcement
    print("\n📡 Cece broadcasts to all sessions...")
    broadcast = hub.broadcast(
        from_session="cece-001",
        subject="Deployment scheduled",
        body="Production deployment scheduled for 2PM"
    )
    print(f"   {broadcast.format_signal()}")
    
    # Get messages for Agent-2
    print("\n📬 Agent-2 checks messages...")
    messages = hub.get_messages("agent-002")
    print(f"   Received {len(messages)} messages:")
    for msg in messages:
        print(f"   • [{msg.type.value}] {msg.subject}")
    
    # Show conversation thread
    print("\n💬 Full conversation thread:")
    thread = hub.get_conversation(request.message_id)
    for msg in thread:
        print(f"   {msg.timestamp}")
        print(f"   {msg.from_session} → {msg.to_session}")
        print(f"   {msg.body}")
        print()


def demo_shared_memory():
    """Demo: Shared memory across sessions."""
    print_section("DEMO 3: Shared Memory")
    
    memory = SharedMemory()
    
    # Cece stores project plan
    print("\n🧠 Cece stores project plan in shared memory...")
    memory.set(
        session_id="cece-001",
        key="project_plan",
        value={
            "phase": "design",
            "tasks": ["api-design", "database-schema", "frontend-mockups"],
            "deadline": "2026-02-01"
        },
        type=MemoryType.STATE,
        tags=["project", "active", "design"]
    )
    print("   ✅ Stored project_plan")
    
    # Agent-2 reads the plan
    print("\n📖 Agent-2 reads project plan from shared memory...")
    plan = memory.get("project_plan")
    print(f"   Phase: {plan['phase']}")
    print(f"   Tasks: {', '.join(plan['tasks'])}")
    print(f"   Deadline: {plan['deadline']}")
    
    # Agent-2 stores task progress
    print("\n📝 Agent-2 stores task progress...")
    memory.set(
        session_id="agent-002",
        key="task_api-design",
        value={
            "status": "completed",
            "owner": "agent-002",
            "completed_at": "2026-01-27"
        },
        type=MemoryType.TASK,
        tags=["task", "completed"]
    )
    print("   ✅ Stored task_api-design")
    
    # Cece searches for tasks
    print("\n🔍 Cece searches for all tasks...")
    tasks = memory.search("task_*")
    print(f"   Found {len(tasks)} task(s):")
    for entry in tasks:
        print(f"   • {entry.key}: {entry.value['status']}")
    
    # Find by tags
    print("\n🏷️  Finding all active items by tag...")
    active_items = memory.get_by_tags(["active"])
    print(f"   Found {len(active_items)} active item(s):")
    for entry in active_items:
        print(f"   • {entry.key} (by {entry.session_id})")
    
    # Show stats
    print("\n📊 Shared Memory Statistics:")
    stats = memory.get_stats()
    print(f"   Total entries: {stats['total_entries']}")
    print(f"   Unique keys: {stats['unique_keys']}")
    print(f"   Unique sessions: {stats['unique_sessions']}")


def demo_full_workflow():
    """Demo: Complete collaborative workflow."""
    print_section("DEMO 4: Complete Workflow")
    
    registry = SessionRegistry()
    hub = CollaborationHub(registry)
    memory = SharedMemory()
    
    print("\n🎯 Scenario: Multi-agent code review workflow")
    print("   Agents: Planner, Developer, Reviewer")
    
    # Register agents
    print("\n1️⃣  Registering agents...")
    registry.register("planner-001", "Planner", "Claude", "Alexa", ["planning", "architecture"])
    registry.register("developer-001", "Developer", "GPT-4", "Alexa", ["python", "coding"])
    registry.register("reviewer-001", "Reviewer", "Claude", "Alexa", ["review", "security"])
    print("   ✅ All agents registered")
    
    # Planner creates plan
    print("\n2️⃣  Planner creates implementation plan...")
    memory.set(
        "planner-001",
        "implementation_plan",
        {"feature": "user-auth", "steps": ["design", "implement", "test", "review"]},
        MemoryType.STATE,
        tags=["plan", "auth"]
    )
    hub.broadcast("planner-001", "Plan ready", "Implementation plan for user-auth is ready")
    print("   ✅ Plan created and broadcast")
    
    # Developer reads and implements
    print("\n3️⃣  Developer reads plan and implements...")
    plan = memory.get("implementation_plan")
    registry.update_status("developer-001", SessionStatus.WORKING, f"Implementing {plan['feature']}")
    print(f"   ⚙️  Developer working on {plan['feature']}")
    
    # Developer stores code
    memory.set(
        "developer-001",
        "code_user-auth",
        {"file": "auth.py", "lines": 250, "tests": "passing"},
        MemoryType.STATE,
        tags=["code", "ready-for-review"]
    )
    
    # Developer requests review
    hub.send(
        "developer-001",
        "reviewer-001",
        MessageType.TASK_OFFER,
        "Code review needed",
        "User auth implementation ready for review",
        data={"file": "auth.py", "priority": "high"}
    )
    print("   ✅ Code complete, review requested")
    
    # Reviewer accepts and reviews
    print("\n4️⃣  Reviewer accepts and reviews code...")
    hub.send(
        "reviewer-001",
        "developer-001",
        MessageType.TASK_ACCEPT,
        "Starting review",
        "Will review the auth code now"
    )
    registry.update_status("reviewer-001", SessionStatus.WORKING, "Reviewing auth.py")
    
    # Reviewer provides feedback
    memory.set(
        "reviewer-001",
        "review_user-auth",
        {"status": "approved", "issues": 0, "suggestions": 2},
        MemoryType.DECISION,
        tags=["review", "approved"]
    )
    
    hub.send(
        "reviewer-001",
        "developer-001",
        MessageType.RESPONSE,
        "Review complete",
        "Code looks great! LGTM with 2 minor suggestions.",
        data={"approved": True}
    )
    print("   ✅ Review complete - approved!")
    
    # Show final state
    print("\n5️⃣  Final state:")
    sessions = registry.list_sessions()
    for session in sessions:
        print(f"   • {session.agent_name}: {session.status.value}")
        if session.current_task:
            print(f"     Task: {session.current_task}")
    
    # Show collaboration stats
    print("\n📊 Workflow Statistics:")
    collab_stats = hub.get_stats()
    memory_stats = memory.get_stats()
    print(f"   Messages exchanged: {collab_stats['total_messages']}")
    print(f"   Memory entries created: {memory_stats['total_entries']}")


def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print("  BlackRoad Session Management - Live Demo")
    print("  [COLLABORATION] + [MEMORY] for the Mesh")
    print("=" * 60)
    
    try:
        # Run demos
        demo_session_discovery()
        input("\nPress Enter to continue to Collaboration demo...")
        
        demo_collaboration()
        input("\nPress Enter to continue to Shared Memory demo...")
        
        demo_shared_memory()
        input("\nPress Enter to continue to Full Workflow demo...")
        
        demo_full_workflow()
        
        print("\n" + "=" * 60)
        print("  ✅ Demo Complete!")
        print("  Session management is now active in the Bridge.")
        print("=" * 60)
        print("\nTry it yourself:")
        print("  python -m sessions register <id> <name> <type>")
        print("  python -m sessions list")
        print("  python -m sessions send <from> <to> <subject> <body>")
        print("  python -m sessions memory-set <session> <key> <value>")
        print("\nSee README.md for full documentation.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
