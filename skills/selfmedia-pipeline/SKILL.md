---
name: selfmedia-pipeline
description: 'End-to-end production pipeline for hand-drawn mascot IP self-media explainer videos (Douyin, Bilibili, Xiaohongshu, YouTube), powered by the Four-Layer Anti-AI Craft Architecture (2.5-head Chibi watercolor silhouette assets, single-read viewer timing budget, continuous-world camera without PPT cross-fades, and all-act pre-render QA gates), single-take <short pause> prosody voiceover, vowel-nucleus synced 40px subtitles, stereo Karplus-Strong Lo-Fi guitar BGM, configurable platform compliance shield, mandatory paired 3:4 + 4:3 dual covers, ready-to-paste copy bundle, and cloud/local backup.'
allowed-tools: text_to_speech image_gen drive google default_api
---
# Selfmedia Pipeline (v3.1 — Portable Hand-Drawn Watercolor Craft, Single-Take Prosody, Dual Covers & Full Copy Bundle)

Turn a topic, draft, or script into a publish-ready, platform-compliant `16:9` `60fps` (`CRF 19`) hand-drawn animated explainer video — ALWAYS bundled automatically upon video completion with **paired cover posters** (default `3:4` vertical + `4:3` horizontal, or platform-configured ratios), **ready-to-paste titles, descriptions, and hashtags (`标题 + 简介 + 话题`)**, and **cloud/archive backup**.

> **IP & Platform Configuration**: Read the user's `ip-profile.yaml` (see `templates/ip-profile.example.yaml`) if supplied. When none is provided, apply the clean neutral defaults (`InkCraft` brand, `#2EE59D` emerald-mint accent, solid-ink studio mascot, `#FAF8F3` cold-press paper, `douyin` + `bilibili` delivery preset).

## Runtime Portability Matrix

Default tool names below target **Gemini Web Tasks** (`allowed-tools: text_to_speech image_gen drive google default_api`). When running in **Claude Code**, **Codex**, or a **local `uv` CLI** environment, map each stage to its local equivalent without changing the creative contract:

| Pipeline Stage | Gemini Web Tasks (Default) | Claude Code / Codex / Local `uv` CLI |
|---|---|---|
| Load sub-skills & refs | `lookup_skills`, `get_skill_resources` | Read `skills/<name>/SKILL.md`, `references/*.md`, `scripts/*.py` |
| Single-take VO synthesis | `text_to_speech:generate_speech` | Google Cloud TTS / Edge-TTS / ElevenLabs / OpenAI TTS -> raw mono WAV |
| Render & audio mixing | Linux sandbox Python (`pycairo`, `ffmpeg`) | `uv run python <render_script>.py` (with `pyproject.toml` + `ffmpeg`) |
| Pre-render visual QA | `view_file` on exported PNGs | Multimodal image read tool on exported PNGs |
| Paired cover posters | `image_gen:generate_image` (`image_references`) | Gemini Image / Imagen / GPT Image / Flux API with reference image |
| Backup & artifact delivery | `drive:create_file`, `google:show_file` | Local `output/` directory + optional `rclone` / cloud upload |

## Core Creative, Audio & Compliance Contract

### 1. Four-Layer Anti-AI & Anti-Homogenization Craft Architecture (`四层去 AI 味与反模板底座`)

Delegate motion rendering to `handdrawn-motion` (`chibi_watercolor_kit.py` + `cairo_handdrawn.py` v5.0 + `motion_rig_kit.py`), strictly enforcing all four layers:

