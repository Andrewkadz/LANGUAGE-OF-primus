from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Dict, Any, Iterable
import json
import time

@dataclass
class MemoryEntry:
    id: str
    ts: float
    english: str
    phi_body: str
    prompt_path: Optional[str] = None
    trace_path: Optional[str] = None
    summary: Optional[str] = None

class PhiMemory:
    """
    Append-only JSONL memory for conversational Φπε sessions.
    Stores english input, mapped Φπε body, file paths, and summaries.
    """
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("", encoding="utf-8")

    def append(self, english: str, phi_body: str, prompt_path: Optional[Path] = None,
               trace_path: Optional[Path] = None, summary: Optional[str] = None) -> MemoryEntry:
        eid = f"m{int(time.time()*1000)}"
        entry = MemoryEntry(
            id=eid,
            ts=time.time(),
            english=english,
            phi_body=phi_body,
            prompt_path=str(prompt_path) if prompt_path else None,
            trace_path=str(trace_path) if trace_path else None,
            summary=summary,
        )
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")
        return entry

    def iter(self) -> Iterable[Dict[str, Any]]:
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue

    def last(self) -> Optional[Dict[str, Any]]:
        last_obj = None
        for obj in self.iter():
            last_obj = obj
        return last_obj
