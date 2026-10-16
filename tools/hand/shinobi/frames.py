"""Shinobi (Fire / red) — hand-pixelled frames.  (palette stub, beats to follow)"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from handkit import Grid, Palette, render, strip, gif, sheet  # noqa: E402

NAME = "shinobi"
BOX = 64
GROUND = 53
X_OFF = 8
ORIGIN = (32, 54)

# 15 opaque colours.
PAL = Palette(NAME, {
    "H": (248, 248, 248), "h": (178, 186, 204), "g": (104, 110, 130),   # steel edge, steel, iron/chain
    "S": (236, 190, 150), "s": (182, 126, 94),                          # skin (eyes, hands)
    "K": (122, 122, 140), "k": (74, 74, 90), "n": (46, 46, 60),         # black cloth: highlight, mid, shadow
    "R": (236, 52, 52), "r": (164, 22, 36), "q": (96, 8, 26),           # red ramp (trigram)
    "L": (118, 84, 56), "l": (70, 48, 32),                              # bandage / wrap
    "B": (36, 36, 48),                                                   # boot / deepest cloth
})
