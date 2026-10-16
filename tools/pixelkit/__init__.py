"""pixelkit — a tiny toolkit for drawing original GBA Fire Emblem-style battle
sprites in code.

Everything is drawn on a *letter canvas*: a 2-D grid of palette letters.
Parts (heads, torsos, boots, weapon heads) are authored as text grids using
those letters; limbs are shaded capsules; weapons are shaded tapered lines;
slash blurs are arcs. The letter canvas is turned into RGBA only at the end,
through each fighter's 16-colour palette, after the outline pass.

Letter conventions (keep these so parts can be shared between fighters):

    .  or space   transparent            o   outline (dark, never pure black)
    S s z         skin   hi / base / shadow
    H h g         hair   hi / base / shadow
    C c k         primary cloth (trigram colour)   hi / base / shadow
    A a q         accent cloth / secondary          hi / base / shadow
    M m n         metal / steel                     hi / base / shadow
    L l j         leather, wood, brown              hi / base / shadow
    w             white (eye glint, teeth, blade edge)
    E e           effect: slash core / slash edge   (not outlined)
    %             ground shadow (semi-transparent)  (not outlined)
    ?             "keep what is under" — a no-op pixel inside a grid

See `tools/STYLE.md` for the drawing rules the fighters follow.
"""
from .canvas import Canvas, Part, grid, flip_part, rot90_part, TRANSPARENT, NO_OUTLINE
from .shapes import capsule, polyline_capsule, blade, arc, ellipse, fill_polygon, line, shaded_ellipse, tapered_chain
from .figure import Figure, BUILD
from .palette import Palette, check_palette
from .sheet import Animation, pack_sheet, preview_gif, preview_png, contact_sheet

__all__ = [
    "Canvas", "Part", "grid", "flip_part", "rot90_part", "TRANSPARENT", "NO_OUTLINE",
    "capsule", "polyline_capsule", "blade", "arc", "ellipse", "fill_polygon", "line", "shaded_ellipse", "tapered_chain",
    "Figure", "BUILD",
    "Palette", "check_palette",
    "Animation", "pack_sheet", "preview_gif", "preview_png", "contact_sheet",
]
