"""
CLI for BlackRoad Session Management.

Command-line interface for session discovery, collaboration, and memory.
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sessions.registry import SessionRegistry, SessionStatus
from sessions.collaboration import CollaborationHub, MessageType
from sessions.memory import SharedMemory, MemoryType


def cmd_register(args):
    """Register a new session."""
    registry = SessionRegistry()
    
    session = registry.register(
        session_id=args.session_id,
        agent_name=args.agent_name,
        agent_type=args.agent_type,
        human_user=args.user,
        capabilities=args.capabilities.split(',') if args.capabilities else [],
    )
    
    print(f"✅ Registered session: {session.session_id}")
    print(f"   Agent: {session.agent_name} ({session.agent_type})")
    print(f"   User: {session.human_user}")
    print(f"   Started: {session.started_at}")


def cmd_list(args):
    """List active sessions."""
    registry = SessionRegistry()
    sessions = registry.list_sessions(include_offline=args.all)
    
    if not sessions:
        print("No active sessions found.")
        return
    
    print(f"\n{'SESSION ID':<20} {'AGENT':<15} {'TYPE':<10} {'STATUS':<10} {'USER':<15}")
    print("=" * 90)
    
    for session in sessions:
        print(f"{session.session_id:<20} {session.agent_name:<15} {session.agent_type:<10} "
              f"{session.status.value:<10} {session.human_user or 'N/A':<15}")
    
    # Print stats
    print(f"\n📊 Stats:")
    stats = registry.get_stats()
    print(f"   Total: {stats['total_sessions']}")
    print(f"   Active: {stats['active_sessions']}")
    print(f"   By status: {stats['by_status']}")


def cmd_ping(args):
    """Ping a session."""
    registry = SessionRegistry()
    
    if registry.ping(args.session_id):
        print(f"✅ Pinged session: {args.session_id}")
    else:
        print(f"❌ Session not found: {args.session_id}")


def cmd_status(args):
    """Update session status."""
    registry = SessionRegistry()
    
    status = SessionStatus(args.status)
    
    if registry.update_status(args.session_id, status, args.task):
        print(f"✅ Updated session {args.session_id}")
        print(f"   Status: {status.value}")
        if args.task:
            print(f"   Task: {args.task}")
    else:
        print(f"❌ Session not found: {args.session_id}")


def cmd_send(args):
    """Send a message to another session."""
    hub = CollaborationHub()
    
    message = hub.send(
        from_session=args.from_session,
        to_session=args.to_session,
        type=MessageType(args.type),
        subject=args.subject,
        body=args.body,
        data=json.loads(args.data) if args.data else {},
    )
    
    print(f"✅ Message sent: {message.message_id}")
    print(f"   {message.format_signal()}")


def cmd_broadcast(args):
    """Broadcast a message to all sessions."""
    hub = CollaborationHub()
    
    message = hub.broadcast(
        from_session=args.from_session,
        subject=args.subject,
        body=args.body,
        data=json.loads(args.data) if args.data else {},
    )
    
    print(f"✅ Broadcast sent: {message.message_id}")
    print(f"   {message.format_signal()}")


def cmd_messages(args):
    """Get messages for a session."""
    hub = CollaborationHub()
    
    messages = hub.get_messages(
        session_id=args.session_id,
        message_type=MessageType(args.type) if args.type else None,
    )
    
    if not messages:
        print(f"No messages for session: {args.session_id}")
        return
    
    print(f"\n📬 Messages for {args.session_id}:")
    print("=" * 90)
    
    for msg in messages:
        target = msg.to_session or "ALL"
        print(f"\n{msg.timestamp}")
        print(f"  From: {msg.from_session} → {target}")
        print(f"  Type: {msg.type.value}")
        print(f"  Subject: {msg.subject}")
        print(f"  Body: {msg.body}")
        if msg.data:
            print(f"  Data: {json.dumps(msg.data, indent=4)}")


def cmd_memory_set(args):
    """Store a value in shared memory."""
    memory = SharedMemory()
    
    # Parse value as JSON if possible
    try:
        value = json.loads(args.value)
    except:
        value = args.value
    
    entry = memory.set(
        session_id=args.session_id,
        key=args.key,
        value=value,
        type=MemoryType(args.type),
        tags=args.tags.split(',') if args.tags else [],
    )
    
    print(f"✅ Stored in shared memory")
    print(f"   Key: {entry.key}")
    print(f"   Type: {entry.type.value}")
    print(f"   Value: {entry.value}")
    print(f"   Entry ID: {entry.entry_id}")


def cmd_memory_get(args):
    """Get a value from shared memory."""
    memory = SharedMemory()
    
    if args.all:
        entries = memory.get_all(args.key)
        
        if not entries:
            print(f"No entries found for key: {args.key}")
            return
        
        print(f"\n📝 Entries for key '{args.key}':")
        print("=" * 90)
        
        for entry in entries:
            print(f"\n{entry.timestamp} (by {entry.session_id})")
            print(f"  Type: {entry.type.value}")
            print(f"  Value: {entry.value}")
            if entry.tags:
                print(f"  Tags: {', '.join(entry.tags)}")
    else:
        value = memory.get(args.key)
        
        if value is None:
            print(f"No value found for key: {args.key}")
        else:
            print(f"✅ Value: {value}")


def cmd_memory_search(args):
    """Search shared memory."""
    memory = SharedMemory()
    
    if args.pattern:
        entries = memory.search(args.pattern)
    elif args.tags:
        tags = args.tags.split(',')
        entries = memory.get_by_tags(tags)
    elif args.session:
        entries = memory.get_by_session(args.session)
    else:
        print("Error: Specify --pattern, --tags, or --session")
        return
    
    if not entries:
        print("No entries found.")
        return
    
    print(f"\n📝 Found {len(entries)} entries:")
    print("=" * 90)
    
    for entry in entries[:20]:  # Limit to 20
        print(f"\n{entry.timestamp}")
        print(f"  Key: {entry.key}")
        print(f"  Type: {entry.type.value}")
        print(f"  Value: {entry.value}")
        print(f"  Session: {entry.session_id}")
        if entry.tags:
            print(f"  Tags: {', '.join(entry.tags)}")


def cmd_stats(args):
    """Show statistics."""
    registry = SessionRegistry()
    hub = CollaborationHub()
    memory = SharedMemory()
    
    print("\n📊 BlackRoad Session Statistics")
    print("=" * 60)
    
    print("\n🔗 Sessions:")
    session_stats = registry.get_stats()
    print(f"  Total: {session_stats['total_sessions']}")
    print(f"  Active: {session_stats['active_sessions']}")
    print(f"  By status: {json.dumps(session_stats['by_status'], indent=4)}")
    
    print("\n💬 Collaboration:")
    collab_stats = hub.get_stats()
    print(f"  Total messages: {collab_stats['total_messages']}")
    print(f"  By type: {json.dumps(collab_stats['by_type'], indent=4)}")
    
    print("\n🧠 Shared Memory:")
    memory_stats = memory.get_stats()
    print(f"  Total entries: {memory_stats['total_entries']}")
    print(f"  Unique keys: {memory_stats['unique_keys']}")
    print(f"  By type: {json.dumps(memory_stats['by_type'], indent=4)}")


def main():
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="BlackRoad Session Management")
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Register command
    register_parser = subparsers.add_parser('register', help='Register a new session')
    register_parser.add_argument('session_id', help='Session ID')
    register_parser.add_argument('agent_name', help='Agent name')
    register_parser.add_argument('agent_type', help='Agent type')
    register_parser.add_argument('--user', help='Human user')
    register_parser.add_argument('--capabilities', help='Comma-separated capabilities')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List active sessions')
    list_parser.add_argument('--all', action='store_true', help='Include offline sessions')
    
    # Ping command
    ping_parser = subparsers.add_parser('ping', help='Ping a session')
    ping_parser.add_argument('session_id', help='Session to ping')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Update session status')
    status_parser.add_argument('session_id', help='Session ID')
    status_parser.add_argument('status', choices=[s.value for s in SessionStatus])
    status_parser.add_argument('--task', help='Current task')
    
    # Send command
    send_parser = subparsers.add_parser('send', help='Send a message')
    send_parser.add_argument('from_session', help='Sender session ID')
    send_parser.add_argument('to_session', help='Recipient session ID')
    send_parser.add_argument('subject', help='Message subject')
    send_parser.add_argument('body', help='Message body')
    send_parser.add_argument('--type', default='request', choices=[t.value for t in MessageType])
    send_parser.add_argument('--data', help='JSON data')
    
    # Broadcast command
    broadcast_parser = subparsers.add_parser('broadcast', help='Broadcast a message')
    broadcast_parser.add_argument('from_session', help='Sender session ID')
    broadcast_parser.add_argument('subject', help='Message subject')
    broadcast_parser.add_argument('body', help='Message body')
    broadcast_parser.add_argument('--data', help='JSON data')
    
    # Messages command
    messages_parser = subparsers.add_parser('messages', help='Get messages')
    messages_parser.add_argument('session_id', help='Session ID')
    messages_parser.add_argument('--type', choices=[t.value for t in MessageType])
    
    # Memory set command
    memory_set_parser = subparsers.add_parser('memory-set', help='Store in shared memory')
    memory_set_parser.add_argument('session_id', help='Session ID')
    memory_set_parser.add_argument('key', help='Memory key')
    memory_set_parser.add_argument('value', help='Value to store')
    memory_set_parser.add_argument('--type', default='state', choices=[t.value for t in MemoryType])
    memory_set_parser.add_argument('--tags', help='Comma-separated tags')
    
    # Memory get command
    memory_get_parser = subparsers.add_parser('memory-get', help='Get from shared memory')
    memory_get_parser.add_argument('key', help='Memory key')
    memory_get_parser.add_argument('--all', action='store_true', help='Get all entries')
    
    # Memory search command
    memory_search_parser = subparsers.add_parser('memory-search', help='Search shared memory')
    memory_search_parser.add_argument('--pattern', help='Key pattern')
    memory_search_parser.add_argument('--tags', help='Comma-separated tags')
    memory_search_parser.add_argument('--session', help='Session ID')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    command_map = {
        'register': cmd_register,
        'list': cmd_list,
        'ping': cmd_ping,
        'status': cmd_status,
        'send': cmd_send,
        'broadcast': cmd_broadcast,
        'messages': cmd_messages,
        'memory-set': cmd_memory_set,
        'memory-get': cmd_memory_get,
        'memory-search': cmd_memory_search,
        'stats': cmd_stats,
    }
    
    handler = command_map.get(args.command)
    if handler:
        handler(args)
    else:
        print(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
