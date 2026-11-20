#!/usr/bin/env python3
"""
`cairo_handdrawn_v4.py` — Indie Hand-Crafted Analog Ink & Cel-Timing Engine (v4.0 — De-AI-ified!)
First-Principles & Tacit-Knowledge Upgrades over v3.0:
1. True Fountain-Pen Pressure Modulation (`nib_pressure`): strokes organically thicken on downward/belly arcs
   and taper into razor-crisp hairlines at entry/exit, with subtle ink-pooling weight at corners (zero digital tubes!).
2. Human Draftsman Graphite Under-Drawing (`pencil_underdraw`): ultra-subtle 11%–15% warm-graphite construction
   lines that overshoot corners by 5–9px — the unmistakable tactile trace of a human animator's rough pass!
3. Hand-Sketched Diagonal Hatch Cast Shadows (`soft_shadow` upgraded): replaces sterile digital grey radial ovals
   with authentic comic/indie-animation parallel pen-hatch shadows grounded right under props and Xeron!
4. Wet-Edge Hand-Swiped Copic Marker Washes (`marker_wash_poly`): layered directional marker passes with subtle
   darker pigment pooling along the outer wet-edge — organic illustration depth instead of computer airbrush gradients!
5. Restrained Climax-Only Luminescence + Comic Motion Smears & Impact Ticks (`draw_impact_ticks`, `draw_smear_arcs`).
6. Snappy 2D Animator Timing (`snap_ease`, `anticipate_overshoot`, `cel_time`) + Plush Xeron Squash/Stretch & Head-Tilt!
"""
import hashlib
import math
import cairo
import numpy as np


PAL = {
    "white":      (1.000, 1.000, 1.000),
    "ink":        (0.082, 0.086, 0.094),  # Warm carbon-sumi fountain-pen ink `#151618`
    "ink_soft":   (0.365, 0.378, 0.398),  # Warm 2B graphite pencil
    "ink_faint":  (0.680, 0.692, 0.708),  # Faint rough-pass construction pencil
    "cat":        (0.055, 0.058, 0.066),  # Deep sumi-ink black fur
    "cat_sheen":  (0.260, 0.275, 0.305),  # Subtle dry-brush fur sheen
    "ear_inner":  (0.435, 0.388, 0.478),  # Muted violet-grey `#6F637A`
    "ear_deep":   (0.310, 0.272, 0.352),
    "mint":       (0.180, 0.898, 0.616),  # Core `#2EE59D`
    "mint_light": (0.720, 0.980, 0.875),  # Soft pastel Copic highlight
    "mint_deep":  (0.055, 0.530, 0.360),  # `#0E875C` deep botanical mint ink
    "mint_wash":  (0.420, 0.930, 0.735),  # Copic G02-style hand-swiped mint wash
    "wood_wash":  (0.790, 0.705, 0.605),  # Warm raw-paper ochre/kraft wash
    "dark_bulb":  (0.280, 0.292, 0.308),  # Smoked charcoal glass
    "red":        (0.790, 0.235, 0.215),  # Vermilion draftsman correction ink `#C93C37`
    "amber":      (0.865, 0.535, 0.195),  # Warm ochre-copper ink
}


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if v < lo else (hi if v > hi else v)


def lerp(a: float, b: float, u: float) -> float:
    return a + (b - a) * u


def ease_out_cubic(x: float) -> float:
    x = clamp(x)
    return 1.0 - (1.0 - x) ** 3


def ease_in_cubic(x: float) -> float:
    x = clamp(x)
    return x * x * x


def ease_in_out(x: float) -> float:
    x = clamp(x)
    return 3 * x * x - 2 * x * x * x


def smootherstep(x: float) -> float:
    x = clamp(x)
    return x * x * x * (x * (x * 6.0 - 15.0) + 10.0)


def spring_overshoot(x: float, tension: float = 1.85) -> float:
    x = clamp(x)
    c = tension
    u = x - 1.0
    return 1.0 + (c + 1.0) * (u ** 3) + c * (u ** 2)


def snap_settle(x: float, overshoot: float = 0.08) -> float:
    """Snappy 2D anime/cel timing: brisk 0->1.08 burst + crisp organic settle to 1.0 (zero floaty sine tween!)."""
    x = clamp(x)
    if x < 0.72:
        u = x / 0.72
        return (1.0 + overshoot) * (1.0 - (1.0 - u) ** 3.2)
    u = (x - 0.72) / 0.28
    return 1.0 + overshoot * math.cos(u * math.pi * 0.5) * (1.0 - u)


def anticipation_curve(x: float, back_amt: float = 0.16) -> float:
    x = clamp(x)
    if x < 0.22:
        u = x / 0.22
        return -back_amt * math.sin(u * math.pi)
    u = (x - 0.22) / 0.78
    return snap_settle(u, overshoot=0.07)


def cel_time(t: float, fps: float = 24.0) -> float:
    """Quantizes continuous time to hand-drawn `24fps` (on 2s/3s feel) for crisp human cel cadence without jitter."""
    return math.floor(t * fps) / fps


def _seed_float(key: str, idx: int = 0) -> float:
    h = hashlib.md5(f"{key}_{idx}".encode("utf-8")).digest()
    return (int.from_bytes(h[:4], "little") / 4294967295.0) * 2.0 - 1.0


def sample_bezier(p0, p1, p2, p3=None, n: int = 28) -> np.ndarray:
    t = np.linspace(0.0, 1.0, n, dtype=np.float64)[:, None]
    p0 = np.asarray(p0, dtype=np.float64)
    p1 = np.asarray(p1, dtype=np.float64)
    p2 = np.asarray(p2, dtype=np.float64)
    if p3 is None:
        return ((1 - t) ** 2) * p0 + 2 * (1 - t) * t * p1 + (t ** 2) * p2
    p3 = np.asarray(p3, dtype=np.float64)
    return ((1 - t) ** 3) * p0 + 3 * ((1 - t) ** 2) * t * p1 + 3 * (1 - t) * (t ** 2) * p2 + (t ** 3) * p3


