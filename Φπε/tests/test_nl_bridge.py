from __future__ import annotations
from pathlib import Path
import sys

# Add repo root for imports
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.nl_bridge import english_to_phipe, phi_trace_to_english, wrap_prompt_file


def test_mapping_basic():
    assert english_to_phipe("Test how change interacts with reason").replace(" ", "") in {"Δ:Ψ", "Ψ:Δ"}


def test_mapping_render_private():
    expr = english_to_phipe("render private reason")
    assert "Π(" in expr and "→ Λ" in expr


def test_trace_summary_counts(tmp_path: Path):
    # Create a tiny fake trace with two Lambda entries and a loop motif
    fake = "Σ(Λ(Ξ, Φ, Φ, Φ, Σ([Δ:Ψ]), Σ(ζ)), Λ(Λ, Φ, Φ, Φ, Σ([Δ:Ψ],[Δ:Ψ]), Σ(ζ, ζ)))\n"
    txt = phi_trace_to_english(fake)
    assert "steps: 2" in txt
    assert "loop_motif_[Δ:Ψ]: 3" in txt or "loop_motif_[Δ:Ψ]: 2" in txt


def test_wrap_header():
    out = wrap_prompt_file("Σ(Δ + Ψ)")
    assert out.startswith("Φπε PRIMUS :: SYMBOL SET")
