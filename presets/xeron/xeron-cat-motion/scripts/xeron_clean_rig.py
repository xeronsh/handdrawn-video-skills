#!/usr/bin/env python3
"""
Xeron Cat Motion v7.0 — FLUID SPINE ACTING + AI UI / ENGINEERING METHODS / AI JARGON ENGINE
Key Upgrades in v7.0:
1. FLUID 3-JOINT FLEXIBLE C/S-CURVE SPINE & SECONDARY FOLLOW-THROUGH (`draw_xeron_actor`):
   - Flexible spline spine (`hip -> waist -> chest -> neck`) replacing rigid block rotation
   - Phase-delayed overlapping action across chest, head nod, independent ear flicks, whisker bounce & 5-wave whip tail
   - Grounded dynamic contact shadow + 12 plug-and-play expressive acting presets (`act_mode`):
     `idle_breathe`, `walk_bouncy`, `sneak_tiptoe`, `vibe_coding`, `furious_typing`, `facepalm`,
     `head_scratch`, `point_explain`, `gacha_pull`, `eureka_jump`, `celebrate_cheer`, `peek_curious`
2. EXPANDED AUTHENTIC AI PRODUCT UI PROPS (`draw_ai_ui_prop`):
   - `claude_code` (`Plan Mode` + `Thinking` + `Subagents` + diff), `cursor` (`Tab` ghost-text + `Composer`),
     `chatgpt`, `chatgpt_canvas` (split editor), `deepseek_r1` (`已深度思考` CoT), `mcp_hub` (USB-C universal dock),
     `doubao`, `muse`, `grok_bot`, `agent_cli`
3. AI ENGINEERING PARADIGMS (`draw_ai_method_prop`) & PLAYFUL AI SLANG GAGS (`draw_ai_jargon_prop`):
   - Methods: `prompt_caching`, `context_compaction`, `rag_pipeline`, `harness_layers`, `subagent_fanout`, `speculative_decoding`
   - Jargon: `vibe_coding`, `gacha_roll`, `hallucination`, `context_rot`, `token_assassin`, `alchemy_distill`, `agent_loop`
"""

import functools
import hashlib
import math
import os
import subprocess
import time
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment
from scipy import signal

W, H = 1920, 1080
FPS = 60
BPM = 88.0
BEAT_S = 60.0 / BPM


def _resolve_font(env_var: str, candidates: list[str], fallback: str | None = None) -> str:
    env_path = os.environ.get(env_var, "").strip()
    if env_path and os.path.exists(env_path):
        return env_path
    for cand in candidates:
        if os.path.exists(cand):
            return cand
    return fallback if fallback is not None else candidates[0]


FONT_SANS_REG = _resolve_font(
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
FONT_SANS_BOLD = _resolve_font(
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
    fallback=FONT_SANS_REG,
)

PAL_RGB = {
    "white": (255, 255, 255),
    "ink": (20, 22, 24),
    "ink_detail": (74, 78, 84),
    "ink_soft": (148, 154, 162),
    "shadow": (232, 236, 240),
    "sub_ink": (22, 26, 30),
    "cat_fill": (22, 22, 25),
    "cat_line": (8, 8, 10),
    "cat_ear": (110, 99, 120),
    "cat_nose": (108, 112, 118),
    "mint": (46, 229, 157),         # #2EE59D core mint high-glow
    "mint_ink": (13, 142, 95),      # #0D8E5F deep high-contrast mint ink
    "soft_mint": (230, 251, 243),
    "pale_mint": (240, 253, 247),
    "blush": (244, 150, 162),
    # Clean secondary hand-drawn marker accents for authentic UIs & warnings
    "blue": (43, 84, 142),
    "soft_blue": (234, 242, 252),
    "orange": (222, 122, 34),
    "soft_orange": (253, 242, 228),
    "red": (201, 59, 53),
    "soft_red": (253, 236, 235),
    "purple": (116, 82, 162),
    "soft_purple": (243, 238, 251),
    # Verified Official Brand Icon Colors
    "g_blue": (66, 133, 244),
    "g_red": (234, 67, 53),
    "g_yellow": (251, 188, 4),
    "g_green": (52, 168, 83),
    "colab_gold": (249, 171, 0),
    "colab_orange": (232, 113, 10),
    "claude_coral": (217, 119, 87),
    "openai_green": (16, 163, 127),
    "meta_blue": (0, 129, 251),
    "ig_pink": (225, 48, 108),
    "fb_blue": (24, 119, 242),
    "xianyu_yellow": (255, 230, 0),
    "xhs_red": (255, 36, 66),
    "doubao_cyan": (45, 218, 182),
    "doubao_violet": (156, 110, 255),
}
PAL_BGR = {k: (v[2], v[1], v[0]) for k, v in PAL_RGB.items()}

_FONT_CACHE = {}
_PATCH_CACHE = {}
_REUSE_BUF = np.full((H, W, 3), 255, dtype=np.uint8)
_TEMP_LAYER_BUF = np.full((H, W, 3), 255, dtype=np.uint8)
_WHITE_BUF = np.full((H, W, 3), 255, dtype=np.uint8)
_GLOBAL_SHAKE_PX = 0.0


def set_global_shake(px: float):
    global _GLOBAL_SHAKE_PX
    _GLOBAL_SHAKE_PX = px


@functools.lru_cache(maxsize=4096)
def det_hash_int(key: str) -> int:
    return int.from_bytes(hashlib.blake2b(key.encode("utf-8"), digest_size=4).digest(), "little")


EXPR_PRESETS = {
    "aloof":          (0.86, 0.86,   0.0,   0.0, 1.00,   0.0,   0.0, "neutral"),
    "side_eye":       (0.68, 0.68,  -3.0,   3.0, 0.95,  -0.06,  0.04, "flat"),
    "skeptical":      (0.56, 1.08,  -6.0,  14.0, 0.95,  -0.12,  0.08, "smug"),
    "deadpan":        (0.06, 0.06,   0.0,   0.0, 1.00,  -0.18, -0.18, "flat"),
    "tired_droop":    (0.42, 0.42,  -9.0,   9.0, 0.92,  -0.26, -0.26, "sigh"),
    "glare":          (0.44, 0.44,  10.0, -10.0, 0.80,  -0.14, -0.14, "flat"),
    "sigh":           (0.04, 0.04,  -8.0,   8.0, 1.00,  -0.22, -0.22, "sigh"),
    "thinking":       (0.76, 1.02,  -4.0,  10.0, 1.00,   0.05, -0.08, "neutral"),
    "eureka":         (1.20, 1.20,  -8.0,   8.0, 1.25,   0.12,  0.12, "neutral"),
    "focus":          (0.78, 0.78,  13.0, -13.0, 0.90,   0.08,  0.08, "neutral"),
    "strain":         (0.12, 0.12,  18.0, -18.0, 0.85,  -0.26, -0.26, "grit"),
    "typing":         (0.80, 0.80,  10.0, -10.0, 0.92,   0.04, -0.04, "flat"),
    "smug":           (0.66, 0.74,  -3.0,   7.0, 0.95,   0.03,  0.08, "smug"),
    "coffee_zen":     (0.54, 0.54,  -2.0,   2.0, 0.96,   0.00,  0.00, "neutral"),
    "satisfied":      (0.15, 0.15,  -5.0,   5.0, 1.00,   0.02,  0.02, "smug"),
    "wink":           (0.88, 0.03,   0.0,   5.0, 1.02,   0.04,  0.10, "smug"),
    "alert":          (1.12, 1.12,  -5.0,   5.0, 1.08,   0.18,  0.18, "neutral"),
    "surprised_tiny": (1.16, 1.16,  -4.0,   4.0, 0.72,   0.14,  0.14, "open_tiny"),
    "blank":          (0.03, 0.03,   0.0,   0.0, 1.00,  -0.32, -0.32, "flat"),
    "dizzy":          (1.10, 1.10,   0.0,   0.0, 1.00,  -0.18, -0.18, "open_tiny"),
}


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if x < lo else (hi if x > hi else x)


def lerp(a: float, b: float, k: float) -> float:
    return a + (b - a) * k


def lerp_pt(p0, p1, k: float):
    return (lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k))


def seg(t: float, t0: float, t1: float) -> float:
    if t1 <= t0:
        return 1.0 if t >= t0 else 0.0
    return clamp((t - t0) / (t1 - t0))


def ease_out(x: float) -> float:
    x = clamp(x)
    return 1.0 - (1.0 - x) ** 3


def ease_in(x: float) -> float:
    x = clamp(x)
    return x * x * x


def ease_in_out(x: float) -> float:
    x = clamp(x)
    return 4 * x * x * x if x < 0.5 else 1.0 - ((-2 * x + 2) ** 3) / 2.0


def smootherstep(x: float) -> float:
    x = clamp(x)
    return x * x * x * (x * (x * 6.0 - 15.0) + 10.0)


def back_out(x: float, s: float = 1.55) -> float:
    x = clamp(x) - 1.0
    return x * x * ((s + 1.0) * x + s) + 1.0


def damped_spring(dt: float, freq: float = 11.5, decay: float = 5.4) -> float:
    if dt <= 0.0:
        return 0.0
    return 1.0 - math.exp(-decay * dt) * math.cos(freq * dt)


def anticipation_spring(u_prog: float, dip: float = 0.14) -> float:
    """Classic animation curve: brief backward anticipation dip (`0..0.22`) -> fast launch + spring settle (`0.22..1.0`)."""
    u_c = clamp(u_prog)
    if u_c < 0.22:
        k = u_c / 0.22
        return -dip * math.sin(k * math.pi)
    k2 = (u_c - 0.22) / 0.78
    return back_out(k2, s=1.42)


@functools.lru_cache(maxsize=32768)
def seeded_floats(key: str, boil_idx: int, count: int) -> np.ndarray:
    h = hashlib.blake2b(f"{key}:{boil_idx}".encode("utf-8"), digest_size=8).digest()
    seed = int.from_bytes(h, "little") & 0xFFFFFFFF
    arr = np.random.default_rng(seed).uniform(-1.0, 1.0, size=count).astype(np.float32)
    arr.flags.writeable = False
    return arr


def soft_boil_floats(key: str, t: float, count: int, hz: float = 5.0) -> np.ndarray:
    phase = t * hz
    idx0 = int(phase)
    frac = phase - idx0
    a = seeded_floats(key, idx0, count)
    if frac < 0.70:
        return a
    b = seeded_floats(key, idx0 + 1, count)
    w = 0.5 - 0.5 * math.cos(((frac - 0.70) / 0.30) * math.pi)
    return a * (1.0 - w) + b * w


def quad_bezier(p0, p1, p2, n: int = 14) -> np.ndarray:
    ts = np.linspace(0.0, 1.0, n, dtype=np.float32)[:, None]
    p0, p1, p2 = [np.asarray(p, dtype=np.float32) for p in (p0, p1, p2)]
    return ((1 - ts) ** 2) * p0 + 2 * (1 - ts) * ts * p1 + (ts ** 2) * p2


def cubic_bezier(p0, p1, p2, p3, n: int = 16) -> np.ndarray:
    ts = np.linspace(0.0, 1.0, n, dtype=np.float32)[:, None]
    p0, p1, p2, p3 = [np.asarray(p, dtype=np.float32) for p in (p0, p1, p2, p3)]
    return ((1 - ts) ** 3) * p0 + 3 * ((1 - ts) ** 2) * ts * p1 + 3 * (1 - ts) * (ts ** 2) * p2 + (ts ** 3) * p3


def rounded_rect_pts(x: float, y: float, w: float, h: float, r: float = 4.5, rot_deg: float = 0.0) -> np.ndarray:
    r = min(r, max(0.5, w * 0.25), max(0.5, h * 0.25))
    corners = [
        (x + w - r, y + r, -math.pi * 0.5, 0.0),
        (x + w - r, y + h - r, 0.0, math.pi * 0.5),
        (x + r, y + h - r, math.pi * 0.5, math.pi),
        (x + r, y + r, math.pi, math.pi * 1.5),
    ]
    pts = []
    for cx, cy, a0, a1 in corners:
        for a in np.linspace(a0, a1, 3):
            pts.append([cx + math.cos(a) * r, cy + math.sin(a) * r])
    arr = np.asarray(pts, dtype=np.float32)
    if abs(rot_deg) > 1e-3:
        mcx, mcy = x + w * 0.5, y + h * 0.5
        arr[:, 0] -= mcx
        arr[:, 1] -= mcy
        rad = math.radians(rot_deg)
        c, s = math.cos(rad), math.sin(rad)
        arr = np.stack([arr[:, 0] * c - arr[:, 1] * s + mcx, arr[:, 0] * s + arr[:, 1] * c + mcy], axis=1)
    return arr


def get_font(fpath: str, size: int):
    key = (fpath, size)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = ImageFont.truetype(fpath, size)
    return _FONT_CACHE[key]


@functools.lru_cache(maxsize=2)
def _get_valid_cmap(fpath: str):
    try:
        from fontTools.ttLib import TTFont
        return set(TTFont(fpath, fontNumber=0).getBestCmap().keys())
    except Exception:
        return None


def sanitize_font_text(text: str, bold: bool = True) -> str:
    cmap = _get_valid_cmap(FONT_SANS_BOLD if bold else FONT_SANS_REG)
    if not cmap:
        return text
    repl = {0x2726: "", 0x2727: "", 0x2728: "", 0x273B: "*", 0x276F: ">", 0x26A1: ""}
    out = []
    for ch in text:
        cp = ord(ch)
        if cp < 32 or cp in cmap:
            out.append(ch)
        elif cp in repl:
            out.append(repl[cp])
    return "".join(out).strip() or text.encode("ascii", "ignore").decode("ascii")


