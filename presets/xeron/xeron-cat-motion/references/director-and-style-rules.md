# Xeron Studio Architecture: DIRECTOR · STYLE · TECHNIQUE & QA Specification (v11.0)

Inspired by open-source code-film architectures (`Lemo-Opuscar`, `ClaudeAnimationBase`, `Bang Motion`, `cth9191/animate`, `xiaoma-studio`, and `chaojifeng-video-design`), Xeron motion production strictly decouples **Directing (`DIRECTOR`)**, **Material Essence (`STYLE`)**, and **Frame Engineering & QA (`TECHNIQUE`)** so scene logic never corrupts visual craft.

---

## Part I — `DIRECTOR` Rules (Narrative, Viewer Read Budget & Audio-Visual Coupling)

### 1. Tacit Viewer Read Budgeting (`单拍单读点时间契约`)
- **Why AI Code Videos Feel Frantic Yet Lifeless**: Code defaults to moving every element simultaneously on a uniform `0 -> 1` curve and cutting the instant an interpolation finishes. Human eye-tracking requires sequential focal reads.
- **Mandatory 4-Phase Beat Envelope (`viewer_read_envelope`)**:
  - **Lead Eye (`0.30–0.40s`)**: Settle camera or Xeron's gaze on the target locus before anything fires.
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

### 2. "Show, Don't Write" & Radical Single-Focus Framing
- **Zero Redundant Text Banners**: Never place centered thesis banners, bracketed explanations, or drooping leader arrows that restate spoken lines. Only crisp, diegetic numbers/tokens (`0%`, `70%`, `80%`, `Fold`, `SOP`, `Skill`) that Xeron physically manipulates may appear in world space.
- **Expressive Shot Scale Rotation**: Rotate deliberately between Wide establishing (`u=20–24`), Medium acting (`u=28–36`), and Close-up emotional/tactile shots (`u=44–64`) instead of locking every act to the same medium-wide distance.

### 3. Three-Tier Audio-Visual Coupling (`三级声画瞬态咬合`)
- **Tier 1 — Macro Act (`段落`)**: Major narrative turns (`<short pause>` > `0.45s`) trigger a camera scale shift or object shape-morph relay.
- **Tier 2 — Phrase (`乐句/气口`)**: Intra-act clause breaths drive camera pan/drift relays or Xeron posture shifts (`crouch -> leap -> sit`).
- **Tier 3 — Vowel-Nucleus Transient (`重音字核`)**: Spoken stress peaks (`280–3200 Hz` vowel nuclei on words like `亮了`, `Fold`, `跑通`, `临界点`) trigger the exact frame of `#2EE59D` mint ignition, paw tap, or comic `draw_impact_ticks`.

---

## Part II — `STYLE` Rules (Material Physics & Silhouette Integrity)

### 1. Immutable Essence (NEVER Violate)
- **Protagonist**: Sleek warm-sumi black cat (`#0E0F12` fur, subtle `#42464E` rim sheen, muted `#6F637A` inner ears, half-lidded `#2EE59D` mint eyes with crisp white catchlights, composed geek-aloof acting).
- **One Color Means One Thing**: `#2EE59D` mint-emerald (`#0E875C` deep text/ink variant) represents **only** threshold crossing, live energy, or verified reusable Skill payoff. Keep pre-threshold states strictly in warm sumi ink (`#151618`) and 2B graphite (`#5D6066`).
- **Persistent Signature**: Bottom-right safe zone (`15%` breathing opacity cursive `Xeron` watermark) + subtle mint pen-stroke trail on agile leaps.

