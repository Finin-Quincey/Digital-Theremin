"""
Waveform Generator

Module that generates sampled waveforms.
"""

import math

def sine(amp, sample_freq, duration):
    """
    Generates a sampled sine wave.
    Parameters:
    - amp: The peak-to-peak amplitude of the waveform (minimum is always zero)
    - sample_freq: Sampling frequency, in Hz
    - duration: The duration of the sample
    """
    return [math.sin(t) for t in range(0, duration, 1/sample_freq)]