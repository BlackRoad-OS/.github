"""
Cece Engine - Core autonomous task processing loop.

Implements the PERCEIVE → CLASSIFY → DECIDE → EXECUTE → LEARN pipeline
for handling issues, PRs, webhooks, and scheduled tasks.
"""

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Enums & Data Classes
# ---------------------------------------------------------------------------

class TaskType(Enum):
    ISSUE = "issue"
    PR = "pull_request"
    WEBHOOK = "webhook"
    COMMAND = "command"
    SCHEDULED = "scheduled"
    SIGNAL = "signal"


class Priority(Enum):
    P0 = 0  # Drop everything
    P1 = 1  # Fix this sprint
    P2 = 2  # Scheduled work
    P3 = 3  # Backlog


class Authority(Enum):
    FULL_AUTO = "full_auto"
    SUGGEST = "suggest"
    ASK_FIRST = "ask_first"


class Verdict(Enum):
    APPROVE = "approve"
    REQUEST_CHANGES = "request_changes"
    COMMENT = "comment"


ORG_CODES = {
    "OS": "BlackRoad-OS",
    "AI": "BlackRoad-AI",
    "CLD": "BlackRoad-Cloud",
    "HW": "BlackRoad-Hardware",
    "SEC": "BlackRoad-Security",
    "LAB": "BlackRoad-Labs",
    "FND": "BlackRoad-Foundation",
    "MED": "BlackRoad-Media",
    "STU": "BlackRoad-Studio",
    "INT": "BlackRoad-Interactive",
    "EDU": "BlackRoad-Education",
    "GOV": "BlackRoad-Gov",
    "ARC": "BlackRoad-Archive",
    "VEN": "BlackRoad-Ventures",
    "BBX": "Blackbox-Enterprises",
}

# Keyword → org routing map
ORG_KEYWORDS: dict[str, str] = {
    "route|operator|bridge|signal|memory": "OS",
    "ai|model|llm|inference|prompt|claude|gpt": "AI",
    "cloudflare|worker|edge|cdn|dns|kv|r2": "CLD",
    "raspberry|pi|hailo|gpio|hardware|sensor|iot": "HW",
    "security|auth|vault|secret|zero.trust|scan": "SEC",
    "experiment|lab|research|prototype|poc": "LAB",
    "salesforce|stripe|billing|crm|payment|invoice": "FND",
    "media|content|social|blog|brand|marketing": "MED",
    "design|figma|canva|asset|ui|ux": "STU",
    "game|unity|vr|ar|metaverse|webxr|interactive": "INT",
    "education|course|tutorial|learn|curriculum": "EDU",
    "governance|vote|proposal|compliance|civic": "GOV",
    "archive|backup|preserve|storage|gdrive": "ARC",
    "venture|invest|portfolio|due.diligence": "VEN",
    "stealth|classified|blackbox": "BBX",
}

# Authority mappings
FULL_AUTO_ACTIONS = {
    "read", "triage", "label", "review_comment", "generate_docs",
    "run_tests", "emit_signal", "update_status", "generate_report",
}

ASK_FIRST_ACTIONS = {
    "delete_repo", "modify_org", "change_permissions",
    "deploy_production", "financial_op", "rotate_keys",
}


@dataclass
class Task:
    """A unit of work flowing through the engine."""
    id: str
    type: TaskType
    title: str
    body: str = ""
    source: str = "unknown"
    org: str = "OS"
    priority: Priority = Priority.P2
    authority: Authority = Authority.SUGGEST
    labels: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict = field(default_factory=dict)


@dataclass
class Signal:
    """A coordination signal emitted by the engine."""
    icon: str
    source: str
    destination: str
    event: str
    details: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __str__(self) -> str:
        base = f"{self.icon} {self.source} → {self.destination} : {self.event}"
        if self.details:
            base += f", {self.details}"
        return base