- **Layer 1 — Pure 2.5-Head Chibi Silhouette & Natural Watercolor Media (`纯正二头身造型与水彩笔刷介质`)**:
  - **Proportional Mascot Integrity**: Keep the IP mascot in clean 2.5-head Chibi proportions (`大圆头 + 小短身 + 小短爪`, configured via `BrandConfig` with `mascot_primary_hex`, `mascot_inner_ear_hex`, `mascot_eye_hex`). Never place a Chibi mascot on props (such as two-wheeled crank bicycles) that force uncanny stretched human legs.
  - **Metaphor-First 1:1 Alignment & Single Unified Scale**: Align spoken copy and visuals to the exact same concrete physical metaphor (e.g., boiling glass kettle `20°C -> 88°C -> 99°C -> 100°C`), and never mix conflicting dual scales (such as `70%/80%` percentages alongside `100°C` physical temperature).
  - **Tactile Paper & Pen Media**: Layer warm `#FAF8F3` cold-press cotton paper grain (`make_paper_stage`), pre-densified wet-edge watercolor washes (`wet_watercolor_wash`, `max_px <= 10.5px`), variable-pressure dip-pen contours (`12fps` `boilSeed` over `60fps` primary motion), hand-drawn `draw_draftsman_callout` leader arrows, and corner Easter eggs (yellow Debug Rubber Duck, peeking mini mascot, achievement toasts). Avoid missing `NotoSansCJK` symbols (`↻`, `✗`, `♠`, `♦` — draw vector icons or brush strike-throughs instead).
- **Layer 2 — Viewer Single-Read Timing Budget & Phase Stagger (`观众单拍读点时间预算`)**:
  - **One Read at a Time**: Sequence every beat via `Lead Eye (0.30–0.40s) -> Reverse Anticipation (0.15–0.20s) -> Fast Snap (0.22–0.28s) -> Payoff Hold (0.85–1.20s)`.
  - **Anti-Twinning**: Stagger motion phases (`eyes -> head +3f -> torso +6f -> limbs -> ears/tail`) via critically damped curves, reserving `accent_hex` (default `#2EE59D`) strictly for threshold/payoff states.
- **Layer 3 — Continuous World & Breath-Valley Camera (`一镜连续世界摄影机`)**:
  - **No PPT Slide Cross-Dissolves**: Never glue isolated slide functions with opacity fades. Drive continuous horizontal/camera pans (`0.48–0.60s` `smootherstep`) cleanly across `<short pause>` breath valleys.
- **Layer 4 — Multi-Act Pre-Render QA Gate (`全幕切片审片门禁`)**:
  - Export and inspect full-act QA contact sheets / Look Frames (`lint_and_render_3zoom_qa`) **before** full video encoding, verifying zero `☐` missing-glyph boxes, zero ear/prop text collisions, and zero intrusion into the `y >= 938` subtitle safe band (props above `y = 850`, subtitles at `y = 956`).

### 2. Single-Take `<short pause>` Prosody Voiceover + 3-Tier Audio-Visual Sync (`100% 音色语速统一`)

- **Never** generate multi-act TTS clips or apply `pydub` breath-chopping / `ffmpeg atempo`.
- Author **one unified prosody script** (`<= 5 min`, default `language_code="cmn-CN"`, `voice="Puck"`, configurable via `ip-profile.yaml`) with explicit `<short pause>` tags at thought/act breaks and spaced letter acronyms (`S O P`).
- Align `40px` subtitles (`y = 956`) directly onto the **unedited studio WAV** via `align_subs_on_raw_vowel_peaks` (`280–3200 Hz` vowel-nucleus peaks + `-38.0 dB` pause valleys), mix tactile foley cues at narrative climaxes, and add stereo Karplus-Strong guitar Lo-Fi BGM (`0.28` speech / `0.58` pause).

### 3. Configurable Platform Multi-Modal Pre-Audit Shield (`多平台语音 ASR + 画面 OCR + 文案防雷红线`)

Apply the compliance preset matching `platform.preset` across spoken TTS script, subtitles, on-screen tokens/icons, and post captions **before** generating audio or frames:

