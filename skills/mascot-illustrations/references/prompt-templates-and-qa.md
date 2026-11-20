# Prompt Templates, Metaphor Design & QA Checklist

Substitute `{{...}}` slots using the user's `ip-profile.yaml` (see `templates/ip-profile.example.yaml`; default `{{BRAND_NAME}}="InkCraft"`, `{{MASCOT_NAME}}="Ink Mascot"`, `{{ACCENT_HEX}}="#2EE59D"`, `{{PAPER_HEX}}="#FAF8F3"`).

## 1. Inventing Fresh Low-Tech Metaphors

Never draw formal box-and-arrow architecture charts. Translate abstract ideas in three steps:

1. **Turn the concept into a physical verb**: filtering, patching a leak, pulling a handbrake, weighing on a scale, unlocking a valve, rifling through drawers, boiling water to `100°C`, snapping a cartridge into a flywheel.
2. **Pick 1 or 2 low-tech props**: glass kettle, index-card cabinet, pipe valve, kitchen strainer, balance scale, funnel, turnstile gate with padlock, handbrake lever, mechanical press, workbench.
3. **Put `{{MASCOT_NAME}}` inside the action**: poking the kettle switch, straddling a cracked pipe with a wrench, sitting inside an open memory drawer turning a valve, or halting a cart at a stop line.

---

## 2. Mode 1.0 — Pure-White Editorial Illustration Template (`16:9`)

Best for articles, technical blogs, and clean conceptual diagrams (non-chibi editorial proportions, pure `#FFFFFF` background):

```text
Generate one standalone 16:9 horizontal Chinese conceptual editorial illustration.
Visual DNA: Pure solid white background (#FFFFFF) edge-to-edge. Minimalist black hand-drawn fountain-pen line art with thin, slightly wobbly imperfect lines. Huge amount of open empty white space (at least 45% pure blank white background). Clean absurd product-sketch feeling. Strictly NO gradients, NO drop shadows, NO paper texture, NO beige/gray tint, NO outer border frame, NO commercial vector style, NO PPT infographic boxes, NO cute chibi mascot proportions, NO realistic UI screenshots.
Recurring Personal IP character required: {{MASCOT_NAME}} — {{MASCOT_VISUAL_LOCK}} (editorial upright C/S-spine proportions, deadpan serious expression, compact torso, thin hand-drawn limbs, no clothes).
Core idea: [One-sentence conceptual point]
Composition:
- [Left / Input element and short label]
- [Center / Main physical action performed by {{MASCOT_NAME}} on 1-2 low-tech props]
- [Right / Output or contrast state and short label]
Handwritten Chinese annotations (render ONLY these 3-4 short labels clearly in neat casual Chinese handwriting, zero top-left title, zero extra English text):
1. [Black label: 2-5 chars]
2. [Orange flow label: 2-5 chars]
3. [Red warning/pain-point label: 2-5 chars]
4. [Optional Accent {{ACCENT_HEX}} or Blue state/result label: 2-5 chars]
Color use: Black ink (#141618) for primary line art, props, and silhouette; {{ACCENT_HEX}} core accent ONLY for mascot eyes and hero breakthrough/active state; Orange (#DE7A22) ONLY for main directional arrows/flow label; Red (#C93B35) ONLY for warning/pain-point accent. Keep drawn subject around 45% of canvas.
```

---

## 3. Mode 2.0 — Warm Watercolor Scene (`2.0a`) & Mixed-Media Studio (`2.0b`) (`16:9`)

### Mode 2.0a: Cold-Press Watercolor Concept Plate (`16:9`)

```text
Generate one standalone 16:9 hand-drawn watercolor illustration on warm cold-press cotton watercolor paper ({{PAPER_HEX}}) with subtle natural paper grain and zero outer border frame.
Visual DNA: Variable-pressure black dip-pen outlines (#151618) layered over soft translucent wet-edge watercolor washes (warm ochre, muted slate, and {{ACCENT_HEX}} reserved strictly for the active payoff/breakthrough state). Keep ~40% open breathing paper space.
Hero character: 2.5-head Chibi {{MASCOT_NAME}} — {{MASCOT_VISUAL_LOCK}} (compact big round head, short sturdy body, stubby expressive paws, composed deadpan expression).
Scene composition:
- [Hero prop & physical action performed by Chibi {{MASCOT_NAME}}]
- [1-2 hand-drawn curved-arrow draftsman callouts with 2-5 char Chinese notes]
- [Optional tiny corner geek Easter egg, e.g. yellow debug rubber duck wearing {{ACCENT_HEX}} glasses]
Bottom-right safe corner: small neat calligraphic signature "{{SIGNATURE_TEXT}}" with a subtle {{ACCENT_HEX}} brush underline. No PPT boxes, no realistic screenshots.
```

### Mode 2.0b: Mixed-Media Real-Object Studio Scene (`16:9`)

```text
Using the minimalist flat 2D hand-drawn {{MASCOT_NAME}} character ({{MASCOT_VISUAL_LOCK}}, editorial proportions), generate one standalone 16:9 mixed-media scene on a pure clean #FFFFFF white studio tabletop with at least 45% blank white space:
- [1 real photographic physical object group in soft studio lighting]
- [Flat 2D hand-drawn {{MASCOT_NAME}} physically interacting with the real object, casting a tiny soft contact shadow]
- [2-3 short handwritten Chinese labels + 1 hand-drawn orange arrow directly on the white background]
No UI screenshots, no PPT boxes, no border frame, no top-left title.
```

