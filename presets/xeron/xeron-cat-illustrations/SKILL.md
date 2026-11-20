---
name: xeron-cat-illustrations
description: Generate 16:9 pure-white hand-drawn Chinese conceptual illustrations, paired 4:3 + 3:4 Douyin/Bilibili cover posters, and mixed-media studio scenes starring the Xeron #2EE59D mint-green-eyed black cat Personal IP, complete with Xeron cursive signatures, dynamic C/S-spine poses, pure 2.5-head Chibi watercolor options, hand-drawn social/GitHub icons, authentic AI product wireframes (Cursor, Claude Code, ChatGPT Canvas, DeepSeek-R1, MCP, Doubao, Muse, Grok Bot, Personal Agent CLI), and playful AI slang metaphors (Vibe Coding, Gacha Roll, Hallucination, Context Rot, Token Assassin, Prompt Caching, Harness). Use whenever the user asks for article illustrations, Douyin 4:3 or 3:4 video covers, storyboard concept cards, clean flat-shaded bold-ink 2D hand-drawn cat or Xeron-cat-style drawings, workflow metaphors, or 2.0 real-object scenes.
allowed-tools: image_gen
---
# Xeron Cat Illustrations

Turn abstract judgments, workflows, AI tool comparisons, AI developer slang ("AI 黑话"), and video cover hooks into memorable hand-drawn ink & `#2EE59D` watercolor illustrations starring the Xeron `#2EE59D` mint-green-eyed black cat IP.

## When to Use

- Generating paired **Douyin `4:3` horizontal (`横封面 4:3`) + `3:4` vertical (`竖封面 3:4`)** or `16:9` Bilibili video cover posters
- Generating `16:9` body illustrations for Chinese articles, blog posts, WeChat posts, Notion docs, or methodology notes
- Illustrating AI workflows, agent comparisons (`Cursor`, `Claude Code`, `ChatGPT Canvas`, `DeepSeek-R1`, `MCP`, `豆包`, `Meta Muse`, `Grok Bot`, `Personal Agent CLI`), AI engineering methods (`Prompt Caching`, `Context Compaction`, `RAG`, `Harness`), or AI slang metaphors (`Vibe Coding`, `抽卡式编程`, `AI 幻觉`, `Context Rot`, `Token 刺客`, `炼丹蒸馏`)
- Producing 2.0 mixed-media real-object studio scenes when tactile realism is requested

## Steps

### 1. Read References and Select Canvas Mode

Load `references/ip-and-style-dna.md` and `references/prompt-templates-and-qa.md` via `get_skill_resources`:

- **Article / Storyboard Mode (`aspect_ratio="16:9"`)**: Pure `#FFFFFF` canvas, 40% to 55% drawn density, zero top-left title, 3 to 4 short handwritten Chinese labels (`2 to 5` chars).
- **Douyin Dual-Cover Poster Mode (Paired `aspect_ratio="3:4"` vertical + `aspect_ratio="4:3"` horizontal)**: Clean `#FAF8F3` cold-press watercolor paper or `#FFFFFF` background, bold brush-pen 2-line Chinese cover headline at top with a `#2EE59D` mint-green watercolor highlight bar + compact sub-line, hero 2.5-head Chibi or expressive C/S-spine Xeron black cat beside central props, and a neat bottom-right `Xeron` cursive signature. Generate `3:4` first, then pass its reference ID in `image_references` to generate the matched `4:3` horizontal cover.

### 2. Lock IP Consistency and Generate

Embed the full Xeron black cat visual lock from `references/ip-and-style-dna.md` into `image_gen:generate_image` (solid `#0D0D0D` cat, sharp upright triangular ears with `#6E6378` muted grey-purple inner ears, flat-topped half-lidded `#2EE59D` mint-green aloof geek eyes with vertical slit pupils, two short grey whiskers per cheek). For batches or paired `4:3` + `3:4` covers, pass the confirmed image in `image_references`.

### 3. Visual QA and Surgical Ear-Clearance Edit

Inspect every generated graphic against `references/prompt-templates-and-qa.md`:

- Verify clean background (zero outer border frame) and 100% accurate, legible Chinese strokes.
- **Cover Ear-Clearance Check**: On `3:4` and `4:3` covers, verify there is a generous clean gap between any top subtitle text and Xeron's pointed ear tips. If text touches an ear tip, run 1 surgical edit scaling the cat/prop group to ~90% and shifting it slightly downward.

## Gotchas

- **Never render realistic SaaS UI screenshots**: Draw `Cursor`, `Claude Code`, `ChatGPT Canvas`, `DeepSeek-R1`, `MCP`, `豆包`, `Muse`, `Grok Bot`, and `Agent CLI` as simplified hand-drawn pen UI wireframes matching each product's real layout signature.
- **Chinese text overload causes typos**: Keep cover headlines to 2 short punchy lines (`4 to 7` chars each) plus at most 1 compact sub-line, and body labels to `2 to 5` common characters.
