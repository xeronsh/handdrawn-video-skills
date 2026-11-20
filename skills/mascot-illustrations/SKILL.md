---
name: mascot-illustrations
description: Generate 16:9 hand-drawn conceptual illustrations, warm watercolor or mixed-media studio scenes, and paired 3:4 + 4:3 Chibi watercolor dual-cover posters starring a configurable creator mascot IP (`{{IP_PROFILE}}`, default solid-ink studio mascot with #2EE59D accent), complete with calligraphic brand signatures, dynamic C/S-spine or 2.5-head Chibi poses, hand-drawn social/GitHub icons, authentic AI product wireframes (Cursor, Claude Code, ChatGPT Canvas, DeepSeek-R1, MCP, Doubao, Muse, Grok Bot, Agent CLI), and playful AI slang metaphors (Vibe Coding, Gacha Roll, Hallucination, Context Rot, Token Assassin, Prompt Caching, Harness). Use whenever the user asks for article illustrations, video cover posters, storyboard concept cards, or hand-drawn workflow metaphors.
allowed-tools: image_gen
---
# Mascot Illustrations

Turn abstract judgments, workflows, AI tool comparisons, AI developer slang ("AI 黑话"), and video cover hooks into memorable hand-drawn ink & watercolor illustrations starring your configurable creator mascot IP (`{{IP_PROFILE}}`).

> **Portability Note**: On Gemini Web Tasks, call `image_gen:generate_image` (with `image_references` for consistency). On Claude Code / Codex / local CLI, pass the rendered prompts to your configured image-generation tool (Imagen / Gemini Image API / GPT Image / Flux).

## When to Use

- Generating **paired video cover posters** (`3:4` vertical + `4:3` horizontal for Douyin/Xiaohongshu, or `16:9` for Bilibili/YouTube)
- Generating `16:9` body illustrations for articles, blog posts, technical docs, or methodology notes
- Illustrating AI workflows, agent comparisons (`Cursor`, `Claude Code`, `ChatGPT Canvas`, `DeepSeek-R1`, `MCP`, `豆包`, `Meta Muse`, `Grok Bot`, `Agent CLI`), AI engineering methods (`Prompt Caching`, `Context Compaction`, `RAG`, `Harness`), or AI slang metaphors (`Vibe Coding`, `抽卡式编程`, `AI 幻觉`, `Context Rot`, `Token 刺客`, `炼丹蒸馏`)
- Producing warm watercolor scenes or mixed-media real-object studio scenes when tactile depth is requested

## Steps

### 1. Load Profile & Select One of the 3 Explicitly Separated Canvas Modes

Load `references/ip-and-style-dna.md` and `references/prompt-templates-and-qa.md` (via `get_skill_resources` or direct file read) and populate `{{IP_PROFILE}}` slots from `templates/ip-profile.example.yaml` (default example: **Ink Mascot / 墨水吉祥物**, `{{BRAND_NAME}}="InkCraft"`, `{{ACCENT_HEX}}="#2EE59D"`):

- **Mode 1.0 — Pure-White Editorial Illustration (`aspect_ratio="16:9"`)**: Pure `#FFFFFF` canvas edge-to-edge, 40%–55% drawn density, zero top-left title, 3–4 short handwritten labels (`2–5` chars), crisp non-chibi expressive editorial C/S-spine mascot proportions. Best for articles, blogs, and clean technical explainers.
- **Mode 2.0 — Warm Watercolor Scene / Mixed-Media Studio (`aspect_ratio="16:9"`)**: Choose either (2a) cold-press `#FAF8F3` watercolor illustration with wet-edge washes (`{{ACCENT_HEX}}` reserved for payoff) for storyboard concept plates, or (2b) mixed-media `#FFFFFF` tabletop with 1 real photographic physical object + flat 2D hand-drawn mascot interacting with it.
- **Mode 3.0 — Chibi Watercolor Dual-Cover Poster (`3:4` vertical + `4:3` horizontal, or `16:9`)**: Clean `#FAF8F3` cold-press watercolor paper (or `#FFFFFF` high-contrast variant), bold brush-pen 2-line Chinese cover headline at top with a `{{ACCENT_HEX}}` watercolor highlight bar + optional compact sub-line, hero **2.5-head Chibi mascot** beside 1–2 iconic props, and a neat bottom-right calligraphic `{{SIGNATURE_TEXT}}` signature. Generate `3:4` first, then pass its reference ID in `image_references` to generate the matched `4:3` horizontal cover.

### 2. Lock IP Consistency and Generate

Embed the full `{{MASCOT_VISUAL_LOCK}}` block from `references/ip-and-style-dna.md` (populated from `ip-profile.yaml`) into the image generation prompt. For multi-image batches or paired `3:4` + `4:3` covers, always pass the first confirmed output in `image_references` so anatomy, eyes, and line weight stay identical.

### 3. Visual QA and Surgical Clearance Edit

Inspect every generated graphic against the Mode-specific QA checklist in `references/prompt-templates-and-qa.md`:

- Verify clean background (zero unwanted outer border frame) and 100% accurate, legible Chinese/English strokes.
- **Cover Head/Ear-Clearance Check**: On `3:4` and `4:3` covers, verify there is a generous clean gap between any top subtitle text and the top of the mascot's ears/head. If text touches the silhouette, run 1 surgical edit scaling the mascot/prop group to ~90% and shifting it slightly downward.

## Gotchas

- **Never mix Mode 1.0 and Mode 3.0 style prompts**: Mode 1.0 forbids Chibi proportions and paper texture to stay ultra-crisp for editorial articles; Mode 3.0 explicitly embraces 2.5-head Chibi proportions and `#FAF8F3` cold-press watercolor texture for high-CTR social covers.
- **Never render realistic SaaS UI screenshots**: Draw `Cursor`, `Claude Code`, `ChatGPT Canvas`, `DeepSeek-R1`, `MCP`, `豆包`, `Muse`, `Grok Bot`, and `Agent CLI` as simplified hand-drawn pen UI wireframes matching each product's recognizable layout signature.
- **Chinese text overload causes typos**: Keep cover headlines to 2 short punchy lines (`4–7` chars each) plus at most 1 compact sub-line, and body labels to `2–5` common characters.