- **Douyin Preset (`douyin`, Default)**:
  - **No Gambling, Exploit, Grey-Market, or Money-Inducement Keywords**: Scrub `赌博` (`别赌博梭哈` -> `千万别上头梭哈`), `硬核漏洞`, `爆漏洞`, `破解`, `白嫖`, `躺赚` -> use `硬核排障经验`, `算力特惠`, `一步登天`.
  - **No Anti-Bot / Multi-Account Bypass Terms**: Scrub `防风控`, `触发风控`, `绕过风控`, `群控`, `养号`, `指纹浏览器/沙盒管号`, `自动续期 Cookie` -> use `本地隔离浏览器环境`, `保持常用服务稳定在线`, `告别重复扫码`.
  - **No Competitor Platform Names/Logos in Automation/Traffic Contexts**: Scrub `小红书`, `闲鱼`, `微信`, `快手`, `B站` as automated targets or funnels -> use `闲置好物平台`, `日常内容账号`, `常用生活网页`.
  - **No Cross-Border Proxy / Blocked Social Media / Unregistered App Calls**: Scrub public proxy IPs (e.g. RFC 5737 doc example `203.0.113.x`), `动态/固定 IP`, `登录海外受限服务` -> use `云端临时连接易重置`, `联动内容创作工作流`.
  - **Mandatory Publish Reminders**: Remind the creator to upload over a direct domestic connection and enable `自主声明 -> 内容由 AI 生成` when applicable.
- **Xiaohongshu Preset (`xiaohongshu`)**: Scrub off-platform contact funnels (`加V`, `私信领`, external links), absolute superlatives (`全网第一`, `100%有效`), and grey-market phrasing.
- **Bilibili Preset (`bilibili`)**: Preserve deep technical vocabulary, scrub grey-market exploits and clickbait violations, and include exact sample-accurate chapter timestamps.
- **YouTube Preset (`youtube`)**: Keep procedural copyright-free BGM/SFX, advertiser-friendly phrasing, clean chapter timestamps (`00:00` required), and high-contrast `16:9` thumbnail readability.

## Execution Workflow & Mandatory Post-Video Delivery Bundle

1. **Profile Load, Compliance Scrub & Prosody `<short pause>` Script**: Load `script-storyboard`, `handdrawn-motion`, and `mascot-illustrations` (via `lookup_skills` on Gemini Web Tasks or local skill reads). Apply the active `BrandConfig` / `ip-profile.yaml`, scrub sensitive terms per platform preset, align metaphors 1:1 between spoken copy and visuals, and author the single-take `<short pause>` TTS script + verbatim `12–24` char subtitle clause list.
2. **Single-Take Voiceover & Sample-Accurate Mapping**: Generate the unified WAV once, verify `voiced_dBFS` uniformity (`<= 3 dB` spread), extract exact clause/pause timestamps via `align_subs_on_raw_vowel_peaks`, and mix foley + stereo Lo-Fi BGM (`0.28 / 0.58`) via `mix_stereo_master`.
3. **Pre-Render QA Gate -> Full `60fps` Master Render & Backup**: Run `lint_and_render_3zoom_qa` and inspect all-act QA stills (`view_file` or multimodal read) to fix any tofu glyphs or layout overlaps first; then encode the full `1920x1080 @ 60fps` (`CRF 19`) MP4 + source `.zip` via `encode_turbo_film`, and save/upload a `<10MB` `720p @ 24fps` preview backup MP4 + `.zip`.
4. **MANDATORY Automatic Delivery Bundle (NEVER Wait to Be Asked!)**: Every time a full video is delivered, automatically generate and deliver ALL of the following together:
   - **Video & Files**: `1080p 60fps` master `.mp4`, storyboard overview sheet, source `.zip`, and backup links (via `google:show_file` / `drive:create_file` on Gemini Web Tasks, or clear local output paths on CLI).
   - **Paired Dual Covers (`双封面必出`, Mode 3.0)**: Generate the primary `3:4` vertical cover (`竖封面 3:4`) with generous whitespace above the mascot's ears/head, then pass it in `image_references` to generate the matched `4:3` horizontal cover (`横封面 4:3`) (plus optional `16:9` cover when Bilibili/YouTube is primary) and display them inline.
   - **Ready-to-Paste Titles, Descriptions & Hashtags (`标题 + 简介 + 话题必出`)**: Provide one-click copyable blocks for (a) 3 candidate hook titles, (b) primary platform short title (`<= 20` chars for Douyin) + compliant description + `#话题` tags, and (c) secondary long-video platform (e.g., Bilibili / YouTube) title + sample-accurate chapter-timestamped description + tags.