---

## 4. Mode 3.0 — Chibi Watercolor Dual-Cover Poster (`3:4` Vertical -> `4:3` Horizontal)

Generate the `3:4` vertical cover FIRST, verify typography and ear/head clearance, then pass its reference ID via `image_references` to generate the matched `4:3` horizontal cover (or `16:9` cover for Bilibili/YouTube).

### Step A — Primary Vertical Cover (`aspect_ratio="3:4"`)

```text
Generate a standalone 3:4 vertical video cover illustration in tactile hand-drawn dip-pen & cold-press watercolor style.

Visual DNA: Warm clean cold-press cotton watercolor paper background ({{PAPER_HEX}}) edge-to-edge (zero outer border frame, zero heavy vignette, zero realistic UI screenshots). Crisp variable-pressure black fountain-pen ink outlines (#151618) paired with soft translucent wet-edge watercolor washes and vibrant {{ACCENT_HEX}} hero accents. Preserve ~40% clean breathing paper space.

Hero Character (strict IP lock, 2.5-head Chibi proportions): 2.5-head Chibi {{MASCOT_NAME}} — {{MASCOT_VISUAL_LOCK}} (big round head, short compact torso, stubby paws, deadpan composed geek attitude).

Composition (3:4 vertical layout with a WIDE clean gap between top text and mascot ears/head):
- Upper Headline Area (centered bold black brush-pen Chinese hand-lettering, 100% crisp and legible):
  Line 1: "[4-6 char hook, e.g. 从踩坑到跑通]"
  Line 2: "[5-7 char payoff, e.g. 搭好这套自动化]" (with a vibrant {{ACCENT_HEX}} watercolor brush highlight bar beneath the key phrase)
  Optional Line 3: "[Short 3-pillar sub-line, positioned well above the mascot's ears/head with generous open paper clearance]"
- Center-to-Lower Hero Visual (scaled compactly inside the lower-middle 55% so the mascot never touches the headline): 2.5-head Chibi {{MASCOT_NAME}} [poking kettle / holding skill cartridge / pulling lever] beside [1 iconic watercolor prop with {{ACCENT_HEX}} threshold glow], flanked by 1-2 tiny floating hand-drawn metaphor icons.
- Bottom-right safe corner: Small neat calligraphic signature "{{SIGNATURE_TEXT}}" with a {{ACCENT_HEX}} brush underline stroke.
```

### Step B — Matched Horizontal Cover (`aspect_ratio="4:3"` or `"16:9"`, with `image_references=[cover_3x4_id]`)

```text
Using the exact 2.5-head Chibi {{MASCOT_NAME}} character, warm {{PAPER_HEX}} cold-press watercolor paper, {{ACCENT_HEX}} highlight palette, props, and brush-pen typography style from the reference 3:4 cover image, recompose it into a balanced 4:3 horizontal video cover poster:
- Keep the exact same 2-line Chinese headline (plus optional sub-line) centered cleanly in the upper-left or top zone with generous open paper clearance above the mascot's head/ears.
- Place Chibi {{MASCOT_NAME}} and the hero prop comfortably in the lower-center/right visual anchor with ~40% breathing whitespace.
- Keep the neat calligraphic "{{SIGNATURE_TEXT}}" signature with {{ACCENT_HEX}} underline in the bottom-right corner. Zero outer border frame, 100% accurate Chinese strokes.
```

---

## 5. Multi-Image Batch Consistency & Surgical Edit Templates

### Batch Consistency (`image_references=[confirmed_id]`)

```text
Using the exact {{MASCOT_NAME}} character design, line weight, and {{ACCENT_HEX}} color lock from the reference image, generate one standalone [16:9 / 3:4] illustration following [Mode 1.0 / Mode 2.0 / Mode 3.0] rules:
[Insert specific scene composition and 3-4 exact short Chinese labels]
```

### Surgical Clearance / Cleanup Edit (`image_references=[flawed_id]`)

```text
Edit the provided image by [removing ONLY the stray top-left title and filling seamlessly with surrounding background / scaling the mascot and prop group to ~90% and shifting it slightly downward to create a clean gap beneath the top headline]. Preserve the mascot character, all intended Chinese lettering, watercolor textures, line art, and composition unchanged.
```

---

## 6. Verifiable QA Checklist

Inspect every generated graphic before delivery:

- [ ] **Mode Match**: Aspect ratio matches target (`16:9` article/plate, `3:4` + `4:3` dual covers) and proportions match the chosen Mode (Mode 1.0 non-chibi pure `#FFFFFF`; Mode 2.0/3.0 warm `#FAF8F3` watercolor / 2.5-head Chibi).
- [ ] **Clean Canvas**: Zero unintended outer border frame, zero muddy vignette, at least `40%` breathing whitespace.
- [ ] **IP Lock**: `{{MASCOT_NAME}}` matches `ip-profile.yaml` silhouette, eye color (`{{MASCOT_EYE_HEX}}`), accent color (`{{ACCENT_HEX}}`), and active physical pose.
- [ ] **Cover Clearance**: On `3:4` and `4:3` covers, generous blank gap exists between headline/sub-line text and the top of the mascot's ears/head.
- [ ] **Typography Integrity**: 100% accurate, crisp Chinese characters with zero garbled strokes or stray English typos; zero unwanted slide headers in Mode 1.0.
