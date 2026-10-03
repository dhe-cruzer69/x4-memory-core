"""Memory layer abstractions."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class MemoryEntry:
    key: str
    value: Any
    layer: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    evidence: List[str] = field(default_factory=list)


class MemoryStore:
    def __init__(self) -> None:
        self._store: Dict[str, List[MemoryEntry]] = {
            "working": [],
            "episodic": [],
            "semantic": [],
        }

    def put(self, layer: str, key: str, value: Any, evidence: List[str] | None = None) -> None:
        if layer not in self._store:
            raise ValueError(f"Unknown layer: {layer}")
        self._store[layer].append(MemoryEntry(key=key, value=value, layer=layer, evidence=evidence or []))

    def get(self, layer: str, key: str) -> MemoryEntry | None:
        for e in reversed(self._store.get(layer, [])):
            if e.key == key:
                return e
        return None