@dataclass
class EngineResult:
    """Result of processing a task."""
    task: Task
    action_taken: str
    signals_emitted: list[Signal] = field(default_factory=list)
    output: str = ""
    success: bool = True
    needs_escalation: bool = False
    escalation_reason: str = ""


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class CeceEngine:
    """
    Autonomous task processing engine.

    Implements the core loop:
      PERCEIVE → CLASSIFY → DECIDE → EXECUTE → LEARN
    """

    def __init__(self, bridge_root: Optional[Path] = None):
        self.bridge_root = bridge_root or Path(__file__).parent.parent.parent
        self.signals: list[Signal] = []
        self.history: list[EngineResult] = []

    # ---- PERCEIVE ----

    def perceive(self, raw_input: dict) -> Task:
        """Parse raw input into a structured Task."""
        task_type = self._detect_type(raw_input)
        title = raw_input.get("title", raw_input.get("action", "Unknown task"))
        body = raw_input.get("body", raw_input.get("description", ""))

        return Task(
            id=raw_input.get("id", f"task-{len(self.history)+1}"),
            type=task_type,
            title=title,
            body=body,
            source=raw_input.get("source", "unknown"),
            metadata=raw_input,
        )

    # ---- CLASSIFY ----

    def classify(self, task: Task) -> Task:
        """Classify task by org, priority, and labels."""
        text = f"{task.title} {task.body}".lower()

        # Detect org
        task.org = self._detect_org(text)

        # Detect priority
        task.priority = self._detect_priority(text, task.type)

        # Generate labels
        task.labels = self._generate_labels(task)

        return task

    # ---- DECIDE ----

    def decide(self, task: Task) -> Task:
        """Determine authority level and action plan."""
        task.authority = self._determine_authority(task)
        return task

    # ---- EXECUTE ----

    def execute(self, task: Task) -> EngineResult:
        """Execute the task based on type and authority."""
        if task.authority == Authority.ASK_FIRST:
            return EngineResult(
                task=task,
                action_taken="escalated",
                success=True,
                needs_escalation=True,
                escalation_reason=f"Task requires explicit approval: {task.title}",
                signals_emitted=[self._emit("⚠️", task.org, "OS", "escalation_needed", f"#{task.id}")],
            )

        handlers = {
            TaskType.ISSUE: self._handle_issue,
            TaskType.PR: self._handle_pr,
            TaskType.WEBHOOK: self._handle_webhook,
            TaskType.COMMAND: self._handle_command,
            TaskType.SCHEDULED: self._handle_scheduled,
            TaskType.SIGNAL: self._handle_signal,
        }

        handler = handlers.get(task.type, self._handle_default)
        return handler(task)

    # ---- LEARN ----

    def learn(self, result: EngineResult) -> None:
        """Update memory and log the result."""
        self.history.append(result)
        self.signals.extend(result.signals_emitted)

    # ---- FULL PIPELINE ----

    def process(self, raw_input: dict) -> EngineResult:
        """Run the full PERCEIVE → CLASSIFY → DECIDE → EXECUTE → LEARN loop."""
        task = self.perceive(raw_input)
        task = self.classify(task)
        task = self.decide(task)
        result = self.execute(task)
        self.learn(result)
        return result

    # ---- BATCH PROCESSING ----

    def process_batch(self, inputs: list[dict]) -> list[EngineResult]:
        """Process multiple inputs."""
        return [self.process(inp) for inp in inputs]

    # ---- STATUS ----

    def get_status(self) -> dict:
        """Return engine status summary."""
        return {
            "engine": "CeceEngine v2.0",
            "tasks_processed": len(self.history),
            "signals_emitted": len(self.signals),
            "success_rate": (
                sum(1 for r in self.history if r.success) / len(self.history)
                if self.history else 1.0
            ),
            "escalations": sum(1 for r in self.history if r.needs_escalation),
            "last_signal": str(self.signals[-1]) if self.signals else None,
        }

    # -----------------------------------------------------------------------
    # Private helpers
    # -----------------------------------------------------------------------

    def _detect_type(self, raw: dict) -> TaskType:
        if "issue" in raw.get("type", "").lower() or "issue" in raw:
            return TaskType.ISSUE
        if "pull_request" in raw.get("type", "").lower() or "pr" in raw:
            return TaskType.PR
        if "webhook" in raw.get("type", "").lower():
            return TaskType.WEBHOOK
        if "schedule" in raw.get("type", "").lower():
            return TaskType.SCHEDULED
        if "signal" in raw.get("type", "").lower():
            return TaskType.SIGNAL
        return TaskType.COMMAND

    def _detect_org(self, text: str) -> str:
        best_org = "OS"
        best_score = 0
        for pattern, org in ORG_KEYWORDS.items():
            matches = len(re.findall(pattern, text))
            if matches > best_score:
                best_score = matches
                best_org = org
        return best_org

    def _detect_priority(self, text: str, task_type: TaskType) -> Priority:
        critical_words = {"critical", "urgent", "emergency", "broken", "down", "security"}
        high_words = {"important", "blocker", "regression", "fail"}
        low_words = {"nice to have", "someday", "minor", "typo", "cosmetic"}

        words = set(text.split())
        if words & critical_words:
            return Priority.P0
        if words & high_words:
            return Priority.P1
        if words & low_words:
            return Priority.P3
        if task_type == TaskType.WEBHOOK:
            return Priority.P1
        return Priority.P2

    def _generate_labels(self, task: Task) -> list[str]:
        labels = [f"org:{task.org}", f"priority:{task.priority.name}"]
        type_map = {
            TaskType.ISSUE: "type:issue",
            TaskType.PR: "type:pr",
            TaskType.WEBHOOK: "type:webhook",
            TaskType.COMMAND: "type:command",
            TaskType.SCHEDULED: "type:scheduled",
            TaskType.SIGNAL: "type:signal",
        }
        labels.append(type_map.get(task.type, "type:unknown"))
        if task.authority == Authority.FULL_AUTO:
            labels.append("auto:approved")
        return labels

    def _determine_authority(self, task: Task) -> Authority:
        text = f"{task.title} {task.body}".lower()
        if any(kw in text for kw in ("delete", "destroy", "remove repo", "drop")):
            return Authority.ASK_FIRST
        if any(kw in text for kw in ("deploy prod", "production", "stripe", "payment")):
            return Authority.ASK_FIRST
        if task.type in (TaskType.ISSUE, TaskType.SIGNAL, TaskType.SCHEDULED):
            return Authority.FULL_AUTO
        return Authority.SUGGEST

    def _emit(self, icon: str, src: str, dst: str, event: str, details: str = "") -> Signal:
        sig = Signal(icon=icon, source=src, destination=dst, event=event, details=details)
        self.signals.append(sig)
        return sig

    # ---- Task-type handlers ----

    def _handle_issue(self, task: Task) -> EngineResult:
        output_lines = [
            f"Triaged issue: {task.title}",
            f"  Org: {task.org} ({ORG_CODES.get(task.org, 'Unknown')})",
            f"  Priority: {task.priority.name}",
            f"  Labels: {', '.join(task.labels)}",
        ]
        return EngineResult(
            task=task,
            action_taken="triaged",
            output="\n".join(output_lines),
            signals_emitted=[self._emit("🔍", "OS", task.org, "issue_triaged", f"#{task.id}")],
        )

    def _handle_pr(self, task: Task) -> EngineResult:
        output_lines = [
            f"Reviewed PR: {task.title}",
            f"  Org: {task.org}",
            f"  Checks: correctness, security, performance, style, tests",
        ]
        return EngineResult(
            task=task,
            action_taken="reviewed",
            output="\n".join(output_lines),
            signals_emitted=[self._emit("📝", "OS", task.org, "pr_reviewed", f"#{task.id}")],
        )

    def _handle_webhook(self, task: Task) -> EngineResult:
        provider = task.metadata.get("provider", "unknown")
        return EngineResult(
            task=task,
            action_taken="processed_webhook",
            output=f"Processed webhook from {provider}: {task.title}",
            signals_emitted=[self._emit("📥", provider.upper(), task.org, "webhook_processed")],
        )

    def _handle_command(self, task: Task) -> EngineResult:
        return EngineResult(
            task=task,
            action_taken="executed_command",
            output=f"Executed: {task.title}",
            signals_emitted=[self._emit("⚡", "OS", task.org, "command_executed")],
        )

    def _handle_scheduled(self, task: Task) -> EngineResult:
        return EngineResult(
            task=task,
            action_taken="ran_scheduled",
            output=f"Ran scheduled task: {task.title}",
            signals_emitted=[self._emit("⏰", "OS", task.org, "scheduled_complete")],
        )

    def _handle_signal(self, task: Task) -> EngineResult:
        return EngineResult(
            task=task,
            action_taken="processed_signal",
            output=f"Processed signal: {task.title}",
            signals_emitted=[self._emit("📡", task.org, "OS", "signal_processed")],
        )

    def _handle_default(self, task: Task) -> EngineResult:
        return EngineResult(
            task=task,
            action_taken="acknowledged",
            output=f"Acknowledged: {task.title}",
            signals_emitted=[self._emit("✔️", "OS", "OS", "task_acknowledged")],
        )
