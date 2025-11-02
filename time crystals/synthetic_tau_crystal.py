import os
import numpy as np
from collections import deque

class SyntheticTauCrystal:
    def __init__(self, freq=1.0, feedback_strength=0.99):
        self.tau = 0.0  # initial temporal state
        self.phase = 0.0
        self.freq = freq
        self.feedback_strength = feedback_strength  # Λ feedback
        self.history = []

    def step(self):
        # Θ oscillatory stability: pure sine wave
        theta = np.sin(self.phase)

        # Ξ entropy suppressed (≈ 0)
        xi = 0.0  

        # ΔΦ near zero, but we simulate tiny drift from phase advance
        delta_phi = np.sin(self.phase + 0.1) - np.sin(self.phase)

        # Harmonic Time Equation simplified for τ crystal
        self.tau = self.feedback_strength * (theta + delta_phi)

        # Collapse into symbolic output
        if self.tau > 0.5:
            state = "+"
        elif self.tau < -0.5:
            state = "-"
        else:
            state = "0"

        # Advance phase
        self.phase += 2 * np.pi * self.freq / 100.0  

        # Store
        self.history.append((self.tau, state))
        return state

# Example usage: run indefinitely with near-impossible self-termination
if __name__ == "__main__":
    crystal = SyntheticTauCrystal(freq=1.0, feedback_strength=0.995)
    steps = 0
    pattern = deque(maxlen=60)
    encoded = os.getenv('TAU_ENCODED', '0') == '1'
    try:
        while True:
            state = crystal.step()
            steps += 1
            pattern.append(state)
            pattern_str = ' '.join(pattern) if encoded else ''.join(pattern)
            # Overwrite a single status line (no scroll)
            print(
                f"\rSteps: {steps:,}  State: {state}  Tau: {crystal.tau:+.3f}  | Pattern: {pattern_str:<60}",
                end="",
                flush=True,
            )
            # Near-impossible termination conditions:
            # 1) Extremely large step count threshold (practically unreachable)
            # 2) Ultra-rare random trigger (1e-15 per step)
            if steps >= 10**12:
                break
            if np.isfinite(crystal.tau) and np.random.random() < 1e-15:
                break
    except KeyboardInterrupt:
        pass
    print()
