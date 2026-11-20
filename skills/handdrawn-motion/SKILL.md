---
name: handdrawn-motion
description: 'Create studio-craft, de-AI-ified 60fps hand-drawn animated explainer videos (.mp4) starring a configurable creator mascot IP (`BrandConfig`, default solid-ink mascot with #2EE59D accent) using a four-layer anti-homogenization architecture: (1) pure 2.5-head Chibi silhouette assets & cold-press watercolor/dip-pen media (chibi_watercolor_kit.py + cairo_handdrawn.py v5.0 with wet-edge washes, warm #FAF8F3 paper grain, and per-element 12fps boilSeed), (2) Polanyi tacit viewer read-budget timing & hand-drawn draftsman callouts/Easter eggs, (3) continuous-world breath-valley horizontal camera pans (zero PPT slide cross-fades), and (4) all-act 3-Zoom pre-render QA gates alongside single-take <short pause> raw-VO vowel-peak alignment.'
---
# Handdrawn Motion (v11.1 — Chibi Watercolor Studio Craft & Four-Layer Anti-AI Architecture)

Build tactile, signature-craft `1920x1080 @ 60fps` (`CRF 19`) hand-drawn watercolor animations starring any parameterized creator mascot IP (`BrandConfig`) without naive programmer-art primitives, uncanny stretched bicycle legs, mechanical `lerp` twinning, or slide-deck cross-fades.

## Bundled Scripts & `BrandConfig` Parameterization

All three scripts live under `scripts/` and resolve sibling imports automatically via `Path(__file__).resolve().parent`:

1. `scripts/cairo_handdrawn.py` — `BrandConfig` (dataclass + `from_file` / `from_dict` / `from_env` + cross-OS font resolver), PyCairo dip-pen (`HandDrawnStage`, `brush_stroke`, `pencil_underdraw`, `marker_wash_poly`, `soft_shadow`), 12fps `boil_offset_xy`, `viewer_read_envelope`, `ContinuousCamera2D`, `shape_morph_poly`, `draw_plush_mascot`, `draw_brand_signature`, `apply_paper_grain`, and `lint_and_render_3zoom_qa`.
2. `scripts/chibi_watercolor_kit.py` — Warm `#FAF8F3` cold-press cotton paper (`make_paper_stage`), pre-densified wet-edge watercolor washes (`wet_watercolor_wash`), 2.5-head Chibi mascot rig (`draw_chibi_mascot`), draftsman callouts (`draw_draftsman_callout`), corner Easter eggs (`draw_debug_duck_egg`, `draw_peek_mini_mascot_egg`, `draw_sticky_badge`), and tactile studio props (`draw_glass_kettle`, `draw_skill_cartridge`, `draw_poker_chip_stack`, `draw_compounding_flywheel`).
3. `scripts/motion_rig_kit.py` — `CleanCanvas` renderer, fluid 3-joint C/S-spine mascot rig (`draw_mascot_actor`, `draw_mascot_at_computer_desk`), official app/social icons (`draw_brand_icon`, `draw_official_app_icon`), AI UI/method/slang props (`draw_ai_ui_prop`, `draw_ai_method_prop`, `draw_ai_jargon_prop`), Karplus-Strong stereo Lo-Fi guitar BGM synth (`synth_studio_lofi_bgm`, `mix_stereo_master`), raw-VO vowel-nucleus subtitle alignment (`align_subs_on_raw_vowel_peaks`, `align_raw_vo_subtitles`), and multi-shard `ffmpeg` H.264 encoder (`encode_turbo_film`).

Configure your IP in one call before rendering:

```python
from cairo_handdrawn import BrandConfig, set_brand_config
cfg = BrandConfig.from_file("templates/ip-profile.example.yaml")  # or BrandConfig.from_env()
set_brand_config(cfg)
```

## Four-Layer Anti-AI & Anti-Homogenization Architecture (v11.1 Spec)

### Layer 1: Pure 2.5-Head Chibi Silhouette & Natural Watercolor Media (`纯正二头身造型与水彩笔刷介质`)

