from __future__ import annotations
import sys
from pathlib import Path
from primus_engine.parser import parse
from primus_engine.reducer import reduce_with_trace
from primus_engine.ast import pretty


def run_file(path: Path) -> None:
    src = path.read_text(encoding='utf-8')
    terms = parse(src)
    # For each non-header term, produce a trace stream
    for term in terms:
        trace_stream = reduce_with_trace(term)
        print(pretty(trace_stream))


def main(argv):
    if len(argv) < 2:
        print("Usage: python -m primus_engine.runner <file1.phipe> [file2.phipe ...]")
        return 1
    for p in argv[1:]:
        run_file(Path(p))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
