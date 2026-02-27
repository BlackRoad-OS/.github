"""
Test suite for BlackRoad Session Management.
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from sessions.registry import SessionRegistry, SessionStatus
from sessions.collaboration import CollaborationHub, MessageType
from sessions.memory import SharedMemory, MemoryType


def test_session_registry():
    """Test session registry functionality."""
    print("\n🧪 Testing Session Registry...")
    
    # Use temp directory
    temp_dir = Path(tempfile.mkdtemp())
    
    try:
        registry = SessionRegistry(temp_dir)
        
        # Register sessions
        session1 = registry.register("test-1", "Test Agent 1", "Claude", "Tester")
        assert session1.session_id == "test-1"
        assert session1.agent_name == "Test Agent 1"
        print("  ✅ Session registration")
        
        session2 = registry.register("test-2", "Test Agent 2", "GPT-4", "Tester",
                                    capabilities=["python", "review"])
        assert "python" in session2.capabilities
        print("  ✅ Session with capabilities")
        
        # List sessions
        sessions = registry.list_sessions()
        assert len(sessions) == 2
        print("  ✅ List sessions")
        
        # Ping
        assert registry.ping("test-1")
        print("  ✅ Ping session")
        
        # Update status
        assert registry.update_status("test-1", SessionStatus.WORKING, "Testing")
        session = registry.get("test-1")
        assert session.status == SessionStatus.WORKING
        assert session.current_task == "Testing"
        print("  ✅ Update status")
        
        # Find sessions
        working = registry.find_sessions(status=SessionStatus.WORKING)
        assert len(working) == 1
        print("  ✅ Find by status")
        
        python_sessions = registry.find_sessions(capability="python")
        assert len(python_sessions) == 1
        print("  ✅ Find by capability")
        
        # Stats
        stats = registry.get_stats()
        assert stats['total_sessions'] == 2
        assert stats['active_sessions'] >= 1
        print("  ✅ Statistics")
        
        print("✅ Session Registry tests passed!")
        
    finally:
        shutil.rmtree(temp_dir)


def test_collaboration_hub():
    """Test collaboration hub functionality."""
    print("\n🧪 Testing Collaboration Hub...")
    
    # Use temp directory
    temp_dir = Path(tempfile.mkdtemp())
    
    try:
        registry = SessionRegistry(temp_dir)
        hub = CollaborationHub(registry, temp_dir / "messages")
        
        # Register sessions
        registry.register("session-1", "Agent 1", "Claude", "Tester")
        registry.register("session-2", "Agent 2", "GPT-4", "Tester")
        
        # Send message
        msg = hub.send(
            "session-1", "session-2",
            MessageType.REQUEST,
            "Test message",
            "This is a test"
        )
        assert msg.from_session == "session-1"
        assert msg.to_session == "session-2"
        print("  ✅ Send message")
        
        # Broadcast
        broadcast = hub.broadcast("session-1", "Announcement", "Test broadcast")
        assert broadcast.to_session is None
        print("  ✅ Broadcast")
        
        # Reply
        reply = hub.reply("session-2", msg, "Got it!")
        assert reply.in_reply_to == msg.message_id
        print("  ✅ Reply")
        
        # Ping
        ping = hub.ping_session("session-1", "session-2")
        assert ping.type == MessageType.PING
        print("  ✅ Ping")
        
        # Get messages
        messages = hub.get_messages("session-2")
        assert len(messages) >= 2  # Direct message + broadcast
        print("  ✅ Get messages")
        
        # Get conversation
        thread = hub.get_conversation(msg.message_id)
        assert len(thread) == 2  # Original + reply
        print("  ✅ Get conversation")
        
        # Stats
        stats = hub.get_stats()
        assert stats['total_messages'] >= 4
        print("  ✅ Statistics")
        
        print("✅ Collaboration Hub tests passed!")
        
    finally:
        shutil.rmtree(temp_dir)


def test_shared_memory():
    """Test shared memory functionality."""
    print("\n🧪 Testing Shared Memory...")
    
    # Use temp directory
    temp_dir = Path(tempfile.mkdtemp())
    
    try:
        memory = SharedMemory(temp_dir)
        
        # Set value
        entry = memory.set(
            "session-1",
            "test_key",
            "test_value",
            type=MemoryType.STATE,
            tags=["test", "example"]
        )
        assert entry.key == "test_key"
        print("  ✅ Set value")
        
        # Get value
        value = memory.get("test_key")
        assert value == "test_value"
        print("  ✅ Get value")
        
        # Set another value for same key
        memory.set("session-2", "test_key", "newer_value")
        
        # Get most recent
        value = memory.get("test_key")
        assert value == "newer_value"
        print("  ✅ Get most recent")
        
        # Get all
        all_entries = memory.get_all("test_key")
        assert len(all_entries) == 2
        print("  ✅ Get all entries")
        
        # Get by session
        session_entries = memory.get_by_session("session-1")
        assert len(session_entries) == 1
        print("  ✅ Get by session")
        
        # Get by tags
        tagged = memory.get_by_tags(["test"])
        assert len(tagged) >= 1
        print("  ✅ Get by tags")
        
        # Search pattern
        memory.set("session-1", "task_1", "Task 1")
        memory.set("session-1", "task_2", "Task 2")
        tasks = memory.search("task_*")
        assert len(tasks) == 2
        print("  ✅ Search pattern")
        
        # Delete
        deleted = memory.delete("test_key")
        assert deleted == 2
        value = memory.get("test_key")
        assert value is None
        print("  ✅ Delete")
        
        # Stats
        stats = memory.get_stats()
        assert stats['total_entries'] >= 2
        print("  ✅ Statistics")
        
        print("✅ Shared Memory tests passed!")
        
    finally:
        shutil.rmtree(temp_dir)


def test_integration():
    """Test integrated workflow."""
    print("\n🧪 Testing Integration...")
    
    # Use temp directory
    temp_dir = Path(tempfile.mkdtemp())
    
    try:
        registry = SessionRegistry(temp_dir)
        hub = CollaborationHub(registry, temp_dir / "messages")
        memory = SharedMemory(temp_dir / "memory")
        
        # Register sessions
        registry.register("planner", "Planner", "Claude", "Tester")
        registry.register("developer", "Developer", "GPT-4", "Tester")
        
        # Planner creates a plan
        memory.set("planner", "project_plan", {
            "phase": "design",
            "tasks": ["api", "database", "frontend"]
        }, type=MemoryType.STATE, tags=["project"])
        print("  ✅ Planner stored plan")
        
        # Developer reads plan
        plan = memory.get("project_plan")
        assert plan["phase"] == "design"
        print("  ✅ Developer read plan")
        
        # Developer asks question
        msg = hub.send(
            "developer", "planner",
            MessageType.REQUEST,
            "API design",
            "Should we use REST or GraphQL?"
        )
        print("  ✅ Developer sent question")
        
        # Planner responds
        hub.reply("planner", msg, "Let's go with REST for now")
        print("  ✅ Planner replied")
        
        # Get conversation
        thread = hub.get_conversation(msg.message_id)
        assert len(thread) == 2
        print("  ✅ Retrieved conversation")
        
        # Developer updates status
        registry.update_status("developer", SessionStatus.WORKING, "Building API")
        print("  ✅ Developer updated status")
        
        # Get stats
        session_stats = registry.get_stats()
        collab_stats = hub.get_stats()
        memory_stats = memory.get_stats()
        
        assert session_stats['total_sessions'] == 2
        assert collab_stats['total_messages'] >= 2
        assert memory_stats['total_entries'] >= 1
        print("  ✅ All stats available")
        
        print("✅ Integration tests passed!")
        
    finally:
        shutil.rmtree(temp_dir)


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("🚀 BlackRoad Session Management Test Suite")
    print("="*60)
    
    try:
        test_session_registry()
        test_collaboration_hub()
        test_shared_memory()
        test_integration()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
