# Handdrawn Motion Studio Architecture: DIRECTOR · STYLE · TECHNIQUE & QA Specification (v11.1)

Inspired by open-source code-film architectures (`Lemo-Opuscar`, `ClaudeAnimationBase`, `Bang Motion`, `cth9191/animate`, `xiaoma-studio`, and `chaojifeng-video-design`), studio motion production strictly decouples **Directing (`DIRECTOR`)**, **Material Essence (`STYLE`)**, and **Frame Engineering & QA (`TECHNIQUE`)** so scene logic never corrupts visual craft.

---

## Part I — `DIRECTOR` Rules (Narrative, Viewer Read Budget & Audio-Visual Coupling)

### 1. Tacit Viewer Read Budgeting (`单拍单读点时间契约`)
- **Why AI Code Videos Feel Frantic Yet Lifeless**: Code defaults to moving every element simultaneously on a uniform `0 -> 1` curve and cutting the instant an interpolation finishes. Human eye-tracking requires sequential focal reads.
- **Mandatory 4-Phase Beat Envelope (`viewer_read_envelope`)**:
  - **Lead Eye (`0.30–0.40s`)**: Settle camera or mascot gaze on the target locus before anything fires.
  - **Reverse Anticipation (`0.15–0.20s`)**: Crouch or pull `12–16%` in the opposite direction of the main force.
  - **Fast Action Snap (`0.22–0.28s`)**: High-velocity impulse crossing the space with `6–8%` organic overshoot.
  - **Payoff Hold (`0.85–1.20s`)**: Hold the resulting state steady (only `12fps` subtle ink boil + tail/ear damped settle) so the viewer absorbs the visual cause-and-effect before reacting or morphing.
- **Phase-Staggered Overlapping Action (`反肢体孪生同步`)**:
  - Never drive head, torso, paws, and tail on the exact same `t` phase. Offset downstream joints via `stagger_time(t, lag_frames)`:
    - Gaze shift: `0 frames`
    - Head turn/nod: `+3 to +4 frames`
    - Spine/torso lean: `+6 to +8 frames`
    - Limbs/paws: `+8 to +10 frames`
    - Ears & S-curve tail whip/settle: `+12 to +16 frames` (critically damped, zero bouncy default springs).

### 2. "Show, Don't Write" & Unified Draftsman Callout Policy
- **Ban PPT Thesis Banners & Glossary Cards**: Never place heavy centered thesis banners, opaque boxed summaries, or pop-up dictionary cards that restate spoken lines word-for-word.
- **Approve Tactile Draftsman Callouts & Diegetic Tokens**: Pair diegetic world numbers/tokens (`20°C`, `100°C`, `Fold`, `SOP`, `Skill`) with light, hand-drawn `draw_draftsman_callout` curved-arrow margin notes (`2–6` chars title + optional concise sub-note) and corner Easter eggs (`draw_debug_duck_egg`, `draw_peek_mini_mascot_egg`, `draw_sticky_badge`) when they sharpen visual cause-and-effect without crowding the silhouette.
- **Expressive Shot Scale Rotation**: Rotate deliberately between Wide establishing (`scale=1.0` / `u=20–24`), Medium acting (`scale=1.35` / `u=28–36`), and Close-up emotional/tactile shots (`scale=1.7+` / `u=44–64`) instead of locking every act to one static distance.

### 3. Three-Tier Audio-Visual Coupling (`三级声画瞬态咬合`)
- **Tier 1 — Macro Act (`段落`)**: Major narrative turns (`<short pause>` > `0.45s`) trigger a smooth breath-valley horizontal camera pan (`0.48–0.60s`), scale shift, or `shape_morph_poly` silhouette relay.
- **Tier 2 — Phrase (`乐句/气口`)**: Intra-act clause breaths drive camera drift or mascot posture shifts (`sit -> alert_crouch -> poke_kettle -> tea_happy`).
- **Tier 3 — Vowel-Nucleus Transient (`重音字核`)**: Spoken stress peaks (`280–3200 Hz` vowel nuclei on payoff words like `亮了`, `Fold`, `跑通`, `临界点`) trigger the exact frame of `accent_hex` (`#2EE59D`) ignition, paw tap, or comic `draw_impact_ticks`.

---

## Part II — `STYLE` Rules (Material Physics & Silhouette Integrity — v11.1)

### 1. Immutable Visual Contract (Configurable via `BrandConfig`)
- **Protagonist**: Pure 2.5-head Chibi silhouette (`draw_chibi_mascot`) or fluid C/S-spine actor (`draw_mascot_actor`) configured by `BrandConfig` (default: warm-sumi `#0D0D0D` solid-ink body, `#42464E` dry-brush rim sheen, muted `#6E6378` inner ears, flat-topped half-lidded `#2EE59D` eyes with crisp white catchlights, composed geek-aloof acting).
- **One Color Means One Thing**: `BrandConfig.accent_hex` (default `#2EE59D` emerald-mint / `#0E875C` deep ink variant) represents **only** threshold crossing, live energy, or verified reusable Skill payoff. Keep pre-threshold states strictly in warm sumi ink (`#151618`) and 2B graphite (`#5D6066`).
- **Persistent Calligraphic Signature**: Subtle corner watermark (`BrandConfig.watermark_text`) + calligraphic `draw_brand_signature` with accent brush underline on hero moments and motion trails.

