# Prompt Templates, Metaphor Design & QA Checklist

## 1. Inventing Fresh Low-Tech Metaphors

Never draw formal box-and-arrow architecture charts. Translate abstract ideas in three steps:

1. **Turn the concept into a physical verb**: filtering, patching a leak, pulling a handbrake, weighing on a scale, unlocking a valve, rifling through drawers, pressing out finished parcels.
2. **Pick 1 or 2 low-tech props**: index-card cabinet, pipe valve, kitchen strainer, balance scale, funnel, turnstile gate with padlock, handbrake lever, workbench, mechanical press, mailbox.
3. **Put the Xeron black cat inside the action**: straddling a cracked pipe with a wrench, sitting inside an open memory drawer turning a valve, catching key envelopes with a sieve, or halting a cart at a stop line.

## 2. Mode 1.0 Standalone Prompt Template (`16:9`)

Fill in the bracketed slots and pass to `image_gen:generate_image` with `aspect_ratio="16:9"`:

```text
Generate one standalone 16:9 horizontal Chinese article illustration.
Visual DNA: Pure solid white background (#FFFFFF) edge-to-edge. Minimalist black hand-drawn pen line art with thin, slightly wobbly imperfect lines. Huge amount of empty white space (at least 45% pure blank white background). Clean absurd product-sketch feeling. Strictly NO gradients, NO drop shadows, NO paper texture, NO beige/gray tint, NO border frame, NO commercial vector style, NO PPT infographic boxes, NO cute chibi mascot style, NO realistic UI screenshots.
Recurring Personal IP character required: Xeron Black Cat, an upright minimalist solid-black cat worker with two sharp pointed triangular ears with muted grey-purple (#6E6378) inner ears, bright mint-green (#2EE59D) flat-topped half-lidded aloof geek eyes with vertical black pupils, tiny dark-grey nose, two short dark-grey whiskers per cheek, closed invisible mouth, compact solid-black oval torso, thin black hand-drawn stick arms and legs, and a thin curved black cat tail (no clothes, deadpan serious expression, not cute).
Core idea: [One-sentence conceptual point]
Composition:
- [Left / Input element and short label]
- [Center / Main physical action performed by Xeron Black Cat on 1-2 low-tech props]
- [Right / Output or contrast state and short label]
Handwritten Chinese annotations (render ONLY these 3-4 short labels clearly in neat casual Chinese handwriting, zero top-left title, zero extra English text):
1. [Black label: 2-5 chars]
2. [Orange flow label: 2-5 chars]
3. [Red warning/pain-point label: 2-5 chars]
4. [Optional Blue state/result label: 2-5 chars]
Color use: Black ink for all line art, props, and the cat's solid-black body (keeping only its muted grey-purple inner ears and bright mint-green eyes). Orange ink ONLY for main directional arrows and flow label. Red ink ONLY for key warning/problem accent. Blue ink ONLY for calm status/result note. Keep drawn subject around 45% of canvas.
```

## 3. Multi-Image Batch Consistency Template (Using `image_references`)

When generating 3 or more illustrations in one session, pass the first confirmed Xeron cat image (or IP sheet) in `image_references` so every subsequent shot keeps identical facial geometry:

```text
Using the upright minimalist black cat worker character from the reference image (solid black head and compact oval body, sharp pointed ears with muted grey-purple inner ears, bright mint-green flat-topped half-lidded aloof eyes, two short dark-grey whiskers per cheek, thin black stick limbs, thin black tail), generate one standalone 16:9 horizontal Chinese article illustration on a pure solid #FFFFFF white background with thin wobbly black hand-drawn pen lines and at least 45% empty white space...
[Insert specific scene composition and 3-4 exact short Chinese labels]
```

## 4. Mode 2.0 Real-Object Studio Prompt Template (`16:9`)