### 2. Decoupled Silhouette Assets vs. Natural Media Brushes
- **Ban Raw Primitive Stick-Drawing**: Never construct bicycles, hands, animals, or complex tools out of bare `rect`/`ellipse`/`line` coordinates (*"2000s Flash programmer art"*), and never project 3D perspective math. Compose props from unified closed silhouettes (*"One shape, one outline"*) or pre-validated 2D turnaround views (`front`, `3/4`, `side`).
- **Four-Pass Natural Media Stack**:
  1. **Warm Gallery Paper Base**: Crisp `#FFFFFF` to `#FCFAF6` paper surface finished with `apply_paper_grain` (`1.6–2.2%` multiplied organic fiber noise to kill sterile digital flat-white without muddying contrast).
  2. **2B Graphite Rough Pass (`pencil_underdraw`)**: Faint `12–16%` construction lines overshooting structural corners by `5–9px`.
  3. **Wet-Edge Copic / Watercolor Wash (`marker_wash_poly` / `p5.brush`)**: Offset (`3–4px` print misregistration) translucent gradient wash with darker outer wet-edge pigment pooling, plus hand-sketched diagonal hatch contact shadows (`soft_shadow`).
  4. **Variable-Pressure Dip-Pen Contour (`brush_stroke` / `perfect-freehand`)**: Analytical round-join strokes (`0.46x` hairline entry -> `1.06x` weighted belly -> `0.46x` exit) with isolated per-element `12fps` (`onTwos`) `boil_offset_xy(key, t)` so moving actors never cause background jitter.

---

## Part III — `TECHNIQUE` & Pre-Render QA Rules

### 1. Pure-Function `f(t)` Determinism & Continuous Morph Camera
- **Pure Frame Determinism**: Every frame `render_frame(t)` must be a pure deterministic function of timestamp `t` (zero mutable cross-frame state) so multi-shard parallel rendering and random-access QA strips match sequential playback pixel-for-pixel.
- **Continuous World + Shape-Morph Relay (`ContinuousCamera2D` + `shape_morph_poly`)**:
  - Replace per-scene `0.24s` opacity cross-dissolves with a persistent 2D world coordinate space, damped `ContinuousCamera2D` push-ins/pans, and arc-length-resampled closed contour morphing (`shape_morph_poly(poly_a, poly_b, u)`) so one hero visual motif transforms seamlessly into the next scene's core object.

### 2. Single-Take `<short pause>` Voiceover Contract
- Synthesize the entire narration (`<= 5 min`) in **one** `text_to_speech:generate_speech` call (`voice="Puck"`, explicit `<short pause>` breath markers, spaced acronyms `S O P`).
- Never splice multi-act TTS clips or apply `ffmpeg atempo`. Align subtitles (`40px` bold, `y=964` safe zone) directly onto the unedited WAV via vowel-nucleus peaks and `-38.0 dB` pause anchors, and master with gentle stereo Karplus-Strong Lo-Fi BGM (`0.29` speech / `0.60` pause).

### 3. Mandatory Three-Zoom Pre-Render QA Gate (`lint_and_render_3zoom_qa`)
Before launching full `60fps` `CRF 19` encoding, run `lint_and_render_3zoom_qa` and visually inspect all 3 outputs via `view_file`:
1. **Gate 1 — Automated Non-Visual Lint + 3 Full-Size `1920x1080` Look Frames**: Assert ink-to-paper contrast, subtitle safe-zone clearance (`y <= 910` for stage floor/props so `y=964` subtitles never collide), and zero out-of-frame clipping; inspect 3 full-res PNGs to sign off on silhouette craft and material texture before animating.
2. **Gate 2 — Contact Sheet + `0.1s` Motion Strip + Anti-Scramble Check**: Render a `10`-frame strip spaced `0.10s` apart across the primary action/morph window; verify visible reverse anticipation, clean contour morphing, `+250ms` motion gate (`> 0.45%`), and `+16.7ms` consecutive-frame stability (`< 5.0%` pixel diff).
3. **Gate 3 — `1:1` Native Pixel Contact Crops**: Inspect `400x400` `1:1` crops centered on Xeron's face/eyes, paw-to-prop contact points, and morph transitions to eliminate floating feet, tangent collisions, or broken strokes.
