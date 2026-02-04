"""
Audit Log Store
Append-only storage with indexing for fast queries.
"""

import time
from collections import defaultdict
from typing import Optional

# AuditEvent is imported at runtime to avoid circular imports


class AuditStore:
    """
    Append-only audit event storage with indexing.

    Indexes:
    - by_actor: actor -> [event_indices]
    - by_action: action -> [event_indices]
    - by_category: category -> [event_indices]
    - by_outcome: outcome -> [event_indices]
    - by_time: sorted chronologically (natural append order)
    """

    def __init__(self, max_events: int = 50000):
        self._events: list[dict] = []
        self._max_events = max_events

        # Indexes for fast lookups
        self._by_actor: dict[str, list[int]] = defaultdict(list)
        self._by_action: dict[str, list[int]] = defaultdict(list)
        self._by_category: dict[str, list[int]] = defaultdict(list)
        self._by_outcome: dict[str, list[int]] = defaultdict(list)

    def append(self, event) -> None:
        """Append an event to the store."""
        evt_dict = event.to_dict()
        idx = len(self._events)

        self._events.append(evt_dict)

        # Update indexes
        self._by_actor[evt_dict["actor"]].append(idx)
        self._by_action[evt_dict["action"]].append(idx)
        self._by_category[evt_dict["category"]].append(idx)
        self._by_outcome[evt_dict["outcome"]].append(idx)

        # Evict oldest if over limit
        if len(self._events) > self._max_events:
            self._compact()

    def query(
        self,
        actor: Optional[str] = None,
        action: Optional[str] = None,
        category: Optional[str] = None,
        outcome: Optional[str] = None,
        since: Optional[float] = None,
        limit: int = 100,
    ) -> list[dict]:
        """
        Query events with optional filters.
        Returns newest first.
        """
        # Start with candidate indices
        candidates = None

        if actor and actor in self._by_actor:
            candidates = set(self._by_actor[actor])
        if action and action in self._by_action:
            action_set = set(self._by_action[action])
            candidates = candidates & action_set if candidates is not None else action_set
        if category and category in self._by_category:
            cat_set = set(self._by_category[category])
            candidates = candidates & cat_set if candidates is not None else cat_set
        if outcome and outcome in self._by_outcome:
            out_set = set(self._by_outcome[outcome])
            candidates = candidates & out_set if candidates is not None else out_set

        # If no filters, use all indices
        if candidates is None:
            candidates = set(range(len(self._events)))

        # Filter by time
        results = []
        for idx in sorted(candidates, reverse=True):
            if idx >= len(self._events):
                continue
            evt = self._events[idx]
            if since and evt["timestamp"] < since:
                continue
            results.append(evt)
            if len(results) >= limit:
                break

        return results

    def count(self) -> int:
        """Total number of stored events."""
        return len(self._events)

    def summary(self) -> dict:
        """Summarize the audit log."""
        by_category = {}
        for cat, indices in self._by_category.items():
            by_category[cat] = len(indices)

        by_outcome = {}
        for out, indices in self._by_outcome.items():
            by_outcome[out] = len(indices)

        by_actor = {}
        for actor, indices in self._by_actor.items():
            by_actor[actor] = len(indices)

        # Top actions
        top_actions = sorted(
            [(a, len(i)) for a, i in self._by_action.items()],
            key=lambda x: x[1],
            reverse=True,
        )[:10]

        return {
            "total_events": len(self._events),
            "by_category": by_category,
            "by_outcome": by_outcome,
            "by_actor": by_actor,
            "top_actions": [{"action": a, "count": c} for a, c in top_actions],
            "oldest_event": self._events[0]["timestamp"] if self._events else None,
            "newest_event": self._events[-1]["timestamp"] if self._events else None,
        }

    def _compact(self) -> None:
        """Remove oldest events and rebuild indexes."""
        # Keep the most recent half
        keep_from = len(self._events) // 2
        self._events = self._events[keep_from:]

        # Rebuild indexes
        self._by_actor.clear()
        self._by_action.clear()
        self._by_category.clear()
        self._by_outcome.clear()

        for idx, evt in enumerate(self._events):
            self._by_actor[evt["actor"]].append(idx)
            self._by_action[evt["action"]].append(idx)
            self._by_category[evt["category"]].append(idx)
            self._by_outcome[evt["outcome"]].append(idx)
