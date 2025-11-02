#!/usr/bin/env python3
from __future__ import annotations
import readline  # history/editing
from pathlib import Path
import subprocess
import sys

# Repo root
REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools import nl_bridge
from tools.phi_memory import PhiMemory
from tools.phiscript import eval_script

AGENT_PATH = REPO_ROOT / "ERCA" / "ERCA_P3.phipe"
PROMPT_PATH = REPO_ROOT / "ERCA" / "prompts" / "N_generated.phipe"
TRACE_PATH = REPO_ROOT / "ERCA" / "traces" / "N.trace"
MEMORY_PATH = REPO_ROOT / "ERCA" / "traces" / "session.jsonl"

mem = PhiMemory(MEMORY_PATH)

print("Φπε Threaded REPL — conversational symbolic interface\n"
      "Commands: :last, :summary, :exit\n")

while True:
    try:
        msg = input("Φπε> ")
    except EOFError:
        print()
        break
    if not msg.strip():
        continue

    if msg.strip().lower() in {":exit", "exit"}:
        break

    if msg.strip().lower() == ":last":
        last = mem.last()
        if last:
            print("Last Φπε:", last.get("phi_body", ""))
            print("Last summary:\n", (last.get("summary", "").strip() or "(none)"))
        else:
            print("(No memory yet)")
        continue

    if msg.strip().lower() == ":summary":
        if TRACE_PATH.exists():
            print(nl_bridge.phi_trace_to_english(TRACE_PATH.read_text(encoding='utf-8')))
        else:
            print("(No trace produced yet)")
        continue

    # Inline PhiScript: :script <commands separated by ';'>
    if msg.startswith(":script"):
        last = mem.last()
        prev_phi = last.get("phi_body") if last else None
        last_summary = last.get("summary") if last else None
        script = msg[len(":script"):].strip()
        if not script:
            print("(No script provided)")
            continue
        body = eval_script(script, prev_expr=prev_phi, last_summary=last_summary)
        wrapped = nl_bridge.wrap_prompt_file(body)
        PROMPT_PATH.parent.mkdir(parents=True, exist_ok=True)
        PROMPT_PATH.write_text(wrapped, encoding="utf-8")
        cmd = [sys.executable, str(REPO_ROOT / 'scripts' / 'erca-run'), str(AGENT_PATH),
               '--prompt', str(PROMPT_PATH), '--out', str(TRACE_PATH)]
        subprocess.run(cmd, cwd=str(REPO_ROOT), check=False)
        if TRACE_PATH.exists():
            summary = nl_bridge.phi_trace_to_english(TRACE_PATH.read_text(encoding='utf-8'), mode='compact', markdown=False)
        else:
            summary = "(No trace produced)\n"
        mem.append(english=f"[PhiScript] {script}", phi_body=body, prompt_path=PROMPT_PATH, trace_path=TRACE_PATH, summary=summary)
        print(summary)
        continue

    # Context from last
    last = mem.last()
    prev_phi = last.get("phi_body") if last else None

    # Map English to Φπε with context
    body = nl_bridge.english_to_phipe(msg, prev_phi=prev_phi)
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
    else:
        summary = "(No trace produced)\n"

    # Append to memory
    mem.append(english=msg, phi_body=body, prompt_path=PROMPT_PATH, trace_path=TRACE_PATH, summary=summary)

    print(summary)