def catmull_rom_chain(pts, samples_per_seg: int = 8) -> np.ndarray:
    arr = np.asarray(pts, dtype=np.float64)
    if len(arr) <= 2:
        return arr
    p_ext = np.vstack([2.0 * arr[0] - arr[1], arr, 2.0 * arr[-1] - arr[-2]])
    out = []
    u = np.linspace(0.0, 1.0, samples_per_seg, endpoint=False)[:, None]
    u2 = u * u
    u3 = u2 * u
    for i in range(len(arr) - 1):
        p0, p1, p2, p3 = p_ext[i], p_ext[i + 1], p_ext[i + 2], p_ext[i + 3]
        seg = 0.5 * (
            (2.0 * p1)
            + (-p0 + p2) * u
            + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * u2
            + (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * u3
        )
        out.append(seg)
    out.append(arr[-1:])
    return np.vstack(out)


class HandDrawnStage:
    """
    Indie Hand-Crafted Analog Ink & Copic Watercolor Stage (v4.0).
    Pure `#FFFFFF` paper space with authentic dip-pen pressure modulation, faint graphite rough-pass overshoots,
    hand-hatched contact shadows, and wet-edge Copic washes — zero sterile digital/AI vector sheen!
    """

    def __init__(self, t: float, width: int = 1920, height: int = 1080):
        self.t = t
        self.w = width
        self.h = height
        # Isolated 12fps (`onTwos`) hand-traced boil step (`ClaudeAnimationBase` standard)
        self.boil_step = int(math.floor(t * 12.0))
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.ctx = cairo.Context(self.surface)
        self.ctx.set_antialias(cairo.ANTIALIAS_BEST)
        self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        self.ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        self.ctx.set_source_rgb(1.0, 1.0, 1.0)
        self.ctx.paint()

    def push_camera(self, zoom: float = 1.0, dx: float = 0.0, dy: float = 0.0, rot_deg: float = 0.0, piv=(960.0, 520.0)):
        self.ctx.save()
        self.ctx.translate(piv[0] + dx, piv[1] + dy)
        if abs(rot_deg) > 1e-4:
            self.ctx.rotate(math.radians(rot_deg))
        if abs(zoom - 1.0) > 1e-4:
            self.ctx.scale(zoom, zoom)
        self.ctx.translate(-piv[0], -piv[1])

    def pop_camera(self):
        self.ctx.restore()

    def soft_shadow(self, cx: float, cy: float, rx: float, ry: float, alpha: float = 0.14):
        """
        Hand-Sketched Diagonal Ink-Hatch Contact Shadow (replaces digital grey airbrush ovals!).
        Draws an ultra-faint graphite wash plus crisp diagonal pencil strokes clipped to an organic ground ellipse.
        """
        if rx <= 2.0 or ry <= 1.0 or alpha <= 0.005:
            return
        ctx = self.ctx
        ctx.save()
        ctx.translate(cx, cy)
        ctx.scale(rx, ry)
        ctx.new_path()
        ctx.arc(0.0, 0.0, 1.0, 0.0, 2.0 * math.pi)
        ctx.set_source_rgba(0.10, 0.11, 0.13, alpha * 0.42)
        ctx.fill_preserve()
        ctx.clip()
        ctx.restore()

        # Crisp hand-sketched diagonal hatch lines inside the shadow footprint
        ctx.save()
        ctx.translate(cx, cy)
        ctx.scale(rx, ry)
        ctx.arc(0.0, 0.0, 1.0, 0.0, 2.0 * math.pi)
        ctx.restore()
        ctx.save()
        ctx.clip()
        sp = max(7.5, min(12.5, rx * 0.14))
        n_h = int((rx * 2.2) / sp)
        ctx.set_source_rgba(0.14, 0.16, 0.19, min(0.36, alpha * 2.1))
        ctx.set_line_width(1.35)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for i in range(-n_h, n_h + 1):
            x0 = cx + i * sp
            ctx.move_to(x0 - ry * 1.1, cy + ry * 1.2)
            ctx.line_to(x0 + ry * 1.1, cy - ry * 1.2)
        ctx.stroke()
        ctx.restore()

    def radial_glow(self, cx: float, cy: float, r_in: float, r_out: float, color="mint", alpha: float = 0.30):
        """Restrained watercolor light-bleed halo (attenuated by 0.62x vs v3.0 to eliminate neon AI-glow!)."""
        eff_a = alpha * 0.62
        if r_out <= 1.0 or eff_a <= 0.005:
            return
        rgb = PAL[color] if isinstance(color, str) else color
        ctx = self.ctx
        grad = cairo.RadialGradient(cx, cy, max(0.0, r_in), cx, cy, r_out)
        grad.add_color_stop_rgba(0.0, min(1.0, rgb[0] + 0.22), min(1.0, rgb[1] + 0.08), min(1.0, rgb[2] + 0.14), eff_a)
        grad.add_color_stop_rgba(0.50, rgb[0], rgb[1], rgb[2], eff_a * 0.38)
        grad.add_color_stop_rgba(1.0, rgb[0], rgb[1], rgb[2], 0.0)
        ctx.set_source(grad)
        ctx.arc(cx, cy, r_out, 0.0, 2.0 * math.pi)
        ctx.fill()

    def pencil_underdraw(self, pts, overshoot: float = 7.5, alpha: float = 0.16, closed: bool = True, key: str = "und"):
        """
        Human Draftsman Rough-Pass Graphite Construction Lines!
        Draws ultra-faint 2B pencil strokes that overshoot straight edges by 5–9px so props look hand-sketched on paper!
        """
        arr = np.asarray(pts, dtype=np.float64)
        if len(arr) < 2 or alpha <= 0.01:
            return
        ctx = self.ctx
        rgb = PAL["ink_soft"]
        ctx.set_source_rgba(rgb[0], rgb[1], rgb[2], alpha)
        ctx.set_line_width(1.25)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        n = len(arr)
        lim = n if closed else n - 1
        for i in range(lim):
            p0 = arr[i]
            p1 = arr[(i + 1) % n]
            d = p1 - p0
            L = float(math.hypot(d[0], d[1]))
            if L < 14.0:
                continue
            u = d / L
            ov0 = overshoot * (0.7 + 0.4 * abs(_seed_float(key, i * 2)))
            ov1 = overshoot * (0.7 + 0.4 * abs(_seed_float(key, i * 2 + 1)))
            q0 = p0 - u * ov0
            q1 = p1 + u * ov1
            ctx.new_path()
            ctx.move_to(q0[0], q0[1])
            ctx.line_to(q1[0], q1[1])
            ctx.stroke()

    def draw_impact_ticks(self, cx: float, cy: float, r_in: float, r_out: float, n_ticks: int = 7, color="ink", alpha: float = 0.85, progress: float = 1.0, key: str = "imp"):
        """Classic comic/indie-anime radial hand-drawn ink impact ticks (`漫画效果线`)."""
        if progress <= 0.02 or alpha <= 0.01:
            return
        for k in range(n_ticks):
            ang = k * (2.0 * math.pi / n_ticks) + _seed_float(key, k) * 0.22
            ri = r_in + _seed_float(key, k + 20) * 4.0
            ro = lerp(ri, r_out, clamp(progress))
            p0 = (cx + math.cos(ang) * ri, cy + math.sin(ang) * ri)
            p1 = (cx + math.cos(ang) * ro, cy + math.sin(ang) * ro)
            self.brush_stroke([p0, p1], width=2.8, color=color, alpha=alpha, roughness=0.35, double_stroke=False, taper_start=0.08, taper_end=0.45, key=f"{key}_{k}")

    def draw_ground_horizon(self, y: float, x0: float = 120.0, x1: float = 1800.0, key: str = "ghor"):
        """
        Organic Broken Draftsman Ground Line (replaces sterile edge-to-edge thin laser grey line!).
        Breaks naturally into 3 hand-sketched segments with subtle end-tapers and tiny ground pebble ticks.
        """
        segs = [
            [(x0, y), (lerp(x0, x1, 0.34), y + 0.8)],
            [(lerp(x0, x1, 0.37), y - 0.6), (lerp(x0, x1, 0.72), y + 0.5)],
            [(lerp(x0, x1, 0.75), y - 0.4), (x1, y)],
        ]
        for si, spts in enumerate(segs):
            self.brush_stroke(
                spts, width=2.6, color="ink_soft", alpha=0.52,
                roughness=0.55, double_stroke=False, taper_start=0.14, taper_end=0.18, key=f"{key}_s{si}",
            )
        # 4 tiny organic floor hatch ticks for handmade paper grounding
        for ti, frac in enumerate((0.14, 0.42, 0.68, 0.88)):
            tx = lerp(x0, x1, frac)
            self.brush_stroke([(tx - 10, y + 7), (tx + 12, y + 6)], width=1.6, color="ink_faint", alpha=0.55, roughness=0.3, double_stroke=False, key=f"{key}_tk{ti}")

    def _stabilized_wobble(self, pts: np.ndarray, s_norm: np.ndarray, roughness: float, key: str, closed: bool = False) -> np.ndarray:
        """World-locked organic hand curvature (82%) + gentle 6fps boil (18%) computed BEFORE Trim-Paths slicing."""
        if roughness <= 0.02 or len(pts) < 2:
            return pts
        amp = min(1.05, roughness * 0.42)
        b = self.boil_step
        ph0 = _seed_float(key, 0) * math.pi
        ph_b = _seed_float(key + "_b", b) * math.pi
        env = 1.0 if closed else np.sin(np.clip(s_norm, 0.0, 1.0) * math.pi) ** 0.62
        wx = amp * (0.82 * np.sin(s_norm * 10.5 + ph0) + 0.20 * np.cos(s_norm * 15.0 + ph_b)) * env
        wy = amp * (0.82 * np.cos(s_norm * 9.0 - ph0) + 0.20 * np.sin(s_norm * 14.0 - ph_b)) * env
        out = pts.copy()
        out[:, 0] += wx
        out[:, 1] += wy
        return out

    def _stroke_path(self, pts: np.ndarray, closed: bool = False):
        ctx = self.ctx
        ctx.new_path()
        ctx.move_to(pts[0, 0], pts[0, 1])
        for px, py in pts[1:]:
            ctx.line_to(px, py)
        if closed:
            ctx.close_path()
        ctx.stroke()

    def brush_stroke(
        self,
        pts,
        width: float = 4.2,
        color="ink",
        alpha: float = 1.0,
        progress: float = 1.0,
        start_trim: float = 0.0,
        taper_start: float = 0.22,
        taper_end: float = 0.22,
        roughness: float = 0.95,
        double_stroke: bool = True,
        closed: bool = False,
        smooth_spline: bool = False,
        key: str = "stk",
    ):
        """
        Variable-Pressure Dip-Pen & Brush Stroke (`PyCairo` analytical `ctx.stroke()`):
        - Zero self-intersecting polygon bowties
        - Authentic hand-inked pressure belly (`0.48x` hairline entry -> `1.12x` weighted belly -> `0.48x` exit)
        - Subtle dry-brush companion nib trace on longer ink strokes for tactile paper feel!
        """
        if progress <= start_trim + 0.004 or alpha <= 0.01:
            return
        arr = np.asarray(pts, dtype=np.float64)
        if len(arr) < 2:
            return
        if smooth_spline and len(arr) >= 3 and not closed:
            arr = catmull_rom_chain(arr, samples_per_seg=7)
        if closed:
            arr = np.vstack([arr, arr[0:1]])

        diffs = np.diff(arr, axis=0)
        seg_l = np.hypot(diffs[:, 0], diffs[:, 1])
        cum = np.concatenate([[0.0], np.cumsum(seg_l)])
        tot_l = float(cum[-1])
        if tot_l < 0.4:
            return

        n_full = max(12, min(180, int(tot_l / 6.0) + 10))
        s_full = np.linspace(0.0, tot_l, n_full)
        xs_f = np.interp(s_full, cum, arr[:, 0])
        ys_f = np.interp(s_full, cum, arr[:, 1])
        full_pts = self._stabilized_wobble(np.stack([xs_f, ys_f], axis=1), s_full / tot_l, roughness, key, closed=closed)

        u0, u1 = clamp(start_trim), clamp(progress)
        if u1 <= u0 + 0.003:
            return
        if u0 <= 0.001 and u1 >= 0.999:
            sub = full_pts
            do_closed = closed
        else:
            s_slice = np.linspace(u0 * tot_l, u1 * tot_l, max(6, int((u1 - u0) * n_full) + 4))
            sub = np.stack([
                np.interp(s_slice, s_full, full_pts[:, 0]),
                np.interp(s_slice, s_full, full_pts[:, 1]),
            ], axis=1)
            do_closed = False

        rgb = PAL[color] if isinstance(color, str) else color
        ctx = self.ctx
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)

        # Layer 1: Subtle warm paper ink-absorption halo
        if width >= 2.8:
            ctx.set_source_rgba(rgb[0], rgb[1], rgb[2], alpha * 0.08)
            ctx.set_line_width(width * 1.44)
            self._stroke_path(sub, closed=do_closed)

        # Layer 2: Multi-tier dip-pen pressure modulation
        n_s = len(sub)
        if not do_closed and n_s >= 10 and (taper_start > 0.04 or taper_end > 0.04):
            ctx.set_source_rgba(rgb[0], rgb[1], rgb[2], alpha * 0.90)
            ctx.set_line_width(width * 0.46)
            self._stroke_path(sub, closed=False)

            i_a1 = int(n_s * clamp(taper_start * 0.55, 0.0, 0.30))
            i_b1 = max(i_a1 + 2, int(n_s * (1.0 - clamp(taper_end * 0.55, 0.0, 0.30))))
            ctx.set_source_rgba(rgb[0], rgb[1], rgb[2], alpha)
            ctx.set_line_width(width * 0.78)
            self._stroke_path(sub[i_a1:i_b1], closed=False)

            i_a2 = int(n_s * clamp(taper_start, 0.0, 0.38))
            i_b2 = max(i_a2 + 2, int(n_s * (1.0 - clamp(taper_end, 0.0, 0.38))))
            if i_b2 - i_a2 >= 2:
                ctx.set_line_width(width * 1.06)
                self._stroke_path(sub[i_a2:i_b2], closed=False)
        else:
            ctx.set_source_rgba(rgb[0], rgb[1], rgb[2], alpha)
            ctx.set_line_width(width)
            self._stroke_path(sub, closed=do_closed)

            # On closed ink contours, add a slightly heavier bottom-right dip-pen shadow arc (`重笔阴影边`)!
            if do_closed and color == "ink" and width >= 3.0 and n_s >= 12:
                ctx.set_source_rgba(rgb[0], rgb[1], rgb[2], alpha * 0.55)
                ctx.set_line_width(width * 1.24)
                self._stroke_path(sub[n_s // 5:(n_s * 3) // 5], closed=False)

        # Layer 3: Organic dry-brush nib companion trace (`0.65px` offset, authentic handmade texture)
        if double_stroke and width >= 2.8 and tot_l > 28.0:
            ox = _seed_float(key + "_ox", 1) * 0.72
            oy = _seed_float(key + "_oy", 2) * 0.72
            sub2 = sub + np.array([[ox, oy]])
            ctx.set_source_rgba(rgb[0], rgb[1], rgb[2], alpha * 0.24)
            ctx.set_line_width(max(1.0, width * 0.34))
            self._stroke_path(sub2, closed=do_closed)

    def marker_wash_poly(self, pts, color="mint_wash", alpha: float = 0.50, offset=(3.5, 4.0), roughness: float = 0.85, key: str = "wsh"):
        """
        Wet-Edge Hand-Swiped Copic Marker Wash:
        1. Slightly offset organic translucent directional wash fill (classic hand-colored print misregistration!)
        2. Soft darker pigment *wet-edge* pooling contour along the outer rim (real alcohol-marker physics!).
        """
        arr = np.asarray(pts, dtype=np.float64).copy()
        if len(arr) < 3 or alpha <= 0.01:
            return
        arr[:, 0] += offset[0]
        arr[:, 1] += offset[1]
        s_n = np.linspace(0.0, 1.0, len(arr))
        arr = self._stabilized_wobble(arr, s_n, roughness, key, closed=True)

        rgb = PAL[color] if isinstance(color, str) else color
        xmin, ymin = arr.min(axis=0)
        xmax, ymax = arr.max(axis=0)
        ctx = self.ctx

        grad = cairo.LinearGradient(xmin, ymin, xmax, ymax)
        r_hi = min(1.0, rgb[0] * 0.62 + 0.38)
        g_hi = min(1.0, rgb[1] * 0.70 + 0.30)
        b_hi = min(1.0, rgb[2] * 0.66 + 0.34)
        r_lo = max(0.0, rgb[0] * 0.84)
        g_lo = max(0.0, rgb[1] * 0.88)
        b_lo = max(0.0, rgb[2] * 0.86)
        grad.add_color_stop_rgba(0.0, r_hi, g_hi, b_hi, alpha * 0.76)
        grad.add_color_stop_rgba(0.58, rgb[0], rgb[1], rgb[2], alpha * 0.96)
        grad.add_color_stop_rgba(1.0, r_lo, g_lo, b_lo, min(1.0, alpha * 1.12))

        ctx.new_path()
        ctx.move_to(arr[0, 0], arr[0, 1])
        for px, py in arr[1:]:
            ctx.line_to(px, py)
        ctx.close_path()
        ctx.set_source(grad)
        ctx.fill_preserve()

        # Subtle watercolor wet-edge pigment ring!
        ctx.set_source_rgba(r_lo, g_lo, b_lo, min(0.45, alpha * 0.42))
        ctx.set_line_width(2.2)
        ctx.stroke()

    def fill_poly(self, pts, color="white", alpha: float = 1.0, roughness: float = 0.45, key: str = "fpl"):
        arr = np.asarray(pts, dtype=np.float64)
        if len(arr) < 3 or alpha <= 0.01:
            return
        s_n = np.linspace(0.0, 1.0, len(arr))
        arr = self._stabilized_wobble(arr, s_n, roughness, key, closed=True)
        rgb = PAL[color] if isinstance(color, str) else color
        ctx = self.ctx
        ctx.new_path()
        ctx.move_to(arr[0, 0], arr[0, 1])
        for px, py in arr[1:]:
            ctx.line_to(px, py)
        ctx.close_path()
        ctx.set_source_rgba(rgb[0], rgb[1], rgb[2], alpha)
        ctx.fill()

    def hachure_fill(self, pts, angle_deg: float = -38.0, spacing: float = 11.5, width: float = 1.55, color="ink_soft", alpha: float = 0.56, progress: float = 1.0, key: str = "hch"):
        if progress <= 0.02 or alpha <= 0.01:
            return
        arr = np.asarray(pts, dtype=np.float64)
        if len(arr) < 3:
            return
        ctx = self.ctx
        ctx.save()
        ctx.new_path()
        ctx.move_to(arr[0, 0], arr[0, 1])
        for px, py in arr[1:]:
            ctx.line_to(px, py)
        ctx.close_path()
        ctx.clip()

        cx, cy = float(arr[:, 0].mean()), float(arr[:, 1].mean())
        xmin, ymin = arr.min(axis=0)
        xmax, ymax = arr.max(axis=0)
        r_bound = max(180.0, math.ceil(math.hypot(xmax - xmin, ymax - ymin) / 120.0) * 120.0)
        rad = math.radians(angle_deg)
        ca, sa = math.cos(rad), math.sin(rad)
        nx, ny = -sa, ca

        eff_sp = max(5.0, spacing)
        n_half = int(r_bound / eff_sp)
        total_lines = 2 * n_half + 1
        n_vis = max(1, int(round(total_lines * clamp(progress))))

        rgb = PAL[color] if isinstance(color, str) else color
        ctx.set_source_rgba(rgb[0], rgb[1], rgb[2], alpha)
        ctx.set_line_width(width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for idx_i, k_off in enumerate(range(-n_half, n_half + 1)):
            if idx_i >= n_vis:
                break
            d = k_off * eff_sp
            if abs(d) > math.hypot(xmax - xmin, ymax - ymin) * 0.55 + eff_sp:
                continue
            p0x, p0y = cx + nx * d - ca * r_bound, cy + ny * d - sa * r_bound
            p1x, p1y = cx + nx * d + ca * r_bound, cy + ny * d + sa * r_bound
            ctx.new_path()
            ctx.move_to(p0x, p0y)
            ctx.line_to(p1x, p1y)
            ctx.stroke()
        ctx.restore()

    def circle_pts(self, cx: float, cy: float, rx: float, ry: float = None, n: int = 44, rot_deg: float = 0.0) -> np.ndarray:
        if ry is None:
            ry = rx
        th = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
        x = np.cos(th) * rx
        y = np.sin(th) * ry
        if abs(rot_deg) > 1e-3:
            r = math.radians(rot_deg)
            ca, sa = math.cos(r), math.sin(r)
            x, y = x * ca - y * sa, x * sa + y * ca
        return np.stack([cx + x, cy + y], axis=1)

    def hand_write_glyphs(self, text: str, cx: float, cy: float, scale: float = 1.0, color="ink", width: float = 4.5, progress: float = 1.0, highlight: bool = False, key: str = "glp"):
        if progress <= 0.01 or not text:
            return
        STROKES = {
            "0": [([(0.50, 0.08), (0.16, 0.28), (0.15, 0.74), (0.50, 0.92), (0.85, 0.72), (0.84, 0.26), (0.50, 0.08)], True)],
            "1": [([(0.30, 0.24), (0.52, 0.08), (0.50, 0.92)], False)],
            "2": [([(0.18, 0.26), (0.50, 0.08), (0.82, 0.24), (0.68, 0.52), (0.16, 0.90)], True), ([(0.16, 0.90), (0.86, 0.89)], False)],
            "3": [([(0.20, 0.18), (0.56, 0.08), (0.80, 0.28), (0.42, 0.48)], True), ([(0.42, 0.48), (0.84, 0.68), (0.52, 0.92), (0.18, 0.84)], True)],
            "4": [([(0.68, 0.08), (0.14, 0.66), (0.88, 0.64)], False), ([(0.66, 0.12), (0.64, 0.92)], False)],
            "5": [([(0.80, 0.10), (0.24, 0.10), (0.20, 0.46)], False), ([(0.20, 0.46), (0.66, 0.44), (0.84, 0.68), (0.52, 0.92), (0.18, 0.84)], True)],
            "6": [([(0.74, 0.10), (0.32, 0.28), (0.16, 0.66), (0.28, 0.88), (0.56, 0.92), (0.84, 0.76), (0.76, 0.54), (0.48, 0.48), (0.18, 0.64)], True)],
            "7": [([(0.16, 0.12), (0.84, 0.10)], False), ([(0.84, 0.10), (0.38, 0.92)], False)],
            "8": [([(0.50, 0.48), (0.20, 0.28), (0.50, 0.08), (0.80, 0.26), (0.50, 0.48), (0.16, 0.72), (0.50, 0.92), (0.84, 0.72), (0.50, 0.48)], True)],
            "9": [([(0.80, 0.34), (0.50, 0.52), (0.18, 0.34), (0.48, 0.08), (0.82, 0.26), (0.74, 0.68), (0.36, 0.92)], True)],
            "%": [
                ([(0.82, 0.10), (0.18, 0.90)], False),
                ([(0.26, 0.12), (0.13, 0.24), (0.26, 0.36), (0.39, 0.24), (0.26, 0.12)], True),
                ([(0.74, 0.64), (0.61, 0.76), (0.74, 0.88), (0.87, 0.76), (0.74, 0.64)], True),
            ],
            "=": [([(0.14, 0.36), (0.86, 0.34)], False), ([(0.16, 0.66), (0.88, 0.64)], False)],
            "+": [([(0.50, 0.18), (0.48, 0.82)], False), ([(0.16, 0.50), (0.84, 0.48)], False)],
            "-": [([(0.18, 0.50), (0.82, 0.48)], False)],
            ".": [([(0.47, 0.84), (0.53, 0.90)], False)],
            "F": [([(0.24, 0.10), (0.22, 0.92)], False), ([(0.22, 0.12), (0.82, 0.10)], False), ([(0.22, 0.50), (0.68, 0.48)], False)],
            "o": [([(0.50, 0.38), (0.20, 0.54), (0.22, 0.84), (0.52, 0.92), (0.80, 0.80), (0.78, 0.50), (0.50, 0.38)], True)],
            "l": [([(0.48, 0.08), (0.47, 0.92)], False)],
            "d": [([(0.78, 0.08), (0.76, 0.92)], False), ([(0.76, 0.48), (0.42, 0.40), (0.18, 0.64), (0.42, 0.90), (0.76, 0.84)], True)],
            "S": [([(0.78, 0.20), (0.48, 0.08), (0.20, 0.24), (0.34, 0.48), (0.78, 0.64), (0.74, 0.86), (0.42, 0.92), (0.18, 0.82)], True)],
            "O": [([(0.50, 0.08), (0.16, 0.28), (0.16, 0.76), (0.50, 0.92), (0.84, 0.74), (0.82, 0.26), (0.50, 0.08)], True)],
            "P": [([(0.22, 0.10), (0.20, 0.92)], False), ([(0.22, 0.12), (0.70, 0.14), (0.82, 0.32), (0.68, 0.50), (0.22, 0.50)], True)],
            "k": [([(0.24, 0.08), (0.22, 0.92)], False), ([(0.74, 0.36), (0.26, 0.64)], False), ([(0.34, 0.58), (0.78, 0.92)], False)],
            "i": [([(0.48, 0.40), (0.48, 0.92)], False), ([(0.48, 0.18), (0.50, 0.24)], False)],
            " ": [],
        }
        cw = 42.0 * scale
        ch_h = 58.0 * scale
        tot_w = len(text) * cw
        x0 = cx - tot_w * 0.5
        y0 = cy - ch_h * 0.5

        if highlight and progress > 0.35:
            hl_p = clamp((progress - 0.35) / 0.55)
            self.brush_stroke(
                [(x0 - 4 * scale, y0 + ch_h * 0.82), (x0 + tot_w + 4 * scale, y0 + ch_h * 0.78)],
                width=14.0 * scale, color="mint_wash", alpha=0.52, progress=hl_p,
                taper_start=0.05, taper_end=0.05, roughness=0.45, double_stroke=False, key=key + "_hlb",
            )

        all_paths = []
        for ci, ch_c in enumerate(text):
            ox = x0 + ci * cw
            for stk, is_crv in STROKES.get(ch_c, []):
                pts = [(ox + px * cw * 0.88, y0 + py * ch_h) for px, py in stk]
                all_paths.append((pts, is_crv))
        if not all_paths:
            return
        n_s = len(all_paths)
        for si, (pts, is_crv) in enumerate(all_paths):
            p_local = clamp(progress * n_s - si)
            if p_local > 0.01:
                self.brush_stroke(
                    pts, width=width, color=color, progress=p_local,
                    roughness=0.40, double_stroke=False, smooth_spline=is_crv,
                    taper_start=0.14, taper_end=0.18, key=f"{key}_{si}",
                )

    def to_bgr(self) -> np.ndarray:
        self.surface.flush()
        buf = np.frombuffer(self.surface.get_data(), dtype=np.uint8).reshape((self.h, self.w, 4))
        return buf[:, :, :3].copy()


# =============================================================================
# EXPRESSIVE PLUSH XERON PUPPET RIG (v4.0 — Squash/Stretch, Head-Tilt & Hand-Hatched Ground Shadow!)
# =============================================================================
def draw_plush_xeron(
    st: HandDrawnStage,
    gx: float,
    gy: float,
    scale: float = 1.0,
    facing: float = 1.0,
    pose: str = "sit",
    phase: float = 0.0,
    squash_x: float = 1.0,
    stretch_y: float = 1.0,
    slope_deg: float = 0.0,
    head_tilt_deg: float = 0.0,
    look_dx: float = 0.0,
    look_dy: float = 0.0,
    blink: float = 0.0,
    happy_eyes: bool = False,
    sweat: bool = False,
    paw_target_world=None,
    key: str = "xcat",
):
    ctx = st.ctx
    ctx.save()
    ctx.translate(gx, gy)
    if abs(slope_deg) > 1e-3:
        ctx.rotate(math.radians(slope_deg))
    ctx.scale(scale * squash_x, scale * stretch_y)

    f = 1.0 if facing >= 0 else -1.0
    t = cel_time(st.t, 24.0)

    if pose not in ("leap", "chin_rest"):
        st.soft_shadow(-f * 4.0, 2.0, 56.0, 12.5, alpha=0.15)

    b_mod = (t + abs(_seed_float(key, 9)) * 2.5) % 4.1
    auto_blink = math.sin(((b_mod - 3.92) / 0.18) * math.pi) if b_mod > 3.92 else 0.0
    eff_blink = clamp(max(blink, auto_blink))

    # 1. Overlapping Plush Brush S-Tail (`跟随与延迟惯性`)
    if pose == "leap":
        tw = math.sin(t * 8.0) * 9.5
        t_pts = sample_bezier((-f * 44, -58), (-f * 108, -78 + tw), (-f * 148, -52 - tw), (-f * 178, -68 + tw), 24)
    elif pose == "crouch":
        tw = math.sin(t * 6.0) * 11.0
        t_pts = sample_bezier((-f * 36, -24), (-f * 102, -16 + tw), (-f * 126, -68 - tw), (-f * 106 + tw, -108), 24)
    else:
        tw = math.sin(t * 1.9 - 0.6) * 8.5
        t_pts = sample_bezier((-f * 32, -20), (-f * 94, -14), (-f * 112, -88 + tw * 0.5), (-f * 76 + tw, -132), 24)
    st.brush_stroke(t_pts, width=16.5, color="cat", roughness=0.45, double_stroke=False, taper_start=0.04, taper_end=0.22, key=key + "_tl")

    # 2. Body Torso & Limbs
    head_cx, head_cy, head_rot = f * 4.0, -170.0, head_tilt_deg

    if pose == "leap":
        torso = st.circle_pts(0.0, -74.0, 56.0, 32.0, n=36, rot_deg=-f * 10.0)
        st.fill_poly(torso, color="cat", roughness=0.35, key=key + "_ltr")
        for li, ox in enumerate((-10.0, 8.0)):
            st.brush_stroke(sample_bezier((-f * 38 + ox, -64), (-f * 68 + ox, -34), (-f * 52 + ox, -14), n=14), width=15.5, color="cat", roughness=0.35, double_stroke=False, taper_start=0.0, taper_end=0.0, key=f"{key}_llg{li}")
        for ai, oy in enumerate((-10.0, 10.0)):
            st.brush_stroke(sample_bezier((f * 40, -76 + oy * 0.4), (f * 72, -56 + oy), (f * 92, -34 + oy), n=14), width=14.5, color="cat", roughness=0.35, double_stroke=False, taper_start=0.0, taper_end=0.0, key=f"{key}_lam{ai}")
        head_cx, head_cy, head_rot = f * 58.0, -118.0, f * 8.0 + head_tilt_deg
    elif pose == "crouch":
        # Low-slung anticipation crouch before takeoff (`压低脊背蓄力`)!
        torso = np.vstack([
            sample_bezier((-58, -4), (-52, -58), (-10, -82), (38, -76), 14),
            sample_bezier((38, -76), (56, -52), (52, -14), (36, -2), 12),
            sample_bezier((36, -2), (8, 1), (-24, 1), (-58, -4), 10),
        ])
        st.fill_poly(torso, color="cat", roughness=0.38, key=key + "_crtr")
        st.fill_poly(st.circle_pts(f * 34.0, -6.0, 14.0, 7.5, n=16), color="cat", key=key + "_crp")
        head_cx, head_cy, head_rot = f * 38.0, -108.0, f * 12.0 + head_tilt_deg
    else:
        breath = math.sin(t * 2.1) * 2.0
        torso = np.vstack([
            sample_bezier((-46, -3), (-54, -48), (-30, -108 + breath), (-14, -142 + breath), 14),
            sample_bezier((-14, -142 + breath), (0, -148 + breath), (16, -142 + breath), (26, -108 + breath), 10),
            sample_bezier((26, -108 + breath), (46, -54), (46, -12), (34, -2), 14),
            sample_bezier((36, -1), (12, 1), (-18, 1), (-46, -2), 10),
        ])
        st.fill_poly(torso, color="cat", roughness=0.40, key=key + "_str")
        back_sheen = sample_bezier((-f * 45, -36), (-f * 36, -84 + breath), (-f * 16, -126 + breath), 14)
        st.brush_stroke(back_sheen, width=3.0, color="cat_sheen", alpha=0.42, roughness=0.22, double_stroke=False, taper_start=0.25, taper_end=0.25, key=key + "_bsh")

        st.fill_poly(st.circle_pts(f * 10.0, -5.0, 13.5, 7.5, n=18), color="cat", roughness=0.2, key=key + "_fpw1")
        st.brush_stroke(sample_bezier((f * 6.0, -68.0), (f * 8.0, -34.0), (f * 9.0, -6.0), 12), width=2.2, color="cat_sheen", alpha=0.55, roughness=0.2, double_stroke=False, key=key + "_cr1")
        if paw_target_world is None:
            st.fill_poly(st.circle_pts(f * 26.0, -5.0, 12.5, 7.0, n=18), color="cat", roughness=0.2, key=key + "_fpw2")
            st.brush_stroke(sample_bezier((f * 22.0, -62.0), (f * 24.0, -32.0), (f * 25.0, -6.0), 12), width=2.2, color="cat_sheen", alpha=0.52, roughness=0.2, double_stroke=False, key=key + "_cr2")
        else:
            lx = (paw_target_world[0] - gx) / (scale * squash_x)
            ly = (paw_target_world[1] - gy) / (scale * stretch_y)
            sh_p = (f * 20.0, -110.0 + breath)
            dx_a, dy_a = lx - sh_p[0], ly - sh_p[1]
            dist_a = math.hypot(dx_a, dy_a)
            if dist_a > 114.0:
                lx = sh_p[0] + dx_a * (114.0 / dist_a)
                ly = sh_p[1] + dy_a * (114.0 / dist_a)
            elb_p = (lerp(sh_p[0], lx, 0.48), lerp(sh_p[1], ly, 0.54) + 15.0)
            st.brush_stroke(sample_bezier(sh_p, elb_p, (lx, ly), n=16), width=16.0, color="cat", roughness=0.35, double_stroke=False, taper_start=0.0, taper_end=0.06, key=key + "_ram")
            st.fill_poly(st.circle_pts(lx, ly, 12.0, 9.8, n=18), color="cat", roughness=0.25, key=key + "_rpw")
        head_cx, head_cy, head_rot = f * 4.0, -170.0 + breath, head_tilt_deg

    # 3. Expressive Plush Head + Ears + Half-Lidded Mint Eyes
    ctx.save()
    ctx.translate(head_cx, head_cy)
    if abs(head_rot) > 1e-3:
        ctx.rotate(math.radians(head_rot))

    for ei, es in enumerate((-1.0, 1.0)):
        ear_tw = math.sin(t * 5.2) * 3.2 if (ei == 1 and int(t * 1.1) % 5 == 0) else 0.0
        p_out = (es * 55.0, -18.0)
        p_tip = (es * (50.0 + ear_tw), -106.0)
        p_in = (es * 9.0, -44.0)
        ear_outer = np.vstack([
            sample_bezier(p_out, (es * 62.0, -64.0), p_tip, n=14),
            sample_bezier(p_tip, (es * 28.0, -78.0), p_in, n=14),
        ])
        st.fill_poly(ear_outer, color="cat", roughness=0.3, key=f"{key}_eo{ei}")
        in_ear = [(es * 45.0, -24.0), (es * (45.5 + ear_tw * 0.8), -89.0), (es * 17.0, -43.0)]
        st.marker_wash_poly(in_ear, color="ear_inner", alpha=0.95, offset=(0, 0), roughness=0.2, key=f"{key}_ei{ei}")
        st.brush_stroke([(es * 36.0, -30.0), (es * 42.0, -72.0)], width=2.0, color="ear_deep", alpha=0.65, roughness=0.2, double_stroke=False, key=f"{key}_efld{ei}")
        st.brush_stroke(ear_outer, width=3.4, color="ink", closed=True, roughness=0.3, double_stroke=False, key=f"{key}_el{ei}")

    th = np.linspace(0.0, 2.0 * math.pi, 48, endpoint=False)
    cheek_bulge = 1.0 + 0.11 * np.maximum(0.0, np.sin(th))
    h_poly = np.stack([np.cos(th) * 66.0 * cheek_bulge, np.sin(th) * 50.5], axis=1)
    st.fill_poly(h_poly, color="cat", roughness=0.35, key=key + "_hd")
    st.brush_stroke(sample_bezier((-36.0, -38.0), (0.0, -48.0), (36.0, -38.0), 14), width=2.6, color="cat_sheen", alpha=0.40, roughness=0.2, double_stroke=False, taper_start=0.3, taper_end=0.3, key=key + "_csh")

    gaze_shift = f * 6.0 + clamp(look_dx, -1.5, 1.5) * 7.0
    for ei, es in enumerate((-1.0, 1.0)):
        ex = gaze_shift + es * 26.0
        ey = 2.0 + clamp(look_dy, -1.0, 1.0) * 4.0
        if happy_eyes:
            arc = sample_bezier((ex - 18, ey + 5), (ex, ey - 12), (ex + 18, ey + 5), n=16)
            st.brush_stroke(arc, width=4.8, color="mint", roughness=0.2, double_stroke=False, key=f"{key}_hey{ei}")
        elif eff_blink > 0.82:
            st.brush_stroke([(ex - 18, ey), (ex + 18, ey)], width=4.2, color="mint", roughness=0.2, double_stroke=False, key=f"{key}_bey{ei}")
        else:
            open_h = 17.8 * (1.0 - 0.85 * eff_blink)
            top_y = ey - open_h * 0.36
            eye_pts = [(ex - 19.8, top_y), (ex + 19.8, top_y)] + [
                (ex + math.cos(a) * 19.8, top_y + math.sin(a) * open_h * 1.25)
                for a in np.linspace(0.0, math.pi, 18)
            ]
            st.marker_wash_poly(eye_pts, color="mint", alpha=0.98, offset=(0, 0), roughness=0.15, key=f"{key}_eyf{ei}")
            px_p = ex + clamp(look_dx, -1.0, 1.0) * 6.5
            st.fill_poly(st.circle_pts(px_p, top_y + open_h * 0.46, 3.8, open_h * 0.46, n=18), color="cat", roughness=0.1, key=f"{key}_pup{ei}")
            if open_h > 9.0:
                st.fill_poly(st.circle_pts(px_p - 3.6, top_y + open_h * 0.26, 2.3, 2.1, n=12), color="white", alpha=0.92, roughness=0.0, key=f"{key}_clt{ei}")
            st.brush_stroke([(ex - 21.5, top_y), (ex + 21.5, top_y)], width=4.4, color="cat", roughness=0.18, double_stroke=False, key=f"{key}_lid{ei}")

    nx_p, ny_p = gaze_shift, 14.0
    st.fill_poly([(nx_p - 5.0, ny_p), (nx_p + 5.0, ny_p), (nx_p, ny_p + 4.6)], color="ear_inner", roughness=0.1, key=key + "_ns")
    for ws in (-1.0, 1.0):
        wx0 = ws * 57.0
        st.brush_stroke([(wx0, 5.5), (wx0 + ws * 25.0, 1.5)], width=2.8, color="ink_soft", roughness=0.22, double_stroke=False, taper_start=0.05, taper_end=0.55, key=f"{key}_w1{ws}")
        st.brush_stroke([(wx0 - ws * 2.0, 14.5), (wx0 + ws * 23.0, 18.5)], width=2.8, color="ink_soft", roughness=0.22, double_stroke=False, taper_start=0.05, taper_end=0.55, key=f"{key}_w2{ws}")

    ctx.restore()
    ctx.restore()


def draw_brush_xeron_sig(st: HandDrawnStage, cx: float, cy: float, scale: float = 1.0, progress: float = 1.0, key: str = "bsig"):
    if progress <= 0.02:
        return

    def tr(pts):
        arr = np.asarray(pts, dtype=np.float64) * scale
        arr[:, 0] += cx
        arr[:, 1] += cy
        return arr

    x1 = [(-52, -16), (-36, -2), (-18, 14)]
    x2 = [(-16, -16), (-35, 0), (-54, 15)]
    eron = [
        (-12, 4), (0, -4), (-6, -11), (-14, -5), (-10, 10), (2, 8),
        (8, -7), (10, 8), (13, -4), (20, -8), (24, -4),
        (32, -6), (26, 4), (30, 10), (39, 8), (41, -4), (33, -7), (42, -4),
        (48, -6), (48, 9), (51, -3), (58, -7), (64, -3), (66, 9), (74, 6), (82, 2),
    ]
    ul = [(-54, 22), (12, 18), (80, 15)]
    if progress > 0.55:
        st.brush_stroke(tr(ul), width=8.5 * scale, color="mint", alpha=0.72, progress=clamp((progress - 0.55) / 0.45), roughness=0.4, double_stroke=False, key=key + "_ul")
    st.brush_stroke(tr(x1), width=4.0 * scale, color="ink", progress=clamp(progress * 2.5), roughness=0.3, double_stroke=False, key=key + "_x1")
    st.brush_stroke(tr(x2), width=3.8 * scale, color="ink", progress=clamp((progress - 0.12) * 2.5), roughness=0.3, double_stroke=False, key=key + "_x2")
    st.brush_stroke(tr(eron), width=3.2 * scale, color="ink", progress=clamp((progress - 0.25) * 1.5), roughness=0.25, smooth_spline=True, double_stroke=False, key=key + "_er")


# =============================================================================
# v5.0 FOUR-LAYER ANTI-AI CRAFT EXTENSIONS:
# 1. Warm Paper Fiber & Multiplied Grain Post-Pass (`apply_paper_grain`) + 12fps Isolated `boil_offset_xy`
# 2. Tacit Viewer Read-Budget Envelope (`viewer_read_envelope`) & Phase Stagger (`stagger_time`)
# 3. Continuous-World Damped Camera (`ContinuousCamera2D`) & Arc-Length Silhouette Morph (`shape_morph_poly`)
# 4. Three-Zoom Visual QA Strip, 1:1 Contact Crop & Non-Visual Bounds Linter (`lint_and_render_3zoom_qa`)
# =============================================================================

_PAPER_GRAIN_CACHE = {}


def apply_paper_grain(bgr: np.ndarray, strength: float = 0.018, seed: int = 2026) -> np.ndarray:
    """
    Applies a subtle, deterministic warm printmaking paper fiber & multiplied grain pass
    to eliminate sterile spreadsheet `#FFFFFF` flat-pixel sheen while keeping >16:1 AAA ink contrast.
    """
    h, w = bgr.shape[:2]
    ckey = (w, h, round(strength, 4), seed)
    if ckey not in _PAPER_GRAIN_CACHE:
        rng = np.random.default_rng(seed)
        fine = rng.normal(0.0, 1.0, size=(h, w)).astype(np.float32)
        coarse_small = rng.normal(0.0, 1.0, size=(max(8, h // 6), max(8, w // 6))).astype(np.float32)
        import cv2 as _cv2
        coarse = _cv2.resize(coarse_small, (w, h), interpolation=_cv2.INTER_CUBIC)
        tex = 1.0 - strength * (0.65 * fine + 0.35 * coarse)
        # Ultra-subtle warm cotton-paper tint `(B=0.992, G=0.997, R=1.000)` clipped cleanly
        mul = np.stack([
            np.clip(tex * 0.993, 0.92, 1.01),
            np.clip(tex * 0.997, 0.93, 1.01),
            np.clip(tex * 1.000, 0.94, 1.01),
        ], axis=2).astype(np.float32)
        _PAPER_GRAIN_CACHE[ckey] = mul
    mul = _PAPER_GRAIN_CACHE[ckey]
    return np.clip(bgr.astype(np.float32) * mul, 0, 255).astype(np.uint8)


def boil_offset_xy(key: str, t: float, s_norm: np.ndarray, amp: float = 0.52, boil_fps: float = 12.0) -> tuple[np.ndarray, np.ndarray]:
    """
    Isolated per-element `12fps` (`onTwos`) line-boil displacement (`ClaudeAnimationBase` rule):
    Each `key` hashes into its own deterministic RNG phase so moving actors NEVER perturb static props.
    """
    boil_frame = int(math.floor(t * boil_fps))
    ph0 = _seed_float(f"{key}:base", 0) * math.pi
    ph_b = _seed_float(f"{key}:twos", boil_frame) * math.pi
    wx = amp * (0.80 * np.sin(s_norm * 10.0 + ph0) + 0.22 * np.cos(s_norm * 15.5 + ph_b))
    wy = amp * (0.80 * np.cos(s_norm * 9.2 - ph0) + 0.22 * np.sin(s_norm * 14.2 - ph_b))
    return wx, wy


def stagger_time(t: float, lag_frames: float = 4.0, fps: float = 60.0) -> float:
    """Offsets secondary limb/head/tail time by `lag_frames` to break mechanical limb twinning."""
    return max(0.0, t - (lag_frames / max(1.0, fps)))


def viewer_read_envelope(
    t: float,
    t_beat0: float,
    lead_s: float = 0.34,
    antic_s: float = 0.18,
    snap_s: float = 0.24,
    hold_s: float = 0.92,
    dip: float = 0.15,
    overshoot: float = 0.07,
) -> dict:
    """
    Polanyi Tacit Viewer Read-Budget Contract (`单拍单读点四段式包络`):
    Sequences `Lead Eye -> Reverse Anticipation -> Fast Action Snap -> Held Payoff`
    and returns `{"pos": float, "eye_ready": float, "in_hold": bool, "done": bool}`.
    - Before `t_beat0 + lead_s`: `pos = 0.0`, `eye_ready` ramps `0 -> 1` so gaze/camera lands first.
    - During `antic_s`: `pos` dips backward to `-dip` (wind-up).
    - During `snap_s`: `pos` launches rapidly across `0 -> 1 + overshoot -> 1.0`.
    - During `hold_s`: `pos = 1.0` with critically damped micro-settle so meaning registers cleanly.
    """
    dt = t - t_beat0
    if dt <= 0.0:
        return {"pos": 0.0, "eye_ready": 0.0, "in_hold": False, "done": False}
    if dt < lead_s:
        return {"pos": 0.0, "eye_ready": ease_out_cubic(dt / max(1e-4, lead_s)), "in_hold": False, "done": False}
    dt_act = dt - lead_s
    if dt_act < antic_s:
        u = dt_act / max(1e-4, antic_s)
        return {"pos": -dip * math.sin(u * math.pi), "eye_ready": 1.0, "in_hold": False, "done": False}
    dt_snap = dt_act - antic_s
    if dt_snap < snap_s:
        u = dt_snap / max(1e-4, snap_s)
        pos = (1.0 + overshoot) * (1.0 - (1.0 - u) ** 3.2)
        return {"pos": pos, "eye_ready": 1.0, "in_hold": False, "done": False}
    dt_hold = dt_snap - snap_s
    settle = overshoot * math.exp(-7.5 * dt_hold) * math.cos(14.0 * dt_hold)
    return {
        "pos": 1.0 + settle,
        "eye_ready": 1.0,
        "in_hold": dt_hold < hold_s,
        "done": dt_hold >= hold_s,
    }


def resample_closed_contour(pts, n: int = 96) -> np.ndarray:
    """
    Resamples any closed 2D silhouette to `n` uniform arc-length vertices, rotating vertex 0
    to the topmost-leftmost anchor so two different shapes morph cleanly without twisting!
    """
    arr = np.asarray(pts, dtype=np.float64)
    if len(arr) < 3:
        raise ValueError("Closed contour requires >= 3 points")
    if np.hypot(*(arr[0] - arr[-1])) > 1e-4:
        arr = np.vstack([arr, arr[0:1]])
    diffs = np.diff(arr, axis=0)
    seg_l = np.hypot(diffs[:, 0], diffs[:, 1])
    cum = np.concatenate([[0.0], np.cumsum(seg_l)])
    tot = float(cum[-1])
    s = np.linspace(0.0, tot, n, endpoint=False)
    xs = np.interp(s, cum, arr[:, 0])
    ys = np.interp(s, cum, arr[:, 1])
    uni = np.stack([xs, ys], axis=1)

    # Align starting vertex to minimum angle around centroid (top-most `-pi/2` anchor)
    cx, cy = float(uni[:, 0].mean()), float(uni[:, 1].mean())
    angs = np.arctan2(uni[:, 1] - cy, uni[:, 0] - cx)
    idx0 = int(np.argmin(np.abs(angs + math.pi * 0.5)))
    uni = np.roll(uni, -idx0, axis=0)
    # Enforce consistent clockwise winding in screen coordinates
    signed_area = 0.5 * float(np.sum(uni[:, 0] * np.roll(uni[:, 1], -1) - np.roll(uni[:, 0], -1) * uni[:, 1]))
    if signed_area < 0.0:
        uni = np.vstack([uni[0:1], uni[1:][::-1]])
    return uni


def shape_morph_poly(pts_a, pts_b, u: float, n: int = 96) -> np.ndarray:
    """
    Smoothly morphs silhouette `pts_a` into `pts_b` (`u in 0..1`) via arc-length & winding-aligned
    interpolation (`cth9191/animate` object shape-morph transition, replacing slide cross-dissolves).
    """
    k = smootherstep(clamp(u))
    ca = resample_closed_contour(pts_a, n=n)
    cb = resample_closed_contour(pts_b, n=n)
    return ca * (1.0 - k) + cb * k


class ContinuousCamera2D:
    """
    Anti-Slide-Deck Persistent World Camera (`Bang Motion` continuous-world choreography):
    Evaluates pure-function `f(t)` camera keyframes `(t, cx, cy, zoom, rot_deg)` with smooth C2
    damped transitions plus subtle organic handheld breathing drift (`0.35 Hz`) so space feels alive.
    """

    def __init__(self, keyframes: list, breath_px: float = 3.2, breath_rot_deg: float = 0.14):
        self.keyframes = sorted(keyframes, key=lambda x: x[0])
        self.breath_px = breath_px
        self.breath_rot_deg = breath_rot_deg

    def sample(self, t: float) -> tuple[float, float, float, float]:
        if not self.keyframes:
            return (960.0, 520.0, 1.0, 0.0)
        if t <= self.keyframes[0][0]:
            _, cx, cy, zm, rt = self.keyframes[0]
        elif t >= self.keyframes[-1][0]:
            _, cx, cy, zm, rt = self.keyframes[-1]
        else:
            cx, cy, zm, rt = self.keyframes[-1][1:]
            for i in range(len(self.keyframes) - 1):
                t0, x0, y0, z0, r0 = self.keyframes[i]
                t1, x1, y1, z1, r1 = self.keyframes[i + 1]
                if t0 <= t <= t1:
                    k = smootherstep((t - t0) / max(1e-4, t1 - t0))
                    cx = lerp(x0, x1, k)
                    cy = lerp(y0, y1, k)
                    zm = math.exp(lerp(math.log(max(0.1, z0)), math.log(max(0.1, z1)), k))
                    rt = lerp(r0, r1, k)
                    break
        bx = math.sin(t * 2.15) * self.breath_px
        by = math.cos(t * 1.65) * (self.breath_px * 0.72)
        br = math.sin(t * 1.35) * self.breath_rot_deg
        return (cx + bx, cy + by, zm, rt + br)

    def apply_to_stage(self, st: HandDrawnStage, t: float):
        cx, cy, zm, rt = self.sample(t)
        st.push_camera(zoom=zm, dx=(960.0 - cx) * zm, dy=(520.0 - cy) * zm, rot_deg=rt, piv=(960.0, 520.0))


def lint_and_render_3zoom_qa(
    render_frame_fn,
    out_dir,
    look_times: list[float],
    motion_strip_t0: float,
    crop_specs: list[tuple[float, int, int, int, str]],
    strip_dt: float = 0.10,
    strip_count: int = 8,
    subtitle_safe_y: int = 928,
) -> dict:
    """
    Executes Layer-4 Pre-Render QA (`xiaoma-studio` + `cth9191/animate` 3-Zoom Visual Gate):
    1. Non-visual bounds & subtitle-zone collision check + `+16.7ms` 60fps anti-scramble check.
    2. Exports full-size `1920x1080` Look Frames (`qa_look_01.png`, ...).
    3. Exports a `0.1s` sequential Motion Strip (`qa_motion_strip.png`) to verify anticipation, morph & settle.
    4. Exports `1:1` native pixel crops (`qa_crops_1to1.png`) on paws/eyes/contacts for `view_file` inspection.
    """
    from pathlib import Path
    import cv2 as _cv2

    out_p = Path(out_dir)
    out_p.mkdir(parents=True, exist_ok=True)
    report = {"look_paths": [], "motion_strip_path": "", "crops_path": "", "warnings": [], "max_step_diff_pct": 0.0}

    # Gate 1: Full-Size Look Frames + Subtitle Safe-Zone Ink Lint
    for idx, lt in enumerate(look_times):
        frm = render_frame_fn(float(lt))
        p_f = out_p / f"qa_look_{idx + 1:02d}_{lt:.2f}s.png"
        _cv2.imwrite(str(p_f), frm)
        report["look_paths"].append(str(p_f))
        gray = _cv2.cvtColor(frm, _cv2.COLOR_BGR2GRAY)
        # Check if heavy stage ink intrudes into bottom subtitle band [subtitle_safe_y:1045, 240:1680] when no subtitle is drawn
        sub_band_ink = float(np.mean(gray[subtitle_safe_y:1035, 260:1660] < 200)) * 100.0
        if sub_band_ink > 18.0:
            report["warnings"].append(f"t={lt:.2f}s bottom subtitle zone ink density {sub_band_ink:.1f}% > 18% (check prop/floor overlap)")
        border_ink = float(np.mean(np.concatenate([gray[:8, :].ravel(), gray[-8:, :].ravel(), gray[:, :8].ravel(), gray[:, -8:].ravel()]) < 180)) * 100.0
        if border_ink > 6.0:
            report["warnings"].append(f"t={lt:.2f}s screen-edge clipping detected ({border_ink:.1f}% dark border pixels)")

    # Gate 2: `0.1s` Sequential Motion Strip + `+16.7ms` 60fps Anti-Scramble Check
    strip_thumbs = []
    max_step = 0.0
    for si in range(strip_count):
        ts = motion_strip_t0 + si * strip_dt
        f0 = render_frame_fn(ts)
        f1 = render_frame_fn(ts + (1.0 / 60.0))
        step_pct = float(np.mean(np.abs(f0.astype(np.int16) - f1.astype(np.int16)) > 28)) * 100.0
        max_step = max(max_step, step_pct)
        th = _cv2.resize(f0, (480, 270), interpolation=_cv2.INTER_AREA)
        _cv2.rectangle(th, (0, 0), (479, 269), (210, 215, 222), 1)
        _cv2.putText(th, f"t={ts:.2f}s | d1f={step_pct:.2f}%", (12, 26), _cv2.FONT_HERSHEY_SIMPLEX, 0.58, (20, 95, 65), 2, _cv2.LINE_AA)
        strip_thumbs.append(th)
    report["max_step_diff_pct"] = round(max_step, 3)
    if max_step >= 5.0:
        report["warnings"].append(f"60fps anti-scramble warning: max +16.7ms frame step {max_step:.2f}% >= 5.0%")

    cols = 4
    rows = int(math.ceil(len(strip_thumbs) / cols))
    while len(strip_thumbs) < rows * cols:
        strip_thumbs.append(np.full((270, 480, 3), 255, dtype=np.uint8))
    grid_rows = [np.hstack(strip_thumbs[r * cols:(r + 1) * cols]) for r in range(rows)]
    strip_img = np.vstack(grid_rows)
    strip_path = out_p / "qa_motion_strip.png"
    _cv2.imwrite(str(strip_path), strip_img)
    report["motion_strip_path"] = str(strip_path)

    # Gate 3: `1:1` Native Pixel Contact Crops (`crop_specs`: list of `(t, cx, cy, half_size, label)`)
    crop_tiles = []
    for ct, cx, cy, hs, lbl in crop_specs:
        frm = render_frame_fn(float(ct))
        h_f, w_f = frm.shape[:2]
        x0 = max(0, min(w_f - hs * 2, int(cx - hs)))
        y0 = max(0, min(h_f - hs * 2, int(cy - hs)))
        crop = frm[y0:y0 + hs * 2, x0:x0 + hs * 2].copy()
        crop_vis = _cv2.resize(crop, (420, 420), interpolation=_cv2.INTER_NEAREST)
        _cv2.rectangle(crop_vis, (0, 0), (419, 419), (180, 188, 198), 2)
        _cv2.putText(crop_vis, f"1:1 {lbl} ({ct:.2f}s)", (12, 28), _cv2.FONT_HERSHEY_SIMPLEX, 0.62, (20, 24, 30), 2, _cv2.LINE_AA)
        crop_tiles.append(crop_vis)
    if crop_tiles:
        crops_img = np.hstack(crop_tiles)
        crops_path = out_p / "qa_crops_1to1.png"
        _cv2.imwrite(str(crops_path), crops_img)
        report["crops_path"] = str(crops_path)

    return report