### 2. Decoupled Silhouette Assets vs. Natural Media Brushes
- **Ban Raw Primitive Stick-Drawing**: Never construct bicycles, hands, animals, or complex tools out of bare `rect`/`ellipse`/`line` coordinates (*"2000s Flash programmer art"*), never put Chibi actors on props that force uncanny stretched legs, and never project 3D perspective math. Compose props from unified closed silhouettes (*"One shape, one outline"*).
- **Four-Pass Natural Media Stack (v11.1)**:
  1. **Warm Cold-Press Watercolor Paper Base (`#FAF8F3`)**: Generated once and blitted via `make_paper_stage` (`get_cold_press_paper_argb`, configurable via `BrandConfig.paper_hex`; optional pure `#FFFFFF` + `apply_paper_grain` `1.6–2.2%` fiber pass for editorial Mode 1.0 scenes).
  2. **2B Graphite Rough Pass (`pencil_underdraw`)**: Faint `12–16%` construction lines overshooting structural corners by `5–9px`.
  3. **Pre-Densified Wet-Edge Watercolor / Copic Wash (`wet_watercolor_wash`, `max_px <= 10.5px` / `marker_wash_poly`)**: Layered translucent watercolor bleed with darker outer wet-edge pigment pooling, plus hand-sketched diagonal hatch contact shadows (`soft_shadow`).
  4. **Variable-Pressure Dip-Pen Contour (`brush_stroke`)**: Analytical round-join strokes (`0.46x` hairline entry -> `1.06x` weighted belly -> `0.46x` exit) with isolated per-element `12fps` (`onTwos`) `boil_offset_xy(key, t)` so moving actors never cause background jitter.

---

## Part III — `TECHNIQUE` & Pre-Render QA Rules (v11.1)

### 1. Pure-Function `f(t)` Determinism & Continuous World Camera
- **Pure Frame Determinism**: Every frame `render_frame(t)` must be a pure deterministic function of timestamp `t` (zero mutable cross-frame state) so multi-shard parallel rendering (`encode_turbo_film`) and random-access QA strips match sequential playback pixel-for-pixel.
- **Continuous World + Shape-Morph Relay (`ContinuousCamera2D` + `shape_morph_poly`)**:
  - Replace per-scene opacity cross-dissolves with a persistent 2D world coordinate space, damped `ContinuousCamera2D` pans across `<short pause>` breath valleys, and arc-length-resampled closed contour morphing (`shape_morph_poly(poly_a, poly_b, u)`).

### 2. Strict Single-Take Raw-VO Voiceover & Audio Mastering Contract (v11.1)
- Synthesize the entire narration (`<= 5 min`) in **one** single-take TTS call (explicit `<short pause>` breath markers, spaced acronyms `S O P`).
- **NEVER** splice multi-act TTS clips, chop breaths with `pydub`, or apply `ffmpeg atempo`.
- Align `40px` bold subtitles (`y = 956` baseline, `y >= 938` safe band) directly onto the **unedited studio WAV** via `align_subs_on_raw_vowel_peaks` (`280–3200 Hz` vowel-nucleus peaks + `-38.0 dB` pause valleys).
- Master audio via `mix_stereo_master` with gentle stereo Karplus-Strong guitar Lo-Fi BGM ducked strictly to **`0.28` speech / `0.58` pause** (`bgm_speech_gain=0.28, bgm_pause_gain=0.58`) plus crisp climax foley cues.

### 3. Mandatory Three-Zoom Pre-Render QA Gate (`lint_and_render_3zoom_qa`)
Before launching full `60fps` `CRF 19` encoding, run `lint_and_render_3zoom_qa` and visually inspect all 3 outputs (`view_file` / multimodal read):

1. **Gate 1 — Automated Non-Visual Lint + Full-Size `1920x1080` Look Frames**: Assert ink-to-paper contrast, subtitle safe-zone clearance (stage floor/props above `y = 850`, `< 16%` ink density inside `y >= 938` band for `y = 956` subtitles), and zero screen-edge clipping (`< 6%` dark border pixels); inspect full-res PNGs for silhouette craft, zero `☐` missing CJK glyphs, and material texture before animating.
2. **Gate 2 — `0.1s` Motion Strip + `+16.7ms` Anti-Scramble Check**: Render an `8–10` frame strip spaced `0.10s` apart across the primary action/morph window; verify visible reverse anticipation, clean contour morphing, and `+16.7ms` consecutive-frame stability (`< 5.0%` pixel diff).
3. **Gate 3 — `1:1` Native Pixel Contact Crops**: Inspect `420x420` `1:1` crops centered on the mascot's face/eyes, paw-to-prop contact points, and callout arrows to eliminate floating feet, ear/text collisions, or broken strokes.
