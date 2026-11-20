# Mascot IP Profile Slots, Visual Style DNA & Authentic AI-UI / Jargon Sketch Guide

## 1. Configurable Character Lock (`{{IP_PROFILE}}`)

Every illustration stars your creator mascot as a composed, expressive system operator performing the core physical action (never a stiff mannequin or idle corner sticker). Fill these template slots from `templates/ip-profile.example.yaml`:

| Slot | Default Neutral Example (`Ink Mascot / 墨水吉祥物`) | Purpose |
|---|---|---|
| `{{BRAND_NAME}}` | `InkCraft` | Creator / studio name |
| `{{SIGNATURE_TEXT}}` | `InkCraft` | Calligraphic corner signature |
| `{{MASCOT_NAME}}` | `Ink Mascot` (`墨水吉祥物`) | Character label in prompts |
| `{{MASCOT_SPECIES}}` | Minimalist solid-ink cat | Swappable to owl, fox, shiba, panda, studio bot, etc. |
| `{{MASCOT_PRIMARY_HEX}}` | `#0D0D0D` | Primary body/head silhouette color |
| `{{MASCOT_SECONDARY_HEX}}` | `#6E6378` | Secondary anatomical accent (e.g., muted grey-purple inner ears) |
| `{{MASCOT_EYE_HEX}}` | `#2EE59D` | Signature expressive eye color |
| `{{ACCENT_HEX}}` | `#2EE59D` | Hero highlight, payoff, active badge & underline color |
| `{{PAPER_HEX}}` | `#FAF8F3` | Warm cold-press cotton watercolor paper (Modes 2.0 & 3.0) |

### Default Neutral Example Features (`Ink Mascot / 墨水吉祥物`)

- **Silhouette & Ink**: Pure solid-ink (`#0D0D0D`) hand-drawn head and compact torso with slightly organic fountain-pen outlines (no clothes).
- **Distinctive Markers**: Two sharp upright triangular ears with muted grey-purple (`#6E6378`) inner ears, flat-topped half-lidded bright mint-green (`#2EE59D`) aloof geek eyes with vertical slit pupils (or mint-rimmed dark shades during Vibe Coding), tiny dark-grey nose, and two short whiskers per cheek.
- **Two Explicit Proportion Systems (Never Confuse)**:
  - **Editorial C/S-Spine Proportions (Mode 1.0 & 2.0b)**: Flexible C/S-curve spine for agile full-body metaphors — leaning forward when typing, reclining with coffee and `[Tab]` key, facepalming while debugging hallucinations, pulling a slot-machine lever, or leaping with a flowing S-tail on eureka moments.
  - **Pure 2.5-Head Chibi Proportions (Mode 2.0a & Mode 3.0)**: Compact big round head, short sturdy body, and stubby expressive paws (`大圆头 + 小短身 + 小短爪`) tailored to warm watercolor scenes and high-impact `3:4` / `4:3` social covers. Never place a Chibi mascot on props like crank bicycles that stretch legs unnaturally.

---

## 2. Three Separated Visual Modes

### Mode 1.0 — Pure-White Editorial Illustration (`16:9` / `21:9`)

- **Canvas**: Pure solid `#FFFFFF` background edge-to-edge (zero paper grain, zero beige cast, zero drop shadows, zero outer border frame).
- **Whitespace Budget**: Drawn elements occupy `40%–55%` of the canvas, preserving at least `45%` open pure-white space.
- **Proportions**: Editorial C/S-spine mascot (strictly non-chibi).
- **Strict Color Coding**:
  - **Primary Ink (`#141618`)**: Line art, mechanical/UI props, hand-drawn icons, primary labels, and mascot silhouette (`{{MASCOT_PRIMARY_HEX}}`).
  - **Core Accent (`{{ACCENT_HEX}}`, default `#2EE59D` / deep ink `#0D8E5F`)**: Hero highlights, active Tab/Cache/MCP badges, and mascot eyes (`{{MASCOT_EYE_HEX}}`).
  - **Secondary Marker Accents**: Orange (`#DE7A22`), Red (`#C93B35`), or Blue (`#2B548E`) sparingly for flow arrows, warnings, or status notes.

### Mode 2.0 — Warm Watercolor Scene (`2.0a`) or Mixed-Media Studio (`2.0b`) (`16:9`)

