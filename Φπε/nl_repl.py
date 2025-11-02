#!/usr/bin/env python3
from __future__ import annotations
import readline  # for input history/editing
from pathlib import Path
import subprocess
import sys

# Ensure repo root discoverable
REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools import nl_bridge

AGENT_PATH = REPO_ROOT / "ERCA" / "ERCA_P3.phipe"
PROMPT_PATH = REPO_ROOT / "ERCA" / "prompts" / "N_generated.phipe"
TRACE_PATH = REPO_ROOT / "ERCA" / "traces" / "N.trace"

print("Φπε REPL — type English prompts. Type 'exit' to quit.\n")

while True:
    try:
        msg = input("Φπε> ")
    except EOFError:
        print()
        break
    if msg.strip().lower() == "exit":
        break
    if not msg.strip():
        continue

    # Map English to Φπε and write prompt
    body = nl_bridge.english_to_phipe(msg)
    wrapped = nl_bridge.wrap_prompt_file(body)
    PROMPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROMPT_PATH.write_text(wrapped, encoding="utf-8")

    # Run via existing CLI runner
    cmd = [sys.executable, str(REPO_ROOT / 'scripts' / 'erca-run'), str(AGENT_PATH),
           '--prompt', str(PROMPT_PATH), '--out', str(TRACE_PATH)]
    subprocess.run(cmd, cwd=str(REPO_ROOT), check=False)

    # Summarize the trace
    if TRACE_PATH.exists():
        summary = nl_bridge.phi_trace_to_english(TRACE_PATH.read_text(encoding='utf-8'), mode='compact', markdown=False)
        print(summary)
    else:
        print("(No trace produced)")