- **Pure 2.5-Head Chibi Mascot (`chibi_watercolor_kit.py` -> `draw_chibi_mascot`)**: Render the protagonist in pure 2.5-head Chibi proportions (`大圆头 + 小短身 + 小短爪`, palette driven by `BrandConfig`: default `#0D0D0D` sumi-ink body, `#6E6378` muted inner ears, flat-topped half-lidded `#2EE59D` aloof geek eyes). Never place a Chibi actor on props like two-wheeled crank bicycles that force uncanny human-length legs.
- **Natural Pigment, Pressure & Paper Grain**: Render onto warm `#FAF8F3` cold-press cotton paper (`make_paper_stage`, configurable via `BrandConfig.paper_hex`), pre-densified wet-watercolor washes (`wet_watercolor_wash`, `max_px <= 10.5px`), variable-pressure dip-pen contours (`brush_stroke`), hand-hatched contact shadows (`soft_shadow`), light draftsman leader-arrow callouts (`draw_draftsman_callout`), and corner Easter eggs (`draw_debug_duck_egg`, `draw_peek_mini_mascot_egg`, `draw_sticky_badge`).
- **CJK Font Safety & Isolated `12fps` (`onTwos`) Line Boil**: Drive primary motion at silky `60fps` while locking organic hand-boil to `12fps` (`onTwos`) per element. Fonts resolve automatically via `HANDDRAWN_FONT_REGULAR`/`BOLD`/`SERIF` -> Debian Noto -> Linux/macOS/Windows fallbacks. Avoid unsupported `NotoSansCJK` glyphs (`↻`, `✗`, `♠`, `♦` — draw vector icons or brush strike-throughs instead so zero `☐` tofu boxes appear).

### Layer 2: Viewer Single-Read Timing Budget & Metaphor-First Logic (`观众单拍读点与声画同构`)

- **Metaphor-First 1:1 Audio-Visual Alignment & Single Scale**: Align spoken copy and visual props to the exact same physical metaphor (e.g., boiling glass kettle `20°C -> 88°C -> 99°C -> 100°C`) and never mix conflicting dual scales (`%` vs `°C`).
- **One Read at a Time (`viewer_read_envelope`)**: Sequence every beat across `Lead Eye (0.30–0.40s) -> Reverse Anticipation (0.15–0.20s) -> Fast Action Snap (0.22–0.28s) -> Payoff Hold (0.85–1.20s)`, staggering secondary motion (`eyes -> head +3f -> torso +6f -> paws +8f -> ears/tail +12f`) and reserving `accent_hex` (`#2EE59D`) strictly for threshold/payoff states.
- **Draftsman Callouts vs. PPT Clutter**: Ban opaque PPT thesis banners, slide boxes, and pop-up glossary cards; use light, curved-arrow `draw_draftsman_callout` margin annotations (`2–6` chars) and corner Easter eggs to reinforce visual causality without repeating full narration.

### Layer 3: Continuous World & Breath-Valley Camera (`一镜连续世界摄影机`)

- **Kill PPT Slide Cross-Dissolves**: Never glue isolated slide functions with opacity fades. Place zones across a continuous workbench/stage and glide horizontally (`0.48–0.60s` `smootherstep` pan via `ContinuousCamera2D` or world-X offset) inside `<short pause>` breath valleys, or relay silhouettes via `shape_morph_poly`.

### Layer 4: Multi-Act 3-Zoom Pre-Render QA Gate (`全幕切片三倍率审片门禁`)

Never encode a full film blind. Enforce pure-function deterministic `f(t)` rendering and run `lint_and_render_3zoom_qa` before full encoding:

1. **Subtitle Safe-Zone Ink Lint**: Verify stage props/floor stay above `y = 850` so `y = 956` `40px` subtitles (`y >= 938` band) have `< 16%` background ink density.
2. **All-Act Visual Inspection (`Look Frames` + `0.1s` Motion Strip + `1:1` Crops)**: Inspect exported PNGs (`view_file` / multimodal read) to verify zero `☐` tofu glyphs, zero ear/arrow text collisions, `< 5.0%` `+16.7ms` frame-step stability, and crisp Chibi contact silhouettes.

## End-to-End Execution Steps

1. **Load Toolkit & Profile**: Load `scripts/cairo_handdrawn.py`, `scripts/motion_rig_kit.py`, `scripts/chibi_watercolor_kit.py`, and `references/director-and-style-rules.md`; initialize `BrandConfig` from `ip-profile.yaml` or env vars.
2. **Synthesize Single-Take `<short pause>` Raw Voiceover**: Author one unified spoken script (`<= 5 min`) with explicit `<short pause>` breath cues and spaced acronyms (`S O P`), generate in a **single** TTS call (NEVER chop breaths or apply `ffmpeg atempo`), align all clauses directly on the unedited WAV via `align_subs_on_raw_vowel_peaks` / `align_raw_vo_subtitles`, and mix tactile foley + stereo Lo-Fi guitar BGM (`0.28` speech / `0.58` pause) via `mix_stereo_master`.
3. **Pass All-Act 3-Zoom QA Gate -> Parallel Multi-Shard `60fps` Encode**: Inspect QA contact sheets and `1:1` crops, fix any micro-collisions, and encode `1920x1080 @ 60fps` (`CRF 19`) via `encode_turbo_film`.
