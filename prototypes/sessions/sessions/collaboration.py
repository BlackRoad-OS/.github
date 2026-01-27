"""
Collaboration Hub - Enable inter-session communication.

Provides message passing, task coordination, and collaboration
capabilities between multiple active sessions.
"""

import json
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
import uuid

from .registry import SessionRegistry, Session


class MessageType(Enum):
    """Types of collaboration messages."""
    PING = "ping"                      # Simple ping/pong
    REQUEST = "request"                # Request for help/action
    RESPONSE = "response"              # Response to request
    BROADCAST = "broadcast"            # Broadcast to all sessions
    NOTIFICATION = "notification"      # Notification/alert
    TASK_OFFER = "task_offer"         # Offer to take on a task
    TASK_ACCEPT = "task_accept"       # Accept task offer
    SYNC = "sync"                      # Sync request
    HANDOFF = "handoff"               # Hand off task to another session


@dataclass
class Message:
    """A collaboration message between sessions."""
    
    message_id: str
    type: MessageType
    from_session: str
    to_session: Optional[str]          # None for broadcast
    subject: str
    body: str
    data: Dict[str, Any]
    timestamp: str
    in_reply_to: Optional[str] = None
    
    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data['type'] = self.type.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create from dictionary."""
        if 'type' in data and isinstance(data['type'], str):
            data['type'] = MessageType(data['type'])
        return cls(**data)
    
    def format_signal(self) -> str:
        """Format as a signal string."""
        emoji_map = {
            MessageType.PING: "🔔",
            MessageType.REQUEST: "❓",
            MessageType.RESPONSE: "✅",
            MessageType.BROADCAST: "📡",
            MessageType.NOTIFICATION: "📢",
            MessageType.TASK_OFFER: "🤝",
            MessageType.TASK_ACCEPT: "👍",
            MessageType.SYNC: "🔄",
            MessageType.HANDOFF: "🎯",
        }
        
        emoji = emoji_map.get(self.type, "💬")
        target = self.to_session or "ALL"
        
        return f"{emoji} {self.from_session} → {target} : [COLLABORATION] {self.subject}"


class CollaborationHub:
    """
    Hub for session collaboration and communication.
    
    Enables sessions to:
    - Send messages to each other
    - Broadcast to all sessions
    - Coordinate on tasks
    - Share work and handoff tasks
    
    Usage:
        hub = CollaborationHub()
        
        # Register sessions first
        hub.registry.register("session-1", "Cece", "Claude", "Alexa")
        hub.registry.register("session-2", "Agent-2", "GPT-4", "Alexa")
        
        # Send a message
        msg = hub.send(
            from_session="session-1",
            to_session="session-2",
            type=MessageType.REQUEST,
            subject="Need help with Python",
            body="Can you review this code?",
            data={"code": "..."}
        )
        
        # Broadcast to all
        hub.broadcast(
            from_session="session-1",
            subject="Deployment starting",
            body="Starting deployment to production"
        )
        
        # Get messages for a session
        messages = hub.get_messages("session-2")
        
        # Reply to a message
        hub.reply(
            from_session="session-2",
            to_message=msg,
            body="Sure, looks good!"
        )
    """
    
    def __init__(
        self,
        registry: Optional[SessionRegistry] = None,
        messages_path: Optional[Path] = None
    ):
        """
        Initialize the collaboration hub.
        
        Args:
            registry: Session registry (created if None)
            messages_path: Path to store messages
        """
        self.registry = registry or SessionRegistry()
        
        if messages_path:
            self.messages_path = Path(messages_path)
        else:
            self.messages_path = self.registry.registry_path / "messages"
        
        self.messages_path.mkdir(exist_ok=True)
        
        self._message_handlers: Dict[MessageType, List[Callable]] = {}
        self._messages: List[Message] = []
        
        self._load_messages()
    
    def _load_messages(self):
        """Load recent messages from disk."""
        messages_file = self.messages_path / "recent_messages.json"
        
        if not messages_file.exists():
            return
        
        try:
            with open(messages_file, 'r') as f:
                data = json.load(f)
            
            self._messages = [
                Message.from_dict(msg_data)
                for msg_data in data.get('messages', [])
            ]
            
        except Exception as e:
            print(f"Warning: Could not load messages: {e}")
    
    def _save_messages(self):
        """Save recent messages to disk."""
        messages_file = self.messages_path / "recent_messages.json"
        
        # Keep only recent messages (last 100)
        recent = self._messages[-100:]
        
        try:
            data = {
                'messages': [msg.to_dict() for msg in recent],
                'updated_at': datetime.utcnow().isoformat(),
            }
            
            with open(messages_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not save messages: {e}")
    
    def send(
        self,
        from_session: str,
        to_session: str,
        type: MessageType,
        subject: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
        in_reply_to: Optional[str] = None,
    ) -> Message:
        """
        Send a message to another session.
        
        Args:
            from_session: Sender session ID
            to_session: Recipient session ID
            type: Message type
            subject: Message subject
            body: Message body
            data: Additional data
            in_reply_to: Message ID this is replying to
        
        Returns:
            The sent Message object
        """
        message = Message(
            message_id=str(uuid.uuid4()),
            type=type,
            from_session=from_session,
            to_session=to_session,
            subject=subject,
            body=body,
            data=data or {},
            timestamp=datetime.utcnow().isoformat(),
            in_reply_to=in_reply_to,
        )
        
        self._messages.append(message)
        self._save_messages()
        
        # Print signal
        print(f"  {message.format_signal()}")
        
        # Trigger handlers
        self._trigger_handlers(message)
        
        return message
    
    def broadcast(
        self,
        from_session: str,
        subject: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Message:
        """
        Broadcast a message to all sessions.
        
        Args:
            from_session: Sender session ID
            subject: Message subject
            body: Message body
            data: Additional data
        
        Returns:
            The broadcast Message object
        """
        message = Message(
            message_id=str(uuid.uuid4()),
            type=MessageType.BROADCAST,
            from_session=from_session,
            to_session=None,
            subject=subject,
            body=body,
            data=data or {},
            timestamp=datetime.utcnow().isoformat(),
        )
        
        self._messages.append(message)
        self._save_messages()
        
        # Print signal
        print(f"  {message.format_signal()}")
        
        # Trigger handlers
        self._trigger_handlers(message)
        
        return message
    
    def reply(
        self,
        from_session: str,
        to_message: Message,
        body: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Message:
        """
        Reply to a message.
        
        Args:
            from_session: Sender session ID
            to_message: Message being replied to
            body: Reply body
            data: Additional data
        
        Returns:
            The reply Message object
        """
        return self.send(
            from_session=from_session,
            to_session=to_message.from_session,
            type=MessageType.RESPONSE,
            subject=f"Re: {to_message.subject}",
            body=body,
            data=data,
            in_reply_to=to_message.message_id,
        )
    
    def ping_session(self, from_session: str, to_session: str) -> Message:
        """
        Ping another session.
        
        Args:
            from_session: Sender session ID
            to_session: Target session ID
        
        Returns:
            The ping Message object
        """
        return self.send(
            from_session=from_session,
            to_session=to_session,
            type=MessageType.PING,
            subject="Ping",
            body="Are you there?",
        )
    
    def get_messages(
        self,
        session_id: str,
        include_broadcasts: bool = True,
        message_type: Optional[MessageType] = None,
        unread_only: bool = False,
    ) -> List[Message]:
        """
        Get messages for a session.
        
        Args:
            session_id: Session to get messages for
            include_broadcasts: Include broadcast messages
            message_type: Filter by message type
            unread_only: Only unread messages (not implemented yet)
        
        Returns:
            List of messages
        """
        messages = [
            msg for msg in self._messages
            if msg.to_session == session_id or
               (include_broadcasts and msg.to_session is None)
        ]
        
        if message_type:
            messages = [msg for msg in messages if msg.type == message_type]
        
        return messages
    
    def get_conversation(self, message_id: str) -> List[Message]:
        """
        Get full conversation thread for a message.
        
        Args:
            message_id: Starting message ID
        
        Returns:
            List of messages in thread
        """
        # Find the root message
        root = next((m for m in self._messages if m.message_id == message_id), None)
        if not root:
            return []
        
        # Find all messages in reply chain
        thread = [root]
        
        # Walk up to find root
        current = root
        while current.in_reply_to:
            parent = next((m for m in self._messages if m.message_id == current.in_reply_to), None)
            if parent:
                thread.insert(0, parent)
                current = parent
            else:
                break
        
        # Walk down to find replies
        def find_replies(msg_id: str):
            replies = [m for m in self._messages if m.in_reply_to == msg_id]
            for reply in replies:
                thread.append(reply)
                find_replies(reply.message_id)
        
        find_replies(thread[-1].message_id)
        
        return thread
    
    def register_handler(self, message_type: MessageType, handler: Callable):
        """
        Register a handler for message type.
        
        Args:
            message_type: Type to handle
            handler: Handler function (receives Message)
        """
        if message_type not in self._message_handlers:
            self._message_handlers[message_type] = []
        
        self._message_handlers[message_type].append(handler)
    
    def _trigger_handlers(self, message: Message):
        """Trigger handlers for a message."""
        handlers = self._message_handlers.get(message.type, [])
        
        for handler in handlers:
            try:
                handler(message)
            except Exception as e:
                print(f"Warning: Message handler failed: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get collaboration statistics."""
        return {
            'total_messages': len(self._messages),
            'by_type': {
                msg_type.value: len([m for m in self._messages if m.type == msg_type])
                for msg_type in MessageType
            },
            'active_sessions': len(self.registry.list_sessions()),
        }
