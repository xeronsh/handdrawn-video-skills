#!/usr/bin/env python3
"""
`v14_chibi_watercolor_kit.py` — Shared Studio Watercolor, 2.5-Head Chibi Xeron Rig, Glass Kettle, Draftsman Callouts & Easter Eggs
for Xeron hand-drawn watercolor motion videos.
"""
import hashlib
import math
import os
import sys
from pathlib import Path
import cairo
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SKILL_SCRIPTS = str(Path(__file__).resolve().parent)
if SKILL_SCRIPTS not in sys.path:
    sys.path.insert(0, SKILL_SCRIPTS)
import cairo_handdrawn as ch
import xeron_clean_rig as xr

W, H = 1920, 1080
FPS = 60


def _resolve_font(env_var: str, candidates: list[str], fallback: str | None = None) -> str:
    env_path = os.environ.get(env_var, "").strip()
    if env_path and os.path.exists(env_path):
        return env_path
    for cand in candidates:
        if os.path.exists(cand):
            return cand
    return fallback if fallback is not None else candidates[0]


FONT_REG = _resolve_font(
    "HANDDRAWN_FONT_REGULAR",
    [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ],
)
FONT_BOLD = _resolve_font(
    "HANDDRAWN_FONT_BOLD",
    [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJKsc-Bold.otf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "C:/Windows/Fonts/msyhbd.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ],
    fallback=FONT_REG,
)
FONT_SERIF_BOLD = _resolve_font(
    "HANDDRAWN_FONT_SERIF",
    [
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
        "/usr/share/fonts/noto-cjk/NotoSerifCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJKsc-Bold.otf",
        "/System/Library/Fonts/Songti.ttc",
        "C:/Windows/Fonts/simsun.ttc",
    ],
    fallback=FONT_BOLD,
)

_BASE_PAPER_ARGB = None
_TEXT_SURF_CACHE = {}


def get_cold_press_paper_argb() -> np.ndarray:
    global _BASE_PAPER_ARGB
    if _BASE_PAPER_ARGB is not None:
        return _BASE_PAPER_ARGB
    rng = np.random.default_rng(1109)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = (xx - W * 0.5) / (W * 0.5)
    ny = (yy - H * 0.46) / (H * 0.54)
    vig = np.clip((nx * nx + ny * ny) * 0.015, 0.0, 0.024)

    fine = rng.normal(0.0, 1.0, (H, W)).astype(np.float32)
    med = cv2.resize(rng.normal(0.0, 1.0, (H // 4, W // 4)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    laid = cv2.resize(rng.normal(0.0, 1.0, (H // 2, W // 18)).astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)
    grain = 0.0080 * fine + 0.0070 * med + 0.0040 * laid

    r = np.clip((0.987 - vig * 0.60 - grain) * 255.0, 234, 255).astype(np.uint8)
    g = np.clip((0.981 - vig * 0.75 - grain) * 255.0, 230, 254).astype(np.uint8)
    b = np.clip((0.966 - vig * 1.00 - grain * 1.08) * 255.0, 222, 252).astype(np.uint8)
    a = np.full((H, W), 255, dtype=np.uint8)
    _BASE_PAPER_ARGB = np.stack([b, g, r, a], axis=2)
    return _BASE_PAPER_ARGB


def make_paper_stage(t: float) -> ch.HandDrawnStage:
    st = ch.HandDrawnStage(t, W, H)
    buf = np.ndarray(shape=(H, W, 4), dtype=np.uint8, buffer=st.surface.get_data())
    np.copyto(buf, get_cold_press_paper_argb())
    st.surface.mark_dirty()
    return st


def _densify_long_edges(pts: np.ndarray, max_seg: float = 42.0) -> np.ndarray:
    arr = np.asarray(pts, dtype=np.float64)
    out = []
    n = len(arr)
    for i in range(n):
        p0, p1 = arr[i], arr[(i + 1) % n]
        dist = float(math.hypot(p1[0] - p0[0], p1[1] - p0[1]))
        steps = max(1, int(math.ceil(dist / max_seg)))
        for k in range(steps):
            u = k / float(steps)
            out.append(p0 * (1.0 - u) + p1 * u)
    return np.asarray(out, dtype=np.float64)


def _subdivide_wet_poly(pts: np.ndarray, bleed: float, rng: np.random.Generator, rounds: int = 2, max_px: float = 9.0) -> np.ndarray:
    cur = _densify_long_edges(pts, max_seg=42.0)
    for r_i in range(rounds):
        nxt = []
        n = len(cur)
        falloff = 0.56 ** r_i
        for i in range(n):
            p0, p1 = cur[i], cur[(i + 1) % n]
            mid = 0.5 * (p0 + p1)
            d = p1 - p0
            seg_len = float(math.hypot(d[0], d[1]))
            if seg_len > 1.2:
                nx, ny = -d[1] / seg_len, d[0] / seg_len
                sigma = min(max_px * falloff, bleed * seg_len * falloff)
                disp = float(np.clip(rng.normal(0.0, sigma), -max_px, max_px))
                mid = mid + np.array([nx * disp, ny * disp])
            nxt.append(p0)
            nxt.append(mid)
        cur = np.asarray(nxt, dtype=np.float64)
    return cur


def wet_watercolor_wash(
    st: ch.HandDrawnStage,
    pts,
    rgb: tuple[float, float, float],
    alpha: float = 0.42,
    bleed: float = 0.13,
    layers: int = 3,
    max_px: float = 9.0,
    boil_fps: float = 0.0,
    key: str = "wc",
):
    arr = np.asarray(pts, dtype=np.float64)
    if len(arr) < 3 or alpha <= 0.008:
        return
    ctx = st.ctx
    b_idx = int(math.floor(st.t * boil_fps)) if boil_fps > 0 else 0
    h_seed = int.from_bytes(hashlib.blake2b(f"{key}:{b_idx}".encode(), digest_size=4).digest(), "little")
    rng = np.random.default_rng(h_seed)

    layer_a = (alpha / max(1, layers)) * 1.26
    for li in range(layers):
        sub_pts = _subdivide_wet_poly(arr, bleed=bleed * (0.78 + 0.12 * li), rng=rng, rounds=2, max_px=max_px)
        ctx.new_path()
        ctx.move_to(sub_pts[0, 0], sub_pts[0, 1])
        for px, py in sub_pts[1:]:
            ctx.line_to(px, py)
        ctx.close_path()
        ctx.set_source_rgba(rgb[0], rgb[1], rgb[2], min(0.62, layer_a))
        ctx.fill()

    rim_pts = _subdivide_wet_poly(arr, bleed=bleed * 0.45, rng=rng, rounds=1, max_px=max_px * 0.6)
    ctx.new_path()
    ctx.move_to(rim_pts[0, 0], rim_pts[0, 1])
    for px, py in rim_pts[1:]:
        ctx.line_to(px, py)
    ctx.close_path()
    ctx.set_source_rgba(rgb[0] * 0.78, rgb[1] * 0.84, rgb[2] * 0.80, min(0.36, alpha * 0.32))
    ctx.set_line_width(1.6)
    ctx.stroke()


def draw_wood_tabletop(st: ch.HandDrawnStage, y: float, x0: float = 90.0, x1: float = 1830.0, tint_rgb=(0.83, 0.76, 0.66), key: str = "tbl"):
    plank = [(x0, y), (x1, y), (x1, y + 22.0), (x0, y + 22.0)]
    wet_watercolor_wash(st, plank, tint_rgb, alpha=0.38, bleed=0.08, max_px=5.5, layers=3, key=key + "_w")
    st.brush_stroke([(x0, y), (x1, y)], width=3.8, color="ink", roughness=0.40, double_stroke=True, key=key + "_top")
    st.brush_stroke([(x0 + 25, y + 22.0), (x1 - 25, y + 22.0)], width=2.0, color="ink_soft", alpha=0.55, roughness=0.35, double_stroke=False, key=key + "_bot")


def draw_ink_text(
    st: ch.HandDrawnStage,
    text: str,
    x: float,
    y: float,
    font_px: int = 30,
    rgb_u8: tuple[int, int, int] = (24, 27, 32),
    align: str = "center",
    alpha: float = 1.0,
    rot_deg: float = 0.0,
    bold: bool = True,
    serif: bool = False,
    swatch_rgb: tuple[float, float, float] = None,
    key: str = "txt",
) -> tuple[int, int]:
    if alpha <= 0.01 or not text:
        return (0, 0)
    fpath = FONT_SERIF_BOLD if serif else (FONT_BOLD if bold else FONT_REG)
    ckey = (text, font_px, rgb_u8, fpath)
    if ckey not in _TEXT_SURF_CACHE:
        if len(_TEXT_SURF_CACHE) > 1500:
            _TEXT_SURF_CACHE.clear()
        font = ImageFont.truetype(fpath, font_px)
        dummy = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        bb = dummy.textbbox((0, 0), text, font=font)
        tw, th = max(8, bb[2] - bb[0]), max(8, bb[3] - bb[1])
        pad = 12
        im = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.text((pad - bb[0], pad - bb[1]), text, font=font, fill=(*rgb_u8, 255))
        arr = np.array(im, dtype=np.uint8)
        a_f = arr[:, :, 3:4].astype(np.float32) / 255.0
        bgra = np.zeros_like(arr)
        bgra[:, :, 0] = (arr[:, :, 2:3] * a_f)[:, :, 0].astype(np.uint8)
        bgra[:, :, 1] = (arr[:, :, 1:2] * a_f)[:, :, 0].astype(np.uint8)
        bgra[:, :, 2] = (arr[:, :, 0:1] * a_f)[:, :, 0].astype(np.uint8)
        bgra[:, :, 3] = arr[:, :, 3]
        _TEXT_SURF_CACHE[ckey] = (bgra, tw, th)

    bgra_src, tw, th = _TEXT_SURF_CACHE[ckey]
    bgra = bgra_src.copy()
    ph, pw = bgra.shape[:2]

    cx = x if align == "center" else (x + tw * 0.5 if align == "left" else x - tw * 0.5)
    if swatch_rgb is not None:
        hw, hh = tw * 0.52 + 12.0, th * 0.34 + 4.0
        sw_poly = [(cx - hw, y + hh * 0.05), (cx + hw, y - hh * 0.08), (cx + hw - 4, y + hh * 1.05), (cx - hw + 3, y + hh * 1.12)]
        wet_watercolor_wash(st, sw_poly, swatch_rgb, alpha=0.42 * alpha, bleed=0.10, max_px=5.5, layers=2, key=key + "_sw")

    surf = cairo.ImageSurface.create_for_data(bgra, cairo.FORMAT_ARGB32, pw, ph, pw * 4)
    bx, by = ch.boil_offset_xy(key, st.t, np.array([0.5]), amp=0.38, boil_fps=12.0)
    ctx = st.ctx
    ctx.save()
    ctx.translate(cx + float(bx[0]), y + float(by[0]))
    if abs(rot_deg) > 1e-3:
        ctx.rotate(math.radians(rot_deg))
    ctx.set_source_surface(surf, -pw * 0.5, -ph * 0.5)
    ctx.paint_with_alpha(ch.clamp(alpha))
    ctx.restore()
    return (tw, th)


def draw_curved_arrow(
    st: ch.HandDrawnStage,
    p_start: tuple[float, float],
    p_end: tuple[float, float],
    bend_px: float = -24.0,
    color: str = "ink",
    width: float = 3.0,
    progress: float = 1.0,
    alpha: float = 1.0,
    key: str = "arr",
):
    if progress <= 0.02 or alpha <= 0.02:
        return
    p = ch.clamp(progress)
    mx = 0.5 * (p_start[0] + p_end[0])
    my = 0.5 * (p_start[1] + p_end[1]) + bend_px
    crv = ch.sample_bezier(p_start, (mx, my), p_end, n=22)
    st.brush_stroke(crv, width=width, color=color, alpha=alpha, progress=p, roughness=0.30, double_stroke=False, taper_start=0.15, taper_end=0.10, key=key)
    if p > 0.72:
        hp = ch.clamp((p - 0.72) / 0.28)
        tx, ty = crv[-1]
        ang = math.atan2(ty - crv[-3][1], tx - crv[-3][0])
        alen = 15.0 * ch.snap_settle(hp, overshoot=0.10)
        w1 = (tx - alen * math.cos(ang - 0.50), ty - alen * math.sin(ang - 0.50))
        w2 = (tx - alen * math.cos(ang + 0.50), ty - alen * math.sin(ang + 0.50))
        st.brush_stroke([w1, (tx, ty), w2], width=width * 0.92, color=color, alpha=alpha, roughness=0.20, double_stroke=False, key=key + "_hd")


def draw_draftsman_callout(
    st: ch.HandDrawnStage,
    note_cx: float,
    note_cy: float,
    target_pt: tuple[float, float],
    title: str,
    sub: str = "",
    accent: str = "ink",
    bend_px: float = -20.0,
    progress: float = 1.0,
    key: str = "call",
):
    if progress <= 0.02:
        return
    p_txt = ch.ease_out_cubic(ch.clamp(progress * 1.35))
    p_arr = ch.clamp((progress - 0.12) / 0.88)

    if accent == "mint":
        t_rgb, sw, arr_col = (10, 118, 78), (0.20, 0.91, 0.63), "mint_deep"
    elif accent == "red":
        t_rgb, sw, arr_col = (176, 44, 38), (0.96, 0.72, 0.68), "red"
    else:
        t_rgb, sw, arr_col = (24, 27, 33), (0.86, 0.82, 0.74), "ink_soft"

    tw, th = draw_ink_text(st, title, note_cx, note_cy, font_px=30, rgb_u8=t_rgb, alpha=p_txt, bold=True, swatch_rgb=sw, key=key + "_t")
    bot_y = note_cy + th * 0.5 + 8.0
    if sub:
        _, sh = draw_ink_text(st, sub, note_cx, note_cy + 39.0, font_px=22, rgb_u8=(68, 74, 84), alpha=p_txt, bold=True, key=key + "_s")
        bot_y = note_cy + 39.0 + sh * 0.5 + 10.0

    top_y = note_cy - th * 0.5 - 10.0
    if target_pt is not None:
        if target_pt[1] > bot_y + 12.0:
            p0 = (note_cx + ch.clamp((target_pt[0] - note_cx) * 0.25, -85.0, 85.0), bot_y + 4.0)
        elif target_pt[1] < top_y - 12.0:
            p0 = (note_cx + ch.clamp((target_pt[0] - note_cx) * 0.25, -85.0, 85.0), top_y - 4.0)
        elif target_pt[0] < note_cx:
            p0 = (note_cx - tw * 0.5 - 16.0, note_cy + (16.0 if sub else 0.0))
        else:
            p0 = (note_cx + tw * 0.5 + 16.0, note_cy + (16.0 if sub else 0.0))
        draw_curved_arrow(st, p0, target_pt, bend_px=bend_px, color=arr_col, width=3.0, progress=p_arr, alpha=p_txt, key=key + "_ar")


def draw_sketch_panel(st: ch.HandDrawnStage, x0: float, y0: float, w: float, h: float, tint_rgb=(0.94, 0.96, 0.93), border_col="ink", alpha: float = 0.72, key: str = "pnl"):
    pts = [(x0, y0), (x0 + w, y0 - 3), (x0 + w - 3, y0 + h), (x0 + 3, y0 + h + 2)]
    st.pencil_underdraw(pts, overshoot=8.5, alpha=0.16 * alpha, key=key + "_u")
    wet_watercolor_wash(st, pts, tint_rgb, alpha=alpha, bleed=0.05, max_px=4.0, layers=2, key=key + "_w")
    st.brush_stroke(pts, width=3.2, color=border_col, alpha=min(1.0, alpha * 1.3), closed=True, double_stroke=False, key=key + "_b")


def draw_sticky_badge(st: ch.HandDrawnStage, cx: float, cy: float, text: str, rot_deg: float = -2.2, mint_toast: bool = False, progress: float = 1.0, key: str = "stk"):
    if progress <= 0.02:
        return
    p = ch.snap_settle(progress, overshoot=0.08)
    w_box = max(220.0, len(text) * 22.5 + 42.0) * p
    h_box = 46.0 * p
    hw, hh = w_box * 0.5, h_box * 0.5
    rad = math.radians(rot_deg)
    ca, sa = math.cos(rad), math.sin(rad)
    pts = [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))]
    st.pencil_underdraw(pts, overshoot=5.0, alpha=0.14, key=key + "_u")
    wet_watercolor_wash(st, pts, (0.20, 0.92, 0.64) if mint_toast else (0.94, 0.90, 0.76), alpha=0.38 if mint_toast else 0.56, bleed=0.07, max_px=4.0, layers=2, key=key + "_w")
    st.brush_stroke(pts, width=2.4, color="mint_deep" if mint_toast else "ink_soft", closed=True, double_stroke=False, key=key + "_b")
    if not mint_toast:
        px_p, py_p = cx + hh * sa, cy - hh * ca
        st.fill_poly(st.circle_pts(px_p, py_p, 5.2, 5.2, n=12), color="mint", key=key + "_pn")
        st.brush_stroke(st.circle_pts(px_p, py_p, 5.2, 5.2, n=12), width=1.8, color="ink", closed=True, double_stroke=False, key=key + "_pnl")
    draw_ink_text(st, text, cx, cy, font_px=21, rgb_u8=(10, 112, 74) if mint_toast else (48, 52, 60), rot_deg=rot_deg, bold=True, key=key + "_tx")


def draw_peek_mini_cat_egg(st: ch.HandDrawnStage, cx: float, cy: float, note: str, key: str = "pkcat"):
    bob = math.sin(st.t * 2.6) * 3.2
    y = cy + bob
    st.brush_stroke([(cx - 42, cy + 16), (cx + 42, cy + 16)], width=2.2, color="ink_faint", double_stroke=False, key=key + "_lg")
    for es in (-1.0, 1.0):
        st.fill_poly([(cx + es * 22, y - 6), (cx + es * 26, y - 30), (cx + es * 7, y - 17)], color="cat", key=f"{key}_e{es}")
    st.fill_poly(st.circle_pts(cx, y, 25.0, 18.0, n=24), color="cat", key=key + "_hd")
    for es in (-1.0, 1.0):
        ex = cx + es * 9.5
        st.fill_poly([(ex - 6, y - 4), (ex + 6, y - 4), (ex + 5, y + 3), (ex - 5, y + 3)], color="mint", key=f"{key}_ey{es}")
        st.fill_poly(st.circle_pts(cx + es * 13, cy + 15, 6.5, 4.5, n=12), color="cat", key=f"{key}_pw{es}")
    draw_ink_text(st, note, cx + 52, cy + 2, font_px=20, rgb_u8=(88, 94, 104), align="left", rot_deg=-1.5, bold=True, key=key + "_nt")


def draw_debug_duck_egg(st: ch.HandDrawnStage, cx: float, gy: float, scale: float = 1.0, mode: str = "stopwatch", caption: str = "", sign_txt: str = "0动静", key: str = "duck"):
    ctx = st.ctx
    ctx.save()
    ctx.translate(cx, gy)
    ctx.scale(scale, scale)
    bob = math.sin(st.t * 4.0) * 2.2
    st.soft_shadow(0.0, 2.0, 30.0, 6.0, alpha=0.13)

    if mode == "teacup_spa":
        cup = [(-36, -32), (36, -32), (28, 0), (-28, 0)]
        wet_watercolor_wash(st, cup, (0.20, 0.91, 0.63), alpha=0.42, bleed=0.06, max_px=3.5, layers=2, key=key + "_cpw")
        st.brush_stroke(cup, width=2.8, color="ink", closed=True, double_stroke=False, key=key + "_cpl")
        st.brush_stroke(ch.sample_bezier((34, -26), (52, -22), (30, -8), n=10), width=2.6, color="ink", double_stroke=False, key=key + "_cph")
        head_y = -42.0 + bob * 0.6
        head = st.circle_pts(2.0, head_y, 15.0, 14.0, n=20)
        wet_watercolor_wash(st, head, (0.96, 0.75, 0.25), alpha=0.90, bleed=0.06, max_px=3.0, layers=2, key=key + "_hw")
        st.brush_stroke(head, width=2.6, color="ink", closed=True, double_stroke=False, key=key + "_hl")
        st.fill_poly([(15, head_y - 3), (26, head_y + 1), (15, head_y + 5)], color="amber", key=key + "_bk")
        st.fill_poly([(-1, head_y - 5), (14, head_y - 5), (13, head_y + 2), (-2, head_y + 2)], color="mint", key=key + "_gl")
        st.brush_stroke([(-1, head_y - 5), (14, head_y - 5), (13, head_y + 2), (-2, head_y + 2)], width=1.6, color="ink", closed=True, double_stroke=False, key=key + "_gll")
    else:
        body = st.circle_pts(0.0, -14.0 + bob, 22.0, 15.5, n=22)
        head = st.circle_pts(8.0, -33.0 + bob, 14.5, 13.5, n=20)
        wet_watercolor_wash(st, body, (0.96, 0.75, 0.25), alpha=0.86, bleed=0.07, max_px=3.5, layers=2, key=key + "_bw")
        st.brush_stroke(body, width=2.6, color="ink", closed=True, double_stroke=False, key=key + "_bl")
        wet_watercolor_wash(st, head, (0.96, 0.75, 0.25), alpha=0.88, bleed=0.07, max_px=3.5, layers=2, key=key + "_hw")
        st.brush_stroke(head, width=2.6, color="ink", closed=True, double_stroke=False, key=key + "_hl")
        st.fill_poly([(20, -36 + bob), (31, -32 + bob), (20, -28 + bob)], color="amber", key=key + "_bk")
        st.fill_poly([(5, -38 + bob), (19, -38 + bob), (18, -31 + bob), (4, -31 + bob)], color="mint", key=key + "_gl")
        st.brush_stroke([(5, -38 + bob), (19, -38 + bob), (18, -31 + bob), (4, -31 + bob)], width=1.6, color="ink", closed=True, double_stroke=False, key=key + "_gll")

        if mode == "judge_zero":
            for sx, px_o in ((-1.0, -36.0), (1.0, 38.0)):
                st.brush_stroke([(sx * 14, -20 + bob), (px_o, -48 + bob)], width=2.4, color="ink", double_stroke=False, key=f"{key}_st{sx}")
                pad = [(px_o - 24, -76 + bob), (px_o + 24, -76 + bob), (px_o + 24, -46 + bob), (px_o - 24, -46 + bob)]
                st.fill_poly(pad, color="white", key=f"{key}_pdf{sx}")
                st.brush_stroke(pad, width=2.2, color="red" if sx > 0 else "ink", closed=True, double_stroke=False, key=f"{key}_pdl{sx}")
                draw_ink_text(st, sign_txt, px_o, -61 + bob, font_px=15, rgb_u8=(180, 42, 36) if sx > 0 else (30, 34, 40), bold=True, key=f"{key}_p0{sx}")
        elif mode == "single_sign":
            st.brush_stroke([(14, -20 + bob), (32, -54 + bob)], width=2.4, color="ink", double_stroke=False, key=key + "_sst")
            pad = [(4, -84 + bob), (64, -84 + bob), (64, -52 + bob), (4, -52 + bob)]
            st.fill_poly(pad, color="white", key=key + "_spdf")
            st.brush_stroke(pad, width=2.2, color="mint_deep", closed=True, double_stroke=False, key=key + "_spdl")
            draw_ink_text(st, sign_txt, 34, -68 + bob, font_px=16, rgb_u8=(10, 118, 78), bold=True, key=key + "_spt")

    ctx.restore()
    if caption:
        draw_ink_text(st, caption, cx, gy + 44.0, font_px=20, rgb_u8=(82, 88, 98), bold=True, key=key + "_cap")


def _solid_tapered_limb(st: ch.HandDrawnStage, pts, w0: float, w1: float, color: str = "cat", key: str = "lmb"):
    arr = np.asarray(pts, dtype=np.float64)
    if len(arr) < 2:
        return
    tang = np.empty_like(arr)
    tang[1:-1] = arr[2:] - arr[:-2]
    tang[0] = arr[1] - arr[0]
    tang[-1] = arr[-1] - arr[-2]
    nrm = np.hypot(tang[:, 0], tang[:, 1])[:, None] + 1e-6
    perp = np.stack([-tang[:, 1] / nrm[:, 0], tang[:, 0] / nrm[:, 0]], axis=1)
    u = np.linspace(0.0, 1.0, len(arr))
    hw = 0.5 * (w0 * (1.0 - u) + w1 * u) * (1.0 + 0.14 * np.sin(u * math.pi))
    poly = np.vstack([arr + perp * hw[:, None], (arr - perp * hw[:, None])[::-1]])
    st.fill_poly(poly, color=color, roughness=0.22, key=key)


def draw_chibi_xeron(
    st: ch.HandDrawnStage,
    gx: float,
    gy: float,
    scale: float = 1.38,
    facing: float = 1.0,
    pose: str = "sit",
    poke_prog: float = 0.0,
    paw_target_world: tuple[float, float] = None,
    expr: str = "aloof",       # "aloof", "sigh_wait", "skeptical", "alert", "happy", "dizzy"
    look_dx: float = 0.75,
    look_dy: float = 0.0,
    heart_ember: float = 0.0,  # Glowing `#2EE59D` confidence ember inside chest
    headband: bool = False,    # Cute gamer headband accessory
    draw_shadow: bool = True,
    key: str = "chibi",
):
    """
    Universal 2.5-Head Flat-Shaded Bold-Ink Chibi Xeron Actor (`纯正二头身短手短脚小黑猫`):
    Supports `sit`, `chin_wait`, `poke_kettle`, `alert_crouch`, `tea_happy`, `leap_arc`, and `hold_pen`!
    """
    ctx = st.ctx
    ctx.save()
    ctx.translate(gx, gy)
    ctx.scale(scale, scale)

    f = 1.0 if facing >= 0 else -1.0
    t = st.t
    t_tail = ch.stagger_time(t, lag_frames=10.0)
    t_head = ch.stagger_time(t, lag_frames=4.0)

    if pose == "leap_arc":
        # Cute compact chibi mid-air bound (stubby tucked paws, sleek bean body, streaming S-tail!)
        tw = math.sin(t_tail * 8.0) * 9.0
        _solid_tapered_limb(st, ch.sample_bezier((-f * 40, -52), (-f * 96, -72 + tw), (-f * 142, -52 - tw), n=18), 17.5, 8.5, color="cat", key=key + "_ltl")
        st.fill_poly(st.circle_pts(0.0, -64.0, 52.0, 32.0, n=32, rot_deg=-f * 12.0), color="cat", roughness=0.26, key=key + "_lbd")
        # Cute short tucked hind & front paws
        st.fill_poly(st.circle_pts(-f * 32.0, -34.0, 14.5, 9.5, n=14, rot_deg=f * 25.0), color="cat", key=key + "_lhp")
        st.fill_poly(st.circle_pts(f * 44.0, -44.0, 14.5, 9.5, n=14, rot_deg=-f * 20.0), color="cat", key=key + "_lfp")
        head_cx, head_cy, head_tilt = f * 42.0, -108.0, f * 6.0
    else:
        if draw_shadow:
            st.soft_shadow(-f * 4.0, 3.0, 62.0, 12.0, alpha=0.16)
        breath = math.sin(t * 2.1) * 1.8
        tw = math.sin(t_tail * (3.8 if expr == "alert" else 1.7) - 0.5) * (11.0 if expr == "alert" else 7.5)
        t_pts = ch.sample_bezier((-f * 34, -18), (-f * 92, -10), (-f * 114, -76 + tw * 0.5), (-f * 78 + tw, -124), n=22)
        _solid_tapered_limb(st, t_pts, 18.0, 8.8, color="cat", key=key + "_tl")

        crouch_dip = 12.0 if pose == "alert_crouch" else 0.0
        top_y = -120.0 + crouch_dip + breath
        torso = np.vstack([
            ch.sample_bezier((-46, -2), (-54, -44), (-34, -92 + crouch_dip), (-16, top_y), n=14),
            ch.sample_bezier((-16, top_y), (0, top_y - 5), (18, top_y), (28, -90 + crouch_dip), n=10),
            ch.sample_bezier((28, -90 + crouch_dip), (48, -46), (46, -10), (34, -2), n=14),
            ch.sample_bezier((34, -2), (10, 2), (-18, 2), (-46, -2), n=10),
        ])
        st.fill_poly(torso, color="cat", roughness=0.28, key=key + "_trs")
        st.brush_stroke(ch.sample_bezier((-f * 44, -32), (-f * 34, -74 + crouch_dip), (-f * 16, top_y + 12), n=12), width=3.0, color="cat_sheen", alpha=0.45, double_stroke=False, key=key + "_bsh")

        if heart_ember > 0.05:
            # Glowing `#2EE59D` confidence flame/ember inside Xeron's chest!
            st.radial_glow(f * 4.0, -64.0 + breath, 4.0, 34.0, color="mint", alpha=0.65 * heart_ember)
            emb = st.circle_pts(f * 4.0, -64.0 + breath, 12.5, 12.5, n=16)
            st.fill_poly(emb, color="mint", alpha=0.95 * heart_ember, key=key + "_emb")
            st.fill_poly(st.circle_pts(f * 4.0, -64.0 + breath, 5.5, 5.5, n=12), color="white", alpha=0.95 * heart_ember, key=key + "_embc")

        st.fill_poly(st.circle_pts(-f * 8.0, -5.0, 14.0, 8.0, n=16), color="cat", key=key + "_bpw1")
        if pose in ("sit", "alert_crouch"):
            st.fill_poly(st.circle_pts(f * 18.0, -5.0, 14.0, 8.0, n=16), color="cat", key=key + "_bpw2")

        head_cx = f * (10.0 if pose == "alert_crouch" else 5.0)
        head_cy = top_y - 32.0
        head_tilt = (f * 6.5 if pose == "chin_wait" else (-f * 4.5 if expr == "skeptical" else 0.0)) + math.sin(t_head * 1.8) * 1.3

        if pose == "chin_wait":
            arm_crv = ch.sample_bezier((f * 26.0, -76.0), (f * 58.0, -14.0), (head_cx + f * 36.0, head_cy + 38.0), n=16)
            _solid_tapered_limb(st, arm_crv, 17.0, 13.5, color="cat", key=key + "_cw_arm")
            st.brush_stroke(arm_crv[3:-2], width=2.4, color="cat_sheen", alpha=0.52, double_stroke=False, key=key + "_cw_shn")
            st.fill_poly(st.circle_pts(head_cx + f * 36.0, head_cy + 38.0, 13.0, 10.5, n=16), color="cat", key=key + "_cw_pw")

        elif pose in ("poke_kettle", "hold_pen") or paw_target_world is not None:
            if paw_target_world is not None:
                lx = (paw_target_world[0] - gx) / scale
                ly = (paw_target_world[1] - gy) / scale
            else:
                lx = f * (72.0 + poke_prog * 28.0)
                ly = -88.0 - poke_prog * 6.0
            sh_p = (f * 22.0, -92.0 + breath)
            dx, dy = lx - sh_p[0], ly - sh_p[1]
            dist = math.hypot(dx, dy)
            if dist > 98.0:
                lx, ly = sh_p[0] + dx * (98.0 / dist), sh_p[1] + dy * (98.0 / dist)
            ctrl = (0.5 * (sh_p[0] + lx), 0.5 * (sh_p[1] + ly) + 12.0)
            _solid_tapered_limb(st, ch.sample_bezier(sh_p, ctrl, (lx, ly), n=14), 17.5, 13.0, color="cat", key=key + "_pk_arm")
            st.fill_poly(st.circle_pts(lx, ly, 12.5, 10.0, n=16), color="cat", key=key + "_pk_pw")
            if pose == "hold_pen":
                # Mint fountain pen held in short paw!
                st.brush_stroke([(lx - f * 12, ly + 12), (lx + f * 22, ly - 22)], width=5.0, color="mint_deep", double_stroke=False, key=key + "_pen")
                st.fill_poly(st.circle_pts(lx + f * 24, ly - 24, 4.0, 4.0, n=8), color="mint", key=key + "_pentip")

    # Head & Ears
    ctx.save()
    ctx.translate(head_cx, head_cy)
    ctx.rotate(math.radians(head_tilt))

    ear_perk = 6.0 if expr == "alert" else (-8.0 if expr == "sigh_wait" else 0.0)
    for ei, es in enumerate((-1.0, 1.0)):
        p_out, p_tip, p_in = (es * 56.0, -18.0), (es * (50.0 - ear_perk * 0.3), -106.0 - ear_perk), (es * 9.0, -44.0)
        ear_o = np.vstack([ch.sample_bezier(p_out, (es * 63.0, -64.0), p_tip, n=14), ch.sample_bezier(p_tip, (es * 28.0, -78.0), p_in, n=14)])
        st.fill_poly(ear_o, color="cat", roughness=0.26, key=f"{key}_eo{ei}")
        wet_watercolor_wash(st, [(es * 45.0, -24.0), (es * 45.5, -89.0 - ear_perk * 0.8), (es * 17.0, -43.0)], (0.45, 0.39, 0.50), alpha=0.92, bleed=0.05, max_px=2.8, layers=2, key=f"{key}_ei{ei}")

    th = np.linspace(0.0, 2.0 * math.pi, 48, endpoint=False)
    c_bulge = 1.0 + 0.12 * np.maximum(0.0, np.sin(th))
    st.fill_poly(np.stack([np.cos(th) * 67.0 * c_bulge, np.sin(th) * 51.0], axis=1), color="cat", roughness=0.28, key=key + "_hd")
    st.brush_stroke(ch.sample_bezier((-36, -39), (0, -49), (36, -39), n=12), width=2.8, color="cat_sheen", alpha=0.40, double_stroke=False, key=key + "_hsh")

    if headband:
        hb = ch.sample_bezier((-60, -20), (0, -34), (60, -20), n=16)
        st.brush_stroke(hb, width=6.5, color="mint", double_stroke=False, key=key + "_hbd")

    b_mod = (t + 0.9) % 4.5
    blink = math.sin(((b_mod - 4.32) / 0.18) * math.pi) if b_mod > 4.32 else 0.0
    gaze_x = f * 6.0 + ch.clamp(look_dx, -1.2, 1.2) * 6.5

    for ei, es in enumerate((-1.0, 1.0)):
        ex = gaze_x + es * 26.5
        ey = 2.0 + ch.clamp(look_dy, -1.0, 1.0) * 4.5
        if expr == "dizzy":
            d_s = 1.0 if ei == 0 else -1.0
            st.brush_stroke([(ex - d_s * 14, ey - 8), (ex + d_s * 10, ey), (ex - d_s * 14, ey + 8)], width=4.2, color="mint", double_stroke=False, key=f"{key}_dzy{ei}")
        elif expr == "happy":
            st.brush_stroke(ch.sample_bezier((ex - 19, ey + 5), (ex, ey - 13), (ex + 19, ey + 5), n=16), width=4.8, color="mint", double_stroke=False, key=f"{key}_hey{ei}")
        elif blink > 0.82:
            st.brush_stroke([(ex - 19, ey), (ex + 19, ey)], width=4.4, color="mint", double_stroke=False, key=f"{key}_bey{ei}")
        else:
            open_fac = 0.68 if expr == "sigh_wait" else (1.12 if expr == "alert" else (0.75 if (expr == "skeptical" and ei == 0) else 0.96))
            open_h = 17.8 * open_fac * (1.0 - 0.85 * blink)
            top_ey = ey - open_h * 0.35
            eye_pts = [(ex - 20.0, top_ey), (ex + 20.0, top_ey)] + [(ex + math.cos(a) * 20.0, top_ey + math.sin(a) * open_h * 1.25) for a in np.linspace(0.0, math.pi, 18)]
            st.fill_poly(eye_pts, color="mint", roughness=0.10, key=f"{key}_ey{ei}")
            px_p = ex + ch.clamp(look_dx, -1.0, 1.0) * 6.0
            st.fill_poly(st.circle_pts(px_p, top_ey + open_h * 0.46, 3.8, open_h * 0.45, n=16), color="cat", key=f"{key}_pp{ei}")
            st.fill_poly(st.circle_pts(px_p - 3.5, top_ey + open_h * 0.25, 2.3, 2.1, n=10), color="white", alpha=0.95, roughness=0.0, key=f"{key}_cl{ei}")
            brow_sl = (3.2 * es if expr == "sigh_wait" else (-4.0 if (expr == "skeptical" and ei == 1) else 0.0))
            st.brush_stroke([(ex - 21.5, top_ey - brow_sl), (ex + 21.5, top_ey + brow_sl)], width=4.6, color="cat", double_stroke=False, key=f"{key}_ld{ei}")

    st.fill_poly([(gaze_x - 4.8, 14.0), (gaze_x + 4.8, 14.0), (gaze_x, 18.5)], color="ear_inner", key=key + "_ns")
    for ws in (-1.0, 1.0):
        wx0 = ws * 58.0
        st.brush_stroke([(wx0, 5.5), (wx0 + ws * 24.0, 2.0)], width=2.6, color="ink_soft", double_stroke=False, key=f"{key}_w1{ws}")
        st.brush_stroke([(wx0 - ws * 2.0, 14.5), (wx0 + ws * 22.0, 18.5)], width=2.6, color="ink_soft", double_stroke=False, key=f"{key}_w2{ws}")
    ctx.restore()

    if pose == "tea_happy":
        mx, my = f * 48.0, -56.0 + math.sin(t * 3.0) * 2.5
        _solid_tapered_limb(st, ch.sample_bezier((f * 18.0, -82.0), (f * 34.0, -64.0), (mx - f * 12.0, my + 4.0), n=12), 16.5, 13.0, color="cat", key=key + "_tm_arm")
        mug = [(mx - 20, my - 22), (mx + 20, my - 22), (mx + 17, my + 20), (mx - 17, my + 20)]
        wet_watercolor_wash(st, mug, (0.20, 0.92, 0.64), alpha=0.55, bleed=0.06, max_px=3.0, layers=2, key=key + "_mugw")
        st.brush_stroke(mug, width=2.8, color="ink", closed=True, double_stroke=False, key=key + "_mugl")
        st.brush_stroke(ch.sample_bezier((mx + f * 20, my - 14), (mx + f * 34, my), (mx + f * 18, my + 12), n=10), width=2.6, color="ink", double_stroke=False, key=key + "_mugh")
        for si in range(2):
            su = ((t * 0.9 + si * 0.5) % 1.0)
            sx_m = mx - 6 + si * 12 + math.sin(su * 6.0) * 4.0
            sy_m = my - 28 - su * 28.0
            st.brush_stroke([(sx_m, sy_m + 12), (sx_m + 3, sy_m)], width=2.2, color="mint_deep", alpha=math.sin(su * math.pi) * 0.75, double_stroke=False, key=f"{key}_mstm{si}")

    ctx.restore()


def draw_glass_kettle(
    st: ch.HandDrawnStage,
    cx: float,
    gy: float,
    scale: float = 1.0,
    temp_c: float = 20.0,
    power_on: bool = False,
    xray_heat: float = 0.0,
    boiling: float = 0.0,
    show_xeron_steam: bool = False,
    key: str = "ktl",
) -> dict:
    ctx = st.ctx
    ctx.save()
    ctx.translate(cx, gy)
    ctx.scale(scale, scale)
    t = st.t

    st.soft_shadow(0.0, 4.0, 145.0, 14.0, alpha=0.16)
    base_pts = [(-112, 0), (112, 0), (102, -28), (-102, -28)]
    st.fill_poly(base_pts, color="ink", alpha=0.88, key=key + "_bs")
    led_col = "mint" if boiling > 0.3 else ("amber" if power_on else "ink_soft")
    st.fill_poly(st.circle_pts(0.0, -14.0, 7.5, 5.0, n=14), color=led_col, key=key + "_led")
    if power_on:
        st.radial_glow(0.0, -14.0, 2.0, 24.0, color="mint" if boiling > 0.3 else "amber", alpha=0.45)

    sw_y = -10.0 if power_on else -24.0
    sw_pts = [(-104, -18), (-134, sw_y - 5), (-134, sw_y + 6), (-104, -8)]
    st.fill_poly(sw_pts, color="mint" if boiling > 0.3 else ("amber" if power_on else "ink_faint"), key=key + "_swp")
    st.brush_stroke(sw_pts, width=2.4, color="ink", closed=True, double_stroke=False, key=key + "_swpl")

    bot_w, top_w = 98.0, 80.0
    y_bot, y_top = -28.0, -268.0
    glass_poly = np.vstack([
        ch.sample_bezier((-bot_w, y_bot), (-108, -110), (-92, -205), (-top_w, y_top), n=16),
        [(top_w, y_top), (top_w + 26, y_top - 10), (top_w + 8, y_top + 32)],
        ch.sample_bezier((top_w + 8, y_top + 32), (96, -190), (108, -110), (bot_w, y_bot), n=14),
    ])
    st.pencil_underdraw([(-bot_w, y_bot), (-top_w, y_top), (top_w, y_top), (bot_w, y_bot)], overshoot=7.0, alpha=0.12, key=key + "_und")
    wet_watercolor_wash(st, glass_poly, (0.89, 0.94, 0.96), alpha=0.36, bleed=0.04, max_px=3.0, layers=2, key=key + "_glw")

    y_water = -202.0
    w_surf_half = 86.0
    if boiling <= 0.02:
        surf_pts = [(-w_surf_half, y_water), (w_surf_half, y_water)]
        water_rgb = (0.72, 0.86, 0.93) if temp_c < 40 else ((0.52, 0.88, 0.82) if xray_heat > 0.2 else (0.70, 0.85, 0.91))
    else:
        xs_w = np.linspace(-w_surf_half, w_surf_half, 26)
        ys_w = y_water + boiling * (np.sin(xs_w * 0.085 + t * 16.0) * 9.5 + np.cos(xs_w * 0.14 - t * 21.0) * 5.5)
        surf_pts = list(zip(xs_w, ys_w))
        water_rgb = (0.20, 0.92, 0.65)

    water_poly = [(-bot_w + 5, y_bot - 4)] + surf_pts + [(bot_w - 5, y_bot - 4)]
    wet_watercolor_wash(st, water_poly, water_rgb, alpha=0.46 + 0.22 * boiling, bleed=0.05, max_px=3.5, layers=2, key=key + "_wtr")
    st.brush_stroke(surf_pts, width=3.4 if boiling > 0.1 else 2.8, color="mint_deep" if boiling > 0.2 else "ink_soft", roughness=0.25, double_stroke=False, key=key + "_mnsc")

    coil_y = y_bot - 10.0
    coil_col = "mint" if (xray_heat > 0.2 or boiling > 0.2) else ("amber" if power_on else "ink_soft")
    st.brush_stroke([(-78, coil_y), (78, coil_y)], width=7.5, color=coil_col, double_stroke=False, key=key + "_coil")

    if xray_heat > 0.05 and boiling <= 0.05:
        for ri in range(3):
            ru = ((t * 0.95 + ri * 0.33) % 1.0)
            ry_w = ch.lerp(coil_y - 8.0, y_water + 34.0, ru)
            rw_w = 68.0 * (1.0 - ru * 0.25)
            ra_w = math.sin(ru * math.pi) * 0.78 * xray_heat
            st.brush_stroke(ch.sample_bezier((-rw_w, ry_w), (0.0, ry_w - 12.0), (rw_w, ry_w), n=16), width=3.0, color="mint_deep", alpha=ra_w, double_stroke=False, key=f"{key}_thw{ri}")
        for bi in range(12):
            bu = ((t * (1.2 + (bi % 3) * 0.35) + bi * 0.19) % 1.0)
            bx_b = ((bi * 37) % 136) - 68.0 + math.sin(t * 6.0 + bi) * 4.5
            by_b = ch.lerp(coil_y - 6.0, y_water + 24.0, bu)
            br_b = (3.2 + (bi % 3) * 1.4) * (1.0 - bu * 0.35) * xray_heat
            if br_b > 1.2:
                bp = st.circle_pts(bx_b, by_b, br_b, br_b, n=10)
                st.fill_poly(bp, color="mint", alpha=0.88 * xray_heat, key=f"{key}_mb{bi}")
                st.brush_stroke(bp, width=1.4, color="ink", alpha=0.75 * xray_heat, closed=True, double_stroke=False, key=f"{key}_mbl{bi}")

    if boiling > 0.05:
        for bi in range(15):
            bu = ((t * (2.4 + (bi % 4) * 0.45) + bi * 0.13) % 1.0)
            bx_b = ((bi * 43) % 142) - 71.0 + math.sin(t * 11.0 + bi) * 7.5
            by_b = ch.lerp(coil_y - 8.0, y_water - 8.0, bu)
            br_b = (5.0 + (bi % 4) * 2.6) * boiling
            bp = st.circle_pts(bx_b, by_b, br_b, br_b, n=12)
            st.fill_poly(bp, color="white" if bi % 2 == 0 else "mint_light", alpha=0.92 * boiling, key=f"{key}_bb{bi}")
            st.brush_stroke(bp, width=2.0, color="mint_deep", alpha=0.90 * boiling, closed=True, double_stroke=False, key=f"{key}_bbl{bi}")

    h_outer = ch.sample_bezier((-86, -246), (-148, -238), (-150, -108), (-96, -88), n=20)
    _solid_tapered_limb(st, h_outer, 16.0, 14.0, color="ink", key=key + "_hndl")
    for gy_t in (-85, -125, -165, -202):
        st.brush_stroke([(-32, gy_t), (-12, gy_t)], width=2.0, color="ink_soft", alpha=0.65, double_stroke=False, key=f"{key}_gtk{gy_t}")
    st.brush_stroke([(-64, -238), (-74, -72)], width=5.5, color="white", alpha=0.72, double_stroke=False, key=key + "_gl_hi")
    st.brush_stroke(glass_poly, width=4.4, color="ink", closed=True, roughness=0.32, double_stroke=True, key=key + "_gl_out")
    ch.draw_brush_xeron_sig(st, 58.0, -14.0, scale=0.32, progress=1.0, key=key + "_bsig")

    lid_pop_deg = -boiling * (11.0 + 7.5 * abs(math.sin(t * 18.0)))
    ctx.save()
    ctx.translate(-top_w, y_top)
    ctx.rotate(math.radians(lid_pop_deg))
    st.fill_poly([(0, 0), (top_w * 2.0, 0), (top_w * 1.85, -16), (top_w * 0.15, -16)], color="ink", key=key + "_lid")
    knob = st.circle_pts(top_w, -24.0, 14.0, 9.0, n=16)
    st.fill_poly(knob, color="mint" if boiling > 0.3 else "wood_wash", key=key + "_knb")
    st.brush_stroke(knob, width=2.6, color="ink", closed=True, double_stroke=False, key=key + "_knbl")
    ctx.restore()

    if boiling > 0.08:
        for pi in range(5):
            pu = ((t * 1.15 + pi * 0.20) % 1.0)
            px_s = top_w + 18.0 + pu * 45.0 + math.sin(pu * 7.0 + pi) * 18.0 - (pi % 2) * 55.0
            py_s = y_top - 24.0 - pu * 165.0
            pr_s = (22.0 + pu * 36.0) * boiling
            pa_s = math.sin(pu * math.pi) * 0.55 * boiling
            puff = st.circle_pts(px_s, py_s, pr_s * 1.25, pr_s * 0.88, n=20)
            wet_watercolor_wash(st, puff, (0.22, 0.93, 0.67), alpha=pa_s, bleed=0.16, max_px=8.0, layers=2, key=f"{key}_stmp{pi}")
            st.brush_stroke(puff[:10], width=2.4, color="mint_deep", alpha=pa_s * 0.9, double_stroke=False, key=f"{key}_stml{pi}")
        st.draw_impact_ticks(top_w + 15.0, y_top - 28.0, 26.0, 74.0, n_ticks=6, color="mint_deep", alpha=0.82 * boiling, key=key + "_bimp")
        if show_xeron_steam:
            ch.draw_brush_xeron_sig(st, top_w + 95.0, y_top - 115.0, scale=0.62, progress=ch.clamp(boiling * 1.4), key=key + "_stmsig")

    ctx.restore()
    return {
        "switch_xy": (cx - 128.0 * scale, gy + sw_y * scale),
        "right_wall_xy": (cx + 96.0 * scale, gy - 145.0 * scale),
        "coil_xy": (cx + 55.0 * scale, gy + (coil_y - 12.0) * scale),
        "top_xy": (cx, gy + (y_top - 28.0) * scale),
    }


def draw_skill_cartridge(st: ch.HandDrawnStage, cx: float, cy: float, scale: float = 1.0, glow: float = 1.0, label: str = "Skill", sub: str = "标准可复用模块", key: str = "skc"):
    """Iconic `#2EE59D` Reusable AI Skill Capsule/Cartridge Prop."""
    w, h = 210.0 * scale, 108.0 * scale
    hw, hh = w * 0.5, h * 0.5
    if glow > 0.1:
        st.radial_glow(cx, cy, 12.0 * scale, 138.0 * scale, color="mint", alpha=0.38 * glow)
    pts = [(cx - hw, cy - hh), (cx + hw, cy - hh), (cx + hw, cy + hh), (cx - hw, cy + hh)]
    st.pencil_underdraw(pts, overshoot=6.0 * scale, alpha=0.16, key=key + "_u")
    wet_watercolor_wash(st, pts, (0.18, 0.91, 0.63), alpha=0.68, bleed=0.06, max_px=4.0, layers=2, key=key + "_w")
    st.brush_stroke(pts, width=3.6 * scale, color="ink", closed=True, double_stroke=False, key=key + "_b")
    # Gold/Mint connector pins on bottom edge
    for pi in range(-2, 3):
        px_c = cx + pi * 26.0 * scale
        pin = [(px_c - 7 * scale, cy + hh), (px_c + 7 * scale, cy + hh), (px_c + 7 * scale, cy + hh + 14 * scale), (px_c - 7 * scale, cy + hh + 14 * scale)]
        st.fill_poly(pin, color="amber", key=f"{key}_pn{pi}")
        st.brush_stroke(pin, width=2.0 * scale, color="ink", closed=True, double_stroke=False, key=f"{key}_pnl{pi}")
    draw_ink_text(st, label, cx, cy - (14.0 * scale if sub else 0.0), font_px=max(16, int(34 * scale)), rgb_u8=(14, 24, 20), bold=True, key=key + "_t")
    if sub and scale >= 0.65:
        draw_ink_text(st, sub, cx, cy + 24.0 * scale, font_px=max(13, int(19 * scale)), rgb_u8=(12, 92, 62), bold=True, key=key + "_s")


def draw_poker_chip_stack(st: ch.HandDrawnStage, cx: float, gy: float, n_chips: int = 6, scale: float = 1.0, key: str = "chps"):
    """Tactile hand-drawn stack of `#2EE59D` strategy/poker chips."""
    st.soft_shadow(cx, gy + 3.0, 56.0 * scale, 10.0 * scale, alpha=0.15)
    for ci in range(n_chips):
        cy_c = gy - (8.0 + ci * 14.5) * scale
        rx, ry = 46.0 * scale, 13.5 * scale
        side = [(cx - rx, cy_c), (cx + rx, cy_c), (cx + rx, cy_c + 12 * scale), (cx - rx, cy_c + 12 * scale)]
        st.fill_poly(side, color="mint_deep" if ci % 2 == 0 else "ink", key=f"{key}_sd{ci}")
        top = st.circle_pts(cx, cy_c, rx, ry, n=24)
        st.fill_poly(top, color="mint" if ci % 2 == 0 else "white", key=f"{key}_tp{ci}")
        st.brush_stroke(top, width=2.4 * scale, color="ink", closed=True, double_stroke=False, key=f"{key}_tpl{ci}")


def draw_compounding_flywheel(st: ch.HandDrawnStage, cx: float, cy: float, r: float, rot_rad: float, mint_glow: float = 0.8, key: str = "flyw"):
    """Sculpted heavy mechanical Compounding Flywheel prop."""
    if mint_glow > 0.1:
        wet_watercolor_wash(st, st.circle_pts(cx, cy, r * 1.15, r * 1.15, n=36), (0.18, 0.91, 0.62), alpha=0.32 * mint_glow, bleed=0.12, max_px=8.0, layers=2, key=key + "_gw")
    outer = st.circle_pts(cx, cy, r, r, n=52)
    inner = st.circle_pts(cx, cy, r * 0.78, r * 0.78, n=48)
    st.fill_poly(outer, color="mint_light" if mint_glow > 0.3 else "white", alpha=0.55, key=key + "_of")
    st.fill_poly(inner, color="white", alpha=0.88, key=key + "_if")
    for si in range(6):
        a = rot_rad + si * (math.pi / 3.0)
        p0 = (cx + math.cos(a) * (r * 0.18), cy + math.sin(a) * (r * 0.18))
        p1 = (cx + math.cos(a) * (r * 0.78), cy + math.sin(a) * (r * 0.78))
        st.brush_stroke([p0, p1], width=max(3.0, r * 0.065), color="mint_deep" if mint_glow > 0.4 else "ink", double_stroke=False, key=f"{key}_sp{si}")
    st.brush_stroke(outer, width=max(4.0, r * 0.075), color="ink", closed=True, double_stroke=True, key=key + "_ol")
    st.brush_stroke(inner, width=max(2.4, r * 0.035), color="mint_deep", closed=True, double_stroke=False, key=key + "_il")
    hub = st.circle_pts(cx, cy, r * 0.19, r * 0.19, n=20)
    st.fill_poly(hub, color="mint", key=key + "_hb")
    st.brush_stroke(hub, width=3.0, color="ink", closed=True, double_stroke=False, key=key + "_hbl")
