---
name: xeron-cat-motion
description: 'Create studio-craft, de-AI-ified 60fps hand-drawn animated explainer videos (.mp4) starring the Xeron #2EE59D mint-green-eyed black cat IP using a four-layer anti-homogenization architecture: (1) pure 2.5-head flat-shaded bold-ink Chibi silhouette assets & cold-press watercolor/dip-pen media (v14_chibi_watercolor_kit.py + cairo_handdrawn.py v5.0 with wet-edge washes, warm #FAF8F3 paper grain, and per-element 12fps boilSeed), (2) Polanyi tacit viewer read-budget timing & hand-drawn draftsman callouts/Easter eggs, (3) continuous-world breath-valley horizontal camera pans (zero PPT slide cross-fades), and (4) all-act pre-render QA gates alongside single-take <short pause> prosody voiceover.'
---
# Xeron Cat Motion (v11.1 — Chibi Watercolor Studio Craft & Four-Layer Anti-AI Architecture)

Build tactile, signature-craft `1920x1080 @ 60fps` (`CRF 19`) hand-drawn watercolor animations starring the Xeron `#2EE59D` mint-green-eyed black cat IP without naive programmer-art primitives, uncanny stretched bicycle legs, mechanical `lerp` twinning, or slide-deck cross-fades.

## Four-Layer Anti-AI & Anti-Homogenization Architecture

### Layer 1: Pure 2.5-Head Chibi Silhouette & Natural Watercolor Media (`纯正二头身造型与水彩笔刷介质`)

- **Pure 2.5-Head Flat-Shaded Bold-Ink Chibi Xeron (`scripts/v14_chibi_watercolor_kit.py` -> `draw_chibi_xeron`)**: Keep Xeron in pure 2.5-head chibi proportions (`大圆头 + 小短身 + 小短爪`, `#0D0D0D` sumi-black fur, `#6E6378` muted grey-purple inner ears, flat-topped half-lidded `#2EE59D` mint-green aloof geek eyes). Never put Chibi Xeron on props like two-wheeled crank bicycles that force uncanny human-length legs.
- **Natural Pigment, Pressure & Paper Grain**: Render onto warm `#FAF8F3` cold-press cotton paper (`make_paper_stage`), pre-densified Tyler Hobbs wet-watercolor washes (`wet_watercolor_wash`, `max_px <= 10.5px`), variable-pressure dip-pen contours (`brush_stroke`), hand-hatched contact shadows (`soft_shadow`), draftsman leader-arrow callouts (`draw_draftsman_callout`), and playful Easter eggs (`draw_debug_duck_egg`, `draw_peek_mini_cat_egg`, `draw_sticky_badge`).
- **CJK Font Safety & Isolated `12fps` (`onTwos`) Line Boil**: Drive primary motion at silky `60fps` while locking organic hand-boil to `12fps` (`onTwos`) per element. Avoid unsupported `NotoSansCJK` glyphs (`↻`, `✗`, `♠`, `♦` — draw vector icons or brush strike-throughs instead so zero `☐` tofu boxes appear).

### Layer 2: Viewer Single-Read Timing Budget & Metaphor-First Logic (`观众单拍读点与声画同构`)

- **Metaphor-First 1:1 Audio-Visual Alignment & Single Scale**: Align spoken copy and visual props to the exact same physical metaphor (e.g., boiling glass kettle `20°C -> 88°C -> 99°C -> 100°C`) and never mix conflicting dual scales (`%` vs `°C`).
- **One Read at a Time (`viewer_read_envelope`)**: Sequence every beat across `Lead Eye (0.30–0.40s) -> Reverse Anticipation (0.15–0.20s) -> Fast Action Snap (0.22–0.28s) -> Payoff Hold (0.85–1.20s)`, staggering secondary motion (`eyes -> head -> torso -> paws -> ears/tail`) and reserving `#2EE59D` for threshold/payoff states.

### Layer 3: Continuous World & Breath-Valley Camera (`一镜连续世界摄影机`)

- **Kill PPT Slide Cross-Dissolves**: Never glue isolated slide functions with opacity fades. Place zones across a continuous workbench/stage and glide horizontally (`0.48–0.60s` `smootherstep` pan) inside `<short pause>` breath valleys.

### Layer 4: Multi-Act Pre-Render QA Gate (`全幕切片审片门禁`)

Never encode a full 2-minute film blind. Enforce deterministic `f(t)` rendering and inspect all-act QA contact sheets via `view_file` before `--encode`:
1. **Subtitle Safe-Zone Ink Lint**: Verify stage props/floor stay above `y = 850` so `y = 956` `40px` subtitles have `< 16%` background ink density.
2. **All-Act Visual Inspection**: Inspect every act's key sub-beats via `view_file` to verify zero `☐` tofu glyphs, zero ear/arrow text collisions, and clean Chibi silhouette poses.

## End-to-End Execution Steps

1. **Load Bundled Toolkit**: Load `scripts/cairo_handdrawn.py`, `scripts/xeron_clean_rig.py`, `scripts/v14_chibi_watercolor_kit.py`, and `references/director-and-style-rules.md` via `get_skill_resources`.
2. **Synthesize Single-Take `<short pause>` Voiceover**: Author one unified spoken script (`<= 5 min`) with explicit `<short pause>` breath cues and spaced acronyms (`S O P`), generate in a **single** `Puck` TTS call, align all clauses via `align_subs_on_raw_vowel_peaks`, and mix tactile foley + stereo Lo-Fi guitar BGM (`0.28` speech / `0.58` pause).
3. **Pass All-Act QA Gate -> Parallel Multi-Shard `60fps` Encode**: Inspect QA contact sheets via `view_file`, fix any micro-collisions, and encode `1920x1080 @ 60fps` (`CRF 19`) via `encode_turbo_film`.