- **Mode 2.0a — Cold-Press Watercolor Concept Plate**: Warm `#FAF8F3` cotton watercolor paper, translucent wet-edge pigment washes, dip-pen ink contours, and `{{ACCENT_HEX}}` payoff glow (matches the `handdrawn-motion` v11.1 video look).
- **Mode 2.0b — Mixed-Media Real-Object Studio Scene**: Place 1 compact real photographic tabletop object (mechanical keyboard, laptop, crumpled notes, brass clip) on a clean `#FFFFFF` studio tabletop with soft natural contact shadows, while the flat 2D hand-drawn `{{MASCOT_NAME}}` physically interacts with it.

### Mode 3.0 — Chibi Watercolor Dual-Cover Poster (`3:4` Vertical + `4:3` Horizontal)

- **Canvas**: Warm cold-press cotton watercolor paper (`{{PAPER_HEX}}`, default `#FAF8F3`) or crisp `#FFFFFF` high-contrast variant, zero outer border frame.
- **Proportions**: Hero **2.5-head Chibi** `{{MASCOT_NAME}}` with expressive tactile props and wet-edge watercolor washes.
- **Typography & Safe Zone**: Bold 2-line brush-pen Chinese headline at top (`4–7` chars per line) with a `{{ACCENT_HEX}}` watercolor highlight swipe beneath the payoff phrase, generous whitespace gap above ear/head tips, and neat bottom-right calligraphic `{{SIGNATURE_TEXT}}` signature.

---

## 3. Authentic AI Interfaces, Engineering Methods & AI Slang Sketch Vocabulary

Draw crisp hand-drawn pen wireframes and physical visual metaphors (never pasted screenshots):

### Authentic AI Product Interfaces
- **Cursor IDE**: Left file tree + code editor showing dashed `{{ACCENT_HEX}}` inline ghost-text autocomplete next to a `[Tab]` key badge + bottom `Composer` multi-file bar.
- **Claude Code**: Terminal TUI with `╭─ ✻ Claude Code ─╮` header, `Plan` (`Shift+Tab`) pill, `Subagents` task tree, `+ / -` diff lines, `Ultrathink` reasoning bar, and `>` prompt.
- **ChatGPT & Canvas**: 6-loop knot emblem + voice-wave pill bar, or split-view `Canvas` with chat on left and live editor + `[润色/修Bug]` floating pill on right.
- **DeepSeek-R1**: Whale badge + collapsible left-bordered quote block `>> 已深度思考 (12s)` above the final answer.
- **MCP (`Model Context Protocol`)**: "USB-C for AI" universal multi-port dock snapping `GitHub`, `Browser`, and `SQL/Docs` USB-C plugs into an Agent.
- **豆包 / Meta Muse / Grok Bot / Agent CLI (`>_`)**: Right-docked companion sidebar (`豆包`), top-avatar borderless proactive cards + `Secure VM` (`Muse`), orbital mark + shared Cloud PC (`Grok Bot`), or headless tiling TUI with `12ms` main chat + parallel `BG#1/#2` worker slots (`Agent CLI`).

### AI Engineering Methods & Playful AI Slang ("AI 黑话")
- **Vibe Coding (`氛围编程`)**: `{{MASCOT_NAME}}` in accent shades sipping coffee and tapping one giant `[Tab]` key while a precarious Jenga tower of `[!] 别动能跑` blocks wobbles behind.
- **Gacha Prompting (`抽卡式编程`)**: 3-reel slot machine (`报错 | 重写 | SSR!`) with `{{MASCOT_NAME}}` yanking the side lever.
- **Hallucination (`AI 幻觉`)**: Shiny floating soap bubbles containing confident nonsense like `1+1=5` and `胡编API()`.
- **Context Rot (`上下文腐烂 / 降智区`)**: Whiteboard crisp at top (`4k 清醒区`) melting into smudged grey scribbles at bottom (`128k 降智失忆`).
- **Token Assassin (`Token 刺客`)**: Wildly spinning `$` meter devouring flying banknotes.
- **Prompt Caching & Harness (`前缀缓存与三层护栏`)**: Padlocked `{{ACCENT_HEX}}` static prefix block (`省90%`), funnel-to-`Handoff` compaction baton, and nested `Prompt ⊂ Context ⊂ Harness` concentric guardrails.