def _get_cached_label_patch(text: str, fsize: int, color_key: str, slant_deg: float, organic: bool, bold: bool = False):
    text = sanitize_font_text(text, bold=bold)
    ckey = (text, fsize, color_key, round(slant_deg, 1), organic, bold)
    if ckey in _PATCH_CACHE:
        return _PATCH_CACHE[ckey]

    font = get_font(FONT_SANS_BOLD if bold else FONT_SANS_REG, fsize)
    rgb = PAL_RGB.get(color_key, PAL_RGB["ink"])
    dummy = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    use_white_halo = (color_key != "white")

    if not organic:
        bbox = dummy.textbbox((0, 0), text, font=font)
        tw, th = max(4, bbox[2] - bbox[0]), max(4, bbox[3] - bbox[1])
        pad = 8
        im = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        if use_white_halo:
            for ox, oy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
                d.text((pad - bbox[0] + ox, pad - bbox[1] + oy), text, font=font, fill=(255, 255, 255, 238))
        d.text((pad - bbox[0], pad - bbox[1]), text, font=font, fill=(*rgb, 255))
    else:
        glyph_boxes = [dummy.textbbox((0, 0), ch, font=font) for ch in text]
        g_widths = [(b[2] - b[0]) + (max(6, int(fsize * 0.28)) if ch == " " else (1 if ord(ch) < 128 else 2)) for ch, b in zip(text, glyph_boxes)]
        total_w = max(8, sum(g_widths))
        max_h = max((max(8, b[3] - b[1]) for b in glyph_boxes), default=fsize)
        pad_outer = 16
        im = Image.new("RGBA", (int(total_w + pad_outer * 2), int(max_h + pad_outer * 2)), (0, 0, 0, 0))
        cur_x = pad_outer
        for idx_c, (ch, gw, gb) in enumerate(zip(text, g_widths, glyph_boxes)):
            if ch == " ":
                cur_x += gw
                continue
            h_ch = int.from_bytes(hashlib.blake2b(f"{text}:{idx_c}".encode(), digest_size=4).digest(), "little")
            is_cjk = ord(ch) > 127
            ch_rot = (slant_deg + ((h_ch % 48) / 10.0 - 2.4)) if is_cjk else 0.0
            ch_dy = (((h_ch // 71) % 5 - 2.0) * 0.9) if is_cjk else 0.0
            pad = 10
            g_img = Image.new("RGBA", (int(gw + pad * 2), int(fsize + pad * 2)), (0, 0, 0, 0))
            gd = ImageDraw.Draw(g_img)
            draw_y = pad - gb[1] + (max_h - (gb[3] - gb[1])) * 0.5
            for ox, oy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
                gd.text((pad + ox, draw_y + oy), ch, font=font, fill=(255, 255, 255, 240))
            gd.text((pad, draw_y), ch, font=font, fill=(*rgb, 255))
            rot_g = g_img.rotate(ch_rot, resample=Image.BICUBIC, expand=False)
            im.alpha_composite(rot_g, (int(round(cur_x - pad)), int(round(pad_outer + ch_dy - pad))))
            cur_x += gw

    arr = np.array(im, dtype=np.uint8)
    bgr_u8 = arr[:, :, [2, 1, 0]]
    alpha_f32 = (arr[:, :, 3:4].astype(np.float32)) * (1.0 / 255.0)
    if len(_PATCH_CACHE) > 2048:
        _PATCH_CACHE.clear()
    _PATCH_CACHE[ckey] = (bgr_u8, alpha_f32)
    return bgr_u8, alpha_f32


SUBTITLE_KEYWORDS = [
    # AI Slang, UIs & Engineering Methods
    "Vibe Coding", "抽卡", "幻觉", "Context Rot", "降智", "Token 刺客", "炼丹", "蒸馏",
    "Cursor", "Claude Code", "ChatGPT", "DeepSeek", "MCP 万能坞", "MCP", "缓存护栏", "前缀缓存",
    "子代理", "Subagents", "RAG", "投机解码", "稳了",
    # Creator & Engineering Workflow Highlights
    "SOP", "Skill", "工作流", "自动化", "工程化", "可复用", "效率杠杆", "复利效应",
    "第一性原理", "深度思考", "核心主线", "内容沉淀", "结构化", "正向循环", "关键阈值",
    "Harness 工程", "Personal Agent", "AI 工作流", "AI 绘画", "手绘动画",
    "方法论", "技术拆解", "实操复盘", "动手实践", "评论区聊聊",
]


def _get_cached_subtitle_patch(subtitle_text: str, fsize: int):
    ckey = ("__SUB_HI__", subtitle_text, fsize)
    if ckey in _PATCH_CACHE:
        return _PATCH_CACHE[ckey]
    eff_fsize = fsize
    s_font = get_font(FONT_SANS_BOLD, eff_fsize)
    dummy = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    sb = dummy.textbbox((0, 0), subtitle_text, font=s_font)
    stw, sth = sb[2] - sb[0], sb[3] - sb[1]
    while stw > 1620 and eff_fsize > 24:
        eff_fsize -= 2
        s_font = get_font(FONT_SANS_BOLD, eff_fsize)
        sb = dummy.textbbox((0, 0), subtitle_text, font=s_font)
        stw, sth = sb[2] - sb[0], sb[3] - sb[1]
    pw, ph = stw + 52, sth + 30
    im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([2, 2, pw - 3, ph - 5], radius=14, fill=(255, 255, 255, 242))

    hit_kw = None
    hit_pos = -1
    for kw in SUBTITLE_KEYWORDS:
        p_idx = subtitle_text.find(kw)
        if p_idx >= 0:
            hit_kw = kw
            hit_pos = p_idx
            break

    x_cursor = 26 - sb[0]
    y_cursor = 11 - sb[1]
    if hit_kw is None:
        d.text((x_cursor, y_cursor), subtitle_text, font=s_font, fill=(*PAL_RGB["sub_ink"], 254))
    else:
        pre = subtitle_text[:hit_pos]
        post = subtitle_text[hit_pos + len(hit_kw):]
        cur = x_cursor
        if pre:
            d.text((cur, y_cursor), pre, font=s_font, fill=(*PAL_RGB["sub_ink"], 254))
            cur += dummy.textlength(pre, font=s_font)
        kw_w = dummy.textlength(hit_kw, font=s_font)
        d.rounded_rectangle([cur - 4, 7, cur + kw_w + 4, ph - 8], radius=7, fill=(*PAL_RGB["soft_mint"], 235))
        d.line([(cur - 2, ph - 9), (cur + kw_w + 2, ph - 9)], fill=(*PAL_RGB["mint"], 255), width=3)
        d.text((cur, y_cursor), hit_kw, font=s_font, fill=(*PAL_RGB["mint_ink"], 255))
        cur += kw_w
        if post:
            d.text((cur, y_cursor), post, font=s_font, fill=(*PAL_RGB["sub_ink"], 254))

    arr = np.array(im, dtype=np.uint8)
    res = (arr[:, :, [2, 1, 0]], (arr[:, :, 3:4].astype(np.float32)) * (1.0 / 255.0))
    _PATCH_CACHE[ckey] = res
    return res


def _blend_patch_inplace(dst_bgr: np.ndarray, patch_bgr_u8: np.ndarray, patch_a: np.ndarray, x0: int, y0: int, alpha_mul: float = 1.0):
    if alpha_mul <= 0.005:
        return
    ph, pw = patch_bgr_u8.shape[:2]
    dh, dw = dst_bgr.shape[:2]
    sx0, sy0 = max(0, -x0), max(0, -y0)
    dx0, dy0 = max(0, x0), max(0, y0)
    w, h = min(pw - sx0, dw - dx0), min(ph - sy0, dh - dy0)
    if w <= 0 or h <= 0:
        return
    roi = dst_bgr[dy0:dy0 + h, dx0:dx0 + w].astype(np.float32)
    pa = patch_a[sy0:sy0 + h, sx0:sx0 + w] * alpha_mul
    pb = patch_bgr_u8[sy0:sy0 + h, sx0:sx0 + w].astype(np.float32)
    dst_bgr[dy0:dy0 + h, dx0:dx0 + w] = (roi + (pb - roi) * pa).astype(np.uint8)


class CleanMintCanvas:
    """Zero-Allocation Native 1920x1080 60fps Renderer."""

    def __init__(self, t: float, cam_cx: float = 960.0, cam_cy: float = 515.0, cam_zoom: float = 1.0, subtitle_size: int = 40, target_img=None, cam_shake_px: float = 0.0):
        self.t = t
        if target_img is not None:
            self.img = target_img
        else:
            _REUSE_BUF.fill(255)
            self.img = _REUSE_BUF
        eff_shk = cam_shake_px if cam_shake_px > 0.0 else (_GLOBAL_SHAKE_PX if target_img is None else 0.0)
        shk_x = math.sin(t * 67.0) * eff_shk if eff_shk > 0.1 else 0.0
        shk_y = math.cos(t * 79.0) * eff_shk * 0.8 if eff_shk > 0.1 else 0.0
        self.cam_cx = cam_cx + shk_x
        self.cam_cy = cam_cy + shk_y
        self.cam_zoom = cam_zoom
        self.subtitle_size = subtitle_size
        self._labels = []

    def world_to_hi(self, pts: np.ndarray) -> np.ndarray:
        out = np.empty_like(pts, dtype=np.float32)
        out[:, 0] = (pts[:, 0] - self.cam_cx) * self.cam_zoom + (W * 0.5)
        out[:, 1] = (pts[:, 1] - self.cam_cy) * self.cam_zoom + (H * 0.5)
        return out

    def wlen(self, px: float) -> int:
        return max(1, int(round(px * self.cam_zoom)))

    def fill_poly(self, pts_world, color_key: str = "white", boil_key: str = "fill", jitter: float = 0.36):
        pts = np.asarray(pts_world, dtype=np.float32)
        if len(pts) < 3:
            return
        if jitter > 0.02:
            jf = soft_boil_floats(f"f:{boil_key}", self.t, len(pts) * 2).reshape(-1, 2)
            pts = pts + jf * jitter
        hi = self.world_to_hi(pts).astype(np.int32)
        cv2.fillPoly(self.img, [hi], PAL_BGR.get(color_key, PAL_BGR["white"]), lineType=cv2.LINE_AA)

    def pen_line(
        self,
        pts_world,
        color_key: str = "ink",
        width: float = 2.0,
        boil_key: str = "pen",
        jitter: float = 0.45,
        progress: float = 1.0,
        closed: bool = False,
        taper: bool = False,
        start_scale: float = 0.72,
        end_scale: float = 0.72,
    ):
        if progress <= 0.005:
            return
        raw = np.asarray(pts_world, dtype=np.float32)
        if closed:
            raw = np.vstack([raw, raw[0:1]])
        n_raw = len(raw)
        if n_raw < 2:
            return

        if n_raw <= 6:
            diffs = raw[1:] - raw[:-1]
            dists = np.hypot(diffs[:, 0], diffs[:, 1])
            if float(np.max(dists)) > 36.0:
                segs = []
                for i in range(n_raw - 1):
                    n_s = max(1, min(8, int(dists[i] / 32.0) + 1))
                    u_v = np.linspace(0.0, 1.0, n_s, endpoint=False, dtype=np.float32)[:, None]
                    segs.append(raw[i] + diffs[i] * u_v)
                segs.append(raw[-1:])
                dense = np.vstack(segs)
            else:
                dense = raw.copy()
        else:
            dense = raw.copy()

        if progress < 0.999:
            dense = dense[: max(2, int(round(len(dense) * clamp(progress))))]
        n_pts = len(dense)
        if n_pts < 2:
            return

        if jitter > 0.02:
            jf = soft_boil_floats(f"p:{boil_key}", self.t, n_pts * 2).reshape(n_pts, 2)
            dense[:, 0] += jf[:, 0] * (jitter * 0.65)
            dense[:, 1] += jf[:, 1] * (jitter * 0.65)

        hi = self.world_to_hi(dense)
        col = PAL_BGR.get(color_key, PAL_BGR["ink"])

        if taper and width >= 2.6 and n_pts >= 5 and not closed:
            tangents = np.empty_like(hi)
            tangents[1:-1] = hi[2:] - hi[:-2]
            tangents[0] = hi[1] - hi[0]
            tangents[-1] = hi[-1] - hi[-2]
            norms = np.hypot(tangents[:, 0], tangents[:, 1])[:, None] + 1e-5
            perp = np.stack([-tangents[:, 1] / norms[:, 0], tangents[:, 0] / norms[:, 0]], axis=1)
            u_s = np.linspace(0.0, 1.0, n_pts, dtype=np.float32)
            prof = (start_scale * (1.0 - u_s) + end_scale * u_s) + 0.38 * np.maximum(0.0, np.sin(u_s * math.pi))
            half_w = (width * self.cam_zoom * 0.5) * prof
            ribbon = np.vstack([hi + perp * half_w[:, None], (hi - perp * half_w[:, None])[::-1]]).astype(np.int32)
            cv2.fillPoly(self.img, [ribbon], col, lineType=cv2.LINE_AA)
        else:
            cv2.polylines(self.img, [hi.astype(np.int32)], False, col, thickness=self.wlen(width), lineType=cv2.LINE_AA)

    def dashed_line(self, p0, p1, dash_len: float = 10.0, gap_len: float = 7.0, color_key: str = "ink_detail", width: float = 1.6, boil_key: str = "dash"):
        x0, y0 = p0
        x1, y1 = p1
        dist = math.hypot(x1 - x0, y1 - y0)
        if dist < 2.0:
            return
        ux, uy = (x1 - x0) / dist, (y1 - y0) / dist
        cur = 0.0
        idx = 0
        while cur < dist:
            end_d = min(dist, cur + dash_len)
            self.pen_line(
                [(x0 + ux * cur, y0 + uy * cur), (x0 + ux * end_d, y0 + uy * end_d)],
                color_key=color_key, width=width, boil_key=f"{boil_key}_{idx}", jitter=0.18, taper=False
            )
            cur += dash_len + gap_len
            idx += 1

    def white_box(self, x: float, y: float, w: float, h: float, width: float = 2.0, fill_key: str = "white", ink_key: str = "ink", boil_key: str = "box", progress: float = 1.0, rot_deg: float = 0.0, corner_r: float = 4.5):
        if w <= 1.0 or h <= 1.0:
            return
        pts = rounded_rect_pts(x, y, w, h, r=corner_r, rot_deg=rot_deg)
        if fill_key and progress > 0.12:
            self.fill_poly(pts, fill_key, boil_key=boil_key)
        if ink_key:
            self.pen_line(pts, color_key=ink_key, width=width, boil_key=boil_key, progress=progress, closed=True)

    def white_ellipse(self, cx: float, cy: float, rx: float, ry: float, n: int = 28, rot_deg: float = 0.0, fill_key: str = "white", ink_key: str = "ink", width: float = 2.0, boil_key: str = "ell", progress: float = 1.0):
        if rx <= 0.5 or ry <= 0.5:
            return
        ang = np.linspace(0, 2 * math.pi, n, endpoint=False, dtype=np.float32)
        pts = np.stack([np.cos(ang) * rx, np.sin(ang) * ry], axis=1)
        if abs(rot_deg) > 1e-3:
            r = math.radians(rot_deg)
            c, s = math.cos(r), math.sin(r)
            pts = np.stack([pts[:, 0] * c - pts[:, 1] * s, pts[:, 0] * s + pts[:, 1] * c], axis=1)
        pts[:, 0] += cx
        pts[:, 1] += cy
        if fill_key and progress > 0.12:
            self.fill_poly(pts, fill_key, boil_key=boil_key)
        if ink_key:
            self.pen_line(pts, color_key=ink_key, width=width, boil_key=boil_key, progress=progress, closed=True)

    def flow_arrow(self, p0, p1, arch_h: float = -28.0, color_key: str = "mint_ink", width: float = 3.0, boil_key: str = "arr", progress: float = 1.0):
        if progress <= 0.01:
            return
        x0, y0 = p0
        x1, y1 = p1
        mx, my = (x0 + x1) * 0.5, (y0 + y1) * 0.5 + arch_h
        curve = quad_bezier((x0, y0), (mx, my), (x1, y1), n=18)
        self.pen_line(curve, color_key=color_key, width=width, boil_key=boil_key, progress=progress, taper=True)
        if progress > 0.78:
            hp = clamp((progress - 0.78) / 0.22)
            tx, ty = curve[-1]
            ang = math.atan2(ty - curve[-3][1], tx - curve[-3][0])
            alen = 17.0 * back_out(hp)
            self.pen_line([[tx - alen * math.cos(ang - 0.52), ty - alen * math.sin(ang - 0.52)], [tx, ty], [tx - alen * math.cos(ang + 0.52), ty - alen * math.sin(ang + 0.52)]], color_key=color_key, width=width * 0.9, boil_key=boil_key + "_h")

    def dust_puff(self, x: float, y: float, u_prog: float, dir_x: float = 1.0, color_key: str = "ink_detail", key: str = "dust"):
        if not (0.01 < u_prog < 0.99):
            return
        grow = ease_out(u_prog)
        shrink = 1.0 - ease_in(clamp((u_prog - 0.45) / 0.55))
        for i in range(2):
            r = (11.0 - i * 3.0) * shrink
            if r > 1.8:
                self.white_ellipse(x + dir_x * (14.0 + i * 18.0) * grow, y - (6.0 + i * 9.0) * grow, r * 1.25, r * 0.85, n=16, width=1.5, ink_key=color_key, boil_key=f"{key}_{i}")

    def smear_arc(self, cx: float, cy: float, rx: float, ry: float, deg0: float, deg1: float, color_key: str = "mint", width: float = 3.0, key: str = "smear"):
        angs = np.linspace(math.radians(deg0), math.radians(deg1), 14, dtype=np.float32)
        pts = np.stack([cx + np.cos(angs) * rx, cy + np.sin(angs) * ry], axis=1)
        self.pen_line(pts, color_key=color_key, width=width, boil_key=key, jitter=0.2, taper=True, start_scale=0.15, end_scale=0.20)

    def impact_burst(self, cx: float, cy: float, r0: float, r1: float, u_prog: float, n_rays: int = 8, color_key: str = "mint", key: str = "burst"):
        if not (0.01 < u_prog < 0.99):
            return
        k = ease_out(u_prog)
        fade = 1.0 - seg(u_prog, 0.55, 1.0)
        for i in range(n_rays):
            a = (i / n_rays) * math.pi * 2.0 + 0.32
            ra, rb = lerp(r0, r1, k * 0.55), lerp(r0 + 9.0, r1 + 18.0, k)
            if rb - ra > 2.0 and fade > 0.12:
                self.pen_line([(cx + math.cos(a) * ra, cy + math.sin(a) * ra), (cx + math.cos(a) * rb, cy + math.sin(a) * rb)], color_key=color_key, width=2.2 * fade + 0.6, boil_key=f"{key}_{i}", jitter=0.15)

    def mint_particle_ring(self, cx: float, cy: float, u_prog: float, max_r: float = 54.0, n_dots: int = 8, key: str = "mring"):
        if not (0.01 < u_prog < 0.99):
            return
        k = ease_out(u_prog)
        fade = 1.0 - seg(u_prog, 0.50, 1.0)
        rad = max_r * k
        dr = max(1.6, 5.2 * fade)
        for i in range(n_dots):
            a = (i / n_dots) * math.pi * 2.0 + u_prog * 0.6
            self.white_ellipse(cx + math.cos(a) * rad, cy + math.sin(a) * rad * 0.65, dr, dr, n=12, fill_key="mint", ink_key="mint_ink", width=1.2, boil_key=f"{key}_{i}")

    def ambient_motes(self, count: int = 7, seed_key: str = "motes"):
        base_seed = det_hash_int(seed_key)
        for i in range(count):
            h_i = det_hash_int(f"{seed_key}:{i}:{base_seed}")
            ox = ((h_i % 1460) - 730.0) + math.sin(self.t * 0.65 + i * 1.7) * 34.0
            oy = (((h_i // 1469) % 540) - 310.0) + math.cos(self.t * 0.52 + i * 2.1) * 24.0
            r_m = 3.6 if i % 2 == 0 else 2.4
            self.white_ellipse(self.cam_cx + ox, self.cam_cy + oy, r_m, r_m, n=10, fill_key="mint" if i % 2 == 0 else "ink_soft", ink_key=None, boil_key=f"{seed_key}_{i}")

    def draw_translucent_layer(self, opacity: float, draw_fn):
        op = clamp(opacity)
        if op <= 0.02:
            return
        if op >= 0.98:
            draw_fn(self)
            return
        _TEMP_LAYER_BUF.fill(255)
        sub = CleanMintCanvas(self.t, self.cam_cx, self.cam_cy, self.cam_zoom, self.subtitle_size, target_img=_TEMP_LAYER_BUF)
        draw_fn(sub)
        gray = cv2.cvtColor(_TEMP_LAYER_BUF, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 252, 255, cv2.THRESH_BINARY_INV)
        blended = cv2.addWeighted(self.img, 1.0 - op, _TEMP_LAYER_BUF, op, 0.0)
        cv2.copyTo(blended, mask, self.img)
        for lbl in sub._labels:
            self._labels.append((*lbl[:6], lbl[6] * op, *lbl[7:]))

    def hand_label(self, text: str, x: float, y: float, size: int = 34, color_key: str = "ink", align: str = "center", alpha: float = 1.0, slant_deg: float = -1.2, organic: bool = True, pop_y: float = 0.0, bold: bool = False):
        if alpha <= 0.01 or not text:
            return
        self._labels.append((text, x, y + pop_y, size, color_key, align, clamp(alpha), slant_deg, organic, bold))

    def finalize(self, subtitle_text: str = "", sub_alpha: float = 0.0, sub_rise_px: float = 0.0, white_fade: float = 0.0, hud_chapter: str = "", film_progress: float = -1.0, global_xeron_wm: bool = False) -> np.ndarray:
        frame_bgr = self.img

        for (text, wx, wy, size, color_key, align, alpha, slant_deg, organic, bold) in self._labels:
            sx = (wx - self.cam_cx) * self.cam_zoom + (W * 0.5)
            sy = (wy - self.cam_cy) * self.cam_zoom + (H * 0.5)
            if sx < -420 or sx > W + 420 or sy < -200 or sy > H + 200:
                continue
            fsize = max(12, int(round(size * self.cam_zoom)))
            pbgr, pa = _get_cached_label_patch(text, fsize, color_key, slant_deg, organic, bold=bold)
            ph, pw = pbgr.shape[:2]
            bj = soft_boil_floats(f"lbl:{text}", self.t, 2) if organic else (0.0, 0.0)
            jx = float(bj[0]) * 0.45 if organic else 0.0
            jy = float(bj[1]) * 0.45 if organic else 0.0
            x0 = int(round((sx - pw * 0.5 if align == "center" else (sx - pw if align == "right" else sx)) + jx))
            y0 = int(round(sy - ph * 0.5 + jy))
            _blend_patch_inplace(frame_bgr, pbgr, pa, x0, y0, alpha_mul=alpha)

        if hud_chapter:
            hbgr, ha = _get_cached_label_patch(hud_chapter, 22, "ink_detail", 0.0, False, bold=True)
            _blend_patch_inplace(frame_bgr, hbgr, ha, 54, 42 - hbgr.shape[0] // 2, alpha_mul=0.88)

        if global_xeron_wm:
            wm_pulse = 0.5 + 0.5 * math.sin(self.t * 2.4)
            wm_alpha = clamp(0.15 + white_fade * 0.28 + wm_pulse * 0.03, 0.12, 0.48)
            wbgr, wa = _get_cached_label_patch("Xeron", 28, "mint_ink" if white_fade > 0.08 else "ink", -6.5, True, bold=False)
            _blend_patch_inplace(frame_bgr, wbgr, wa, W - wbgr.shape[1] - 34, H - wbgr.shape[0] - 22, alpha_mul=wm_alpha)

        if subtitle_text and sub_alpha > 0.01:
            sbgr, sa = _get_cached_subtitle_patch(subtitle_text, self.subtitle_size)
            sh_p, sw_p = sbgr.shape[:2]
            stx = (W - sw_p) // 2
            sty = int(round(964 + sub_rise_px))
            _blend_patch_inplace(frame_bgr, sbgr, sa, stx, sty, alpha_mul=sub_alpha)

        if white_fade > 0.005:
            wf = clamp(white_fade)
            cv2.addWeighted(frame_bgr, 1.0 - wf, _WHITE_BUF, wf, 0.0, dst=frame_bgr)
        return frame_bgr


# =============================================================================
# STUDIO STEREO LO-FI CHILLHOP BGM SYNTHESIZER (`Karplus-Strong Guitar + Rhodes + Boom-Bap`)
# =============================================================================
@functools.lru_cache(maxsize=256)
def _karplus_strong_pluck(freq_hz: float, dur_s: float, sr: int = 24000, brightness: float = 0.65) -> np.ndarray:
    n_tot = int(dur_s * sr)
    delay = max(4, int(round(sr / max(35.0, freq_hz))))
    rng = np.random.default_rng(int(round(freq_hz * 100)))
    burst = rng.uniform(-1.0, 1.0, size=delay).astype(np.float64)
    b_lp, a_lp = signal.butter(2, clamp(brightness, 0.15, 0.90), btype="low")
    burst = signal.lfilter(b_lp, a_lp, burst)
    burst -= np.mean(burst)

    x = np.zeros(n_tot, dtype=np.float64)
    x[:delay] = burst
    decay_g = 0.9935
    stretch_s = 0.42
    a_poly = np.zeros(delay + 2, dtype=np.float64)
    a_poly[0] = 1.0
    a_poly[delay] = -decay_g * (1.0 - stretch_s)
    a_poly[delay + 1] = -decay_g * stretch_s
    y = signal.lfilter([1.0], a_poly, x).astype(np.float32)
    fade_n = min(int(0.08 * sr), n_tot)
    if fade_n > 0:
        y[-fade_n:] *= np.linspace(1.0, 0.0, fade_n, dtype=np.float32)
    mx = float(np.max(np.abs(y))) + 1e-6
    return (y / mx)


def synth_studio_lofi_bgm(total_dur_s: float, shot_configs: list, sr: int = 24000) -> tuple[np.ndarray, np.ndarray]:
    n_samples = int(total_dur_s * sr) + sr * 2
    bgm_L = np.zeros(n_samples, dtype=np.float32)
    bgm_R = np.zeros(n_samples, dtype=np.float32)

    PROGRESSION = [
        (87.31,  [174.61, 220.00, 261.63, 329.63, 392.00], [174.61, 261.63, 329.63, 392.00, 523.25, 392.00, 329.63, 261.63], [659.25, 783.99, 880.00, 783.99]),
        (82.41,  [164.81, 196.00, 246.94, 293.66, 392.00], [164.81, 246.94, 293.66, 392.00, 493.88, 392.00, 293.66, 246.94], [587.33, 659.25, 783.99, 659.25]),
        (73.42,  [146.83, 174.61, 220.00, 261.63, 329.63], [146.83, 220.00, 261.63, 329.63, 440.00, 329.63, 261.63, 220.00], [523.25, 659.25, 880.00, 659.25]),
        (98.00,  [196.00, 261.63, 293.66, 329.63, 440.00], [196.00, 261.63, 329.63, 440.00, 523.25, 440.00, 329.63, 293.66], [880.00, 783.99, 659.25, 587.33]),
    ]

    bar_s = BEAT_S * 4.0
    eighth_s = BEAT_S * 0.5
    n_bars = int(math.ceil(total_dur_s / bar_s))
    rng = np.random.default_rng(2026)

    is_short_clip = total_dur_s <= 25.0
    ch1_drop = 0.0 if is_short_clip else (shot_configs[0]["t0"] + shot_configs[0]["dur"] * 0.70 if len(shot_configs) >= 1 else 0.0)
    ch3_start = 0.0 if is_short_clip else (shot_configs[2]["t0"] if len(shot_configs) >= 3 else 40.0)
    ch6_start = total_dur_s * 0.55 if is_short_clip else (shot_configs[5]["t0"] if len(shot_configs) >= 6 else 115.0)
    ch8_start = total_dur_s + 10.0 if is_short_clip else (shot_configs[7]["t0"] if len(shot_configs) >= 8 else 170.0)

    t_k = np.arange(int(0.22 * sr), dtype=np.float32) / sr
    kick_wave = 0.52 * np.sin(2 * math.pi * (48.0 + 95.0 * np.exp(-t_k * 36.0)) * t_k) * np.exp(-t_k * 13.5)

    t_s = np.arange(int(0.14 * sr), dtype=np.float32) / sr
    rim_noise = signal.lfilter(*signal.butter(2, [0.08, 0.42], btype="band"), rng.normal(0, 1, len(t_s))).astype(np.float32)
    snare_wave = (0.24 * np.sin(2 * math.pi * 215.0 * t_s) * np.exp(-t_s * 38.0) + 0.22 * rim_noise * np.exp(-t_s * 26.0)).astype(np.float32)

    t_h = np.arange(int(0.055 * sr), dtype=np.float32) / sr
    hat_noise = signal.lfilter(*signal.butter(2, 0.45, btype="high"), rng.normal(0, 1, len(t_h))).astype(np.float32)
    hat_wave = (0.085 * hat_noise * np.exp(-t_h * 58.0)).astype(np.float32)

    def _add_mono(t_on: float, wv: np.ndarray, gain_l: float, gain_r: float):
        i0 = int(t_on * sr)
        if i0 < 0 or i0 >= n_samples:
            return
        i1 = min(n_samples, i0 + len(wv))
        seg_w = wv[: i1 - i0]
        bgm_L[i0:i1] += seg_w * gain_l
        bgm_R[i0:i1] += seg_w * gain_r

    for b in range(n_bars):
        bt0 = b * bar_s
        if bt0 >= total_dur_s:
            break
        bass_f, rhodes_fs, arp_fs, bell_fs = PROGRESSION[b % len(PROGRESSION)]

        is_intro = bt0 < ch1_drop
        is_intimate = (ch1_drop <= bt0 < ch3_start) or (bt0 >= ch8_start)
        is_climax = (ch6_start <= bt0 < ch8_start)

        i0, i1 = int(bt0 * sr), min(n_samples, int((bt0 + bar_s * 1.04) * sr))
        lt = np.arange(i1 - i0, dtype=np.float32) / sr
        env_r = np.exp(-lt * 0.92) * (1.0 - np.exp(-lt * 55.0))
        chord_sum = np.zeros_like(lt)
        for fi, cf in enumerate(rhodes_fs):
            tine = 0.05 * np.sin(2 * math.pi * (cf * 6.0) * lt) * np.exp(-lt * 16.0) if fi >= 2 else 0.0
            chord_sum += (0.16 * np.sin(2 * math.pi * cf * lt) + 0.035 * np.sin(4 * math.pi * cf * lt) * np.exp(-lt * 3.0) + tine)
        trem_l = 0.78 + 0.22 * np.sin(2 * math.pi * 3.2 * lt)
        trem_r = 0.78 + 0.22 * np.cos(2 * math.pi * 3.2 * lt)
        r_gain = 0.42 if not is_intro else 0.24
        bgm_L[i0:i1] += chord_sum * env_r * trem_l * r_gain
        bgm_R[i0:i1] += chord_sum * env_r * trem_r * r_gain

        if not is_intro:
            for ei, gf in enumerate(arp_fs):
                swing = 0.032 if (ei % 2 == 1) else 0.0
                gt = bt0 + ei * eighth_s + swing
                pluck = _karplus_strong_pluck(gf, 1.35, sr=sr, brightness=0.62 if is_intimate else 0.72)
                vel = 0.26 if ei in (0, 3, 6) else 0.19
                pan_r = 0.35 + 0.35 * (ei / 7.0)
                _add_mono(gt, pluck, vel * (1.0 - pan_r * 0.45), vel * (0.55 + pan_r * 0.45))

        for bo, bdur, bmul in ((0.0, BEAT_S * 1.9, 1.0), (BEAT_S * 2.5, BEAT_S * 1.1, 1.0), (BEAT_S * 3.5, BEAT_S * 0.5, 1.5)):
            bi0 = int((bt0 + bo) * sr)
            bi1 = min(n_samples, int((bt0 + bo + bdur) * sr))
            if bi0 < bi1:
                blt = np.arange(bi1 - bi0, dtype=np.float32) / sr
                bf = bass_f * (1.122 if bmul > 1.2 else 1.0)
                b_env = np.exp(-blt * 2.2) * (1.0 - np.exp(-blt * 65.0))
                bwv = (0.30 * np.sin(2 * math.pi * bf * blt) + 0.10 * np.sin(4 * math.pi * bf * blt) * np.exp(-blt * 5.0)) * b_env
                bgm_L[bi0:bi1] += bwv * 0.65
                bgm_R[bi0:bi1] += bwv * 0.65

        if not is_intimate:
            for k_off in (0.0, BEAT_S * 1.53, BEAT_S * 2.0):
                _add_mono(bt0 + k_off, kick_wave, 0.72, 0.72)
            if not is_intro:
                for s_off in (BEAT_S * 1.0, BEAT_S * 3.0):
                    _add_mono(bt0 + s_off, snare_wave, 0.62, 0.68)
        for hi_i in range(8):
            sw_h = 0.030 if (hi_i % 2 == 1) else 0.0
            hg = 0.55 if not is_intimate else 0.28
            _add_mono(bt0 + hi_i * eighth_s + sw_h, hat_wave, hg * 0.85, hg * 1.05)

        if is_climax:
            for m_i, mf in enumerate(bell_fs):
                mt = bt0 + m_i * BEAT_S + (0.25 * BEAT_S if m_i == 2 else 0.0)
                mi0 = int(mt * sr)
                mi1 = min(n_samples, mi0 + int(0.85 * sr))
                if mi0 < mi1:
                    mlt = np.arange(mi1 - mi0, dtype=np.float32) / sr
                    bell = (0.14 * np.sin(2 * math.pi * mf * mlt) + 0.05 * np.sin(2 * math.pi * (mf * 2.0) * mlt) * np.exp(-mlt * 9.0)) * np.exp(-mlt * 3.4) * (1.0 - np.exp(-mlt * 90.0))
                    bgm_L[mi0:mi1] += bell * (0.75 if m_i % 2 == 0 else 0.45)
                    bgm_R[mi0:mi1] += bell * (0.45 if m_i % 2 == 0 else 0.75)

    d1, d2 = int(0.038 * sr), int(0.061 * sr)
    rev_L = np.zeros_like(bgm_L)
    rev_R = np.zeros_like(bgm_R)
    rev_L[d1:] += bgm_R[:-d1] * 0.18
    rev_R[d2:] += bgm_L[:-d2] * 0.18
    bgm_L = bgm_L + rev_L
    bgm_R = bgm_R + rev_R

    b_lp, a_lp = signal.butter(2, 7500.0 / (sr * 0.5), btype="low")
    bgm_L = signal.lfilter(b_lp, a_lp, bgm_L).astype(np.float32)
    bgm_R = signal.lfilter(b_lp, a_lp, bgm_R).astype(np.float32)
    return bgm_L, bgm_R


import re as _re


def _align_subs_viterbi(seg_wav: AudioSegment, subs: list, sp0_abs: float) -> list:
    """Exact acoustic pause-valley Viterbi DP alignment on clean mono TTS waveform."""
    if not subs:
        return []
    mono = seg_wav.set_channels(1).set_frame_rate(24000)
    samples = np.array(mono.get_array_of_samples(), dtype=np.float32) / 32768.0
    sr, hop = 24000, 240
    n_f = len(samples) // hop
    if n_f < 10 or len(subs) == 1:
        return [(sp0_abs, sp0_abs + len(seg_wav) / 1000.0, subs[0][0] if isinstance(subs[0], tuple) else subs[0])]

    rms = np.sqrt(np.mean(samples[:n_f * hop].reshape(n_f, hop) ** 2, axis=1) + 1e-10)
    peak_rms = float(np.max(rms))
    silent = rms <= (peak_rms * 0.042)
    act_idx = np.where(~silent)[0]
    if len(act_idx) < 4:
        return [(sp0_abs, sp0_abs + len(seg_wav) / 1000.0, subs[0][0] if isinstance(subs[0], tuple) else subs[0])]

    i_first, i_last = int(act_idx[0]), int(act_idx[-1])
    sp_cum = np.cumsum((~silent).astype(np.float64))
    total_sp_frames = max(1.0, sp_cum[i_last] - sp_cum[i_first])

    cands = []
    in_s, s0 = False, 0
    for i in range(i_first + 8, i_last - 8):
        if silent[i] and not in_s:
            in_s, s0 = True, i
        elif not silent[i] and in_s:
            in_s = False
            if (i - s0) >= 3:
                cands.append((s0, i, (i - s0) * 0.01))

    norm_specs = [(s if isinstance(s, tuple) else (s, "comma")) for s in subs]
    M = len(norm_specs)
    weights = np.array([
        max(1.0, len(_re.findall(r"[\u4e00-\u9fff]", st)) * 1.0 + len(_re.findall(r"[A-Za-z0-9]+", st)) * 1.55)
        for st, _ in norm_specs
    ], dtype=np.float64)
    exp_sp_frames = total_sp_frames * (weights / np.sum(weights))

    nodes = [(i_first, i_first, 0.0)] + cands + [(i_last, i_last, 0.0)]
    N_nodes = len(nodes)
    INF = 1e18
    dp = np.full((M + 1, N_nodes), INF, dtype=np.float64)
    parent = np.full((M + 1, N_nodes), -1, dtype=np.int32)
    dp[0, 0] = 0.0

    for m in range(1, M + 1):
        exp_f = exp_sp_frames[m - 1]
        btype = norm_specs[m - 1][1]
        j_range = [N_nodes - 1] if m == M else range(1, N_nodes - 1)
        cum_exp = float(np.sum(exp_sp_frames[:m]))
        for j in j_range:
            j_s0, _, pdur = nodes[j]
            pause_bonus = 0.0
            if m < M:
                pause_bonus = (-min(0.65, pdur) * 2.8 + (1.2 if pdur < 0.16 else 0.0)) if btype == "strong" else (-min(0.30, pdur) * 1.4)
            cum_act = sp_cum[j_s0] - sp_cum[i_first]
            cum_err = (cum_act - cum_exp) / max(50.0, total_sp_frames * 0.08)
            for prev_j in range(0, j):
                if dp[m - 1, prev_j] >= INF * 0.5:
                    continue
                act_f = sp_cum[j_s0] - sp_cum[nodes[prev_j][1]]
                if act_f < max(14.0, exp_f * 0.38):
                    continue
                rel_err = (act_f - exp_f) / max(32.0, exp_f)
                cost = dp[m - 1, prev_j] + (rel_err ** 2) * 4.5 + (cum_err ** 2) * 1.6 + pause_bonus
                if cost < dp[m, j]:
                    dp[m, j] = cost
                    parent[m, j] = prev_j

    if dp[M, N_nodes - 1] >= INF * 0.5:
        tc = sp0_abs + i_first * 0.01
        rem = (i_last - i_first) * 0.01
        out_fb = []
        for (st, _), w in zip(norm_specs, weights / np.sum(weights)):
            dt = rem * float(w)
            out_fb.append((tc, tc + dt - 0.02, st))
            tc += dt
        return out_fb

    chosen = [0] * (M + 1)
    cur = N_nodes - 1
    for m in range(M, 0, -1):
        chosen[m] = cur
        cur = int(parent[m, cur])

    wins_rel = []
    dur_wav_s = len(samples) / sr
    for m in range(1, M + 1):
        p_prev = nodes[chosen[m - 1]]
        p_curr = nodes[chosen[m]]
        w0 = max(0.0, p_prev[1] * 0.01 - 0.02)
        w1 = min(dur_wav_s, p_curr[0] * 0.01 + 0.04)
        if wins_rel and w0 <= wins_rel[-1][1] + 0.01:
            mid = 0.5 * (wins_rel[-1][1] + w0)
            wins_rel[-1] = (wins_rel[-1][0], mid - 0.01, wins_rel[-1][2])
            w0 = mid + 0.01
        wins_rel.append((w0, max(w0 + 0.25, w1), norm_specs[m - 1][0]))
    return [(sp0_abs + a, sp0_abs + b, s) for a, b, s in wins_rel]




def _expected_spoken_syllables(text: str) -> float:
    """Counts Mandarin characters + spoken English acronym letters / syllables / digits."""
    n_zh = len(_re.findall(r"[\u4e00-\u9fff]", text))
    n_en = 0.0
    for tok in _re.findall(r"[A-Za-z]+|\d+(?:\.\d+)?", text):
        if tok.isupper() and len(tok) <= 5:
            n_en += len(tok)
        elif tok[0].isdigit():
            n_en += len(tok)
        else:
            v = len(_re.findall(r"[aeiouyAEIOUY]+", tok.rstrip("eE") or tok))
            n_en += max(1, v)
    return max(1.0, float(n_zh) + n_en)


def align_subs_on_raw_vowel_peaks(raw_seg: AudioSegment, subs: list) -> list:
    """
    Zero-drift acoustic alignment on UNTRIMMED raw TTS audio BEFORE breath-trimming!
    Combines 280-3200 Hz vowel syllable-nucleus peak counting with raw TTS punctuation pause priors
    (`>= 720ms` for sentence periods/semicolons, `>= 320ms` for commas).
    Returns list of `(raw_start_s, raw_end_s, raw_pause_after_s, text)`.
    """
    if not subs:
        return []
    mono = raw_seg.set_channels(1).set_frame_rate(24000)
    x = np.array(mono.get_array_of_samples(), dtype=np.float32) / 32768.0
    sr, hop = 24000, 240
    n_f = len(x) // hop
    norm = [(s if isinstance(s, (tuple, list)) else (s, "comma")) for s in subs]
    if n_f < 12 or len(norm) == 1:
        return [(0.0, len(raw_seg) / 1000.0, 0.0, norm[0][0])]

    b, a = signal.butter(3, [280.0 / (sr * 0.5), 3200.0 / (sr * 0.5)], btype="band")
    xf = signal.filtfilt(b, a, x)
    rms_full = np.sqrt(np.mean(x[:n_f * hop].reshape(n_f, hop) ** 2, axis=1) + 1e-12)
    rms_vow = np.sqrt(np.mean(xf[:n_f * hop].reshape(n_f, hop) ** 2, axis=1) + 1e-12)
    rms_db = 20.0 * np.log10(rms_full + 1e-9)

    win_g = signal.windows.gaussian(9, std=2.2)
    win_g /= np.sum(win_g)
    env_s = np.convolve(rms_vow, win_g, mode="same")
    voiced = rms_db > -38.0
    pk_th = float(np.percentile(env_s[voiced], 22)) * 0.55 if np.any(voiced) else 0.01
    peaks, _ = signal.find_peaks(env_s, height=pk_th, distance=11, prominence=pk_th * 0.32)

    syl_cum = np.zeros(n_f + 1, dtype=np.float64)
    for p in peaks:
        syl_cum[p + 1:] += 1.0
    tot_peaks = max(1.0, syl_cum[-1])

    silent = rms_db < -39.5
    act_idx = np.where(~silent)[0]
    if len(act_idx) < 4:
        return [(0.0, len(raw_seg) / 1000.0, 0.0, norm[0][0])]
    i_first, i_last = int(act_idx[0]), int(act_idx[-1]) + 1

    cands = []
    cur = i_first + 6
    while cur < i_last - 6:
        if silent[cur]:
            nxt = cur
            while nxt < i_last and silent[nxt]:
                nxt += 1
            dur_s = (nxt - cur) * 0.01
            if dur_s >= 0.14:
                cands.append((cur, nxt, dur_s))
            cur = nxt
        else:
            cur += 1

    M = len(norm)
    exp_raw = np.array([_expected_spoken_syllables(s[0]) for s in norm], dtype=np.float64)
    exp_syls = exp_raw * (tot_peaks / np.sum(exp_raw))

    nodes = [(i_first, i_first, 0.0)] + cands + [(i_last, i_last, 0.0)]
    N = len(nodes)
    INF = 1e18
    dp = np.full((M + 1, N), INF, dtype=np.float64)
    par = np.full((M + 1, N), -1, dtype=np.int32)
    dp[0, 0] = 0.0

    for m in range(1, M + 1):
        es = exp_syls[m - 1]
        btype = norm[m - 1][1]
        cum_es = float(np.sum(exp_syls[:m]))
        j_range = [N - 1] if m == M else range(1, N - 1)
        for j in j_range:
            j_s0, _, pdur = nodes[j]
            p_cost = 0.0
            if m < M:
                if btype == "strong":
                    p_cost = (-8.0 - min(0.5, pdur - 0.72) * 3.0) if pdur >= 0.72 else (-2.0 if pdur >= 0.55 else 6.0)
                else:
                    p_cost = (-3.6 - min(0.45, pdur - 0.35) * 2.0) if pdur >= 0.35 else (-1.2 if pdur >= 0.22 else 3.5)

            cum_act = syl_cum[j_s0] - syl_cum[i_first]
            cum_err = (cum_act - cum_es) / max(3.2, tot_peaks * 0.05)

            for pj in range(0, j):
                if dp[m - 1, pj] >= INF * 0.5:
                    continue
                act_s = syl_cum[j_s0] - syl_cum[nodes[pj][1]]
                if act_s < max(2.0, es * 0.52) or act_s > max(es * 1.58, es + 6.0):
                    continue
                syl_err = (act_s - es) / max(2.0, es * 0.22)
                cost = dp[m - 1, pj] + (syl_err ** 2) * 3.2 + (cum_err ** 2) * 2.0 + p_cost
                if cost < dp[m, j]:
                    dp[m, j] = cost
                    par[m, j] = pj

    if dp[M, N - 1] >= INF * 0.5:
        wins_fb = _align_subs_viterbi(raw_seg, subs, 0.0)
        return [(a, b, 0.0, s) for a, b, s in wins_fb]

    chosen = [0] * (M + 1)
    cur = N - 1
    for m in range(M, 0, -1):
        chosen[m] = cur
        cur = int(par[m, cur])

    out = []
    for m in range(1, M + 1):
        n0, n1 = nodes[chosen[m - 1]], nodes[chosen[m]]
        out.append((n0[1] * 0.01, n1[0] * 0.01, n1[2], norm[m - 1][0]))
    return out


def breath_trim_with_timemap(raw_seg: AudioSegment, atempo: float = 1.05, thresh_db: float = -39.5, comma_ms: int = 175, period_ms: int = 235):
    """
    Trims bloated >230ms/>420ms TTS pauses to natural human breaths (`175ms` comma, `235ms` period)
    AND returns `(trimmed_1x_seg, map_raw_s_to_nat_s)` with sample-accurate piecewise-linear mapping!
    """
    sr = raw_seg.frame_rate
    mono = raw_seg.set_channels(1)
    arr = np.array(mono.get_array_of_samples(), dtype=np.float32)
    step = int(sr * 0.01)
    n_f = len(arr) // step
    rms_db = np.full(n_f, -90.0, dtype=np.float32)
    for i in range(n_f):
        chunk = arr[i * step:(i + 1) * step]
        r = float(np.sqrt(np.mean(chunk * chunk) + 1e-9))
        rms_db[i] = 20.0 * np.log10(r / 32768.0 + 1e-9)

    is_sil = rms_db < thresh_db
    non_sil = np.where(~is_sil)[0]
    i0 = max(0, int(non_sil[0]) - 4)
    i1 = min(n_f, int(non_sil[-1]) + 8)

    raw_knots = [0.0, i0 * 10.0]
    nat_knots = [0.0, 0.0]
    res = None
    cur = i0
    nat_cursor_ms = 0.0
    while cur < i1:
        if not is_sil[cur]:
            nxt = cur
            while nxt < i1 and not is_sil[nxt]:
                nxt += 1
            seg_c = mono[cur * 10:nxt * 10]
        else:
            nxt = cur
            while nxt < i1 and is_sil[nxt]:
                nxt += 1
            sil_ms = (nxt - cur) * 10
            keep_ms = period_ms if sil_ms > 420 else (comma_ms if sil_ms > 230 else sil_ms)
            seg_c = mono[cur * 10:cur * 10 + keep_ms]

        if res is None:
            res = seg_c
            added_ms = float(len(seg_c))
        else:
            cf = min(14, len(res) // 4, len(seg_c) // 4)
            if cf >= 2:
                res = res.append(seg_c, crossfade=cf)
                added_ms = float(len(seg_c) - cf)
            else:
                res = res + seg_c
                added_ms = float(len(seg_c))

        nat_cursor_ms += added_ms
        raw_knots.append(nxt * 10.0)
        nat_knots.append(nat_cursor_ms)
        cur = nxt

    raw_knots.append(float(len(mono)))
    nat_knots.append(nat_cursor_ms)
    rk = np.array(raw_knots, dtype=np.float64) / 1000.0
    nk = np.array(nat_knots, dtype=np.float64) / (1000.0 * atempo)

    def map_fn(t_raw_s: float) -> float:
        return float(np.interp(t_raw_s, rk, nk))

    return res, map_fn


def align_and_trim_natural_vo(raw_wav_path: Path, out_nat_wav_path: Path, subs: list, atempo: float = 1.05) -> list:
    """
    One-call helper:
    1) Aligns `subs` on untrimmed `raw_wav_path` via `align_subs_on_raw_vowel_peaks`.
    2) Breath-trims + applies FFmpeg `atempo` into `out_nat_wav_path` (~4.8 chars/sec natural cadence).
    3) Maps exact `(raw_w0, raw_w1)` into relative natural audio windows `[(rel_w0, rel_w1, text), ...]`.
    """
    raw = AudioSegment.from_wav(str(raw_wav_path))
    raw_spans = align_subs_on_raw_vowel_peaks(raw, subs)
    nat_1x, map_fn = breath_trim_with_timemap(raw, atempo=atempo)
    tmp_1x = out_nat_wav_path.with_name(out_nat_wav_path.stem + "_tmp1x.wav")
    nat_1x.export(str(tmp_1x), format="wav")
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(tmp_1x), "-filter:a", f"atempo={atempo:.3f}",
        "-ar", "24000", "-ac", "1", str(out_nat_wav_path),
    ], check=True)
    tmp_1x.unlink(missing_ok=True)
    return [(map_fn(r0), map_fn(r1), stxt) for (r0, r1, _, stxt) in raw_spans]


def mix_stereo_master(
    shot_configs: list,
    wav_dir: Path,
    out_wav: Path,
    foley_cues=None,
    tick_solo_windows=None,
    compute_only_meta: bool = False,
    lead_first_ms: int = 550,
    tail_last_ms: int = 3400,
):
    cursor_ms = 0
    vo_segments = []
    for idx, sh in enumerate(shot_configs):
        seg_wav = AudioSegment.from_wav(str(wav_dir / sh["wav"]))
        if seg_wav.dBFS != float("-inf"):
            seg_wav = seg_wav.apply_gain(-14.8 - seg_wav.dBFS)
        lead_ms = lead_first_ms if idx == 0 else 420
        tail_ms = tail_last_ms if idx == len(shot_configs) - 1 else 520
        total_ms = lead_ms + len(seg_wav) + tail_ms
        sh["t0"] = cursor_ms / 1000.0
        sh["sp0"] = (cursor_ms + lead_ms) / 1000.0
        sh["sp1"] = (cursor_ms + lead_ms + len(seg_wav)) / 1000.0
        cursor_ms += total_ms
        sh["t1"] = cursor_ms / 1000.0
        sh["dur"] = sh["t1"] - sh["t0"]

        if "rel_sub_windows" in sh:
            rel_w = sh["rel_sub_windows"]
            abs_w = []
            for mi, (rw0, rw1, stxt) in enumerate(rel_w):
                aw0 = sh["sp0"] + max(0.0, rw0 - 0.03)
                if mi < len(rel_w) - 1:
                    nxt_aw0 = sh["sp0"] + max(0.0, rel_w[mi + 1][0] - 0.03)
                    aw1 = min(nxt_aw0 - 0.02, sh["sp0"] + rw1 + 0.14)
                else:
                    extra_h = 0.55 if idx == len(shot_configs) - 1 else 0.18
                    aw1 = min(sh["t1"] - 0.05, sh["sp0"] + rw1 + extra_h)
                abs_w.append((round(aw0, 3), round(max(aw0 + 0.25, aw1), 3), stxt))
            sh["sub_windows"] = abs_w
        else:
            sh["sub_windows"] = _align_subs_viterbi(seg_wav, sh.get("subs", []), sh["sp0"])
        vo_segments.append((lead_ms, seg_wav, tail_ms))

    total_dur_s = cursor_ms / 1000.0
    if compute_only_meta:
        return total_dur_s

    sr = 24000
    vo_track = AudioSegment.silent(duration=0, frame_rate=sr)
    for lead_ms, seg_wav, tail_ms in vo_segments:
        vo_track += AudioSegment.silent(duration=lead_ms, frame_rate=sr) + seg_wav.set_frame_rate(sr).set_channels(1) + AudioSegment.silent(duration=tail_ms, frame_rate=sr)

    vo_samples = np.array(vo_track.get_array_of_samples(), dtype=np.float32) / 32768.0
    n_vo = len(vo_samples)

    bgm_L, bgm_R = synth_studio_lofi_bgm(total_dur_s, shot_configs, sr=sr)
    bgm_L, bgm_R = bgm_L[:n_vo], bgm_R[:n_vo]
    bgm_peak = max(float(np.max(np.abs(bgm_L))), float(np.max(np.abs(bgm_R))), 1e-4)
    bgm_L = bgm_L * (0.86 / bgm_peak)
    bgm_R = bgm_R * (0.86 / bgm_peak)

    vo_env = np.abs(vo_samples)
    win_sc = int(0.18 * sr)
    vo_act = np.convolve(vo_env, np.ones(win_sc, dtype=np.float32) / win_sc, mode="same")
    duck_gain = np.where(vo_act > 0.015, 0.42, 0.76).astype(np.float32)

    for tw0, tw1 in (tick_solo_windows or []):
        duck_gain[int(max(0, tw0) * sr): int(min(total_dur_s, tw1) * sr)] = 0.0

    fade_s = min(2.6, max(0.8, tail_last_ms / 1000.0 * 0.85))
    fade_len = int(fade_s * sr)
    if fade_len < n_vo:
        duck_gain[n_vo - fade_len:] *= np.linspace(1.0, 0.0, fade_len, dtype=np.float32)
    win_sm = int(0.16 * sr)
    duck_smooth = np.convolve(duck_gain, np.ones(win_sm, dtype=np.float32) / win_sm, mode="same")

    foley = np.zeros(n_vo, dtype=np.float32)
    rng_a = np.random.default_rng(42)
    for kind, t_sec, param in (foley_cues or []):
        idx0 = int(t_sec * sr)
        if not (0 <= idx0 < n_vo):
            continue
        if kind == "watch_tick":
            idx1 = min(n_vo, idx0 + int(0.035 * sr))
            lt = np.arange(idx1 - idx0, dtype=np.float32) / sr
            foley[idx0:idx1] += float(param) * (0.65 * np.sin(2 * math.pi * 2950.0 * lt) + 0.45 * np.sin(2 * math.pi * 5120.0 * lt)) * np.exp(-lt * 145.0)
        elif kind == "morse":
            dur_m = float(param)
            idx1 = min(n_vo, idx0 + int(dur_m * sr))
            lt = np.arange(idx1 - idx0, dtype=np.float32) / sr
            env_m = np.minimum(1.0, lt / 0.012) * np.minimum(1.0, (dur_m - lt) / 0.018)
            foley[idx0:idx1] += 0.15 * np.sin(2 * math.pi * 820.0 * lt) * np.clip(env_m, 0.0, 1.0)
        elif kind == "meow":
            idx1 = min(n_vo, idx0 + int(0.26 * sr))
            lt = np.arange(idx1 - idx0, dtype=np.float32) / sr
            ph_m = np.cumsum(2 * math.pi * (560.0 + 180.0 * np.sin(np.pi * lt / 0.26)) / sr)
            foley[idx0:idx1] += 0.15 * (np.sin(ph_m) + 0.35 * np.sin(2 * ph_m)) * np.sin(np.pi * lt / 0.26)
        elif kind == "clunk":
            idx1 = min(n_vo, idx0 + int(0.20 * sr))
            lt = np.arange(idx1 - idx0, dtype=np.float32) / sr
            foley[idx0:idx1] += 0.30 * np.sin(2 * math.pi * (param * np.exp(-lt * 18.0) + 52.0) * lt) * np.exp(-lt * 20.0)
        elif kind == "tap":
            idx1 = min(n_vo, idx0 + int(0.07 * sr))
            lt = np.arange(idx1 - idx0, dtype=np.float32) / sr
            foley[idx0:idx1] += 0.15 * np.sin(2 * math.pi * param * lt) * np.exp(-lt * 48.0)
        elif kind == "chime":
            idx1 = min(n_vo, idx0 + int(0.42 * sr))
            lt = np.arange(idx1 - idx0, dtype=np.float32) / sr
            foley[idx0:idx1] += 0.17 * (np.sin(2 * math.pi * param * lt) + 0.4 * np.sin(2 * math.pi * param * 1.5 * lt)) * np.exp(-lt * 7.5)
        elif kind == "whoosh":
            idx1 = min(n_vo, idx0 + int(0.34 * sr))
            lt = np.arange(idx1 - idx0, dtype=np.float32) / sr
            w_env = np.sin(np.pi * lt / 0.34) ** 1.4
            n_w = np.convolve(rng_a.normal(0.0, 1.0, size=len(lt)).astype(np.float32), np.ones(12) / 12.0, mode="same")
            foley[idx0:idx1] += float(param) * n_w * w_env
        elif kind == "boing":
            idx1 = min(n_vo, idx0 + int(0.28 * sr))
            lt = np.arange(idx1 - idx0, dtype=np.float32) / sr
            f_b = float(param) * (1.0 + 0.48 * (1.0 - np.exp(-lt * 12.0)))
            foley[idx0:idx1] += 0.18 * np.sin(2 * math.pi * f_b * lt) * np.exp(-lt * 11.0)

    out_L = np.clip((vo_samples + bgm_L * duck_smooth + foley) * 32767.0, -32500, 32500).astype(np.int16)
    out_R = np.clip((vo_samples + bgm_R * duck_smooth + foley) * 32767.0, -32500, 32500).astype(np.int16)
    stereo_i16 = np.empty(n_vo * 2, dtype=np.int16)
    stereo_i16[0::2] = out_L
    stereo_i16[1::2] = out_R

    stereo_seg = AudioSegment(stereo_i16.tobytes(), frame_rate=sr, sample_width=2, channels=2)
    stereo_seg.export(str(out_wav), format="wav")
    return total_dur_s


def draw_xeron_signature(
    cc: CleanMintCanvas,
    cx: float,
    cy: float,
    scale: float = 1.0,
    color_key: str = "ink",
    width: float = 1.8,
    rot_deg: float = -4.0,
    underline_mint: bool = True,
    progress: float = 1.0,
    key: str = "xsig",
):
    if progress <= 0.02:
        return
    rad = math.radians(rot_deg)
    ca, sa = math.cos(rad), math.sin(rad)

    def tr(pts_local):
        arr = np.asarray(pts_local, dtype=np.float32) * scale
        rx = arr[:, 0] * ca - arr[:, 1] * sa + cx
        ry = arr[:, 0] * sa + arr[:, 1] * ca + cy
        return np.stack([rx, ry], axis=1)

    x_s1 = [(-44, -12), (-32, -2), (-18, 11)]
    x_s2 = [(-16, -13), (-31, 0), (-46, 12)]
    eron = [
        (-13, 3), (-3, -3), (-7, -9), (-14, -4), (-11, 8), (-1, 7),
        (4, -6), (6, 7), (8, -3), (14, -6), (17, -3),
        (24, -5), (19, 3), (22, 8), (30, 7), (32, -3), (25, -6), (33, -3),
        (38, -5), (38, 8), (40, -2), (46, -6), (51, -3), (52, 8), (59, 5), (65, 2),
    ]
    cc.pen_line(tr(x_s1), color_key=color_key, width=width * 1.1, boil_key=key + "_x1", jitter=0.25, progress=clamp(progress * 2.2), taper=True)
    cc.pen_line(tr(x_s2), color_key=color_key, width=width * 1.05, boil_key=key + "_x2", jitter=0.25, progress=clamp((progress - 0.15) * 2.2), taper=True)
    cc.pen_line(tr(eron), color_key=color_key, width=width * 0.92, boil_key=key + "_er", jitter=0.22, progress=clamp((progress - 0.25) * 1.4), taper=True)
    if underline_mint and progress > 0.55:
        ul = [(-46, 16), (4, 13), (56, 11)]
        cc.pen_line(tr(ul), color_key="mint", width=max(1.3, width * 0.85), boil_key=key + "_ul", jitter=0.20, progress=clamp((progress - 0.55) * 2.2), taper=True)


def draw_xeron_motion_trail(
    cc: CleanMintCanvas,
    p0,
    p_ctrl,
    p1,
    progress: float = 1.0,
    sig_scale: float = 0.52,
    key: str = "xtrail",
):
    if not (0.06 < progress < 0.94):
        return
    arc_full = quad_bezier(p0, p_ctrl, p1, n=24)
    end_i = max(4, min(19, int(len(arc_full) * clamp(progress * 0.82))))
    arc = arc_full[:end_i]
    fade = 1.0 - seg(progress, 0.65, 0.95)
    cc.pen_line(arc, color_key="mint", width=max(1.2, 2.3 * fade), boil_key=key + "_arc", jitter=0.20, taper=True, start_scale=0.12, end_scale=0.75)
    mid_idx = max(1, len(arc) // 2)
    mx, my = arc[mid_idx]
    tang = arc[min(len(arc) - 1, mid_idx + 1)] - arc[max(0, mid_idx - 1)]
    ang_deg = clamp(math.degrees(math.atan2(float(tang[1]), float(tang[0]))), -28.0, 28.0)
    draw_xeron_signature(
        cc, float(mx) - 24.0, float(my) - 18.0, scale=sig_scale,
        color_key="mint_ink", width=1.25, rot_deg=ang_deg,
        underline_mint=False, progress=clamp(progress * 1.5), key=key + "_sig"
    )


def draw_spoked_gear(cc: CleanMintCanvas, cx: float, cy: float, r: float, rot_deg: float, key: str, n_teeth: int = 10, color_key: str = "ink", fill_key: str = "white", progress: float = 1.0):
    if progress <= 0.05 or r < 3.0:
        return
    rad0 = math.radians(rot_deg)
    tooth_h = max(4.0, r * 0.16)
    for ti in range(n_teeth):
        a = rad0 + (ti / n_teeth) * math.pi * 2.0
        cc.pen_line(
            [(cx + math.cos(a) * (r - 1.5), cy + math.sin(a) * (r - 1.5)), (cx + math.cos(a) * (r + tooth_h), cy + math.sin(a) * (r + tooth_h))],
            color_key=color_key, width=max(1.8, r * 0.07), boil_key=f"{key}_t{ti}", progress=progress, taper=False, jitter=0.25
        )
    cc.white_ellipse(cx, cy, r, r, fill_key=fill_key, ink_key=color_key, width=2.0, boil_key=key + "_b", progress=progress)
    for si in range(4):
        sa = rad0 + si * (math.pi * 0.5)
        cc.pen_line([(cx + math.cos(sa) * r * 0.28, cy + math.sin(sa) * r * 0.28), (cx + math.cos(sa) * r * 0.86, cy + math.sin(sa) * r * 0.86)], color_key=color_key, width=1.6, boil_key=f"{key}_sp{si}", progress=progress, taper=False, jitter=0.2)
    cc.white_ellipse(cx, cy, r * 0.28, r * 0.28, fill_key="white", ink_key=color_key, width=1.7, boil_key=key + "_h", progress=progress)


def draw_giant_tourbillon(
    cc: CleanMintCanvas,
    cx: float,
    cy: float,
    R: float,
    t: float,
    speed_mul: float = 1.0,
    sec_hand_deg: float = None,
    mint_highlight: bool = True,
    progress: float = 1.0,
    key: str = "tourb",
):
    if progress <= 0.02:
        return (cx, cy - R * 0.85)
    cc.white_ellipse(cx, cy, R, R, fill_key="white", ink_key="ink", width=2.5, boil_key=key + "_bz1", progress=progress, n=56)
    cc.white_ellipse(cx, cy, R * 0.91, R * 0.91, fill_key=None, ink_key="ink_detail", width=1.5, boil_key=key + "_bz2", progress=progress, n=56)

    if progress > 0.35:
        for ti in range(36):
            ang = (ti / 36.0) * math.pi * 2.0
            major = (ti % 3 == 0)
            r_in = R * (0.83 if major else 0.87)
            cc.pen_line(
                [(cx + math.cos(ang) * r_in, cy + math.sin(ang) * r_in), (cx + math.cos(ang) * R * 0.91, cy + math.sin(ang) * R * 0.91)],
                color_key="ink" if major else "ink_detail", width=2.2 if major else 1.2, boil_key=f"{key}_tk{ti}", taper=False, jitter=0.18
            )

        draw_xeron_signature(cc, cx, cy - R * 0.74, scale=max(0.52, R / 460.0), color_key="ink_detail", width=1.55, rot_deg=0.0, underline_mint=False, progress=progress, key=key + "_xengr")

        g_base = t * 85.0 * speed_mul
        draw_spoked_gear(cc, cx - R * 0.36, cy - R * 0.22, R * 0.25, g_base, key + "_g1", n_teeth=12, color_key="ink_detail")
        draw_spoked_gear(cc, cx + R * 0.35, cy + R * 0.20, R * 0.23, -g_base * 1.25, key + "_g2", n_teeth=10, color_key="ink_detail")
        draw_spoked_gear(cc, cx + R * 0.24, cy - R * 0.34, R * 0.16, g_base * 1.6, key + "_g3", n_teeth=8, color_key="mint_ink" if mint_highlight else "ink_detail", fill_key="soft_mint" if mint_highlight else "white")

        cage_r = R * 0.34
        cage_rot = math.radians(g_base * 0.65)
        cc.white_ellipse(cx, cy, cage_r, cage_r, fill_key="pale_mint" if mint_highlight else "white", ink_key="mint_ink" if mint_highlight else "ink", width=2.1, boil_key=key + "_cg", n=40)
        for bi in range(3):
            ba = cage_rot + bi * (math.pi * 2.0 / 3.0)
            cc.pen_line([(cx, cy), (cx + math.cos(ba) * cage_r, cy + math.sin(ba) * cage_r)], color_key="ink", width=2.2, boil_key=f"{key}_cb{bi}", taper=False)

        breath = 1.0 + 0.16 * math.sin(t * (16.0 if speed_mul > 1.5 else 3.2))
        sp_thetas = np.linspace(0.4, 5.8 * math.pi, 54, dtype=np.float32)
        sp_rads = (sp_thetas / (5.8 * math.pi)) * (cage_r * 0.62) * breath
        sp_pts = np.stack([cx + np.cos(sp_thetas + cage_rot * 2.0) * sp_rads, cy + np.sin(sp_thetas + cage_rot * 2.0) * sp_rads], axis=1)
        cc.pen_line(sp_pts, color_key="mint_ink" if mint_highlight else "ink", width=1.6, boil_key=key + "_hsp", jitter=0.15, taper=False)
        cc.white_ellipse(cx, cy, R * 0.045, R * 0.045, fill_key="mint" if mint_highlight else "ink", ink_key="ink", width=1.6, boil_key=key + "_jewel")

        s_deg = sec_hand_deg if sec_hand_deg is not None else (-90.0 + t * 52.0 * speed_mul)
        s_rad = math.radians(s_deg)
        tail_pt = (cx - math.cos(s_rad) * R * 0.20, cy - math.sin(s_rad) * R * 0.20)
        tip_pt = (cx + math.cos(s_rad) * R * 0.88, cy + math.sin(s_rad) * R * 0.88)
        if speed_mul > 1.8:
            cc.smear_arc(cx, cy, R * 0.78, R * 0.78, s_deg - 28.0, s_deg - 2.0, color_key="mint", width=3.2, key=key + "_ssm")
        cc.pen_line([tail_pt, tip_pt], color_key="ink", width=2.8, boil_key=key + "_sec", taper=True, start_scale=1.2, end_scale=0.45)
        return tip_pt
    return (cx, cy - R * 0.85)


# =============================================================================
# PART 1: FLUID 3-JOINT C/S-SPINE XERON CAT ACTOR (`draw_xeron_actor` v7.0)
# =============================================================================
def solve_ik_2bone(p_root, p_target, len1: float, len2: float, bend_dir: float = 1.0):
    x0, y0 = p_root
    x1, y1 = p_target
    dx, dy = x1 - x0, y1 - y0
    d = math.hypot(dx, dy)
    max_r = max(1e-3, (len1 + len2) * 0.992)
    min_r = abs(len1 - len2) + 1e-3
    if d > max_r:
        sc = max_r / d
        dx, dy = dx * sc, dy * sc
        x1, y1 = x0 + dx, y0 + dy
        d = max_r
    elif d < min_r:
        d = min_r
    cos_a = clamp((len1 * len1 + d * d - len2 * len2) / (2.0 * len1 * d), -1.0, 1.0)
    ang = math.atan2(dy, dx) + bend_dir * math.acos(cos_a)
    return (x0 + math.cos(ang) * len1, y0 + math.sin(ang) * len1), (x1, y1)


def draw_xeron_actor(
    cc: CleanMintCanvas,
    gx: float,
    gy: float,
    u: float = 24.5,
    t: float = 0.0,
    facing: float = 1.0,
    posture: str = "stand",     # "stand", "sit_swing", "belly_up", "airplane_overload"
    act_mode: str = "",         # v7.0 presets: "idle_breathe", "walk_bouncy", "sneak_tiptoe", "vibe_coding", "furious_typing", "facepalm", "head_scratch", "point_explain", "gacha_pull", "eureka_jump", "celebrate_cheer", "peek_curious"
    act_prog: float = 0.0,      # optional 0..1 progress for one-shot presets like "gacha_pull" or "eureka_jump"
    expr: str = "aloof",
    sq: float = 0.0,
    lean_deg: float = 0.0,
    spine_curve: float = 0.0,   # v7.0 C/S-spine bend (-1.0..+1.0; positive bends chest forward in facing dir)
    head_nod_deg: float = 0.0,
    vel_x: float = 0.0,
    vel_y: float = 0.0,
    look_x: float = 0.0,
    look_y: float = 0.0,
    walk_phase: float = 0.0,
    walk_amp: float = 0.0,
    hand_l_world=None,
    hand_r_world=None,
    foot_l_world=None,
    foot_r_world=None,
    wear_glasses: bool = False,
    wear_shades: bool = False,  # v7.0 cool pixel/dark shades for Vibe Coding!
    puffed_fur: bool = False,
    fluffy_tail: bool = False,
    cheek_blush: bool = False,
    spiral_eyes: bool = False,
    floor_y: float = None,      # optional ground Y for dynamic contact shadow when airborne
    draw_shadow: bool = True,
    boil_key: str = "xeron",
):
    # Special Iconic Pose A: Classic Aloof Sitting Cat (`cat_sit` — 极简平涂粗线条端坐绕尾，纯净负空间剪影！)
    if posture == "cat_sit":
        f_dir = 1.0 if facing >= 0 else -1.0
        if draw_shadow:
            cc.white_ellipse(gx, gy + 0.06 * u, 1.55 * u, 0.25 * u, fill_key="shadow", ink_key=None, boil_key=boil_key + "_cs_sh")
        # Graceful tail curling out on floor behind/beside haunch
        t_dir = -f_dir
        sway = math.sin(t * 1.35) * 0.22 * u
        tail_pts = cubic_bezier(
            (gx + t_dir * 0.85 * u, gy - 0.35 * u),
            (gx + t_dir * 2.05 * u, gy - 0.05 * u),
            (gx + t_dir * 2.85 * u, gy - 0.65 * u + sway * 0.5),
            (gx + t_dir * 2.55 * u, gy - 1.55 * u + sway),
            18,
        )
        cc.pen_line(tail_pts, color_key="cat_line", width=max(4.4, 0.35 * u), boil_key=boil_key + "_cs_tl", jitter=0.24, taper=True, start_scale=1.10, end_scale=0.55)
        # Sleek pear-shaped seated cat body resting cleanly on `gy`
        b_top_l, b_top_r = (gx - 0.72 * u, gy - 2.95 * u), (gx + 0.72 * u, gy - 2.95 * u)
        b_hip_l, b_hip_r = (gx - 1.38 * u, gy - 0.48 * u), (gx + 1.38 * u, gy - 0.48 * u)
        b_bot = (gx, gy + 0.04 * u)
        sit_body = np.vstack([
            cubic_bezier(b_top_l, (gx - 1.10 * u, gy - 2.05 * u), (gx - 1.52 * u, gy - 1.05 * u), b_hip_l, 10),
            cubic_bezier(b_hip_l, (gx - 1.15 * u, gy + 0.04 * u), (gx - 0.55 * u, gy + 0.06 * u), b_bot, 8),
            cubic_bezier(b_bot, (gx + 0.55 * u, gy + 0.06 * u), (gx + 1.15 * u, gy + 0.04 * u), b_hip_r, 8),
            cubic_bezier(b_hip_r, (gx + 1.52 * u, gy - 1.05 * u), (gx + 1.10 * u, gy - 2.05 * u), b_top_r, 10),
        ])
        cc.fill_poly(sit_body, "cat_fill", boil_key=boil_key + "_cs_bf", jitter=0.24)
        cc.pen_line(sit_body, color_key="cat_line", width=2.0, closed=True, taper=False, boil_key=boil_key + "_cs_bl")
        # Subtle neat front paws tucked at base
        for ps in (-0.36, 0.36):
            cc.white_ellipse(gx + (ps + f_dir * 0.14) * u, gy - 0.08 * u, 0.28 * u, 0.16 * u, fill_key="cat_fill", ink_key="cat_line", width=1.5, boil_key=f"{boil_key}_cs_pw{ps}")
        # Head & Ears perched cleanly atop seated body!
        p_a = EXPR_PRESETS.get(expr, EXPR_PRESETS["aloof"])
        lid_l, lid_r, brow_l, brow_r, pup_mul, ep_l, ep_r, mouth_mode = p_a
        hrad = math.radians(head_nod_deg)
        ch_r, sh_r_ang = math.cos(hrad), math.sin(hrad)
        neck_x, neck_y = gx + f_dir * 0.08 * u, gy - 2.98 * u
        def hpt_s(lx: float, ly: float):
            return (neck_x + (lx * u) * ch_r - (ly * u) * sh_r_ang, neck_y + (lx * u) * sh_r_ang + (ly * u) * ch_r)
        hcx_s, hcy_s = hpt_s(f_dir * 0.04, -1.36)
        for e_i, (eside, ep_y) in enumerate(((-1.0, ep_l), (1.0, ep_r))):
            ob, ib = hpt_s(eside * 1.82, -1.67), hpt_s(eside * 0.32, -2.76)
            tip = hpt_s(eside * (1.58 - ep_y * 0.65), -4.60 - ep_y * 0.55)
            ep_poly = np.vstack([quad_bezier(ob, hpt_s(eside * 1.98, -2.91), tip, 10), quad_bezier(tip, hpt_s(eside * 0.96, -3.61), ib, 10)])
            cc.fill_poly(ep_poly, "cat_fill", boil_key=f"{boil_key}_csef{e_i}", jitter=0.22)
            cc.pen_line(ep_poly, color_key="cat_line", width=2.0, boil_key=f"{boil_key}_csel{e_i}", jitter=0.22)
            p_tip = (lerp(tip[0], hcx_s, 0.16), lerp(tip[1], hcy_s, 0.24))
            p_out, p_in = hpt_s(eside * 1.56, -2.04), hpt_s(eside * 0.60, -2.67)
            in_poly = [p_out, p_tip, p_in, (lerp(p_out[0], p_in[0], 0.5), lerp(p_out[1], p_in[1], 0.5) - 0.10 * u)]
            cc.fill_poly(in_poly, "cat_ear", boil_key=f"{boil_key}_csie{e_i}", jitter=0.16)
        ang = np.linspace(0, 2 * math.pi, 38, endpoint=False, dtype=np.float32)
        bulge = 1.0 + 0.08 * np.maximum(0.0, np.sin(ang))
        lx_h, ly_h = np.cos(ang) * 2.02 * bulge, -1.36 + np.sin(ang) * 1.56
        head_pts = np.stack([neck_x + (lx_h * u) * ch_r - (ly_h * u) * sh_r_ang, neck_y + (lx_h * u) * sh_r_ang + (ly_h * u) * ch_r], axis=1)
        cc.fill_poly(head_pts, "cat_fill", boil_key=boil_key + "_cshf", jitter=0.24)
        cc.pen_line(head_pts, color_key="cat_line", width=2.1, closed=True, taper=False, boil_key=boil_key + "_cshl", jitter=0.24)
        b_cyc = (t + (det_hash_int(boil_key) % 7) * 0.61) % 4.8
        extra_close = clamp(math.sin((((b_cyc - 4.60) / 0.20) ** 0.75) * math.pi) if (b_cyc > 4.60 and expr not in ("wink", "satisfied", "sigh")) else 0.0)
        f_dx_l, f_dy_l = f_dir * 0.24 + look_x * 0.18, -1.42 + look_y * 0.10
        for es, lid_open_e, brow_deg_e in ((-1.0, lid_l, brow_l), (1.0, lid_r, brow_r)):
            ecx, ecy = hpt_s(f_dx_l + es * 0.78, f_dy_l)
            ew, open_fac = 0.56 * u, lid_open_e * (1.0 - 0.90 * extra_close)
            eh = 0.48 * u * open_fac
            if open_fac <= 0.20:
                if expr in ("satisfied", "wink"):
                    cc.pen_line(quad_bezier((ecx - ew, ecy + 0.06 * u), (ecx, ecy - 0.22 * u), (ecx + ew, ecy + 0.06 * u), 10), color_key="mint", width=2.5, boil_key=f"{boil_key}_cssat{es}")
                else:
                    cc.pen_line([(ecx - ew, ecy), (ecx + ew, ecy)], color_key="mint", width=2.5, boil_key=f"{boil_key}_csblk{es}")
            else:
                b_rad = math.radians(brow_deg_e + head_nod_deg)
                dx_b, dy_b = math.cos(b_rad) * ew, math.sin(b_rad) * ew
                tm_y = ecy - eh * 0.30
                p_tl, p_tr = (ecx - dx_b, tm_y - dy_b), (ecx + dx_b, tm_y + dy_b)
                eye_poly = [p_tl, p_tr] + [(ecx + math.cos(at) * ew, tm_y + math.sin(at) * eh * 1.25) for at in np.linspace(0.0, math.pi, 14)]
                cc.fill_poly(eye_poly, "mint", boil_key=f"{boil_key}_csey{es}", jitter=0.12)
                px = ecx + clamp(look_x, -1.0, 1.0) * ew * 0.38
                pw = max(1.6, 0.11 * u * pup_mul)
                cc.fill_poly([(px - pw, tm_y), (px + pw, tm_y), (px + pw * 0.85, tm_y + eh * 0.86), (px - pw * 0.85, tm_y + eh * 0.86)], "cat_line", boil_key=f"{boil_key}_cspp{es}")
                cc.pen_line(eye_poly, color_key="cat_line", width=1.6, closed=True, taper=False, boil_key=f"{boil_key}_cser{es}")
                cc.pen_line([(p_tl[0] - 2.0, p_tl[1]), (p_tr[0] + 2.0, p_tr[1])], color_key="cat_line", width=2.5, boil_key=f"{boil_key}_cslid{es}", taper=False)
        nx, ny = hpt_s(f_dx_l, f_dy_l + 0.44)
        cc.fill_poly([(nx - 0.14 * u, ny), (nx + 0.14 * u, ny), (nx, ny + 0.12 * u)], "cat_nose", boil_key=boil_key + "_csnt")
        cc.pen_line([(nx - 0.12 * u, ny + 0.30 * u), (nx, ny + 0.24 * u), (nx + 0.16 * u, ny + 0.22 * u)], color_key="cat_nose", width=1.4, boil_key=boil_key + "_csmth")
        for ws in (-1.0, 1.0):
            wx0, wy0 = hpt_s(ws * 1.58, -1.18)
            cc.pen_line([(wx0, wy0), (wx0 + ws * 0.88 * u, wy0 - 0.05 * u)], color_key="ink_detail", width=1.7, boil_key=f"{boil_key}_csw1{ws}")
            cc.pen_line([(wx0, wy0 + 0.24 * u), (wx0 + ws * 0.82 * u, wy0 + 0.33 * u)], color_key="ink_detail", width=1.7, boil_key=f"{boil_key}_csw2{ws}")
        return (hcx_s, hcy_s)

    # Special Pose: Four-paws-up collapsed pancake cat (`四脚朝天瘫成猫饼`)
    if posture == "belly_up":
        if draw_shadow:
            cc.white_ellipse(gx + 0.1 * u, gy + 0.08 * u, 3.2 * u, 0.34 * u, fill_key="shadow", ink_key=None, boil_key=boil_key + "_shd")
        cy_b = gy - 0.52 * u
        cc.white_ellipse(gx + 0.35 * u, cy_b, 2.55 * u, 0.56 * u, fill_key="cat_fill", ink_key="cat_line", width=2.1, boil_key=boil_key + "_bu_t")
        for pi, (px_o, ang_p) in enumerate(((-0.95, -125.0), (-0.15, -75.0), (0.95, -105.0), (1.75, -55.0))):
            tw_p = math.sin(t * 6.0 + pi * 1.5) * 6.0
            rad_p = math.radians(ang_p + tw_p)
            p0 = (gx + px_o * u, cy_b - 0.25 * u)
            p1 = (p0[0] + math.cos(rad_p) * 1.15 * u, p0[1] + math.sin(rad_p) * 1.15 * u)
            cc.pen_line([p0, p1], color_key="cat_line", width=max(3.2, 0.24 * u), boil_key=f"{boil_key}_bp{pi}", taper=True)
            cc.white_ellipse(p1[0], p1[1], 0.19 * u, 0.15 * u, fill_key="cat_fill", ink_key="cat_line", width=1.2, boil_key=f"{boil_key}_bpp{pi}")
        cc.pen_line(quad_bezier((gx + 2.75 * u, cy_b + 0.12 * u), (gx + 3.65 * u, gy - 0.08 * u), (gx + 4.35 * u, gy - 0.22 * u), 12), color_key="cat_line", width=max(4.0, 0.30 * u), boil_key=boil_key + "_btl")
        hcx, hcy = gx - 2.15 * u, gy - 0.92 * u
        for es in (-1.0, 1.0):
            ep_pts = [(hcx + es * 1.35 * u, hcy - 0.35 * u), (hcx + es * 1.75 * u, hcy - 1.95 * u), (hcx + es * 0.35 * u, hcy - 1.05 * u)]
            cc.fill_poly(ep_pts, "cat_fill", boil_key=f"{boil_key}_be{es}")
            cc.pen_line(ep_pts, color_key="cat_line", width=1.9, closed=True, taper=False, boil_key=f"{boil_key}_bel{es}")
            in_pts = [(hcx + es * 1.18 * u, hcy - 0.58 * u), (hcx + es * 1.50 * u, hcy - 1.62 * u), (hcx + es * 0.52 * u, hcy - 1.00 * u)]
            cc.fill_poly(in_pts, "cat_ear", boil_key=f"{boil_key}_bie{es}")
        cc.white_ellipse(hcx, hcy, 1.88 * u, 1.18 * u, fill_key="cat_fill", ink_key="cat_line", width=2.1, boil_key=boil_key + "_bhd")
        for es in (-1.0, 1.0):
            ex, ey = hcx + es * 0.72 * u, hcy - 0.05 * u
            th_s = np.linspace(0.0, 4.2 * math.pi, 26, dtype=np.float32) + t * 9.0 * es
            rr_s = np.linspace(0.05 * u, 0.48 * u, 26, dtype=np.float32)
            cc.pen_line(np.stack([ex + np.cos(th_s) * rr_s, ey + np.sin(th_s) * rr_s], axis=1), color_key="mint", width=2.2, boil_key=f"{boil_key}_sp{es}", taper=False, jitter=0.08)
        return (hcx, hcy)

    # -------------------------------------------------------------------------
    # v8.0 Calm, Aloof, Composed Acting System (`安静高冷本色：丰富定格姿态，拒绝多动症高频晃动`)
    # 85% composed stillness + slow 0.35Hz breathing + lazy 4.5s feline tail sway;
    # actions transition smoothly (`ease_in_out`) into a steady HELD POSE!
    # -------------------------------------------------------------------------
    f_dir = 1.0 if facing >= 0 else -1.0
    am = act_mode.lower().strip()
    extra_hip_dy = 0.0
    extra_hip_dx = 0.0
    ear_flick_l = 0.0
    ear_flick_r = 0.0
    prop_overlay = None
    # Gentle transition progress `pose_k` (defaults to 1.0 steady hold unless `act_prog` is animating `0..1`)
    pose_k = ease_in_out(clamp(act_prog)) if act_prog > 0.001 else 1.0

    # Subtle, barely perceptible calm breathing (`0.38 Hz`, ~1px) + rare single ear twitch every ~6.5s
    calm_breath = math.sin(t * 2.2) * 0.012
    tw_mod = (t + (det_hash_int(boil_key) % 11) * 0.53) % 6.8
    if tw_mod > 6.56 and am not in ("quiet_facepalm", "furious_typing"):
        ear_flick_r = math.sin(((tw_mod - 6.56) / 0.24) * math.pi) * 0.16

    if am in ("idle_breathe", "calm_stand", ""):
        sq += calm_breath
        spine_curve += math.sin(t * 1.6) * 0.03

    elif am in ("hand_on_hip", "arms_crossed"):
        # Clean Negative-Space Aloof Hip-Rest (`外扩叉腰高冷静立` — zero chest overlap!)
        lean_deg += -f_dir * 2.2 * pose_k
        spine_curve += -0.08 * pose_k
        sq += calm_breath
        prop_overlay = ("hand_on_hip", pose_k)

    elif am == "hands_behind_back":
        # Calm captain / old-cadre inspection stance (`背手巡视掌舵`) — rock-steady!
        lean_deg += -f_dir * 2.5 * pose_k
        spine_curve += -0.12 * pose_k
        sq += calm_breath
        prop_overlay = ("hands_behind", pose_k)

    elif am in ("sip_coffee", "vibe_coding"):
        # Quietly holding Xeron coffee mug (`安静端杯淡定旁观`), zero BPM bouncing!
        expr = "coffee_zen" if expr == "aloof" else expr
        lean_deg += -f_dir * 2.0
        spine_curve += -0.06
        sq += calm_breath
        prop_overlay = ("sip_coffee", pose_k)

    elif am == "one_tap":
        # Smooth single one-finger tap (`一指禅轻点即收`) driven by `act_prog` (0->0.5 reach, 0.5->1.0 settle)
        tap_arc = math.sin(clamp(act_prog if act_prog > 0.001 else 0.5) * math.pi)
        lean_deg += f_dir * 4.0 * tap_arc
        spine_curve += 0.12 * tap_arc
        prop_overlay = ("one_tap", tap_arc)

    elif am in ("calm_point", "point_explain"):
        # Steady, composed presenter pointing (`从容稳稳指点，绝不上下乱抖`)!
        lean_deg += f_dir * 2.5 * pose_k
        spine_curve += -0.08 * pose_k
        sq += calm_breath
        prop_overlay = ("calm_point", pose_k)

    elif am == "push_aside":
        # Aloof side-eye one-paw shove (`嫌弃地一爪推开`)
        expr = "side_eye" if expr == "aloof" else expr
        push_k = ease_out(clamp(act_prog if act_prog > 0.001 else 1.0))
        look_x = -f_dir * 0.75
        prop_overlay = ("push_aside", push_k)

    elif am == "chin_rest":
        # Quiet thoughtful chin-rest (`托腮沉思`)
        expr = "thinking" if expr == "aloof" else expr
        lean_deg += f_dir * 3.0 * pose_k
        spine_curve += 0.14 * pose_k
        head_nod_deg += f_dir * 4.0 * pose_k
        prop_overlay = ("chin_rest", pose_k)

    elif am in ("quiet_facepalm", "facepalm"):
        # Still, deadpan forehead palm (`安静扶额叹气，不晃脑袋`)
        expr = "sigh"
        lean_deg += f_dir * 6.0 * pose_k
        spine_curve += 0.28 * pose_k
        head_nod_deg += f_dir * 9.0 * pose_k
        prop_overlay = ("quiet_facepalm", pose_k)

    elif am == "head_scratch":
        # Calm skeptical head tilt (`微歪头疑惑`) — steady hold!
        expr = "skeptical" if expr == "aloof" else expr
        head_nod_deg += -f_dir * 8.0 * pose_k
        prop_overlay = ("chin_rest", pose_k)

    elif am == "furious_typing":
        # Focused low-amplitude desk typing (for high-workload keyboard scenes)
        expr = "tired_droop" if expr == "aloof" else expr
        lean_deg += f_dir * 9.0
        spine_curve += 0.38
        prop_overlay = "desk_typing"

    elif am in ("clean_walk", "walk_bouncy", "sneak_tiptoe"):
        # Composed, grounded feline walk (`从容踱步`, gentle cadence, zero rubber-hose bouncing!)
        if walk_amp <= 0.01:
            walk_amp = 0.65
        if abs(walk_phase) < 1e-4:
            walk_phase = t * 5.2
        lean_deg += f_dir * 3.0 * walk_amp
        spine_curve += 0.08 * walk_amp

    elif am in ("air_leap", "parkour_leap"):
        # Agile feline mid-air parkour bound (`曲膝腾空跃姿` — tucked bent knees, sleek C-spine, streaming tail!)
        lean_deg += f_dir * 13.5 * pose_k
        spine_curve += 0.30 * pose_k
        extra_hip_dy += 1.22 * u * pose_k
        vel_x = f_dir * 260.0 if abs(vel_x) < 1.0 else vel_x
        prop_overlay = ("air_leap", pose_k)

    elif am in ("celebrate_cheer", "eureka_jump", "gacha_pull"):
        # Restrained aloof nod of approval (`高冷微微颔首认可`, no frantic jumping!)
        expr = "satisfied" if expr == "aloof" else expr
        head_nod_deg += math.sin(clamp(act_prog if act_prog > 0.001 else 0.5) * math.pi) * 5.0
        prop_overlay = ("hand_on_hip", 1.0)

    # Ground Contact Shadow
    ground_ref = floor_y if floor_y is not None else gy
    air_h = max(0.0, ground_ref - gy)
    if draw_shadow and posture != "sit_swing":
        sh_scale = clamp(1.0 - air_h / (6.5 * u), 0.35, 1.0)
        cc.white_ellipse(gx, ground_ref + 0.08 * u, 1.48 * u * sh_scale, 0.24 * u * sh_scale, fill_key="shadow", ink_key=None, boil_key=boil_key + "_shd")

    p_a = EXPR_PRESETS.get(expr, EXPR_PRESETS["aloof"])
    lid_l, lid_r, brow_l, brow_r, pup_mul, ep_l, ep_r, mouth_mode = p_a
    ep_l += ear_flick_l
    ep_r += ear_flick_r
    if posture == "airplane_overload":
        puffed_fur = True
        ep_l, ep_r = -0.42, -0.42
        lid_l, lid_r = 0.04, 0.04

    sq_tot = clamp(sq, -0.22, 0.24)
    sx = 1.0 + sq_tot * 0.45
    sy = 1.0 / max(0.72, sx)

    is_sitting = posture in ("sit_swing", "chair_seated")
    if is_sitting:
        hip_x, hip_y = gx + extra_hip_dx, gy - 0.30 * u * sy + extra_hip_dy
    else:
        walk_bob = (abs(math.sin(walk_phase)) ** 1.4) * 0.16 * u * walk_amp
        hip_x, hip_y = gx + extra_hip_dx, gy - 3.42 * u * sy - walk_bob + extra_hip_dy

    eff_curve = clamp(spine_curve, -0.85, 0.85)
    lean_rad_base = math.radians(lean_deg)

    def bpt(lx: float, ly: float):
        h_n = clamp(-ly / 3.18, -0.15, 1.25)
        bend_dx = f_dir * eff_curve * (h_n * abs(h_n)) * 0.78 * u
        local_ang = lean_rad_base + f_dir * eff_curve * h_n * 0.28
        ca, sa = math.cos(local_ang), math.sin(local_ang)
        lxs = lx * u * sx + bend_dx
        lys = ly * u * sy
        return (hip_x + lxs * ca - lys * sa, hip_y + lxs * sa + lys * ca)

    if posture != "chair_seated":
        # 1. Slow, Languid, Aloof Feline S-Tail (`慢速优雅猫尾微摆`, ~0.24 Hz = 4.2s per cycle!)
        t_dir = -1.0 if facing >= 0 else 1.0
        tb = bpt(t_dir * 0.82, -0.22)
        vel_drag_x = clamp(-vel_x * 0.035, -1.0 * u, 1.0 * u)
        vel_drag_y = clamp(-vel_y * 0.028, -0.75 * u, 0.75 * u)
        w1 = math.sin(t * 1.45 - 0.4) * 0.22 * u + vel_drag_y * 0.4
        w2 = math.sin(t * 1.45 - 1.2) * 0.40 * u + vel_drag_y * 0.8
        t_curve = cubic_bezier(
            tb,
            (tb[0] + t_dir * 1.15 * u + vel_drag_x * 0.3, tb[1] + 0.62 * u + w1 * 0.4),
            (tb[0] + t_dir * 2.25 * u + vel_drag_x * 0.7, tb[1] + 0.06 * u + w1),
            (tb[0] + t_dir * 2.95 * u + vel_drag_x, tb[1] - 0.72 * u + w2),
            18,
        )
        if fluffy_tail:
            cc.pen_line(t_curve, color_key="cat_line", width=max(8.5, 0.65 * u), boil_key=boil_key + "_tail", jitter=0.65, taper=True, start_scale=0.95, end_scale=1.20)
        else:
            cc.pen_line(t_curve, color_key="cat_line", width=max(4.2, 0.34 * u), boil_key=boil_key + "_tail", jitter=0.28, taper=True, start_scale=1.08, end_scale=0.54)

    # 2. Grounded Standing / Calm Walking Legs
    if not is_sitting:
        custom_feet = (foot_l_world, foot_r_world)
        for li, side in enumerate((-0.52, 0.52)):
            l_root = bpt(side, 0.06)
            foot_tilt = 0.0
            if custom_feet[li] is not None:
                ft_t = custom_feet[li]
                foot_tilt = -12.0 * f_dir
            elif am in ("air_leap", "parkour_leap"):
                is_lead = (li == 1) if facing >= 0 else (li == 0)
                if is_lead:
                    ft_t = bpt(f_dir * 1.05, 1.52)
                    foot_tilt = 22.0 * f_dir
                else:
                    ft_t = bpt(-f_dir * 1.18, 1.82)
                    foot_tilt = 38.0 * f_dir
            elif walk_amp > 0.02:
                ph = walk_phase + (0.0 if li == 0 else math.pi)
                stride = math.sin(ph) * 1.15 * u * walk_amp * f_dir
                swing = max(0.0, -math.cos(ph))
                lift = (swing ** 1.3) * 0.55 * u * walk_amp
                ft_t = (gx + side * 0.48 * u + stride, ground_ref - lift)
                foot_tilt = -swing * 12.0 * f_dir
            else:
                ft_t = (gx + side * 0.62 * u, gy)
            knee, foot = solve_ik_2bone(l_root, ft_t, 2.02 * u, 2.02 * u, bend_dir=(0.30 if facing >= 0 else -0.30))
            ctrl_k = (knee[0] * 1.16 - (l_root[0] + foot[0]) * 0.08, knee[1] * 1.16 - (l_root[1] + foot[1]) * 0.08)
            cc.pen_line(quad_bezier(l_root, ctrl_k, foot, n=14), color_key="cat_line", width=max(3.0, 0.25 * u), boil_key=f"{boil_key}_lg{li}", jitter=0.26, taper=True, start_scale=1.08, end_scale=0.82)
            f_len = 0.44 if facing > 0.15 else (-0.44 if facing < -0.15 else (0.38 if li == 1 else -0.38))
            fr = math.radians(foot_tilt)
            cc.pen_line([foot, (foot[0] + math.cos(fr) * (f_len * u), foot[1] + math.sin(fr) * abs(f_len * u) + 0.04 * u)], color_key="cat_line", width=max(2.9, 0.23 * u), boil_key=f"{boil_key}_ft{li}", jitter=0.22, taper=True)

    # Head Coordinate Frame
    neck_anchor = bpt(f_dir * 0.10, -3.18)
    head_rot_deg = lean_deg * 0.32 + eff_curve * f_dir * 8.0 + head_nod_deg
    hrad = math.radians(head_rot_deg)
    ch_r, sh_r_ang = math.cos(hrad), math.sin(hrad)

    def hpt(lx: float, ly: float):
        lxs, lys = lx * u * sx, ly * u * sy
        return (neck_anchor[0] + lxs * ch_r - lys * sh_r_ang, neck_anchor[1] + lxs * sh_r_ang + lys * ch_r)

    hcx, hcy = hpt(f_dir * 0.04, -1.36)

    # 3. Composed Arms & Held Pose Targets
    sh_l, sh_r = bpt(-0.86, -2.75), bpt(0.86, -2.75)
    arm_swing = math.sin(walk_phase) * 0.65 * u * walk_amp
    def_hl = bpt(-1.52, 0.15)
    def_hr = bpt(1.52, 0.15)
    if walk_amp > 0.05:
        def_hl = (def_hl[0] - arm_swing * 0.6 * f_dir, def_hl[1] - abs(arm_swing) * 0.12)
        def_hr = (def_hr[0] + arm_swing * 0.6 * f_dir, def_hr[1] - abs(arm_swing) * 0.12)

    p_kind = prop_overlay[0] if isinstance(prop_overlay, tuple) else prop_overlay
    p_val = prop_overlay[1] if isinstance(prop_overlay, tuple) else 1.0

    if p_kind == "hand_on_hip":
        # Outer elbow forms a crisp negative-space `<` outside the waist (`-1.22` / `+1.22` hip edge), other arm relaxed!
        if facing >= 0:
            def_hl = lerp_pt(def_hl, bpt(-1.26, -0.78), p_val)
            def_hr = bpt(1.48, 0.18)
        else:
            def_hr = lerp_pt(def_hr, bpt(1.26, -0.78), p_val)
            def_hl = bpt(-1.48, 0.18)
    elif p_kind == "hands_behind":
        def_hl = lerp_pt(def_hl, bpt(-0.42, -0.52), p_val)
        def_hr = lerp_pt(def_hr, bpt(0.42, -0.52), p_val)
    elif p_kind == "sip_coffee":
        # Hold coffee mug cleanly OUT TO THE SIDE in pure-white space (`2.18 * u`) so zero chest overlap!
        if facing >= 0:
            def_hr = bpt(2.18, -1.62)
            def_hl = bpt(-1.42, 0.16)
        else:
            def_hl = bpt(-2.18, -1.62)
            def_hr = bpt(1.42, 0.16)
    elif p_kind == "one_tap":
        if facing >= 0:
            def_hr = lerp_pt(bpt(1.45, -0.65), (gx + 2.45 * u, hip_y - 1.95 * u), p_val)
            def_hl = bpt(-1.32, 0.12)
        else:
            def_hl = lerp_pt(bpt(-1.45, -0.65), (gx - 2.45 * u, hip_y - 1.95 * u), p_val)
            def_hr = bpt(1.32, 0.12)
    elif p_kind == "calm_point":
        if facing >= 0:
            def_hr = lerp_pt(def_hr, (gx + 2.35 * u, hip_y - 2.35 * u), p_val)
            def_hl = bpt(-1.25, -0.35)
        else:
            def_hl = lerp_pt(def_hl, (gx - 2.35 * u, hip_y - 2.35 * u), p_val)
            def_hr = bpt(1.25, -0.35)
    elif p_kind == "push_aside":
        # Push toward `-f_dir` while looking away!
        if facing >= 0:
            def_hl = lerp_pt(bpt(-1.2, -1.4), (gx - 2.65 * u, hip_y - 1.95 * u), p_val)
            def_hr = bpt(1.35, 0.12)
        else:
            def_hr = lerp_pt(bpt(1.2, -1.4), (gx + 2.65 * u, hip_y - 1.95 * u), p_val)
            def_hl = bpt(-1.35, 0.12)
    elif p_kind == "chin_rest":
        if facing >= 0:
            def_hr = lerp_pt(def_hr, hpt(0.45, -0.22), p_val)
            def_hl = bpt(-1.25, -0.25)
        else:
            def_hl = lerp_pt(def_hl, hpt(-0.45, -0.22), p_val)
            def_hr = bpt(1.25, -0.25)
    elif p_kind == "quiet_facepalm":
        if facing >= 0:
            def_hr = lerp_pt(def_hr, hpt(0.55, -1.45), p_val)
            def_hl = bpt(-1.38, 0.20)
        else:
            def_hl = lerp_pt(def_hl, hpt(-0.55, -1.45), p_val)
            def_hr = bpt(1.38, 0.20)
    elif p_kind == "air_leap":
        if facing >= 0:
            def_hr = lerp_pt(def_hr, bpt(1.75, -1.08), p_val)
            def_hl = lerp_pt(def_hl, bpt(-1.58, -0.62), p_val)
        else:
            def_hl = lerp_pt(def_hl, bpt(-1.75, -1.08), p_val)
            def_hr = lerp_pt(def_hr, bpt(1.58, -0.62), p_val)
    elif p_kind == "desk_typing":
        alt = math.sin(t * 14.0) * 0.18 * u
        def_hl = (gx + f_dir * 1.55 * u, hip_y - 1.25 * u + alt)
        def_hr = (gx + f_dir * 2.05 * u, hip_y - 1.25 * u - alt)

    tgt_l = hand_l_world if hand_l_world is not None else def_hl
    tgt_r = hand_r_world if hand_r_world is not None else def_hr

    def render_arm(sh, tgt, bdir, akey, front_halo: bool = False):
        elb, paw = solve_ik_2bone(sh, tgt, 2.22 * u, 2.22 * u, bend_dir=bdir)
        ctrl_e = (elb[0] * 1.15 - (sh[0] + paw[0]) * 0.075, elb[1] * 1.15 - (sh[1] + paw[1]) * 0.075)
        arm_pts = quad_bezier(sh, ctrl_e, paw, n=14)
        w_arm = max(2.9, 0.24 * u)
        if front_halo:
            cc.pen_line(arm_pts[3:], color_key="white", width=w_arm + 3.2, boil_key=akey + "_hl", jitter=0.16, taper=True, start_scale=0.95, end_scale=0.95)
            cc.white_ellipse(paw[0], paw[1], 0.24 * u, 0.20 * u, fill_key="white", ink_key=None, boil_key=akey + "_phl")
        cc.pen_line(arm_pts, color_key="cat_line", width=w_arm, boil_key=akey, jitter=0.25, taper=True, start_scale=1.08, end_scale=0.80)
        cc.white_ellipse(paw[0], paw[1], 0.19 * u, 0.15 * u, fill_key="cat_fill", ink_key="cat_line", width=1.2, boil_key=akey + "_p")
        return paw

    # If `hands_behind`, draw BOTH arms behind torso so paws clasp cleanly behind the back!
    if p_kind == "hands_behind":
        paw_back = render_arm(sh_l, tgt_l, -0.32, boil_key + "_armL", front_halo=False)
        paw_front = render_arm(sh_r, tgt_r, 0.32, boil_key + "_armR", front_halo=False)
    else:
        if facing >= 0:
            paw_back = render_arm(sh_l, tgt_l, -0.36, boil_key + "_armL", front_halo=False)
        else:
            paw_back = render_arm(sh_r, tgt_r, 0.36, boil_key + "_armR", front_halo=False)

    # 4. Composed Pear Torso
    t_top_l, t_top_r = bpt(-0.78, -3.15), bpt(0.78, -3.15)
    t_hip_l, t_hip_r, t_bot = bpt(-1.36, -0.55), bpt(1.36, -0.55), bpt(0.0, 0.28)
    torso_curve = np.vstack([
        cubic_bezier(t_top_l, bpt(-1.18, -2.15), bpt(-1.52, -1.15), t_hip_l, 10),
        cubic_bezier(t_hip_l, bpt(-1.15, 0.20), bpt(-0.55, 0.32), t_bot, 8),
        cubic_bezier(t_bot, bpt(0.55, 0.32), bpt(1.15, 0.20), t_hip_r, 8),
        cubic_bezier(t_hip_r, bpt(1.52, -1.15), bpt(1.18, -2.15), t_top_r, 10),
    ])
    cc.fill_poly(torso_curve, "cat_fill", boil_key=boil_key + "_tf", jitter=(1.8 if puffed_fur else 0.26))
    cc.pen_line(torso_curve, color_key="cat_line", width=2.0, boil_key=boil_key + "_tl", jitter=(2.0 if puffed_fur else 0.26), closed=True, taper=False)

    if posture == "sit_swing":
        for li, side in enumerate((-0.48, 0.48)):
            l_root = bpt(side, 0.16)
            # Calm, unhurried subtle leg hang (`1.2 rad/s` lazy sway, not frantic kicking!)
            sw_ang = math.sin(t * 1.3 + (0.0 if li == 0 else math.pi)) * 0.12
            knee = (l_root[0] + math.sin(sw_ang * 0.5) * 0.48 * u, l_root[1] + 1.12 * u)
            foot = (knee[0] + math.sin(sw_ang) * 0.72 * u, knee[1] + math.cos(sw_ang) * 1.42 * u)
            cc.pen_line(quad_bezier(l_root, knee, foot, n=12), color_key="cat_line", width=max(3.0, 0.25 * u), boil_key=f"{boil_key}_slg{li}", jitter=0.24, taper=True)
            cc.pen_line([foot, (foot[0] + math.cos(sw_ang * 0.6) * 0.40 * u, foot[1] + 0.08 * u)], color_key="cat_line", width=max(2.9, 0.23 * u), boil_key=f"{boil_key}_sft{li}", jitter=0.20, taper=True)

    # 5. Head & Upright Sharp Ears
    ear_lag = clamp(-vel_x * 0.0012, -0.20, 0.20)
    for e_i, (eside, ep_y) in enumerate(((-1.0, ep_l), (1.0, ep_r))):
        outer_base = hpt(eside * 1.82, -1.36 - 0.31)
        inner_base = hpt(eside * 0.32, -1.36 - 1.40)
        if posture == "airplane_overload":
            tip = hpt(eside * 3.05, -1.36 - 1.45)
        else:
            tip = hpt(eside * (1.58 - ep_y * 0.65) + ear_lag, -1.36 - 3.24 - ep_y * 0.55)
        c1 = hpt(eside * 1.98, -1.36 - 1.55)
        c3 = hpt(eside * 0.96, -1.36 - 2.25)
        ear_poly = np.vstack([quad_bezier(outer_base, c1, tip, 10), quad_bezier(tip, c3, inner_base, 10)])
        cc.fill_poly(ear_poly, "cat_fill", boil_key=f"{boil_key}_ef{e_i}", jitter=0.24)
        cc.pen_line(ear_poly, color_key="cat_line", width=2.0, boil_key=f"{boil_key}_el{e_i}", jitter=0.24, taper=False)

        p_tip = (lerp(tip[0], hcx, 0.16), lerp(tip[1], hcy, 0.24))
        p_out = hpt(eside * 1.56, -1.36 - 0.68)
        p_in = hpt(eside * 0.60, -1.36 - 1.31)
        n1 = (lerp(p_out[0], p_in[0], 0.32), lerp(p_out[1], p_in[1], 0.32) - 0.16 * u)
        n2 = (lerp(p_out[0], p_in[0], 0.52), lerp(p_out[1], p_in[1], 0.52) + 0.04 * u)
        n3 = (lerp(p_out[0], p_in[0], 0.70), lerp(p_out[1], p_in[1], 0.70) - 0.14 * u)
        in_poly = [p_out, p_tip, p_in, n3, n2, n1]
        cc.fill_poly(in_poly, "cat_ear", boil_key=f"{boil_key}_ie{e_i}", jitter=0.18)
        cc.pen_line(in_poly, color_key="cat_line", width=1.3, boil_key=f"{boil_key}_iel{e_i}", jitter=0.18, closed=True, taper=False)

    ang = np.linspace(0, 2 * math.pi, 38, endpoint=False, dtype=np.float32)
    bulge = 1.0 + 0.08 * np.maximum(0.0, np.sin(ang))
    lx_h = np.cos(ang) * 2.02 * bulge
    ly_h = -1.36 + np.sin(ang) * 1.56
    head_pts = np.stack([
        neck_anchor[0] + (lx_h * u * sx) * ch_r - (ly_h * u * sy) * sh_r_ang,
        neck_anchor[1] + (lx_h * u * sx) * sh_r_ang + (ly_h * u * sy) * ch_r,
    ], axis=1)
    cc.fill_poly(head_pts, "cat_fill", boil_key=boil_key + "_hf", jitter=0.26)
    cc.pen_line(head_pts, color_key="cat_line", width=2.1, boil_key=boil_key + "_hl", jitter=0.26, closed=True, taper=False)

    # Calm natural blink every ~4.8s
    b_cyc = (t + (det_hash_int(boil_key) % 7) * 0.61) % 4.8
    auto_b = math.sin((((b_cyc - 4.60) / 0.20) ** 0.75) * math.pi) if (b_cyc > 4.60 and expr not in ("wink", "strain", "sigh", "satisfied", "deadpan", "blank")) else 0.0
    extra_close = clamp(auto_b, 0.0, 1.0)

    eff_look_x = (-f_dir * 0.72 if expr == "side_eye" else look_x)
    f_dx_l = facing * 0.24 + eff_look_x * 0.18
    f_dy_l = -1.42 + look_y * 0.10

    for idx_e, (es, lid_open_e, brow_deg_e) in enumerate(((-1.0, lid_l, brow_l), (1.0, lid_r, brow_r))):
        ecx, ecy = hpt(f_dx_l + es * 0.78, f_dy_l)
        ew = 0.56 * u
        open_fac = lid_open_e * (1.0 - 0.90 * extra_close)
        eh = 0.48 * u * open_fac

        if spiral_eyes:
            th_s = np.linspace(0.0, 3.8 * math.pi, 22, dtype=np.float32) + t * 5.5 * es
            rr_s = np.linspace(0.05 * u, 0.46 * u, 22, dtype=np.float32)
            cc.pen_line(np.stack([ecx + np.cos(th_s) * rr_s, ecy + np.sin(th_s) * rr_s], axis=1), color_key="mint", width=2.0, boil_key=f"{boil_key}_sp{es}", taper=False, jitter=0.1)
        elif open_fac <= 0.20:
            if expr == "strain":
                d_s = 1.0 if es < 0 else -1.0
                cc.pen_line([(ecx - d_s * ew * 0.78, ecy - 0.19 * u), (ecx + d_s * ew * 0.52, ecy), (ecx - d_s * ew * 0.78, ecy + 0.19 * u)], color_key="mint", width=2.3, boil_key=f"{boil_key}_str{es}", jitter=0.15, taper=False)
            elif expr in ("satisfied", "wink"):
                cc.pen_line(quad_bezier((ecx - ew, ecy + 0.06 * u), (ecx, ecy - 0.22 * u), (ecx + ew, ecy + 0.06 * u), n=10), color_key="mint", width=2.5, boil_key=f"{boil_key}_sat{es}", jitter=0.15)
            else:
                cc.pen_line([(ecx - ew, ecy), (ecx + ew, ecy)], color_key="mint", width=2.6, boil_key=f"{boil_key}_blk{es}", jitter=0.12, taper=False)
        else:
            b_rad = math.radians(brow_deg_e + head_rot_deg)
            dx_b, dy_b = math.cos(b_rad) * ew, math.sin(b_rad) * ew
            top_mid_y = ecy - eh * 0.30
            p_tl, p_tr = (ecx - dx_b, top_mid_y - dy_b), (ecx + dx_b, top_mid_y + dy_b)
            eye_poly = [p_tl, p_tr] + [(ecx + math.cos(at) * ew, top_mid_y + math.sin(at) * eh * 1.25) for at in np.linspace(0.0, math.pi, 14)]
            cc.fill_poly(eye_poly, "mint", boil_key=f"{boil_key}_ey{es}", jitter=0.12)
            px = ecx + clamp(eff_look_x, -1.0, 1.0) * ew * 0.42
            pw = max(1.6, 0.11 * u * pup_mul)
            pup = [(px - pw, top_mid_y), (px + pw, top_mid_y), (px + pw * 0.85, top_mid_y + eh * 0.86), (px - pw * 0.85, top_mid_y + eh * 0.86)]
            cc.fill_poly(pup, "cat_line", boil_key=f"{boil_key}_pp{es}", jitter=0.05)
            cc.pen_line(eye_poly, color_key="cat_line", width=1.6, boil_key=f"{boil_key}_er{es}", jitter=0.12, closed=True, taper=False)
            cc.pen_line([(p_tl[0] - math.cos(b_rad) * 2.5, p_tl[1] - math.sin(b_rad) * 2.5), (p_tr[0] + math.cos(b_rad) * 2.5, p_tr[1] + math.sin(b_rad) * 2.5)], color_key="cat_line", width=2.5, boil_key=f"{boil_key}_lid{es}", jitter=0.12, taper=False)

    if wear_glasses:
        gl_c = hpt(f_dx_l - 0.78, f_dy_l)
        gr_c = hpt(f_dx_l + 0.78, f_dy_l)
        cc.white_ellipse(gl_c[0], gl_c[1], 0.68 * u, 0.62 * u, fill_key=None, ink_key="mint", width=2.1, boil_key=boil_key + "_ggL")
        cc.white_ellipse(gr_c[0], gr_c[1], 0.68 * u, 0.62 * u, fill_key=None, ink_key="mint", width=2.1, boil_key=boil_key + "_ggR")
        cc.pen_line([(gl_c[0] + 0.66 * u, gl_c[1]), (gr_c[0] - 0.66 * u, gr_c[1])], color_key="mint", width=2.0, boil_key=boil_key + "_ggB", taper=False)

    nx, ny = hpt(f_dx_l, f_dy_l + 0.44)
    cc.fill_poly([(nx - 0.14 * u, ny), (nx + 0.14 * u, ny), (nx, ny + 0.12 * u)], "cat_nose", boil_key=boil_key + "_nt", jitter=0.06)
    cc.pen_line([(nx, ny + 0.11 * u), (nx, ny + 0.24 * u)], color_key="cat_nose", width=1.4, boil_key=boil_key + "_ns", jitter=0.08, taper=False)
    if mouth_mode == "smug":
        cc.pen_line([(nx - 0.10 * u, ny + 0.30 * u), (nx + 0.02 * u, ny + 0.25 * u), (nx + 0.24 * u, ny + 0.16 * u)], color_key="cat_nose", width=1.6, boil_key=boil_key + "_mth", jitter=0.08)
    else:
        cc.pen_line([(nx - 0.12 * u, ny + 0.32 * u), (nx, ny + 0.25 * u), (nx + 0.12 * u, ny + 0.32 * u)], color_key="cat_nose", width=1.3, boil_key=boil_key + "_mth", jitter=0.08, taper=False)

    # Steady whiskers (no vertical jitter!)
    for ws in (-1.0, 1.0):
        wx0, wy0 = hpt(ws * 1.58, -1.18)
        cc.pen_line([(wx0, wy0), (wx0 + ws * 0.88 * u, wy0 - 0.05 * u)], color_key="ink_detail", width=1.7, boil_key=f"{boil_key}_w1_{ws}", jitter=0.14)
        cc.pen_line([(wx0, wy0 + 0.24 * u), (wx0 + ws * 0.82 * u, wy0 + 0.33 * u)], color_key="ink_detail", width=1.7, boil_key=f"{boil_key}_w2_{ws}", jitter=0.14)

    if p_kind != "hands_behind":
        use_halo = p_kind in ("quiet_facepalm",)
        if facing >= 0:
            paw_front = render_arm(sh_r, tgt_r, 0.42, boil_key + "_armR", front_halo=use_halo)
        else:
            paw_front = render_arm(sh_l, tgt_l, -0.42, boil_key + "_armL", front_halo=use_halo)

    if cheek_blush:
        for bs in (-1.0, 1.0):
            bcx, bcy = hpt(f_dx_l + bs * 1.25, f_dy_l + 0.38)
            for bi_l in (-0.11, 0.11):
                cc.pen_line(
                    [(bcx + (bi_l - 0.10) * u, bcy + 0.12 * u), (bcx + (bi_l + 0.10) * u, bcy - 0.12 * u)],
                    color_key="blush", width=2.1, boil_key=f"{boil_key}_bl{bs}_{bi_l}", jitter=0.10, taper=True
                )

    # Composed Micro-Props (Held Steady!)
    if p_kind == "sip_coffee":
        mug_x, mug_y = paw_front[0] + f_dir * 0.34 * u, paw_front[1] - 0.12 * u
        cc.white_box(mug_x - 0.44 * u, mug_y - 0.48 * u, 0.88 * u, 0.96 * u, fill_key="white", ink_key="ink", width=2.1, corner_r=5.0, boil_key=boil_key + "_mug")
        cc.pen_line(quad_bezier((mug_x + f_dir * 0.44 * u, mug_y - 0.26 * u), (mug_x + f_dir * 0.78 * u, mug_y), (mug_x + f_dir * 0.44 * u, mug_y + 0.26 * u), 8), width=2.0, boil_key=boil_key + "_mgh")
        cc.pen_line([(mug_x - 0.22 * u, mug_y), (mug_x + 0.22 * u, mug_y)], color_key="mint", width=2.4, boil_key=boil_key + "_mgm")
        sy_s = mug_y - 0.68 * u - ((t * 0.55) % 1.0) * 0.45 * u
        cc.pen_line([(mug_x, sy_s + 0.22 * u), (mug_x + 0.08 * u, sy_s)], color_key="ink_soft", width=1.6, boil_key=boil_key + "_stm")

    elif p_kind == "calm_point" and hand_l_world is None and hand_r_world is None:
        tip_x = paw_front[0] + f_dir * 1.95 * u
        tip_y = paw_front[1] - 1.05 * u
        cc.pen_line([paw_front, (tip_x, tip_y)], color_key="ink", width=2.4, boil_key=boil_key + "_pstk", taper=True, start_scale=1.1, end_scale=0.65)
        cc.white_ellipse(tip_x, tip_y, 0.15 * u, 0.15 * u, fill_key="mint", ink_key="mint_ink", width=1.3, boil_key=boil_key + "_ptip")

    return (hcx, hcy)


# =============================================================================
# PART 2: SOCIAL, DEV & CRYPTO HAND-DRAWN ICON KIT (`draw_brand_icon`)
# =============================================================================
def draw_brand_icon(
    cc: CleanMintCanvas,
    kind: str,
    cx: float,
    cy: float,
    r: float = 26.0,
    accent: bool = True,
    progress: float = 1.0,
    key: str = "ico",
):
    if progress <= 0.02:
        return
    k = kind.lower().strip()

    if k == "github":
        cc.white_ellipse(cx, cy, r, r, fill_key="cat_fill", ink_key="cat_line", width=2.0, boil_key=key + "_bg", progress=progress)
        if progress > 0.35:
            ears = [
                (cx - 0.46 * r, cy - 0.10 * r), (cx - 0.48 * r, cy - 0.60 * r), (cx - 0.15 * r, cy - 0.36 * r),
                (cx + 0.15 * r, cy - 0.36 * r), (cx + 0.48 * r, cy - 0.60 * r), (cx + 0.46 * r, cy - 0.10 * r),
            ]
            cc.fill_poly(ears, "white", boil_key=key + "_ge", jitter=0.15)
            cc.white_ellipse(cx, cy - 0.04 * r, 0.54 * r, 0.42 * r, fill_key="white", ink_key=None, boil_key=key + "_gh")
            body = [(cx - 0.24 * r, cy + 0.28 * r), (cx + 0.24 * r, cy + 0.28 * r), (cx + 0.28 * r, cy + 0.94 * r), (cx - 0.28 * r, cy + 0.94 * r)]
            cc.fill_poly(body, "white", boil_key=key + "_gb", jitter=0.15)
            tail = quad_bezier((cx - 0.22 * r, cy + 0.60 * r), (cx - 0.66 * r, cy + 0.54 * r), (cx - 0.54 * r, cy + 0.18 * r), n=10)
            cc.pen_line(tail, color_key="white", width=max(2.4, 0.15 * r), boil_key=key + "_gt", jitter=0.15, taper=False)

    elif k in ("x", "twitter"):
        cc.white_box(cx - r, cy - r, 2 * r, 2 * r, corner_r=r * 0.30, width=2.0, boil_key=key + "_bg", progress=progress)
        if progress > 0.35:
            bar1 = [(cx - 0.52 * r, cy - 0.50 * r), (cx - 0.26 * r, cy - 0.50 * r), (cx + 0.52 * r, cy + 0.50 * r), (cx + 0.26 * r, cy + 0.50 * r)]
            cc.fill_poly(bar1, "white", boil_key=key + "_xb1", jitter=0.15)
            cc.pen_line(bar1, width=1.8, boil_key=key + "_xl1", closed=True, taper=False, jitter=0.18)
            cc.pen_line([(cx + 0.48 * r, cy - 0.50 * r), (cx - 0.48 * r, cy + 0.50 * r)], width=max(2.4, 0.14 * r), boil_key=key + "_xl2", jitter=0.18)

    elif k in ("telegram", "tg"):
        cc.white_ellipse(cx, cy, r, r, fill_key="soft_blue" if accent else "white", ink_key="blue" if accent else "ink", width=2.0, boil_key=key + "_bg", progress=progress)
        if progress > 0.35:
            col = "blue" if accent else "ink"
            dart = [(cx - 0.56 * r, cy + 0.04 * r), (cx + 0.50 * r, cy - 0.44 * r), (cx + 0.22 * r, cy + 0.48 * r), (cx - 0.08 * r, cy + 0.16 * r)]
            cc.fill_poly(dart, "white", boil_key=key + "_tdf", jitter=0.15)
            cc.pen_line(dart, color_key=col, width=1.9, boil_key=key + "_td", closed=True, taper=False, jitter=0.2)
            cc.pen_line([(cx + 0.48 * r, cy - 0.42 * r), (cx - 0.08 * r, cy + 0.16 * r), (cx - 0.14 * r, cy + 0.42 * r)], color_key=col, width=1.5, boil_key=key + "_tc", jitter=0.18, taper=False)

    elif k in ("bilibili", "bili"):
        col = "blue" if accent else "ink"
        cc.pen_line([(cx - 0.38 * r, cy - 0.96 * r), (cx - 0.10 * r, cy - 0.62 * r)], color_key=col, width=2.0, boil_key=key + "_ba1", progress=progress)
        cc.pen_line([(cx + 0.38 * r, cy - 0.96 * r), (cx + 0.10 * r, cy - 0.62 * r)], color_key=col, width=2.0, boil_key=key + "_ba2", progress=progress)
        cc.white_box(cx - 0.94 * r, cy - 0.62 * r, 1.88 * r, 1.36 * r, corner_r=r * 0.28, ink_key=col, width=2.0, boil_key=key + "_btv", progress=progress)
        if progress > 0.4:
            cc.white_box(cx - 0.72 * r, cy - 0.42 * r, 1.44 * r, 0.94 * r, corner_r=r * 0.16, ink_key=col, width=1.3, boil_key=key + "_bin")
            cc.pen_line([(cx - 0.44 * r, cy - 0.08 * r), (cx - 0.18 * r, cy + 0.08 * r)], color_key=col, width=2.0, boil_key=key + "_be1")
            cc.pen_line([(cx + 0.44 * r, cy - 0.08 * r), (cx + 0.18 * r, cy + 0.08 * r)], color_key=col, width=2.0, boil_key=key + "_be2")

    elif k in ("douyin", "tiktok"):
        cc.white_box(cx - r, cy - r, 2 * r, 2 * r, corner_r=r * 0.30, width=2.0, boil_key=key + "_bg", progress=progress)
        if progress > 0.35:
            for ox, oy, ck, wd in (((-2.0, -1.5, "blue", 1.8), (2.0, 1.5, "red", 1.8)) if accent else ()) + ((0.0, 0.0, "ink", 2.6),):
                cc.pen_line([(cx + 0.08 * r + ox, cy + 0.32 * r + oy), (cx + 0.08 * r + ox, cy - 0.52 * r + oy)], color_key=ck, width=wd, boil_key=key + ck + "s", taper=False)
                flag = quad_bezier((cx + 0.08 * r + ox, cy - 0.50 * r + oy), (cx + 0.28 * r + ox, cy - 0.22 * r + oy), (cx + 0.52 * r + ox, cy - 0.16 * r + oy), n=10)
                cc.pen_line(flag, color_key=ck, width=wd, boil_key=key + ck + "f")
            cc.white_ellipse(cx - 0.16 * r, cy + 0.36 * r, 0.26 * r, 0.22 * r, fill_key="white", ink_key="ink", width=2.3, boil_key=key + "_nh")

    elif k == "youtube":
        cc.white_box(cx - 1.08 * r, cy - 0.74 * r, 2.16 * r, 1.48 * r, corner_r=r * 0.34, ink_key="red" if accent else "ink", width=2.0, boil_key=key + "_bg", progress=progress)
        if progress > 0.35:
            tri = [(cx - 0.22 * r, cy - 0.34 * r), (cx - 0.22 * r, cy + 0.34 * r), (cx + 0.36 * r, cy)]
            cc.fill_poly(tri, "red" if accent else "ink", boil_key=key + "_yt", jitter=0.15)

    elif k == "discord":
        cc.white_box(cx - r, cy - r, 2 * r, 2 * r, corner_r=r * 0.32, width=1.9, boil_key=key + "_bg", progress=progress)
        if progress > 0.35:
            mask = [
                (cx - 0.52 * r, cy - 0.42 * r), (cx - 0.22 * r, cy - 0.52 * r), (cx - 0.14 * r, cy - 0.38 * r),
                (cx + 0.14 * r, cy - 0.38 * r), (cx + 0.22 * r, cy - 0.52 * r), (cx + 0.52 * r, cy - 0.42 * r),
                (cx + 0.66 * r, cy + 0.28 * r), (cx + 0.34 * r, cy + 0.48 * r), (cx + 0.22 * r, cy + 0.32 * r),
                (cx - 0.22 * r, cy + 0.32 * r), (cx - 0.34 * r, cy + 0.48 * r), (cx - 0.66 * r, cy + 0.28 * r),
            ]
            cc.fill_poly(mask, "soft_blue" if accent else "white", boil_key=key + "_dmf", jitter=0.18)
            cc.pen_line(mask, color_key="blue" if accent else "ink", width=1.8, boil_key=key + "_dm", closed=True, taper=False)
            cc.white_ellipse(cx - 0.24 * r, cy - 0.02 * r, 0.13 * r, 0.15 * r, fill_key="ink", ink_key=None, boil_key=key + "_de1")
            cc.white_ellipse(cx + 0.24 * r, cy - 0.02 * r, 0.13 * r, 0.15 * r, fill_key="ink", ink_key=None, boil_key=key + "_de2")

    elif k == "wechat":
        cc.white_ellipse(cx - 0.16 * r, cy - 0.14 * r, 0.72 * r, 0.58 * r, width=1.9, boil_key=key + "_wc1", progress=progress)
        if progress > 0.35:
            cc.white_ellipse(cx - 0.38 * r, cy - 0.24 * r, 0.08 * r, 0.08 * r, fill_key="ink", ink_key=None, boil_key=key + "_wce1")
            cc.white_ellipse(cx + 0.06 * r, cy - 0.24 * r, 0.08 * r, 0.08 * r, fill_key="ink", ink_key=None, boil_key=key + "_wce2")
            cc.white_ellipse(cx + 0.30 * r, cy + 0.24 * r, 0.58 * r, 0.46 * r, width=1.9, boil_key=key + "_wc2")
            cc.white_ellipse(cx + 0.14 * r, cy + 0.18 * r, 0.07 * r, 0.07 * r, fill_key="ink", ink_key=None, boil_key=key + "_wce3")
            cc.white_ellipse(cx + 0.46 * r, cy + 0.18 * r, 0.07 * r, 0.07 * r, fill_key="ink", ink_key=None, boil_key=key + "_wce4")

    elif k in ("terminal", "cli"):
        cc.white_box(cx - r, cy - 0.82 * r, 2 * r, 1.64 * r, corner_r=r * 0.24, width=2.0, boil_key=key + "_bg", progress=progress)
        if progress > 0.35:
            cc.pen_line([(cx - 0.52 * r, cy - 0.28 * r), (cx - 0.14 * r, cy + 0.02 * r), (cx - 0.52 * r, cy + 0.32 * r)], width=2.2, boil_key=key + "_gt", taper=False)
            if int(cc.t * 2.5) % 2 == 0:
                cc.pen_line([(cx + 0.02 * r, cy + 0.32 * r), (cx + 0.50 * r, cy + 0.32 * r)], color_key="mint_ink" if accent else "ink", width=2.4, boil_key=key + "_cur", taper=False)

    elif k == "git_pr":
        cc.white_box(cx - r, cy - r, 2 * r, 2 * r, corner_r=r * 0.28, width=1.9, boil_key=key + "_bg", progress=progress)
        if progress > 0.35:
            cc.pen_line([(cx - 0.38 * r, cy - 0.44 * r), (cx - 0.38 * r, cy + 0.44 * r)], width=2.0, boil_key=key + "_gp1", taper=False)
            branch = quad_bezier((cx - 0.38 * r, cy - 0.36 * r), (cx + 0.38 * r, cy - 0.36 * r), (cx + 0.38 * r, cy + 0.36 * r), n=10)
            cc.pen_line(branch, color_key="mint_ink" if accent else "ink", width=2.0, boil_key=key + "_gp2")
            for px_n, py_n in ((cx - 0.38 * r, cy - 0.48 * r), (cx - 0.38 * r, cy + 0.48 * r), (cx + 0.38 * r, cy + 0.44 * r)):
                cc.white_ellipse(px_n, py_n, 0.16 * r, 0.16 * r, width=1.8, boil_key=f"{key}_{int(px_n)}{int(py_n)}")

    elif k in ("crypto", "kline", "candlestick"):
        cc.white_box(cx - 1.05 * r, cy - 0.85 * r, 2.10 * r, 1.70 * r, corner_r=r * 0.24, width=1.9, boil_key=key + "_bg", progress=progress)
        if progress > 0.35:
            candles = [(-0.52, -0.10, 0.38, "white", "ink"), (0.0, -0.35, 0.18, "soft_mint", "mint_ink"), (0.52, -0.52, -0.02, "mint", "mint_ink")]
            for x_o, y_t, y_b, fk, ik in candles:
                kx = cx + x_o * r
                cc.pen_line([(kx, cy + (y_t - 0.22) * r), (kx, cy + (y_b + 0.22) * r)], color_key=ik, width=1.5, boil_key=f"{key}_wk{x_o}", taper=False)
                cc.white_box(kx - 0.16 * r, cy + y_t * r, 0.32 * r, (y_b - y_t) * r, fill_key=fk, ink_key=ik, width=1.6, corner_r=2.0, boil_key=f"{key}_cd{x_o}")


# =============================================================================
# PART 3: AUTHENTIC AI PRODUCT INTERACTION UI PROPS (`draw_ai_ui_prop` — 10 UIs)
# =============================================================================


def draw_official_app_icon(
    cc: CleanMintCanvas,
    kind: str,
    cx: float,
    cy: float,
    r: float = 30.0,
    t: float = 0.0,
    progress: float = 1.0,
    key: str = "appico",
):
    """
    Verified authentic vector hand-drawn icons for AI & social platforms:
    `notebooklm`, `gemini`, `flow`, `colab`, `claude`, `openai`/`chatgpt`/`codex`,
    `doubao`, `gmail`, `mail`/`outlook`, `chrome`/`browser`, `github`,
    `hermes`, `openclaw`, `grok`, `meta`, `instagram`, `facebook`, `threads`,
    `xianyu`, `xiaohongshu`.
    """
    if progress <= 0.02:
        return
    er = r * back_out(clamp(progress))
    k = kind.lower().strip()

    if k == "notebooklm":
        # Official NotebookLM: 3 bold eccentric semicircular arches sharing the left tangent foot!
        yb = cy + er * 0.50
        xl = cx - er * 0.96
        sw = max(3.5, er * 0.165)
        for ai, rad_f in enumerate((0.96, 0.67, 0.38)):
            rk = er * rad_f
            acx = xl + rk
            angs = np.linspace(math.pi, 0.0, 22, dtype=np.float32)
            pts = [(xl + sw * 0.14 * ai, yb + er * 0.08)]
            for a in angs:
                pts.append((acx + math.cos(a) * rk, yb - math.sin(a) * rk))
            pts.append((acx + rk, yb + er * 0.08))
            cc.pen_line(pts, color_key="ink", width=sw, boil_key=f"{key}_nla{ai}", jitter=0.14, taper=False)

    elif k == "gemini":
        # Official 2025/2026 Google Gemini freestanding 4-point concave sparkle star (each arm tip pure Google color: Red top, Blue left, Green bottom, Yellow right!)
        rs = er * 1.10
        k_in = rs * 0.18
        top_p, rgt_p, bot_p, lft_p = (cx, cy - rs), (cx + rs, cy), (cx, cy + rs), (cx - rs, cy)
        c_tr = quad_bezier(top_p, (cx + k_in, cy - k_in), rgt_p, 14)
        c_rb = quad_bezier(rgt_p, (cx + k_in, cy + k_in), bot_p, 14)
        c_bl = quad_bezier(bot_p, (cx - k_in, cy + k_in), lft_p, 14)
        c_lt = quad_bezier(lft_p, (cx - k_in, cy - k_in), top_p, 14)
        # Split at midpoint of each concave arc (index 7) so each sharp tip is 100% pure single color!
        m_tr, m_rb, m_bl, m_lt = 7, 7, 7, 7
        arm_top = [(cx, cy), *c_lt[m_lt:].tolist(), *c_tr[:m_tr + 1].tolist()]
        arm_rgt = [(cx, cy), *c_tr[m_tr:].tolist(), *c_rb[:m_rb + 1].tolist()]
        arm_bot = [(cx, cy), *c_rb[m_rb:].tolist(), *c_bl[:m_bl + 1].tolist()]
        arm_lft = [(cx, cy), *c_bl[m_bl:].tolist(), *c_lt[:m_lt + 1].tolist()]
        cc.fill_poly(arm_top, "g_red", boil_key=key + "_gat", jitter=0.08)
        cc.fill_poly(arm_rgt, "g_yellow", boil_key=key + "_gar", jitter=0.08)
        cc.fill_poly(arm_bot, "g_green", boil_key=key + "_gab", jitter=0.08)
        cc.fill_poly(arm_lft, "g_blue", boil_key=key + "_gal", jitter=0.08)
        full_star = np.vstack([c_tr[:-1], c_rb[:-1], c_bl[:-1], c_lt])
        cc.pen_line(full_star, color_key="ink", width=1.5, closed=True, taper=False, jitter=0.12, boil_key=key + "_gmo")

    elif k == "flow":
        # Official Google Labs Flow: dark squircle + luminous cyan-blue swirling vortex ring + crisp white `Flow`!
        cc.white_box(cx - er * 1.06, cy - er * 0.96, er * 2.12, er * 1.92, fill_key="cat_fill", ink_key="ink", corner_r=er * 0.40, width=2.0, boil_key=key + "_flbg")
        for si_f, (a0, a1, ck_f) in enumerate(((0.15, 2.85, "doubao_cyan"), (3.25, 5.95, "g_blue"))):
            angs = np.linspace(a0 + t * 0.6, a1 + t * 0.6, 16, dtype=np.float32)
            pts = [(cx + math.cos(a) * er * 0.74, cy + math.sin(a) * er * 0.66) for a in angs]
            cc.pen_line(pts, color_key=ck_f, width=max(3.0, er * 0.14), boil_key=f"{key}_flr{si_f}", jitter=0.12, taper=True)
        cc.hand_label("Flow", cx, cy + 1, size=max(16, int(er * 0.60)), color_key="white", organic=False, bold=True)

    elif k == "colab":
        # Official Google Colaboratory: freestanding interlocking golden-amber + deep-orange `CO` rings!
        rw = max(5.2, er * 0.28)
        lx, rx = cx - er * 0.50, cx + er * 0.46
        rr = er * 0.50
        for a_deg0, a_deg1, ck_c in ((52, 145, "colab_gold"), (145, 225, "colab_orange"), (225, 308, "colab_gold")):
            angs = np.linspace(math.radians(a_deg0), math.radians(a_deg1), 12, dtype=np.float32)
            pts = [(lx + math.cos(a) * rr, cy + math.sin(a) * rr) for a in angs]
            cc.pen_line(pts, color_key=ck_c, width=rw, boil_key=f"{key}_clc{a_deg0}", jitter=0.10, taper=False)
        for a_deg0, a_deg1, ck_c in ((-45, 135, "colab_orange"), (135, 315, "colab_gold")):
            angs = np.linspace(math.radians(a_deg0), math.radians(a_deg1), 16, dtype=np.float32)
            pts = [(rx + math.cos(a) * rr, cy + math.sin(a) * rr) for a in angs]
            cc.pen_line(pts, color_key=ck_c, width=rw, boil_key=f"{key}_clo{a_deg0}", jitter=0.10, taper=False)

    elif k == "claude":
        # Official Anthropic Claude 12-ray terracotta-coral asymmetric sunburst!
        ray_lens = (1.00, 0.74, 0.94, 0.70, 0.98, 0.76, 0.96, 0.72, 1.00, 0.75, 0.92, 0.74)
        rot0 = t * 0.35
        sw_c = max(2.4, er * 0.15)
        for ri, rl in enumerate(ray_lens):
            a = rot0 + ri * (math.pi * 2.0 / 12.0)
            cc.pen_line([(cx, cy), (cx + math.cos(a) * er * rl, cy + math.sin(a) * er * rl)], color_key="claude_coral", width=sw_c, boil_key=f"{key}_clr{ri}", jitter=0.10, taper=False)
        cc.white_ellipse(cx, cy, er * 0.28, er * 0.28, fill_key="claude_coral", ink_key=None, boil_key=key + "_clh")

    elif k in ("openai", "chatgpt", "codex"):
        bg_fill = "openai_green" if k == "chatgpt" else ("soft_blue" if k == "codex" else "white")
        fg_col = "white" if k == "chatgpt" else ("g_blue" if k == "codex" else "ink")
        cc.white_ellipse(cx, cy, er, er, fill_key=bg_fill, ink_key="ink" if k != "chatgpt" else "openai_green", width=1.9, boil_key=key + "_oabg")
        for li in range(6):
            ang = li * (math.pi / 3.0) + 0.26
            pcx = cx + math.cos(ang) * er * 0.30
            pcy = cy + math.sin(ang) * er * 0.30
            cc.white_ellipse(pcx, pcy, er * 0.38, er * 0.23, rot_deg=math.degrees(ang) + 30.0, fill_key=None, ink_key=fg_col, width=max(1.8, er * 0.085), boil_key=f"{key}_oap{li}")

    elif k == "doubao":
        for ri_d, (ang_d, ck_d) in enumerate(((-2.2, "doubao_violet"), (2.1, "g_blue"), (0.0, "doubao_cyan"))):
            angs = np.linspace(ang_d - 1.35, ang_d + 1.35, 14, dtype=np.float32)
            ox_d, oy_d = math.cos(ang_d) * er * 0.16, math.sin(ang_d) * er * 0.16
            pts = [(cx + ox_d + math.cos(a) * er * 0.72, cy + oy_d + math.sin(a) * er * 0.72) for a in angs]
            cc.pen_line(pts, color_key=ck_d, width=max(3.6, er * 0.26), boil_key=f"{key}_db{ri_d}", jitter=0.10, taper=True)

    elif k == "gmail":
        cc.white_box(cx - er * 1.12, cy - er * 0.84, er * 2.24, er * 1.68, fill_key="white", ink_key="ink_soft", corner_r=er * 0.24, width=1.8, boil_key=key + "_gmb")
        sw_m = max(3.6, er * 0.22)
        xl, xr = cx - er * 0.78, cx + er * 0.78
        yt, yb = cy - er * 0.50, cy + er * 0.54
        cc.pen_line([(xl, yb), (xl, yt + er * 0.12)], color_key="g_blue", width=sw_m, boil_key=key + "_gml", taper=False)
        cc.pen_line([(xr, yb), (xr, yt + er * 0.12)], color_key="g_green", width=sw_m, boil_key=key + "_gmr", taper=False)
        cc.pen_line([(cx + er * 0.34, yt + er * 0.26), (xr, yt)], color_key="g_yellow", width=sw_m, boil_key=key + "_gmy", taper=False)
        cc.pen_line([(xl, yt), (cx, cy + er * 0.18), (cx + er * 0.44, yt + er * 0.18)], color_key="g_red", width=sw_m, boil_key=key + "_gmv", taper=False)

    elif k in ("mail", "outlook"):
        is_ol = (k == "outlook")
        cc.white_box(cx - er * 1.10, cy - er * 0.80, er * 2.20, er * 1.60, fill_key="soft_blue" if is_ol else "white", ink_key="g_blue" if is_ol else "ink_detail", corner_r=er * 0.20, width=2.0, boil_key=key + "_mv")
        cc.pen_line([(cx - er * 1.04, cy - er * 0.72), (cx, cy + er * 0.12), (cx + er * 1.04, cy - er * 0.72)], color_key="g_blue" if is_ol else "ink_detail", width=2.1, boil_key=key + "_mfl", taper=False)

    elif k in ("chrome", "browser"):
        sw_ch = max(3.2, er * 0.24)
        for a0, a1, ck_ch in ((-150, -30, "g_red"), (-30, 90, "g_yellow"), (90, 210, "g_green")):
            angs = np.linspace(math.radians(a0), math.radians(a1), 12, dtype=np.float32)
            pts = [(cx + math.cos(a) * er * 0.76, cy + math.sin(a) * er * 0.76) for a in angs]
            cc.pen_line(pts, color_key=ck_ch, width=sw_ch, boil_key=f"{key}_chr{a0}", jitter=0.10, taper=False)
        cc.white_ellipse(cx, cy, er * 0.42, er * 0.42, fill_key="g_blue", ink_key="white", width=2.0, boil_key=key + "_chc")

    elif k == "github":
        draw_brand_icon(cc, "github", cx, cy, r=er, progress=1.0, key=key + "_gh")

    elif k == "hermes":
        # Nous Hermes dark circular badge with crisp white winged `H` caduceus crest!
        cc.white_ellipse(cx, cy, er, er, fill_key="cat_fill", ink_key="ink", width=2.0, boil_key=key + "_hbg")
        w_l = [(cx - er * 0.28, cy - er * 0.18), (cx - er * 0.76, cy - er * 0.52), (cx - er * 0.62, cy - er * 0.08)]
        w_r = [(cx + er * 0.28, cy - er * 0.18), (cx + er * 0.76, cy - er * 0.52), (cx + er * 0.62, cy - er * 0.08)]
        cc.fill_poly(w_l, "white", boil_key=key + "_hwl")
        cc.fill_poly(w_r, "white", boil_key=key + "_hwr")
        cc.hand_label("H", cx, cy + er * 0.10, size=max(16, int(er * 0.95)), color_key="white", organic=False, bold=True)

    elif k == "openclaw":
        # OpenClaw vibrant red lobster mascot with twin antennae, segmented tail & giant V-claw!
        cc.white_ellipse(cx - er * 0.22, cy + er * 0.44, er * 0.34, er * 0.26, fill_key="g_red", ink_key="ink", width=1.8, boil_key=key + "_ltl")
        cc.white_ellipse(cx - er * 0.20, cy + er * 0.04, er * 0.54, er * 0.44, fill_key="g_red", ink_key="ink", width=2.0, boil_key=key + "_lbd")
        cc.pen_line(quad_bezier((cx - er * 0.32, cy - er * 0.36), (cx - er * 0.46, cy - er * 0.80), (cx - er * 0.22, cy - er * 0.98), 8), color_key="g_red", width=2.4, boil_key=key + "_la1")
        cc.pen_line(quad_bezier((cx - er * 0.08, cy - er * 0.36), (cx - er * 0.04, cy - er * 0.80), (cx + er * 0.18, cy - er * 0.98), 8), color_key="g_red", width=2.4, boil_key=key + "_la2")
        claw = [
            (cx + er * 0.10, cy + er * 0.06), (cx + er * 0.58, cy - er * 0.72), (cx + er * 1.00, cy - er * 0.48),
            (cx + er * 0.52, cy - er * 0.08), (cx + er * 1.00, cy + er * 0.18), (cx + er * 0.56, cy + er * 0.56),
        ]
        cc.fill_poly(claw, "g_red", boil_key=key + "_lclf")
        cc.pen_line(claw, color_key="ink", width=2.0, closed=True, taper=False, boil_key=key + "_lcl")
        cc.white_ellipse(cx - er * 0.34, cy - er * 0.02, er * 0.10, er * 0.10, fill_key="white", ink_key=None, boil_key=key + "_le1")
        cc.white_ellipse(cx - er * 0.08, cy - er * 0.02, er * 0.10, er * 0.10, fill_key="white", ink_key=None, boil_key=key + "_le2")

    elif k == "grok":
        cc.white_box(cx - er, cy - er, er * 2.0, er * 2.0, fill_key="cat_fill", ink_key="ink", corner_r=er * 0.22, width=2.0, boil_key=key + "_gkbg")
        sw_g = max(2.6, er * 0.18)
        cc.pen_line([(cx - er * 0.56, cy - er * 0.32), (cx + er * 0.04, cy + er * 0.56)], color_key="white", width=sw_g, boil_key=key + "_gx1", taper=False)
        cc.pen_line([(cx - er * 0.54, cy + er * 0.56), (cx + er * 0.38, cy - er * 0.58)], color_key="white", width=sw_g, boil_key=key + "_gx2", taper=False)
        cc.pen_line([(cx + er * 0.44, cy - er * 0.46), (cx + er * 0.44, cy + er * 0.56)], color_key="white", width=sw_g, boil_key=key + "_gx3", taper=False)

    elif k == "meta":
        t_vals = np.linspace(0.0, math.pi * 2.0, 36, dtype=np.float32)
        pts = []
        for tv in t_vals:
            denom = 1.0 + math.sin(tv) ** 2
            px_m = cx + (er * 0.96 * math.cos(tv)) / denom
            py_m = cy + (er * 0.88 * math.sin(tv) * math.cos(tv)) / denom
            pts.append((px_m, py_m))
        cc.pen_line(pts, color_key="meta_blue", width=max(3.2, er * 0.18), closed=True, boil_key=key + "_meta", jitter=0.10, taper=False)

    elif k == "instagram":
        cc.white_box(cx - er, cy - er, er * 2.0, er * 2.0, fill_key="ig_pink", ink_key="ink", corner_r=er * 0.44, width=2.0, boil_key=key + "_igbg")
        cc.white_box(cx - er * 0.66, cy - er * 0.66, er * 1.32, er * 1.32, fill_key=None, ink_key="white", corner_r=er * 0.34, width=max(2.2, er * 0.11), boil_key=key + "_igin")
        cc.white_ellipse(cx, cy, er * 0.34, er * 0.34, fill_key=None, ink_key="white", width=max(2.2, er * 0.11), boil_key=key + "_igl")
        cc.white_ellipse(cx + er * 0.40, cy - er * 0.40, er * 0.09, er * 0.09, fill_key="white", ink_key=None, boil_key=key + "_igd")

    elif k == "facebook":
        cc.white_ellipse(cx, cy, er, er, fill_key="fb_blue", ink_key="ink", width=2.0, boil_key=key + "_fb")
        cc.hand_label("f", cx + er * 0.06, cy + er * 0.08, size=max(22, int(er * 1.45)), color_key="white", organic=False, bold=True)

    elif k == "threads":
        # Authentic Meta Threads black squircle + continuous `@` spiral (outer C-arch + inner `a` loop + right-side curl)!
        cc.white_box(cx - er, cy - er, er * 2.0, er * 2.0, fill_key="cat_fill", ink_key="ink", corner_r=er * 0.44, width=2.0, boil_key=key + "_thbg")
        sw_t = max(2.5, er * 0.135)
        outer_angs = np.linspace(0.35, math.pi * 1.78, 24, dtype=np.float32)
        outer_pts = [(cx + math.cos(a) * er * 0.64, cy - math.sin(a) * er * 0.68) for a in outer_angs]
        cc.pen_line(outer_pts, color_key="white", width=sw_t, boil_key=key + "_tho", jitter=0.10, taper=False)
        # Inner `a` arch + horizontal bowl
        top_a = quad_bezier((cx - er * 0.26, cy - er * 0.22), (cx + er * 0.14, cy - er * 0.44), (cx + er * 0.30, cy + er * 0.06), 12)
        cc.pen_line(top_a, color_key="white", width=sw_t, boil_key=key + "_tha", jitter=0.10, taper=False)
        cc.white_ellipse(cx - er * 0.02, cy + er * 0.14, er * 0.32, er * 0.22, fill_key=None, ink_key="white", width=sw_t, boil_key=key + "_thi")
        curl_r = quad_bezier((cx + er * 0.30, cy + er * 0.06), (cx + er * 0.36, cy + er * 0.42), (cx + er * 0.56, cy + er * 0.22), 8)
        cc.pen_line(curl_r, color_key="white", width=sw_t, boil_key=key + "_thc", jitter=0.10, taper=False)

    elif k == "xianyu":
        cc.white_box(cx - er, cy - er, er * 2.0, er * 2.0, fill_key="xianyu_yellow", ink_key="ink", corner_r=er * 0.38, width=2.2, boil_key=key + "_xy")
        cc.hand_label("闲鱼", cx, cy - er * 0.06, size=max(18, int(er * 0.68)), color_key="ink", organic=False, bold=True)
        wv = quad_bezier((cx + er * 0.04, cy + er * 0.54), (cx + er * 0.36, cy + er * 0.40), (cx + er * 0.68, cy + er * 0.54), 8)
        cc.pen_line(wv, color_key="ink", width=max(2.2, er * 0.09), boil_key=key + "_xyw", taper=False)

    elif k == "xiaohongshu":
        cc.white_box(cx - er, cy - er, er * 2.0, er * 2.0, fill_key="xhs_red", ink_key="ink", corner_r=er * 0.38, width=2.2, boil_key=key + "_xhs")
        cc.hand_label("小红书", cx, cy, size=max(15, int(er * 0.48)), color_key="white", organic=False, bold=True)


def draw_jolly_mascot(
    cc: CleanMintCanvas,
    cx: float,
    cy: float,
    r: float = 34.0,
    t: float = 0.0,
    progress: float = 1.0,
    key: str = "jolly",
):
    """
    Hand-drawn clean flat-shaded bold-ink portrait of Meta Muse's official mascot `Jolly` (`Jollybot`):
    Earless round cream-oatmeal fuzzy hood-suit silhouette, inset smooth oval face,
    wide-set black dot eyes, tiny smile + blush, holding a glowing `#2EE59D`/blue wish orb!
    """
    if progress <= 0.02:
        return
    s = r * back_out(clamp(progress))
    bob = math.sin(t * 2.4) * (s * 0.05)
    cy_b = cy + bob
    # Fuzzy earless pill/pear hood-suit body (`soft_orange` warm oatmeal-cream + soft organic jitter)
    cc.white_ellipse(cx, cy_b + s * 0.10, s * 0.88, s * 1.04, fill_key="soft_orange", ink_key="ink", width=2.0, boil_key=key + "_suit")
    # Stubby little plush legs at bottom
    cc.white_ellipse(cx - s * 0.34, cy_b + s * 1.04, s * 0.22, s * 0.16, fill_key="soft_orange", ink_key="ink", width=1.8, boil_key=key + "_lgL")
    cc.white_ellipse(cx + s * 0.34, cy_b + s * 1.04, s * 0.22, s * 0.16, fill_key="soft_orange", ink_key="ink", width=1.8, boil_key=key + "_lgR")
    # Inset smooth oval face cutout
    cc.white_ellipse(cx, cy_b - s * 0.32, s * 0.60, s * 0.44, fill_key="white", ink_key="ink_detail", width=1.6, boil_key=key + "_face")
    # Wide-set black dot eyes + rosy blush + tiny gentle `u` smile!
    for es in (-1.0, 1.0):
        cc.white_ellipse(cx + es * s * 0.26, cy_b - s * 0.36, s * 0.08, s * 0.10, fill_key="cat_line", ink_key=None, boil_key=f"{key}_ey{es}")
        cc.white_ellipse(cx + es * s * 0.36, cy_b - s * 0.22, s * 0.10, s * 0.06, fill_key="blush", ink_key=None, boil_key=f"{key}_bl{es}")
    cc.pen_line(quad_bezier((cx - s * 0.09, cy_b - s * 0.26), (cx, cy_b - s * 0.19), (cx + s * 0.09, cy_b - s * 0.26), 8), width=1.7, boil_key=key + "_sm")
    # Glowing translucent wish orb held in both chubby paws at tummy!
    orb_r = s * 0.32 * (1.0 + 0.06 * math.sin(t * 3.8))
    cc.white_ellipse(cx, cy_b + s * 0.36, orb_r, orb_r, fill_key="soft_mint", ink_key="mint_ink", width=2.0, boil_key=key + "_orb")
    cc.pen_line(quad_bezier((cx - orb_r * 0.6, cy_b + s * 0.32), (cx, cy_b + s * 0.20), (cx + orb_r * 0.6, cy_b + s * 0.42), 8), color_key="blue", width=1.8, boil_key=key + "_osw")
    # Chubby paws hugging left/right of the orb
    cc.white_ellipse(cx - orb_r * 1.05, cy_b + s * 0.36, s * 0.22, s * 0.16, fill_key="soft_orange", ink_key="ink", width=1.7, boil_key=key + "_pwL")
    cc.white_ellipse(cx + orb_r * 1.05, cy_b + s * 0.36, s * 0.22, s * 0.16, fill_key="soft_orange", ink_key="ink", width=1.7, boil_key=key + "_pwR")


def draw_ai_ui_prop(
    cc: CleanMintCanvas,
    kind: str,
    x: float,
    y: float,
    w: float,
    h: float,
    t: float = 0.0,
    active: bool = True,
    unplugged: bool = False,
    progress: float = 1.0,
    key: str = "ui",
):
    """
    Draw crisp flat-shaded bold-ink pure-white wireframes of 10 real AI product interfaces:
    - `cursor`: File tree + code editor + `#2EE59D` ghost-text `[Tab]` completion + bottom `Composer · Agent` bar
    - `claude_code`: `╭─ * Claude Code ─╮` TUI + `Plan Mode (Shift+Tab)` + `Subagents` + `+/-` diff + `>` prompt
    - `chatgpt`: Left sidebar + 6-loop knot emblem + rounded composer pill with voice bars & `↑` send
    - `chatgpt_canvas`: Split-view left chat + right live `Canvas` code/doc editor with floating `[Fix bugs]` pill
    - `deepseek_r1`: Whale badge + collapsible `>> 已深度思考 (12s)` CoT reasoning block + crisp output
    - `mcp_hub`: "USB-C for AI" universal multi-port dock snapping `GitHub` / `Browser` / `DB` plugs into Agent
    - `doubao`: Browser window + docked right-hand Doubao sidebar (`Alt+K`) + quick chips + mic pill
    - `muse`: Top-anchored animated Muse avatar + proactive feed cards + `Muse Secure VM` approval bar
    - `grok_bot`: Orbital `Ø` mark + 3 Bot avatars + split-pane chat & shared cloud PC + weekly quota bar
    - `agent_cli`: `>_ Agent CLI` headless tiling TUI + instant main chat (`秒回`) + parallel `[BG]` slots
    """
    if progress <= 0.02:
        return
    k = kind.lower().strip()

    if k == "cursor":
        cc.white_box(x, y, w, h, corner_r=9.0, width=2.2, boil_key=key + "_win", progress=progress)
        if progress > 0.35:
            # Top IDE tab bar
            cc.pen_line([(x + 4, y + 28), (x + w - 4, y + 28)], width=1.4, boil_key=key + "_tb", taper=False)
            cc.white_box(x + 12, y + 6, 108, 22, fill_key="soft_mint", ink_key="mint_ink", corner_r=4.0, width=1.4, boil_key=key + "_tab")
            cc.hand_label("Cursor IDE", x + 66, y + 17, size=14, color_key="mint_ink", organic=False, bold=True)
            # Left narrow file tree
            ft_x = x + w * 0.22
            cc.pen_line([(ft_x, y + 28), (ft_x, y + h - 38)], color_key="ink_soft", width=1.3, boil_key=key + "_ft", taper=False)
            for fi in range(4):
                cc.pen_line([(x + 12, y + 44 + fi * 18), (ft_x - 10, y + 44 + fi * 18)], color_key="ink_detail", width=1.4, boil_key=f"{key}_fl{fi}", taper=False)
            # Code lines + animated Ghost-Text Inline `Tab` Autocomplete!
            ed_x = ft_x + 14
            cc.pen_line([(ed_x, y + 46), (ed_x + w * 0.32, y + 46)], color_key="ink", width=2.0, boil_key=key + "_c1", taper=False)
            ghost_reveal = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(t * 4.5)) if active else 0.7
            gw = (w * 0.44) * ghost_reveal
            cc.white_box(ed_x + 12, y + 60, w * 0.50, 24, fill_key="pale_mint", ink_key=None, corner_r=4.0, boil_key=key + "_ghbg")
            cc.dashed_line((ed_x + 16, y + 72), (ed_x + 16 + gw, y + 72), dash_len=8.0, gap_len=5.0, color_key="mint_ink", width=2.1, boil_key=key + "_ghl")
            # Crisp `[Tab]` badge right next to ghost completion!
            tb_x = min(x + w - 58, ed_x + 24 + gw)
            cc.white_box(tb_x, y + 61, 44, 21, fill_key="mint", ink_key="ink", corner_r=5.0, width=1.6, boil_key=key + "_tbdg")
            cc.hand_label("Tab", tb_x + 22, y + 71, size=13, color_key="ink", organic=False, bold=True)
            # Bottom floating `Composer · Agent` multi-file bar
            cc.white_box(ed_x, y + h - 36, w - (ed_x - x) - 14, 26, fill_key="white", ink_key="ink", corner_r=7.0, width=1.6, boil_key=key + "_cmp")
            cc.hand_label("Composer · 多文件改码 ✓", ed_x + (w - (ed_x - x) - 14) * 0.5, y + h - 23, size=13, color_key="ink_detail", organic=False)

    elif k == "claude_code":
        cc.white_box(x, y, w, h, corner_r=8.0, width=2.2, boil_key=key + "_tui", progress=progress)
        if progress > 0.35:
            cc.white_box(x + 10, y + 10, w - 20, 32, fill_key="soft_orange", ink_key="orange", corner_r=6.0, width=1.8, boil_key=key + "_hdr")
            draw_official_app_icon(cc, "claude", x + 28, y + 26, r=12.5, t=t, key=key + "_clico")
            cc.hand_label("Claude Code", x + 112, y + 26, size=21, color_key="orange", organic=False, bold=True)
            # `Plan Mode` pill (`Shift+Tab`)!
            cc.white_box(x + w - 96, y + 15, 78, 22, fill_key="soft_mint", ink_key="mint_ink", corner_r=5.0, width=1.4, boil_key=key + "_plp")
            cc.hand_label("Plan", x + w - 57, y + 26, size=18, color_key="mint_ink", organic=False, bold=True)

            # Subagent parallel dispatch line + +/- Diff lines
            cc.white_ellipse(x + 20, y + 56, 4.0, 4.0, fill_key="mint", ink_key="mint_ink", width=1.2, boil_key=key + "_blt")
            cc.hand_label("3 Subagents 并行", x + 132, y + 58, size=19, bold=True, color_key="ink", organic=False)
            cc.pen_line([(x + 24, y + 76), (x + w - 42, y + 76)], color_key="red", width=2.0, boil_key=key + "_dfm", taper=False)
            cc.pen_line([(x + 24, y + 90), (x + w - 22, y + 90)], color_key="mint_ink", width=2.2, boil_key=key + "_dfp", taper=False)

            # Thinking / Prompt bar at bottom
            cc.white_box(x + 12, y + 102, w - 24, 24, fill_key="soft_purple", ink_key="purple", corner_r=5.0, width=1.3, boil_key=key + "_thk")
            cc.hand_label("Ultrathink 深度推理", x + w * 0.5, y + 114, size=18, bold=True, color_key="purple", organic=False)
            cc.pen_line([(x + 16, y + h - 20), (x + 23, y + h - 14), (x + 16, y + h - 8)], color_key="orange", width=2.0, boil_key=key + "_chv", taper=False)
            if int(t * 2.5) % 2 == 0:
                cc.pen_line([(x + 30, y + h - 9), (x + 44, y + h - 9)], width=2.0, boil_key=key + "_cur", taper=False)

    elif k in ("chatgpt_canvas", "canvas"):
        cc.white_box(x, y, w, h, corner_r=10.0, width=2.1, boil_key=key + "_win", progress=progress)
        if progress > 0.35:
            mid_c = x + w * 0.38
            cc.pen_line([(mid_c, y + 8), (mid_c, y + h - 8)], width=1.6, boil_key=key + "_div", taper=False)
            # Left chat column
            cc.hand_label("Chat", x + (mid_c - x) * 0.5, y + 24, size=15, color_key="ink_detail", organic=False, bold=True)
            cc.white_box(x + 12, y + 40, mid_c - x - 24, 28, corner_r=8.0, width=1.4, boil_key=key + "_cb1")
            cc.white_box(x + 12, y + h - 34, mid_c - x - 24, 22, corner_r=10.0, width=1.5, boil_key=key + "_cinp")
            # Right live Canvas editor pane
            cc.white_box(mid_c + 10, y + 12, x + w - mid_c - 20, h - 24, fill_key="pale_mint", ink_key="mint_ink", corner_r=7.0, width=1.7, boil_key=key + "_cvp")
            cc.hand_label("Canvas 实时画布", mid_c + (x + w - mid_c) * 0.5, y + 28, size=14, color_key="mint_ink", organic=False, bold=True)
            for li in range(3):
                lw = (x + w - mid_c - 44) * (0.85 if li != 1 else 0.62)
                cc.pen_line([(mid_c + 22, y + 52 + li * 20), (mid_c + 22 + lw, y + 52 + li * 20)], color_key="ink", width=1.7, boil_key=f"{key}_cl{li}", taper=False)
            pop_dy = math.sin(t * 4.5) * 2.5 if active else 0.0
            cc.white_box(x + w - 92, y + h - 42 + pop_dy, 74, 22, fill_key="mint", ink_key="ink", corner_r=9.0, width=1.5, boil_key=key + "_fx")
            cc.hand_label("+ 润色 / 修Bug", x + w - 55, y + h - 31 + pop_dy, size=11, color_key="ink", organic=False, bold=True)

    elif k in ("deepseek_r1", "deepseek"):
        cc.white_box(x, y, w, h, corner_r=10.0, width=2.1, boil_key=key + "_win", progress=progress)
        if progress > 0.35:
            cc.white_ellipse(x + 26, y + 24, 11.0, 8.0, fill_key="soft_blue", ink_key="blue", width=1.7, boil_key=key + "_whl")
            cc.hand_label("DeepSeek-R1", x + 102, y + 24, size=16, color_key="blue", organic=False, bold=True)
            # Signature collapsible grey-blue `已深度思考 (用时 12s)` CoT block!
            cc.white_box(x + 14, y + 44, w - 28, 56, fill_key="soft_blue", ink_key="blue", corner_r=6.0, width=1.5, boil_key=key + "_cot")
            cc.pen_line([(x + 22, y + 52), (x + 22, y + 92)], color_key="blue", width=2.6, boil_key=key + "_cotb", taper=False)
            cc.hand_label(">> 已深度思考 (12s)", x + 108, y + 58, size=13, color_key="blue", organic=False, bold=True)
            cc.pen_line([(x + 30, y + 78), (x + w - 34, y + 78)], color_key="ink_detail", width=1.4, boil_key=key + "_ctl1", taper=False)
            # Final crisp answer below
            cc.pen_line([(x + 18, y + 116), (x + w - 24, y + 116)], color_key="mint_ink", width=2.2, boil_key=key + "_ans1", taper=False)
            cc.pen_line([(x + 18, y + 132), (x + w * 0.68, y + 132)], color_key="ink", width=1.8, boil_key=key + "_ans2", taper=False)

    elif k in ("mcp_hub", "mcp"):
        # Model Context Protocol: "USB-C for AI" universal multi-port dock!
        cc.white_box(x, y + h * 0.28, w * 0.52, h * 0.56, fill_key="soft_mint", ink_key="mint_ink", corner_r=10.0, width=2.3, boil_key=key + "_dock", progress=progress)
        if progress > 0.35:
            cc.hand_label("MCP 万能坞", x + w * 0.26, y + h * 0.46, size=17, color_key="mint_ink", organic=False, bold=True)
            cc.hand_label("USB-C for AI", x + w * 0.26, y + h * 0.66, size=13, color_key="ink_detail", organic=False)
            plugs = [("GitHub", 0.36), ("Browser", 0.56), ("SQL/Docs", 0.76)]
            snap = ease_out(0.55 + 0.45 * math.sin(t * 3.2)) if active else 1.0
            for pi, (plbl, py_f) in enumerate(plugs):
                py_p = y + h * py_f
                gap = (1.0 - snap) * 14.0 if pi == 1 else 0.0
                px_p = x + w * 0.52 + 8.0 + gap
                # USB-C metal tip + plug body
                cc.white_box(px_p - 8, py_p - 5, 10, 10, fill_key="mint", ink_key="ink", corner_r=2.0, width=1.4, boil_key=f"{key}_tip{pi}")
                cc.white_box(px_p + 2, py_p - 10, w * 0.40, 20, fill_key="white", ink_key="ink", corner_r=5.0, width=1.6, boil_key=f"{key}_plg{pi}")
                cc.hand_label(plbl, px_p + 2 + w * 0.20, py_p, size=12, color_key="ink", organic=False, bold=True)

    elif k == "chatgpt":
        cc.white_box(x, y, w, h, corner_r=10.0, width=2.1, boil_key=key + "_win", progress=progress)
        if progress > 0.35:
            sb_x = x + w * 0.22
            cc.pen_line([(sb_x, y + 4), (sb_x, y + h - 4)], color_key="ink_detail", width=1.3, boil_key=key + "_sb", taper=False)
            for si in range(3):
                cc.pen_line([(x + 12, y + 26 + si * 18), (sb_x - 10, y + 26 + si * 18)], color_key="ink_detail", width=1.3, boil_key=f"{key}_sl{si}", taper=False)
            kcx, kcy = x + w * 0.61, y + h * 0.27
            draw_official_app_icon(cc, "chatgpt", kcx, kcy, r=20.0, t=t, key=key + "_oaico")
            cc.hand_label("ChatGPT", kcx, y + h * 0.52, size=22, bold=True, color_key="ink", organic=False)
            px, py, pw, ph = sb_x + 14, y + h - 42, w * 0.78 - 26, 30
            cc.white_box(px, py, pw, ph, corner_r=14.0, width=1.8, boil_key=key + "_pill")
            for wi in range(4):
                wh = 4.0 + (abs(math.sin(t * 7.0 + wi * 1.1)) * 7.0 if active else 2.0)
                wx_b = px + pw - 52 + wi * 6
                cc.pen_line([(wx_b, py + 15 - wh * 0.5), (wx_b, py + 15 + wh * 0.5)], color_key="ink_detail", width=1.6, boil_key=f"{key}_wv{wi}", taper=False)
            scx, scy = px + pw - 16, py + 15
            cc.white_ellipse(scx, scy, 9.5, 9.5, fill_key="cat_fill", ink_key="cat_line", width=1.3, boil_key=key + "_snd")
            cc.pen_line([(scx, scy + 4), (scx, scy - 4)], color_key="white", width=1.7, boil_key=key + "_sa1", taper=False)

    elif k == "doubao":
        cc.white_box(x, y, w, h, corner_r=9.0, width=2.1, boil_key=key + "_win", progress=progress)
        if progress > 0.35:
            cc.pen_line([(x + 4, y + 24), (x + w - 4, y + 24)], width=1.4, boil_key=key + "_tb", taper=False)
            sp_x = x + w * 0.52
            cc.pen_line([(sp_x, y + 24), (sp_x, y + h - 4)], width=1.7, boil_key=key + "_sp", taper=False)
            cc.white_box(x + 14, y + 42, sp_x - x - 28, 16, fill_key="soft_blue", ink_key="blue", width=1.2, corner_r=3.0, boil_key=key + "_sel")
            av_x, av_y = sp_x + 24, y + 44
            draw_official_app_icon(cc, "doubao", av_x, av_y, r=14.0, t=t, key=key + "_dbico")
            cc.hand_label("豆包侧栏", sp_x + (x + w - sp_x) * 0.58, y + 44, size=20, bold=True, color_key="blue", organic=False)
            cc.white_box(sp_x + 10, y + h - 34, x + w - sp_x - 20, 24, corner_r=11.0, ink_key="blue", width=1.6, boil_key=key + "_inp")
        if unplugged:
            sway = math.sin(t * 3.4) * 7.0
            cord = cubic_bezier((x + 26, y + h), (x + 18 + sway, y + h + 28), (x + 38 + sway, y + h + 44), (x + 52 + sway, y + h + 52), 14)
            cc.pen_line(cord, width=1.9, boil_key=key + "_crd")
            cc.white_box(x + 48 + sway, y + h + 46, 16, 13, fill_key="red", ink_key="ink", width=1.5, boil_key=key + "_plg")

    elif k == "muse":
        # Borderless-feel vertical Meta Muse card starring authentic Jolly mascot + zero-config wish input + Secure VM Sentinel!
        cc.white_box(x, y, w, h, corner_r=18.0, width=2.2, ink_key="mint_ink", boil_key=key + "_card", progress=progress)
        if progress > 0.35:
            draw_jolly_mascot(cc, x + w * 0.5, y + 58, r=35.0, t=t, key=key + "_jolly")
            draw_official_app_icon(cc, "meta", x + w * 0.5 - 118, y + 118, r=15.0, t=t, key=key + "_mico")
            cc.hand_label("Meta Muse · Jolly", x + w * 0.5 + 16, y + 118, size=23, bold=True, color_key="ink", organic=False)
            cc.white_box(x + 22, y + 146, w - 44, 52, fill_key="pale_mint", ink_key="mint_ink", corner_r=22.0, width=1.9, boil_key=key + "_wishinp")
            cc.hand_label("对着聊天框许愿...", x + w * 0.5, y + 172, size=20, bold=True, color_key="mint_ink", organic=False)
            cc.white_box(x + 22, y + 214, w - 44, 46, fill_key="white", ink_key="ink_detail", corner_r=10.0, width=1.6, boil_key=key + "_actc")
            cc.hand_label("零配置按钮 · 后台全消化 ✓", x + w * 0.5, y + 237, size=19, bold=True, color_key="ink", organic=False)
            cc.white_box(x + 18, y + h - 56, w - 36, 40, fill_key="soft_mint", ink_key="mint_ink", corner_r=9.0, width=1.9, boil_key=key + "_vm")
            cc.hand_label("Muse Secure VM · Sentinel", x + w * 0.5, y + h - 36, size=18, bold=True, color_key="mint_ink", organic=False)

    elif k == "grok_bot":
        cc.white_box(x, y, w, h, corner_r=10.0, width=2.1, boil_key=key + "_win", progress=progress)
        if progress > 0.35:
            cc.pen_line([(x + 4, y + 36), (x + w - 4, y + 36)], width=1.5, boil_key=key + "_hdr", taper=False)
            draw_official_app_icon(cc, "grok", x + 26, y + 18, r=12.5, t=t, key=key + "_gkico")
            cc.hand_label("Grok Bot", x + 104, y + 18, size=21, bold=True, color_key="ink", organic=False)
            sp_g = x + w * 0.38
            cc.pen_line([(sp_g, y + 36), (sp_g, y + h - 34)], width=1.5, boil_key=key + "_gsp", taper=False)
            vm_x, vm_y, vm_w, vm_h = sp_g + 10, y + 46, x + w - sp_g - 20, h - 90
            cc.white_box(vm_x, vm_y, vm_w, vm_h, corner_r=5.0, width=1.6, boil_key=key + "_cvm")
            cc.hand_label("共享云电脑", vm_x + vm_w * 0.5, vm_y + 22, size=18, bold=True, color_key="ink_detail", organic=False)

    elif k in ("agent_cli", "personal_agent", "pi_cli", "cli_tui"):
        cc.white_box(x, y, w, h, corner_r=9.0, width=2.3, boil_key=key + "_tui", progress=progress)
        if progress > 0.35:
            cc.white_box(x + 8, y + 8, w - 16, 30, fill_key="soft_mint", ink_key="mint_ink", corner_r=5.0, width=1.6, boil_key=key + "_top")
            cc.hand_label(">_ Agent CLI", x + 88, y + 23, size=17, color_key="mint_ink", organic=False, bold=True)
            mid_x = x + w * 0.45
            cc.pen_line([(mid_x, y + 42), (mid_x, y + h - 10)], width=1.7, boil_key=key + "_div", taper=False)
            cc.hand_label("> 主对话秒回", x + (mid_x - x) * 0.5, y + 66, size=15, color_key="ink", organic=False)
            cc.white_box(x + 14, y + 86, mid_x - x - 28, 26, fill_key="soft_mint", ink_key="mint_ink", corner_r=6.0, width=1.5, boil_key=key + "_fast")
            cc.hand_label("12ms 零阻塞", x + (mid_x - x) * 0.5, y + 99, size=13, color_key="mint_ink", organic=False, bold=True)
            for si, (stxt, scol, sfill) in enumerate([("BG#1 全链扫描", "mint_ink", "soft_mint"), ("BG#2 写文件审批 ✓", "orange", "soft_orange")]):
                sy_b = y + 52 + si * 48
                cc.white_box(mid_x + 12, sy_b, x + w - mid_x - 24, 38, fill_key=sfill, ink_key=scol, corner_r=6.0, width=1.6, boil_key=f"{key}_bg{si}")
                cc.hand_label(stxt, mid_x + (x + w - mid_x) * 0.52, sy_b + 19, size=13, color_key=scol, organic=False)


# =============================================================================
# PART 4: AI ENGINEERING PARADIGM DIAGRAMS (`draw_ai_method_prop` — 6 Methods)
# =============================================================================
def draw_ai_method_prop(
    cc: CleanMintCanvas,
    kind: str,
    x: float,
    y: float,
    w: float,
    h: float,
    t: float = 0.0,
    progress: float = 1.0,
    key: str = "mth",
):
    """
    Procedural hand-drawn diagrams explaining core AI engineering methods:
    - `prompt_caching`: Padlocked `#2EE59D` static `KV Cache` prefix (`90% 省钱提速`) + small live query tail
    - `context_compaction`: Funnel compressing bloated history scroll into a crisp `#2EE59D` `Handoff.md` baton
    - `rag_pipeline`: Magnet pulling top-K `#2EE59D` chunks from Vector DB drawer into Prompt
    - `harness_layers`: Concentric `Prompt ⊂ Context ⊂ Harness 护栏闭环` engineering architecture
    - `subagent_fanout`: Lead Agent splitting tasks to 3 parallel Worker Subagents & merging `✓`
    - `speculative_decoding`: Speedy `Draft 小模型` guessing 4 tokens ahead + `Verifier 大模型` batch stamping `✓`
    """
    if progress <= 0.02:
        return
    k = kind.lower().strip()

    if k in ("prompt_caching", "kv_cache"):
        cc.white_box(x, y, w, h, corner_r=10.0, width=2.1, boil_key=key + "_card", progress=progress)
        if progress > 0.35:
            cc.hand_label("Prompt Caching 前缀缓存", x + w * 0.5, y + 24, size=16, color_key="ink", organic=False, bold=True)
            # Locked static prefix block (72% width) + live dynamic tail (22% width)
            bx, by, bh_b = x + 16, y + 48, h - 68
            lw = (w - 40) * 0.70
            rw = (w - 40) * 0.26
            cc.white_box(bx, by, lw, bh_b, fill_key="soft_mint", ink_key="mint_ink", corner_r=7.0, width=2.0, boil_key=key + "_pfx")
            # Hand-drawn padlock icon
            lkx, lky = bx + 26, by + bh_b * 0.5 + 4
            cc.white_box(lkx - 10, lky - 6, 20, 16, fill_key="mint", ink_key="ink", corner_r=3.0, width=1.6, boil_key=key + "_lk")
            cc.pen_line(quad_bezier((lkx - 6, lky - 6), (lkx, lky - 18), (lkx + 6, lky - 6), 8), width=1.8, boil_key=key + "_lka")
            cc.hand_label("固定前缀 HIT · 省90%", bx + lw * 0.56, by + bh_b * 0.5, size=14, color_key="mint_ink", organic=False, bold=True)
            cc.white_box(bx + lw + 8, by, rw, bh_b, fill_key="soft_orange", ink_key="orange", corner_r=7.0, width=1.7, boil_key=key + "_dyn")
            cc.hand_label("新提问", bx + lw + 8 + rw * 0.5, by + bh_b * 0.5, size=13, color_key="orange", organic=False, bold=True)

    elif k in ("harness_layers", "harness"):
        cx, cy = x + w * 0.5, y + h * 0.54
        rx_o, ry_o = w * 0.46, h * 0.42
        cc.white_ellipse(cx, cy, rx_o, ry_o, fill_key="pale_mint", ink_key="mint_ink", width=2.2, boil_key=key + "_r3", progress=progress)
        if progress > 0.35:
            cc.white_ellipse(cx, cy + 8, rx_o * 0.68, ry_o * 0.66, fill_key="white", ink_key="blue", width=1.8, boil_key=key + "_r2")
            cc.white_ellipse(cx, cy + 14, rx_o * 0.36, ry_o * 0.36, fill_key="soft_orange", ink_key="orange", width=1.7, boil_key=key + "_r1")
            cc.hand_label("Harness 护栏·缓存·工具闭环", cx, cy - ry_o + 18, size=14, color_key="mint_ink", organic=False, bold=True)
            cc.hand_label("Context 上下文装配", cx, cy - ry_o * 0.40, size=13, color_key="blue", organic=False, bold=True)
            cc.hand_label("Prompt", cx, cy + 14, size=13, color_key="orange", organic=False, bold=True)
            ang = t * 2.2
            ox, oy = cx + math.cos(ang) * rx_o * 0.92, cy + math.sin(ang) * ry_o * 0.92
            cc.white_ellipse(ox, oy, 10, 10, fill_key="mint", ink_key="ink", width=1.5, boil_key=key + "_orb")

    elif k in ("context_compaction", "handoff"):
        cc.white_box(x, y, w, h, corner_r=10.0, width=2.0, boil_key=key + "_bg", progress=progress)
        if progress > 0.35:
            # Funnel squeezing bloated scroll on left -> crisp Handoff baton on right!
            fn = [(x + w * 0.34, y + 22), (x + w * 0.56, y + h * 0.42), (x + w * 0.56, y + h * 0.58), (x + w * 0.34, y + h - 22)]
            cc.fill_poly(fn, "soft_mint", boil_key=key + "_fnf")
            cc.pen_line(fn, color_key="mint_ink", width=2.0, closed=True, taper=False, boil_key=key + "_fn")
            for li in range(4):
                cc.pen_line([(x + 16, y + 32 + li * 20), (x + w * 0.30, y + 36 + li * 18)], color_key="ink_detail", width=1.8, boil_key=f"{key}_sl{li}")
            cc.white_box(x + w * 0.62, y + h * 0.36, w * 0.32, h * 0.28, fill_key="mint", ink_key="ink", corner_r=6.0, width=1.9, boil_key=key + "_ho")
            cc.hand_label("Handoff 精华", x + w * 0.78, y + h * 0.50, size=13, color_key="ink", organic=False, bold=True)

    elif k == "rag_pipeline":
        cc.white_box(x, y, w, h, corner_r=10.0, width=2.0, boil_key=key + "_bg", progress=progress)
        if progress > 0.35:
            cc.white_box(x + 14, y + 26, w * 0.30, h - 42, corner_r=6.0, width=1.8, boil_key=key + "_db")
            cc.hand_label("向量库", x + 14 + w * 0.15, y + 46, size=14, color_key="ink", organic=False, bold=True)
            u_pull = (t * 1.1) % 1.0
            cx_d = lerp(x + w * 0.36, x + w * 0.64, ease_out(u_pull))
            cc.white_box(cx_d, y + h * 0.40, 44, 26, fill_key="soft_mint", ink_key="mint_ink", corner_r=4.0, width=1.6, boil_key=key + "_doc")
            cc.hand_label("Top-K", cx_d + 22, y + h * 0.40 + 13, size=11, color_key="mint_ink", organic=False, bold=True)
            cc.white_box(x + w * 0.68, y + 26, w * 0.26, h - 42, fill_key="soft_mint", ink_key="mint_ink", corner_r=6.0, width=1.8, boil_key=key + "_ag")
            cc.hand_label("精准回答", x + w * 0.81, y + h * 0.52, size=13, color_key="mint_ink", organic=False, bold=True)

    elif k == "subagent_fanout":
        cc.white_box(x, y, w, h, corner_r=10.0, width=2.0, boil_key=key + "_bg", progress=progress)
        if progress > 0.35:
            cc.white_box(x + 14, y + h * 0.36, w * 0.26, h * 0.28, fill_key="cat_fill", ink_key="cat_line", corner_r=6.0, width=1.8, boil_key=key + "_ld")
            cc.hand_label("主 Agent", x + 14 + w * 0.13, y + h * 0.50, size=13, color_key="mint", organic=False, bold=True)
            for wi, wlbl in enumerate(("搜文档", "改代码", "跑测试")):
                wy = y + 18 + wi * ((h - 30) / 3.0)
                cc.flow_arrow((x + 16 + w * 0.26, y + h * 0.50), (x + w * 0.54, wy + 14), arch_h=(wi - 1) * 12.0, color_key="mint_ink", width=2.0, boil_key=f"{key}_fa{wi}")
                cc.white_box(x + w * 0.56, wy, w * 0.36, 28, fill_key="soft_mint", ink_key="mint_ink", corner_r=5.0, width=1.5, boil_key=f"{key}_wk{wi}")
                cc.hand_label(f"{wlbl} ✓", x + w * 0.74, wy + 14, size=12, color_key="mint_ink", organic=False, bold=True)

    elif k == "speculative_decoding":
        cc.white_box(x, y, w, h, corner_r=10.0, width=2.0, boil_key=key + "_bg", progress=progress)
        if progress > 0.35:
            cc.hand_label("投机解码 · 小模型狂猜 + 大模型批改 ✓", x + w * 0.5, y + 24, size=14, color_key="ink", organic=False, bold=True)
            for ti_k in range(4):
                tx_k = x + 22 + ti_k * ((w - 44) / 4.0)
                stamped = ((int(t * 4.0) % 5) > ti_k)
                cc.white_box(tx_k, y + 48, (w - 68) / 4.0, h - 66, fill_key="soft_mint" if stamped else "white", ink_key="mint_ink" if stamped else "ink_detail", corner_r=6.0, width=1.7, boil_key=f"{key}_tk{ti_k}")
                cc.hand_label("✓" if stamped else "猜..", tx_k + (w - 68) / 8.0, y + 48 + (h - 66) * 0.5, size=16, color_key="mint_ink" if stamped else "ink_detail", organic=False, bold=True)


# =============================================================================
# PART 5: PLAYFUL AI SLANG / JARGON VISUAL GAGS (`draw_ai_jargon_prop` — 7 Gags)
# =============================================================================
def draw_ai_jargon_prop(
    cc: CleanMintCanvas,
    kind: str,
    cx: float,
    cy: float,
    scale: float = 1.0,
    t: float = 0.0,
    progress: float = 1.0,
    key: str = "jrg",
):
    """
    Playful flat-shaded bold-ink visual gag props explaining popular AI developer slang ("AI 黑话"):
    - `gacha_roll` (`抽卡式编程`): 3-reel slot machine (`报错` | `重写` | `SSR 跑通`) + animated pull lever
    - `vibe_coding` (`Vibe Coding 氛围编程`): Wobbling Jenga tower of `Bug / 屎山` blocks held up by `[Tab]`
    - `hallucination` (`AI 幻觉 · 一本正经胡说`): Floating dreamy soap bubbles with `1+1=5` & `胡编API()`
    - `context_rot` (`Context Rot 上下文降智区`): Crisp top whiteboard melting into murky grey scribbles at bottom
    - `token_assassin` (`Token 刺客 / 烧钱表`): Wildly spinning `$ Token` meter + flying bills
    - `alchemy_distill` (`炼丹与蒸馏`): Bubbling `GPU 炼丹炉` dripping pure `#2EE59D` drops into a mini flask
    - `agent_loop` (`鬼打墙死循环`): Spinning ouroboros wheel `报错 -> 道歉 -> 再报错`
    """
    if progress <= 0.02:
        return
    k = kind.lower().strip()
    s = scale

    if k == "gacha_roll":
        bw, bh = 210 * s, 168 * s
        bx, by = cx - bw * 0.5, cy - bh * 0.5
        cc.white_box(bx, by, bw, bh, fill_key="white", ink_key="ink", corner_r=12.0 * s, width=2.3, boil_key=key + "_cab", progress=progress)
        if progress > 0.35:
            cc.white_box(bx + 14 * s, by + 12 * s, bw - 28 * s, 30 * s, fill_key="soft_orange", ink_key="orange", corner_r=6.0 * s, width=1.7, boil_key=key + "_top")
            cc.hand_label("[SSR] 抽卡式编程", cx, by + 27 * s, size=max(12, int(16 * s)), color_key="orange", organic=False, bold=True)
            reels = [("报错", "red", "soft_red"), ("重写", "ink_detail", "white"), ("SSR!", "mint_ink", "soft_mint")]
            rw = (bw - 38 * s) / 3.0
            for ri, (rtxt, rcol, rfill) in enumerate(reels):
                rx_i = bx + 14 * s + ri * (rw + 5 * s)
                jy = math.sin(t * 16.0 + ri * 2.1) * 4.5 * s
                cc.white_box(rx_i, by + 54 * s, rw, 66 * s, fill_key=rfill, ink_key=rcol, corner_r=5.0 * s, width=1.8, boil_key=f"{key}_rl{ri}")
                cc.hand_label(rtxt, rx_i + rw * 0.5, by + 87 * s + jy, size=max(12, int(15 * s)), color_key=rcol, organic=False, bold=True)
            cc.hand_label("再Roll一次一定跑通", cx, by + bh - 20 * s, size=max(19, int(21 * s)), color_key="ink_detail", organic=False)
            # Slot machine side lever (auto-faces center stage so Xeron can grab the red ball directly!)
            l_side = -1.0 if cx > 960.0 else 1.0
            ang_lv = -0.62 + 0.95 * (0.5 + 0.5 * math.sin(t * 5.2))
            lx0 = bx if l_side < 0 else (bx + bw)
            ly0 = by + 98 * s
            lx1 = lx0 + l_side * math.cos(ang_lv) * 44 * s
            ly1 = ly0 + math.sin(ang_lv) * 50 * s
            cc.pen_line([(lx0, ly0), (lx1, ly1)], width=3.0, boil_key=key + "_arm")
            cc.white_ellipse(lx1, ly1, 11.5 * s, 11.5 * s, fill_key="red", ink_key="ink", width=1.8, boil_key=key + "_knb")
            return (lx1, ly1)

    elif k == "vibe_coding":
        # Precarious wobbling Jenga tower of code blocks!
        for bi in range(4):
            sway = math.sin(t * 5.5 + bi * 0.7) * (bi + 1) * 4.2 * s
            rot_b = math.sin(t * 5.5) * (bi + 1) * 2.4
            bw_b, bh_b = (126 - bi * 8) * s, 28 * s
            is_top = (bi == 3)
            cc.white_box(
                cx - bw_b * 0.5 + sway, cy + (42 - bi * 31) * s, bw_b, bh_b,
                fill_key="soft_red" if is_top else ("soft_mint" if bi == 0 else "white"),
                ink_key="red" if is_top else ("mint_ink" if bi == 0 else "ink"),
                rot_deg=rot_b, corner_r=4.0 * s, width=1.9, boil_key=f"{key}_jb{bi}"
            )
            lbl = "[!] 别动能跑" if is_top else ("Tab 糊出来的" if bi == 2 else ("AI 生成 v2" if bi == 1 else "Vibe 地基"))
            cc.hand_label(lbl, cx + sway, cy + (56 - bi * 31) * s, size=max(19, int(21 * s)), color_key="red" if is_top else "ink", organic=False, bold=is_top)

    elif k == "hallucination":
        # Dreamy floating soap bubbles containing confident nonsense (`1+1=5`, `import 空气`)!
        bubbles = [
            (-52, 18, 34, "1+1 = 5", "purple", "soft_purple"),
            (38, -24, 42, "胡编API()", "red", "soft_red"),
            (-8, -68, 28, "一本正经", "mint_ink", "soft_mint"),
        ]
        for bi, (ox, oy, br, btxt, bcol, bfill) in enumerate(bubbles):
            by_f = cy + oy * s + math.sin(t * 3.2 + bi * 1.7) * 9.0 * s
            bx_f = cx + ox * s + math.cos(t * 2.4 + bi) * 5.0 * s
            cc.white_ellipse(bx_f, by_f, br * s, br * 0.78 * s, fill_key=bfill, ink_key=bcol, width=1.8, boil_key=f"{key}_bb{bi}")
            cc.hand_label(btxt, bx_f, by_f, size=max(19, int(21 * s)), color_key=bcol, organic=False, bold=True)
        cc.hand_label("AI 幻觉冒泡", cx, cy + 68 * s, size=max(12, int(15 * s)), color_key="purple", organic=False, bold=True)

    elif k == "context_rot":
        bw, bh = 186 * s, 148 * s
        bx, by = cx - bw * 0.5, cy - bh * 0.5
        cc.white_box(bx, by, bw, bh, corner_r=8.0 * s, width=2.1, boil_key=key + "_wb", progress=progress)
        if progress > 0.35:
            cc.hand_label("4k 清醒区 ✓", cx, by + 24 * s, size=max(19, int(21 * s)), color_key="mint_ink", organic=False, bold=True)
            cc.pen_line([(bx + 18 * s, by + 44 * s), (bx + bw - 18 * s, by + 44 * s)], color_key="mint_ink", width=2.0, boil_key=key + "_l1", taper=False)
            # Smudged murky bottom "Dumb Zone" (`上下文腐烂 / 降智区`)!
            cc.white_box(bx + 8 * s, by + 64 * s, bw - 16 * s, bh - 74 * s, fill_key="shadow", ink_key="ink_soft", corner_r=6.0 * s, width=1.5, boil_key=key + "_rot")
            for si in range(3):
                wy = by + (80 + si * 18) * s
                scrib = [(bx + (18 + j * 24) * s, wy + math.sin(t * 8.0 + j + si) * 5.0 * s) for j in range(6)]
                cc.pen_line(scrib, color_key="ink_detail", width=1.7, boil_key=f"{key}_sc{si}", jitter=0.9)
            cc.hand_label("128k 降智失忆 !", cx, by + bh - 22 * s, size=max(19, int(21 * s)), color_key="red", organic=False, bold=True)

    elif k == "token_assassin":
        bw, bh = 184 * s, 142 * s
        bx, by = cx - bw * 0.5, cy - bh * 0.5
        cc.white_box(bx, by, bw, bh, fill_key="soft_red", ink_key="red", corner_r=10.0 * s, width=2.2, boil_key=key + "_mtr", progress=progress)
        if progress > 0.35:
            cc.hand_label("$ Token 刺客表", cx, by + 24 * s, size=max(12, int(15 * s)), color_key="red", organic=False, bold=True)
            # Wildly spinning dial gauge!
            gcx, gcy = cx, by + 84 * s
            cc.white_ellipse(gcx, gcy, 38 * s, 38 * s, fill_key="white", ink_key="ink", width=2.0, boil_key=key + "_dl")
            ang_n = t * 14.0
            cc.pen_line([(gcx, gcy), (gcx + math.cos(ang_n) * 30 * s, gcy + math.sin(ang_n) * 30 * s)], color_key="red", width=2.6, boil_key=key + "_ndl")
            # Flying `$` bills sucked up!
            for fi in range(2):
                fy = by - (10 + ((t * 2.2 + fi * 0.5) % 1.0) * 36) * s
                fx = cx + (fi - 0.5) * 64 * s
                cc.white_box(fx - 18 * s, fy - 10 * s, 36 * s, 20 * s, fill_key="soft_orange", ink_key="orange", rot_deg=14.0 * (fi * 2 - 1), width=1.5, boil_key=f"{key}_bl{fi}")
                cc.hand_label("$$", fx, fy, size=max(18, int(20 * s)), color_key="orange", organic=False, bold=True)

    elif k == "alchemy_distill":
        # GPU Cauldron (`炼丹炉`) -> Condenser Pipe -> Fast Mini Flask (`蒸馏小钢炮`)
        cc.white_ellipse(cx - 46 * s, cy + 18 * s, 42 * s, 34 * s, fill_key="cat_fill", ink_key="cat_line", width=2.2, boil_key=key + "_pot")
        cc.hand_label("炼丹炉", cx - 46 * s, cy + 18 * s, size=max(19, int(21 * s)), color_key="mint", organic=False, bold=True)
        tube = quad_bezier((cx - 24 * s, cy - 16 * s), (cx + 12 * s, cy - 58 * s), (cx + 52 * s, cy - 12 * s), 14)
        cc.pen_line(tube, color_key="mint_ink", width=2.6, boil_key=key + "_tb")
        drop_y = cy - 8 * s + ((t * 2.4) % 1.0) * 24 * s
        cc.white_ellipse(cx + 52 * s, drop_y, 5 * s, 7 * s, fill_key="mint", ink_key="mint_ink", width=1.3, boil_key=key + "_drp")
        flask = [(cx + 42 * s, cy + 14 * s), (cx + 62 * s, cy + 14 * s), (cx + 76 * s, cy + 50 * s), (cx + 28 * s, cy + 50 * s)]
        cc.fill_poly(flask, "soft_mint", boil_key=key + "_flf")
        cc.pen_line(flask, color_key="mint_ink", width=2.0, closed=True, taper=False, boil_key=key + "_flk")
        cc.hand_label("蒸馏精华", cx + 52 * s, cy + 68 * s, size=max(19, int(21 * s)), color_key="mint_ink", organic=False, bold=True)

    elif k == "agent_loop":
        r_lp = 54 * s
        cc.white_ellipse(cx, cy, r_lp, r_lp, fill_key="soft_orange", ink_key="orange", width=2.2, boil_key=key + "_whl")
        ang_l = t * 5.0
        cc.smear_arc(cx, cy, r_lp + 8 * s, r_lp + 8 * s, math.degrees(ang_l), math.degrees(ang_l) + 110, color_key="red", width=2.8, key=key + "_sm")
        cc.hand_label("报错⇄道歉", cx, cy, size=max(11, int(14 * s)), color_key="red", organic=False, bold=True)


# =============================================================================
# PART 6: REUSABLE SCENE & DESK PROPS (`draw_scene_prop`)
# =============================================================================
def draw_scene_prop(cc: CleanMintCanvas, kind: str, x: float, y: float, scale: float = 1.0, t: float = 0.0, progress: float = 1.0, key: str = "prop"):
    if progress <= 0.02:
        return
    k = kind.lower().strip()
    s = scale

    if k == "laptop_desk":
        w_d = 560.0 * s
        cc.white_box(x, y, w_d, 16.0 * s, width=2.2, boil_key=key + "_dt", progress=progress)
        cc.pen_line([(x + 26 * s, y + 16 * s), (x + 26 * s, y + 156 * s)], width=2.1, boil_key=key + "_dl1", progress=progress)
        cc.pen_line([(x + w_d - 26 * s, y + 16 * s), (x + w_d - 26 * s, y + 156 * s)], width=2.1, boil_key=key + "_dl2", progress=progress)
        if progress > 0.4:
            lx = x + 92 * s
            cc.white_box(lx, y - 9 * s, 96 * s, 9 * s, width=1.8, boil_key=key + "_lkb")
            scr = [(lx + 84 * s, y - 9 * s), (lx + 106 * s, y - 74 * s), (lx + 114 * s, y - 72 * s), (lx + 92 * s, y - 9 * s)]
            cc.fill_poly(scr, "cat_fill", boil_key=key + "_lsf", jitter=0.2)
            cc.white_ellipse(lx + 46 * s, y - 5 * s, 2.8 * s, 2.8 * s, fill_key="mint", ink_key=None, boil_key=key + "_tp")

    elif k == "vps_tower":
        tw, th = 78.0 * s, 128.0 * s
        cc.white_box(x - tw * 0.5, y - th, tw, th, corner_r=7.0, width=2.1, boil_key=key + "_tw", progress=progress)
        if progress > 0.4:
            for vi in range(3):
                cc.pen_line([(x - tw * 0.30, y - th + (26 + vi * 14) * s), (x + tw * 0.30, y - th + (26 + vi * 14) * s)], color_key="ink_detail", width=1.5, boil_key=f"{key}_vt{vi}", taper=False)
            blink = int(t * 4.0) % 2 == 0
            cc.white_ellipse(x - tw * 0.22, y - 26 * s, 4.5 * s, 4.5 * s, fill_key="mint" if blink else "white", ink_key="mint_ink", width=1.5, boil_key=key + "_led1")
            cc.white_ellipse(x + tw * 0.02, y - 26 * s, 4.5 * s, 4.5 * s, fill_key="orange", ink_key="orange", width=1.5, boil_key=key + "_led2")

    elif k == "signal_dish":
        cc.pen_line([(x - 22 * s, y), (x, y - 42 * s), (x + 22 * s, y)], width=2.0, boil_key=key + "_db", progress=progress, taper=False)
        dish = quad_bezier((x - 26 * s, y - 66 * s), (x - 8 * s, y - 34 * s), (x + 24 * s, y - 48 * s), n=14)
        cc.pen_line(dish, width=2.2, boil_key=key + "_dc", progress=progress)
        if progress > 0.5:
            for wi in range(2):
                wu = ((t * 1.4 + wi * 0.5) % 1.0)
                wr = (18.0 + wu * 34.0) * s
                arc_p = np.stack([x + 12 * s + np.cos(np.linspace(-1.1, -0.1, 10)) * wr, y - 58 * s + np.sin(np.linspace(-1.1, -0.1, 10)) * wr], axis=1)
                cc.pen_line(arc_p, color_key="mint_ink", width=max(1.2, 2.2 * (1.0 - wu)), boil_key=f"{key}_wa{wi}")




# =============================================================================
# PART 7: AUTONOMOUS VIEWER EASTER EGGS & EMOTIONAL-VALUE MICRO-GAGS (`draw_easter_egg`)
# =============================================================================

def draw_cat_at_computer_desk(
    cc: CleanMintCanvas,
    desk_x: float,
    floor_y: float,
    u: float = 25.0,
    t: float = 0.0,
    mode: str = "typing",   # "typing" (leaning forward, paws on keyboard) or "slump_sigh" (leaning back in chair exhausted)
    expr: str = None,
    key: str = "workdesk",
):
    """
    Spatially locked side-view workstation (`小黑猫标准电脑前坐姿工位`):
    - Ergonomic study chair on left (`desk_x - 95`) supporting Xeron's hips cleanly at seat height
    - Xeron seated facing RIGHT (`+1.0`), bent knees & feet tucked naturally UNDER the desk (`zero` table-bar clipping!)
    - Desk surface (`desk_x .. desk_x + 340`) at chest/elbow height with an open laptop facing LEFT toward Xeron
    - Both paws placed accurately ON the laptop keyboard (`typing`) or resting exhausted in lap (`slump_sigh`)
    """
    seat_y = floor_y - 112.0
    desk_y = floor_y - 148.0
    desk_w = 345.0
    chair_cx = desk_x - 88.0

    # 1. Ergonomic Study Chair (base on floor_y, post, seat cushion, curved backrest)
    cc.white_ellipse(chair_cx, floor_y + 2.0, 52.0, 8.0, fill_key="shadow", ink_key=None, boil_key=key + "_csh")
    cc.pen_line([(chair_cx, seat_y + 14.0), (chair_cx, floor_y - 12.0)], width=3.0, boil_key=key + "_cpst", taper=False)
    cc.pen_line([(chair_cx - 42.0, floor_y), (chair_cx, floor_y - 12.0), (chair_cx + 42.0, floor_y)], width=2.6, boil_key=key + "_cleg", taper=False)
    # Curved chair backrest behind Xeron
    cc.pen_line([(chair_cx - 38.0, seat_y + 6.0), (chair_cx - 52.0, seat_y - 42.0)], width=2.8, boil_key=key + "_cbkarm")
    cc.white_box(chair_cx - 60.0, seat_y - 102.0, 18.0, 68.0, fill_key="white", ink_key="ink", corner_r=7.0, width=2.2, rot_deg=-6.0, boil_key=key + "_cbk")
    # Chair seat cushion
    cc.white_box(chair_cx - 46.0, seat_y, 96.0, 15.0, fill_key="soft_mint", ink_key="ink", corner_r=6.0, width=2.2, boil_key=key + "_cseat")

    # 2. Seated Xeron Cat (hips resting right on chair seat cushion, knees bent forward into space under desk!)
    is_typing = (mode == "typing")
    is_chin = (mode == "chin_rest")
    eff_expr = expr if expr is not None else ("focus" if is_typing else ("deadpan" if is_chin else "sigh"))
    lean = 10.5 if is_typing else -8.5
    scurve = 0.28 if is_typing else -0.18
    head_nod = 6.0 if is_typing else 12.0

    # Seated legs tucked cleanly under desk (`desk_y = floor_y - 148`, knees at `seat_y + 6`, feet at `floor_y - 34`)
    hip_gx = chair_cx + (6.0 if is_typing else -4.0)
    # Draw tail curling gracefully out behind the chair backrest in open white space!
    sway = math.sin(t * 1.4) * 6.0
    t_pts = cubic_bezier(
        (hip_gx - 22.0, seat_y - 8.0),
        (chair_cx - 78.0, seat_y + 6.0),
        (chair_cx - 118.0, seat_y - 24.0 + sway * 0.5),
        (chair_cx - 106.0, seat_y - 72.0 + sway),
        16,
    )
    cc.pen_line(t_pts, color_key="cat_line", width=max(4.2, 0.34 * u), boil_key=key + "_tail", jitter=0.25, taper=True, start_scale=1.08, end_scale=0.55)

    # Draw seated thighs -> knees -> lower legs hanging cleanly in open space BEFORE desk leg!
    for li, ox in enumerate((-5.0, 9.0)):
        h_pt = (hip_gx + 8.0 + ox * 0.5, seat_y - 4.0)
        k_pt = (chair_cx + 52.0 + ox, seat_y + 6.0)
        f_pt = (chair_cx + 56.0 + ox, floor_y - 38.0 + li * 6.0)
        cc.pen_line([h_pt, k_pt], color_key="cat_line", width=max(3.4, 0.26 * u), boil_key=f"{key}_sth{li}", taper=True)
        cc.pen_line([k_pt, f_pt], color_key="cat_line", width=max(3.1, 0.24 * u), boil_key=f"{key}_ssh{li}", taper=True)
        cc.pen_line([f_pt, (f_pt[0] + 12.0, f_pt[1] + 2.0)], color_key="cat_line", width=max(2.9, 0.22 * u), boil_key=f"{key}_sft{li}", taper=True)

    # Laptop coordinates on desk (`kb_x = desk_x + 36 .. desk_x + 148`, screen angled up-right facing LEFT toward Xeron!)
    kb_x = desk_x + 38.0
    kb_w = 112.0
    kb_y = desk_y - 10.0
    if is_typing:
        tap_l = math.sin(t * 12.0) * 3.8
        tap_r = -math.sin(t * 12.0) * 3.8
        hl_tgt = (kb_x + 24.0, kb_y - 3.0 + tap_l)
        hr_tgt = (kb_x + 54.0, kb_y - 2.0 + tap_r)
        lk_x, lk_y = 0.85, 0.15
    elif is_chin:
        # Left elbow resting on desk, paw propping chin (`单爪托腮坐在电脑前`), right paw resting on keyboard!
        hl_tgt = (hip_gx + 22.0, desk_y - 54.0)
        hr_tgt = (kb_x + 36.0, kb_y - 2.0)
        lk_x, lk_y = 0.65, 0.10
        lean, scurve, head_nod = 8.0, 0.22, 5.0
    else:
        hl_tgt = (chair_cx + 46.0, seat_y - 2.0)
        hr_tgt = (desk_x + 20.0, desk_y - 3.0)
        lk_x, lk_y = 0.35, 0.25

    # Render Xeron upper body seated on `seat_y` (`posture="sit_swing"` places hips right above `gy`, we hide default swing legs via custom seated legs? Wait: `sit_swing` draws its own swing legs! Let's pass a new `posture="chair_seated"` that skips standing/swing legs since we just drew exact chair-seated legs!)
    hcx, hcy = draw_xeron_actor(
        cc, hip_gx, seat_y + 6.0, u=u, t=t, facing=1.0,
        posture="chair_seated", expr=eff_expr,
        lean_deg=lean, spine_curve=scurve, head_nod_deg=head_nod,
        look_x=lk_x, look_y=lk_y,
        hand_l_world=hl_tgt, hand_r_world=hr_tgt,
        draw_shadow=False, boil_key=key + "_cat"
    )

    # 3. Desk Table & Open Laptop Facing Xeron (drawn right in front of Xeron, ZERO waist overlap!)
    cc.white_box(desk_x, desk_y, desk_w, 15.0, fill_key="white", ink_key="ink", corner_r=4.0, width=2.3, boil_key=key + "_dt")
    cc.pen_line([(desk_x + 54.0, desk_y + 15.0), (desk_x + 54.0, floor_y)], width=2.3, boil_key=key + "_dl1", taper=False)
    cc.pen_line([(desk_x + desk_w - 24.0, desk_y + 15.0), (desk_x + desk_w - 24.0, floor_y)], width=2.3, boil_key=key + "_dl2", taper=False)

    # Laptop base/keyboard + tilted screen facing LEFT toward Xeron's eyes!
    cc.white_box(kb_x, kb_y, kb_w, 10.0, fill_key="white", ink_key="ink", corner_r=3.0, width=2.0, boil_key=key + "_lkb")
    hinge_x, hinge_y = kb_x + kb_w - 6.0, kb_y
    top_x, top_y = hinge_x + 28.0, kb_y - 98.0
    scr_poly = [(hinge_x - 8.0, hinge_y), (top_x - 8.0, top_y), (top_x + 2.0, top_y + 2.0), (hinge_x + 2.0, hinge_y)]
    cc.fill_poly(scr_poly, "cat_fill", boil_key=key + "_lscr")
    cc.pen_line(scr_poly, color_key="cat_line", width=1.8, closed=True, taper=False, boil_key=key + "_lscrl")
    # Subtle #2EE59D screen glow cone toward Xeron's face!
    cc.pen_line([(top_x - 10.0, top_y + 12.0), (hinge_x - 10.0, hinge_y - 8.0)], color_key="mint", width=2.4, boil_key=key + "_lglow", taper=False)
    if is_typing:
        # Tiny crisp key-tap ticks right above keyboard
        for ki in range(2):
            ky_t = kb_y - 16.0 - ((t * 6.0 + ki * 0.5) % 1.0) * 10.0
            kx_t = kb_x + 28.0 + ki * 26.0
            cc.pen_line([(kx_t, ky_t + 5.0), (kx_t - 3.0, ky_t)], color_key="mint_ink", width=1.8, boil_key=f"{key}_ktk{ki}")
    return (hcx, hcy)


def draw_callout_note(
    cc: CleanMintCanvas,
    target_pt: tuple[float, float],
    note_pt: tuple[float, float],
    title: str,
    sub: str = "",
    align: str = "center",
    arch_h: float = -18.0,
    color_key: str = "mint_ink",
    title_size: int = 30,
    sub_size: int = 22,
    progress: float = 1.0,
    key: str = "cnote",
):
    """
    Big, high-legibility hand-drawn callout annotation (`大字号手绘引线批注`):
    Draws a crisp fountain-pen arrow from below/beside `note_pt` to `target_pt` + large `30px` bold annotation!
    """
    if progress <= 0.02:
        return
    p = ease_out(clamp(progress))
    ty_title = note_pt[1] - (16.0 if sub else 0.0)
    ty_bottom = (ty_title + 34.0 + 18.0) if sub else (ty_title + 22.0)
    # Start arrow cleanly BELOW the text block if target is below, or ABOVE if target is above!
    if target_pt[1] > note_pt[1] + 24.0:
        arr_start = (note_pt[0], ty_bottom)
    elif target_pt[1] < note_pt[1] - 24.0:
        arr_start = (note_pt[0], ty_title - 22.0)
    else:
        arr_start = (note_pt[0] + (18.0 if align == "right" else -18.0), note_pt[1])
    cc.flow_arrow(arr_start, target_pt, arch_h=arch_h, color_key=color_key, width=2.8, boil_key=key + "_arr", progress=p)
    if p > 0.25:
        ta = clamp((p - 0.25) / 0.75)
        cc.hand_label(title, note_pt[0], ty_title, size=title_size, color_key=color_key, align=align, organic=False, bold=True, alpha=ta)
        if sub:
            cc.hand_label(sub, note_pt[0], ty_title + title_size + 6.0, size=sub_size, color_key="ink_detail", align=align, organic=False, bold=True, alpha=ta)


def draw_easter_egg(
    cc: CleanMintCanvas,
    kind: str,
    x: float,
    y: float,
    scale: float = 1.0,
    t: float = 0.0,
    text: str = "",
    progress: float = 1.0,
    key: str = "egg",
):
    """
    Subtle, high-delight flat-shaded bold-ink background/corner Easter eggs (`画面彩蛋与情绪价值挂件`)
    designed to reward eagle-eyed viewers and spark Danmaku/comment resonance without cluttering center stage:
    - `peek_mini_cat`: Tiny upside-down/sideways mini black cat peeking from frame edge (`暗中观察`)
    - `rubber_duck`: Programmer debugging rubber duck wearing `#2EE59D` geek glasses (`Debug 护法鸭`)
    - `catnip_coffee`: `猫薄荷冰美式 / 续命水` cup with drifting mint steam heart/leaf
    - `sticky_rant`: Tilted mini sticky note with relatable inner monologue (`能跑就行别动` / custom `text`)
    - `achievement_toast`: Game-style pop-up badge (`解锁成就：人间清醒 +1` / custom `text`)
    - `battery_hp`: Mini RPG `SAN 值 / 精力条` meter recovering to `#2EE59D` 100%
    - `fourth_wall_sign`: Tiny wooden placard (`看到这的都是同频狠人` / custom `text`)
    - `loading_fish`: Spinning hand-drawn dried-fish (`小鱼干 Loading...`) save icon
    - `server_probe_6`: 6-node green heartbeat strip (`6 Nodes Online · Backup OK`)
    - `resonance_whisper`: Subtle tilted margin note (`<- 世另我` / custom `text`)
    """
    if progress <= 0.02:
        return
    k = kind.lower().strip()
    s = scale * back_out(clamp(progress))
    if s <= 0.05:
        return

    if k == "peek_mini_cat":
        # Peeks out, blinks #2EE59D eyes, and bobs gently!
        bob = math.sin(t * 2.8) * 5.0 * s
        cy_p = y + bob
        for es in (-1.0, 1.0):
            ep = [(x + es * 18 * s, cy_p - 6 * s), (x + es * 22 * s, cy_p - 26 * s), (x + es * 6 * s, cy_p - 15 * s)]
            cc.fill_poly(ep, "cat_fill", boil_key=f"{key}_pe{es}")
            cc.pen_line(ep, color_key="cat_line", width=1.6, closed=True, taper=False, boil_key=f"{key}_pel{es}")
        cc.white_ellipse(x, cy_p, 22 * s, 16 * s, fill_key="cat_fill", ink_key="cat_line", width=1.8, boil_key=key + "_phd")
        blink = (int(t * 2.2) % 7 == 0)
        for es in (-1.0, 1.0):
            ex = x + es * 8.5 * s
            if blink:
                cc.pen_line([(ex - 5 * s, cy_p - 2 * s), (ex + 5 * s, cy_p - 2 * s)], color_key="mint", width=2.0, boil_key=f"{key}_pbl{es}")
            else:
                cc.white_box(ex - 5 * s, cy_p - 5 * s, 10 * s, 6.5 * s, fill_key="mint", ink_key="cat_line", corner_r=2.0, width=1.2, boil_key=f"{key}_pey{es}")
        # Two tiny paws resting on ledge line
        cc.pen_line([(x - 34 * s, y + 10 * s), (x + 34 * s, y + 10 * s)], color_key="ink_soft", width=1.5, boil_key=key + "_ldg")
        for ps in (-11.0, 11.0):
            cc.white_ellipse(x + ps * s, y + 9 * s, 5.5 * s, 4.2 * s, fill_key="cat_fill", ink_key="cat_line", width=1.2, boil_key=f"{key}_ppw{ps}")
        if text:
            cc.hand_label(text, x, cy_p - 34 * s, size=max(19, int(21 * s)), color_key="ink_detail")

    elif k == "rubber_duck":
        rock = math.sin(t * 4.2) * 4.0
        cc.white_ellipse(x, y, 20 * s, 14 * s, rot_deg=rock, fill_key="soft_orange", ink_key="ink", width=1.8, boil_key=key + "_db")
        cc.white_ellipse(x + 10 * s, y - 15 * s, 12 * s, 11 * s, rot_deg=rock, fill_key="soft_orange", ink_key="ink", width=1.8, boil_key=key + "_dh")
        beak = [(x + 20 * s, y - 17 * s), (x + 29 * s, y - 14 * s), (x + 20 * s, y - 11 * s)]
        cc.fill_poly(beak, "orange", boil_key=key + "_dbk")
        cc.pen_line(beak, width=1.4, closed=True, taper=False, boil_key=key + "_dbkl")
        # Tiny #2EE59D geek glasses on the rubber duck!
        cc.white_box(x + 9 * s, y - 19 * s, 8 * s, 5.5 * s, fill_key="mint", ink_key="ink", corner_r=1.5, width=1.3, boil_key=key + "_dgl")
        cc.hand_label(text or "Debug 护法", x, y + 24 * s, size=max(19, int(20 * s)), color_key="ink_detail", organic=False)

    elif k == "catnip_coffee":
        cc.white_box(x - 16 * s, y - 22 * s, 32 * s, 38 * s, fill_key="white", ink_key="ink", corner_r=4.0 * s, width=1.8, boil_key=key + "_cup")
        cc.white_box(x - 19 * s, y - 27 * s, 38 * s, 7 * s, fill_key="soft_mint", ink_key="mint_ink", corner_r=2.5 * s, width=1.6, boil_key=key + "_lid")
        cc.pen_line([(x + 4 * s, y - 27 * s), (x + 11 * s, y - 40 * s)], color_key="mint_ink", width=2.1, boil_key=key + "_strw")
        cc.hand_label(text or "续命冰美式", x, y + 28 * s, size=max(19, int(20 * s)), color_key="mint_ink", organic=False)

    elif k == "sticky_rant":
        sway = math.sin(t * 2.5) * 1.8
        cc.white_box(x - 125 * s, y - 32 * s, 250 * s, 64 * s, fill_key="pale_mint", ink_key="ink_detail", rot_deg=-3.5 + sway, corner_r=4.0 * s, width=1.6, boil_key=key + "_stk")
        cc.white_ellipse(x, y - 26 * s, 4.5 * s, 4.5 * s, fill_key="mint", ink_key="ink", width=1.3, boil_key=key + "_pin")
        cc.hand_label(text or "能跑就行千万别动", x, y + 2 * s, size=max(19, int(21 * s)), color_key="ink", slant_deg=-3.0)

    elif k == "achievement_toast":
        lbl = text or "解锁成就：人间清醒 +1"
        bw = max(240.0, len(lbl) * 23.5) * s
        bh = 48.0 * s
        cc.white_box(x - bw * 0.5, y - bh * 0.5, bw, bh, fill_key="soft_mint", ink_key="mint_ink", corner_r=18.0 * s, width=1.9, boil_key=key + "_tst")
        sx_t = x - bw * 0.5 + 22 * s
        r_st = 7.5 * s * (0.9 + 0.15 * math.sin(t * 7.0))
        star = [
            (sx_t, y - r_st), (sx_t + r_st * 0.3, y - r_st * 0.3), (sx_t + r_st, y),
            (sx_t + r_st * 0.3, y + r_st * 0.3), (sx_t, y + r_st), (sx_t - r_st * 0.3, y + r_st * 0.3),
            (sx_t - r_st, y), (sx_t - r_st * 0.3, y - r_st * 0.3),
        ]
        cc.fill_poly(star, "mint", boil_key=key + "_str")
        cc.pen_line(star, color_key="ink", width=1.2, closed=True, taper=False, boil_key=key + "_strl")
        cc.hand_label(lbl, x + 10 * s, y, size=max(20, int(22 * s)), color_key="mint_ink", organic=False, bold=True)

    elif k == "battery_hp":
        bw, bh = 118 * s, 26 * s
        cc.white_box(x - bw * 0.5, y - bh * 0.5, bw, bh, corner_r=5.0 * s, width=1.7, boil_key=key + "_bat")
        cc.white_box(x + bw * 0.5, y - 6 * s, 5 * s, 12 * s, fill_key="ink", ink_key="ink", corner_r=1.5, width=1.2, boil_key=key + "_bcap")
        fill_r = clamp(0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * 2.2)))
        cc.white_box(x - bw * 0.5 + 4 * s, y - bh * 0.5 + 4 * s, (bw - 8 * s) * fill_r, bh - 8 * s, fill_key="mint", ink_key=None, corner_r=3.0 * s, boil_key=key + "_bf")
        cc.hand_label(text or "SAN 值稳住", x, y - bh * 0.5 - 12 * s, size=max(19, int(20 * s)), color_key="mint_ink", organic=False, bold=True)

    elif k == "fourth_wall_sign":
        lbl = text or "刷到这的都是同频狠人"
        bw = max(240.0, len(lbl) * 28.5 + 36.0) * s
        cc.pen_line([(x, y), (x, y - 44 * s)], width=2.6, boil_key=key + "_pst")
        cc.white_box(x - bw * 0.5, y - 88 * s, bw, 44 * s, fill_key="white", ink_key="ink", rot_deg=2.2, corner_r=5.0 * s, width=1.8, boil_key=key + "_brd")
        cc.hand_label(lbl, x, y - 66 * s, size=max(20, int(22 * s)), color_key="mint_ink", slant_deg=2.0, bold=True)

    elif k == "loading_fish":
        ang = t * 3.6
        ca, sa = math.cos(ang), math.sin(ang)
        pts_f = [(-18, 0), (-6, -9), (10, -7), (20, -13), (17, 0), (20, 13), (10, 7), (-6, 9)]
        tr_f = [(x + (px * ca - py * sa) * s, y + (px * sa + py * ca) * s) for px, py in pts_f]
        cc.fill_poly(tr_f, "soft_mint", boil_key=key + "_fshf")
        cc.pen_line(tr_f, color_key="mint_ink", width=1.7, closed=True, taper=False, boil_key=key + "_fsh")
        cc.hand_label(text or "小鱼干加载中..", x, y + 26 * s, size=max(18, int(20 * s)), color_key="ink_soft", organic=False)

    elif k == "server_probe_6":
        bw, bh = 156 * s, 30 * s
        cc.white_box(x - bw * 0.5, y - bh * 0.5, bw, bh, corner_r=6.0 * s, width=1.6, ink_key="ink_detail", boil_key=key + "_srv")
        for ni in range(6):
            pulse = ((int(t * 5.0) + ni) % 6 == 0)
            nx_i = x - bw * 0.5 + (18 + ni * 24) * s
            cc.white_ellipse(nx_i, y, (5.2 if pulse else 4.0) * s, (5.2 if pulse else 4.0) * s, fill_key="mint", ink_key="mint_ink", width=1.2, boil_key=f"{key}_nd{ni}")
        cc.hand_label(text or "6 Nodes All Green", x, y - bh * 0.5 - 11 * s, size=max(18, int(19 * s)), color_key="ink_soft", organic=False)

    elif k == "resonance_whisper":
        cc.hand_label(text or "<- 世另我 (真实)", x, y + math.sin(t * 3.0) * 2.5 * s, size=max(20, int(22 * s)), color_key="ink_soft", slant_deg=-2.5, alpha=0.78)


def get_active_subtitle(shot_configs: list, t: float):
    for sh in shot_configs:
        for st0, st1, stxt in sh.get("sub_windows", []):
            if st0 <= t <= st1:
                u_in = clamp((t - st0) / 0.16)
                u_out = clamp((st1 - t) / 0.16)
                return stxt, min(ease_out(u_in), u_out), (1.0 - ease_out(u_in)) * 8.0
    return "", 0.0, 0.0


def resolve_expression_timeline(t: float, keyframes: list, blend_dur: float = 0.20):
    if not keyframes:
        return "aloof", "aloof", 1.0
    prev_e = keyframes[0][1]
    curr_e = prev_e
    mix = 1.0
    for kt, ke in keyframes:
        if t >= kt:
            prev_e = curr_e
            curr_e = ke
            mix = smootherstep(clamp((t - kt) / max(0.01, blend_dur))) if prev_e != curr_e else 1.0
        else:
            break
    return prev_e, curr_e, mix


def encode_turbo_film(script_path: Path, shard_flag: str, total_dur_s: float, master_wav: Path, mp4_path: Path, n_shards: int = 2):
    """Zero-friction multi-shard H.264 encoder with non-blocking DEVNULL pipes + instant -c:v copy mux."""
    import os
    import sys
    tmp_dir = mp4_path.parent
    shards = [tmp_dir / f"_turbo_shard_{i}.mp4" for i in range(n_shards)]
    procs = [
        subprocess.Popen(
            [sys.executable, "-B", str(script_path), shard_flag, str(i), str(n_shards), str(sf)],
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        for i, sf in enumerate(shards)
    ]
    for p in procs:
        if p.wait() != 0:
            raise RuntimeError("Turbo shard worker failed")
    lst = tmp_dir / "_turbo_concat.txt"
    lst.write_text("\n".join(f"file '{sf.resolve()}'" for sf in shards) + "\n")
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(lst),
        "-i", str(master_wav),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", "-shortest", str(mp4_path),
    ], check=True)
    for sf in shards:
        sf.unlink(missing_ok=True)
    lst.unlink(missing_ok=True)


# Backward-compatible aliases
CleanCanvas = CleanMintCanvas
draw_xeron_cat = draw_xeron_actor
mix_narration_and_score = mix_stereo_master
mix_full_film_audio = mix_stereo_master
encode_clean_film = encode_turbo_film