```text
Using the minimalist flat 2D solid-black hand-drawn cat worker character (pointed ears with muted grey-purple inner ears, bright mint-green flat-topped half-lidded aloof eyes, two short dark-grey whiskers per cheek, thin stick limbs and cat tail), generate one standalone 16:9 mixed-media scene on a pure clean #FFFFFF white studio tabletop with at least 45% blank white space:
- [1 real photographic physical object group in soft studio lighting]
- [Flat 2D hand-drawn Xeron black cat physically interacting with the real object, casting a tiny soft contact shadow]
- [2-3 short handwritten Chinese labels + 1 hand-drawn orange arrow directly on the white background]
No UI screenshots, no PPT boxes, no border frame, no top-left title.
```

## 5. Verifiable QA Checklist

Check every generated image before showing it to the user:

- [ ] Aspect ratio is `16:9` (or panoramic `21:9` / `4:1` for long-scroll mode).
- [ ] Background is clean pure `#FFFFFF` white with zero beige tint, paper grain, vignette, or outer frame.
- [ ] At least 40% of the canvas is open whitespace.
- [ ] Xeron black cat has pointed ears (muted grey-purple inner), flat-topped half-lidded bright mint-green eyes, and short whiskers (not a round earless blob and not a cute wide-eyed cartoon kitten).
- [ ] Xeron black cat performs the core physical action rather than standing idle on the side.
- [ ] All handwritten Chinese characters are accurate, legible, and free of garbled strokes.
- [ ] Zero English words appear on the canvas except intentional technical proper nouns.
- [ ] Zero slide titles or diagram category headers appear in the top-left corner.

### Surgical Edit Prompt (If a Stray Title or Minor Flaw Appears)

Pass the flawed image in `image_references` and call `image_gen:generate_image`:

```text
Edit the provided image by removing ONLY [the stray top-left title / wrong label] and filling that area seamlessly with the surrounding pure #FFFFFF white background. Preserve the black cat character, all other handwritten Chinese labels, line art, arrows, and composition unchanged.
```

## 6. Douyin / Social Video Cover Poster Template (`aspect_ratio="3:4"`)

Use this verified prompt template whenever generating a `3:4` vertical cover (`竖封面 3:4`) for Douyin, Bilibili, or Xiaohongshu:

```text
Generate a standalone 3:4 vertical Douyin video cover illustration in minimalist Chinese hand-drawn ink style.

Visual DNA: Pure solid white background (#FFFFFF) edge-to-edge. Minimalist black fountain-pen hand-drawn line art with crisp organic ink strokes and vibrant mint-green (#2EE59D) core accents. Around 45% open pure-white space. Strictly NO paper texture, NO beige/gray tint, NO gradients, NO drop shadows, NO outer border frame, NO cute chibi style.

Hero Character (strict IP lock): Xeron Black Cat - a minimalist upright solid-black (#0D0D0D) cat character with two sharp pointed triangular ears featuring muted grey-purple (#6E6378) inner ears, iconic flat-topped half-lidded bright mint-green (#2EE59D) aloof geek eyes with vertical black slit pupils, tiny dark-grey nose, two short dark-grey whiskers on each cheek, compact solid-black oval torso (no clothes), thin black stick limbs, and a curved black cat tail.

Composition (3:4 vertical layout with wide pure-white gap between top text and cat ears):
- Upper Headline Area (centered bold black brush-pen Chinese hand-lettering, 100% crisp and legible):
  Line 1: "[4-6 char hook, e.g. 别再重复造轮]"
  Line 2: "[5-7 char payoff, e.g. 把流程做成Skill]" (with a vibrant #2EE59D mint-green marker highlight bar beneath the key phrase)
  Optional Line 3: "[Short 3-pillar sub-line, positioned with generous white space well above the cat's ear tips]"
- Center-to-Lower Hero Visual (scaled compactly in lower-middle 55% so ear tips never touch top text): Xeron Black Cat [sitting with folded arms / sipping tea / pulling lever] atop [1 iconic mechanical or conceptual prop with #2EE59D mint-green highlights], flanked by 1-2 tiny floating hand-drawn metaphor icons.
- Bottom-right safe corner: Small neat cursive signature "Xeron" with a #2EE59D mint-green underline stroke.
```
