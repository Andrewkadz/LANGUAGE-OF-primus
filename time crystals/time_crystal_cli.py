#!/usr/bin/env python
"""
Time Crystal CLI

Run the multi-scale tau crystal in the terminal with optional real-time
ASCII/Unicode sparkline and spaced pattern output. Optionally stream
state over UDP for integration.

Examples (PowerShell):
  # Finite run, 300 steps, terminal plot + encoded pattern
  # and ASCII-safe blocks (useful on Windows consoles)
  # No visualization files created
  py -3 time_crystal_cli.py --steps 300 --terminal-plot --encoded --ascii --skip-vis

  # Infinite run with UDP publish to localhost:9999
  py -3 time_crystal_cli.py --infinite --terminal-plot --encoded --udp 127.0.0.1:9999

Press Ctrl+C to stop.
"""

import argparse
import json
import os
import socket
import sys
import time
from collections import deque
from typing import List, Optional, Tuple

import numpy as np

# Local import
from multi_scale_tau_crystal import TemporalAnchorModule


def sparkline(vals: List[float], width: int = 60, ascii_only: bool = False) -> str:
    if not vals:
        return ' ' * width
    recent = vals[-width:]
    vmin = min(recent)
    vmax = max(recent)
    if vmax - vmin < 1e-9:
        return '-' * len(recent) + ' ' * (width - len(recent))
    unicode_blocks = ['\u2581','\u2582','\u2583','\u2584','\u2585','\u2586','\u2587','\u2588']
    ascii_blocks = ['.', ':', '-', '=', '+', '*', '#', '@']
    blocks = ascii_blocks if ascii_only else unicode_blocks
    out = []
    for v in recent:
        t = (v - vmin) / (vmax - vmin)
        idx = int(t * (len(blocks) - 1))
        out.append(blocks[idx])
    if len(out) < width:
        out.extend([' '] * (width - len(out)))
    s = ''.join(out)
    if not ascii_only:
        enc = (getattr(sys.stdout, 'encoding', None) or 'utf-8').lower()
        try:
            s.encode(enc, errors='strict')
        except Exception:
            # Fallback to ASCII blocks
            out = []
            for v in recent:
                t = (v - vmin) / (vmax - vmin)
                idx = int(t * (len(ascii_blocks) - 1))
                out.append(ascii_blocks[idx])
            if len(out) < width:
                out.extend([' '] * (width - len(out)))
            s = ''.join(out)
    return s


def parse_udp(target: Optional[str]) -> Optional[Tuple[str, int]]:
    if not target:
        return None
    if ':' not in target:
        raise ValueError("--udp must be in host:port form, e.g., 127.0.0.1:9999")
    host, port_s = target.rsplit(':', 1)
    return host, int(port_s)


def run_cli(steps: Optional[int], infinite: bool, encoded: bool, ascii_only: bool, terminal_plot: bool, udp_target: Optional[str]):
    anchor_module = TemporalAnchorModule()
    pattern = deque(maxlen=60)

    udp_addr = parse_udp(udp_target)
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) if udp_addr else None

    def publish(step: int, field_harm: float, anchor: str):
        if not udp_sock:
            return
        payload = {
            't': time.time(),
            'step': step,
            'anchor': anchor,
            'harmonic': field_harm,
        }
        data = json.dumps(payload).encode('utf-8')
        udp_sock.sendto(data, udp_addr)  # type: ignore[arg-type]

    current_step = 0
    try:
        if infinite:
            while True:
                field = anchor_module.generate_harmonic_time_field()
                ctx = anchor_module.ai_temporal_context()

                anchor = ctx['temporal_anchor']
                sym = '+' if anchor == 'FLOW+' else ('-' if anchor == 'FLOW-' else '0')
                pattern.append(sym)
                pattern_str = ' '.join(pattern) if encoded else ''.join(pattern)

                if terminal_plot and current_step % 5 == 0:
                    plot_str = sparkline(list(anchor_module.harmonic_field), width=60, ascii_only=ascii_only)
                    print(
                        f"\rStep {current_step:>9,d} | Anchor: {anchor:5s} | Mode: {ctx['processing_mode']:10s} | "
                        f"Scale: {ctx['attention_scale']:5s} | Mem: {ctx['memory_priority']:.2f} | "
                        f"Harm: {field['harmonic']:+.3f} | Plot: {plot_str} | Pat: {pattern_str:<60}",
                        end='', flush=True
                    )
                elif current_step % 20 == 0:
                    print(
                        f"Step {current_step:3d}: {anchor:6s} | Mode: {ctx['processing_mode']:10s} | "
                        f"Scale: {ctx['attention_scale']:5s} | Memory: {ctx['memory_priority']:.2f}"
                    )

                publish(current_step, field['harmonic'], anchor)
                current_step += 1
        else:
            total = 100 if steps is None else steps
            for step in range(total):
                field = anchor_module.generate_harmonic_time_field()
                ctx = anchor_module.ai_temporal_context()

                anchor = ctx['temporal_anchor']
                sym = '+' if anchor == 'FLOW+' else ('-' if anchor == 'FLOW-' else '0')
                pattern.append(sym)
                pattern_str = ' '.join(pattern) if encoded else ''.join(pattern)

                if terminal_plot and step % 5 == 0:
                    plot_str = sparkline(list(anchor_module.harmonic_field), width=60, ascii_only=ascii_only)
                    print(
                        f"\rStep {step:>9,d} | Anchor: {anchor:5s} | Mode: {ctx['processing_mode']:10s} | "
                        f"Scale: {ctx['attention_scale']:5s} | Mem: {ctx['memory_priority']:.2f} | "
                        f"Harm: {field['harmonic']:+.3f} | Plot: {plot_str} | Pat: {pattern_str:<60}",
                        end='', flush=True
                    )
                elif step % 20 == 0:
                    print(
                        f"Step {step:3d}: {anchor:6s} | Mode: {ctx['processing_mode']:10s} | "
                        f"Scale: {ctx['attention_scale']:5s} | Memory: {ctx['memory_priority']:.2f}"
                    )
                publish(step, field['harmonic'], anchor)
            if terminal_plot:
                print()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")
    finally:
        if udp_sock:
            udp_sock.close()


def main():
    p = argparse.ArgumentParser(description="Time Crystal CLI (multi-scale tau crystal)")
    p.add_argument('--steps', type=int, default=300, help='Finite run steps (ignored if --infinite)')
    p.add_argument('--infinite', action='store_true', help='Run indefinitely until Ctrl+C')
    p.add_argument('--encoded', action='store_true', help='Show spaced pattern symbols (e.g., "+ + 0 0 - -")')
    p.add_argument('--terminal-plot', action='store_true', help='Show real-time sparkline plot in console')
    p.add_argument('--ascii', action='store_true', help='Force ASCII plot characters for Windows consoles')
    p.add_argument('--udp', type=str, default=None, help='Send JSON state via UDP to host:port')
    p.add_argument('--skip-vis', action='store_true', help='No-op placeholder (visualization lives in demo script)')

    args = p.parse_args()

    run_cli(
        steps=args.steps,
        infinite=args.infinite,
        encoded=args.encoded,
        ascii_only=args.ascii,
        terminal_plot=args.terminal_plot,
        udp_target=args.udp,
    )


if __name__ == '__main__':
    main()
