"""enigma_core: a deterministic, tested Enigma I simulator.

This package is the single source of cryptographic truth for the documentary.
Blender, Manim and Remotion never compute encryption themselves; they read the
event stream produced here (see events.py).
"""
from .configuration import MachineConfig
from .machine import EnigmaMachine

__all__ = ["EnigmaMachine", "MachineConfig"]
