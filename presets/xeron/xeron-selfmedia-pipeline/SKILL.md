---
name: xeron-selfmedia-pipeline
description: 'End-to-end production pipeline for Xeron #2EE59D black cat IP self-media videos on Douyin and Bilibili, powered by the Four-Layer Anti-AI Craft Architecture (pure 2.5-head Chibi silhouette assets & cold-press watercolor media, single-read viewer timing budget, continuous-world camera without PPT slide cross-fades, and pre-render QA gates), single-take <short pause> prosody Puck voiceover, vowel-nucleus synced 40px subtitles, stereo Lo-Fi guitar BGM, Douyin ASR/OCR/caption compliance shield, mandatory paired 4:3 + 3:4 dual covers, ready-to-paste titles/descriptions/hashtags, and Google Drive backup.'
allowed-tools: text_to_speech image_gen drive google default_api
---
# Xeron Selfmedia Pipeline (v3.1 — Chibi Watercolor Craft, Single-Take Prosody, Dual 4:3+3:4 Covers & Full Copy Bundle)

Turn a topic, draft, or script into a publish-ready, Douyin-compliant `16:9` `60fps` (`CRF 19`) Xeron black cat hand-drawn animated video — ALWAYS bundled automatically upon video completion with **paired `4:3` horizontal + `3:4` vertical covers**, **ready-to-paste titles, descriptions, and hashtags (`标题 + 简介 + 话题`)**, and **Google Drive cloud backup**.

## Core Creative, Audio & Compliance Contract

### 1. Four-Layer Anti-AI & Anti-Homogenization Craft Architecture (`四层去 AI 味与反模板底座`)

Delegate motion rendering to `xeron-cat-motion` (`v14_chibi_watercolor_kit.py` + `cairo_handdrawn.py` v5.0), strictly enforcing all four layers:
- **Layer 1 — Pure 2.5-Head Chibi Silhouette & Natural Watercolor Media (`纯正二头身造型与水彩笔刷介质`)**:
  - **Pure 2.5-Head Flat-Shaded Bold-Ink Chibi Xeron**: Keep Xeron in pure 2.5-head chibi proportions (`大圆头 + 小短身 + 小短爪`, `#0D0D0D` solid black fur, `#6E6378` muted grey-purple inner ears, flat-topped half-lidded `#2EE59D` mint-green aloof geek eyes). Never put chibi Xeron on props like two-wheeled crank bicycles that force uncanny stretched human legs.
  - **Metaphor-First 1:1 Alignment & Single Unified Scale**: Align spoken copy and visuals to the exact same concrete physical metaphor (e.g., boiling glass kettle `20°C -> 88°C -> 99°C -> 100°C`), and never mix conflicting dual scales (such as `70%/80%` percentages alongside `100°C` physical temperature).
  - **Tactile Paper & Pen Media**: Layer warm cold-press cotton paper grain (`#FAF8F3`), pre-densified wet-edge watercolor washes (`max_px <= 10.5px`), organic dip-pen contours (`12fps` `boilSeed` over `60fps` primary motion), hand-drawn `draw_draftsman_callout` leader arrows, and geek Easter eggs (yellow Debug Rubber Duck, peeking mini cat, achievement toasts). Avoid missing `NotoSansCJK` symbols (`↻`, `✗`, `♠`, `♦` — draw vector icons/strike-throughs instead).
- **Layer 2 — Viewer Single-Read Timing Budget & Phase Stagger (`观众单拍读点时间预算`)**:
  - **One Read at a Time**: Sequence every beat via `Lead Eye (0.30–0.40s) -> Reverse Anticipation (0.15–0.20s) -> Fast Snap (0.22–0.28s) -> Payoff Hold (0.85–1.20s)`.
  - **Anti-Twinning**: Stagger motion phases (`eyes -> head +3f -> torso +6f -> limbs -> ears/tail`) via critically damped curves, reserving `#2EE59D` for threshold/payoff states.
- **Layer 3 — Continuous World & Breath-Valley Camera (`一镜连续世界摄影机`)**:
  - **No PPT Slide Cross-Dissolves**: Never glue isolated slide functions with opacity fades. Drive continuous horizontal/camera pans cleanly across `<short pause>` breath valleys.
- **Layer 4 — Multi-Act Pre-Render QA Gate (`全幕切片审片门禁`)**:
  - Export and inspect full-act QA contact sheets / Look Frames via `view_file` **before** full video encoding, verifying zero `☐` missing-glyph boxes, zero ear/prop text collisions, and zero intrusion into the `y >= 938` subtitle safe band.

### 2. Single-Take `<short pause>` Prosody Voiceover + 3-Tier Audio-Visual Sync (`100% 音色语速统一`)

- **Never** generate multi-act TTS clips or apply `pydub` breath-chopping / `ffmpeg atempo`.
- Author **one unified prosody script** (`<= 5 min`, `language_code="cmn-CN"`, `voice="Puck"`) with explicit `<short pause>` tags at thought/act breaks and spaced letter acronyms (`S O P`).
- Align `40px` subtitles directly onto the **unedited studio WAV** (`280–3200 Hz` vowel-nucleus peaks + `-38.0 dB` pause valleys), mix tactile foley cues at narrative climaxes, and add stereo Karplus-Strong guitar Lo-Fi BGM (`0.28` speech / `0.58` pause).

### 3. Douyin Multi-Modal Pre-Audit Shield (`抖音语音 ASR + 画面 OCR + 简介防雷红线`)

Scrub all machine-audit trigger classes across spoken TTS script, subtitles, on-screen tokens/icons, and post captions **before** generating audio or frames:
- **No Gambling, Exploit, Grey-Market, or Money-Inducement Keywords**: Scrub `赌博` (`别赌博梭哈` -> `千万别上头梭哈`), `硬核漏洞`, `爆漏洞`, `破解`, `白嫖`, `躺赚` -> use `硬核排障经验`, `算力特惠`, `一步登天`.
- **No Anti-Bot / Multi-Account Bypass Terms**: Scrub `防风控`, `触发风控`, `绕过风控`, `群控`, `养号`, `指纹浏览器/沙盒管号`, `自动续期 Cookie` -> use `本地隔离浏览器环境`, `保持常用服务稳定在线`, `告别重复扫码`.
- **No Competitor Platform Names/Logos in Automation/Traffic Contexts**: Scrub `小红书`, `闲鱼`, `微信`, `快手`, `B站` as automated targets or funnels -> use `闲置好物平台`, `日常内容账号`, `常用生活网页`.
- **No Cross-Border Proxy / Blocked Social Media / Unregistered App Calls**: Scrub overseas public IPs (`203.0.113.x`), `动态/固定 IP`, `登录 Google`, `Instagram/Facebook/Threads/X/Telegram` -> use `云端临时连接易重置`, `联动内容创作工作流`.
- **Mandatory Publish Reminders**: Remind the user to upload over a direct domestic network connection (no proxy) and check `自主声明 -> 内容由 AI 生成`.

## Execution Workflow & Mandatory Post-Video Delivery Bundle

1. **Compliance Scrub & Prosody `<short pause>` Script**: Load `xeron-cat-motion` and `xeron-cat-illustrations` via `lookup_skills`. Scrub sensitive terms, align metaphors between spoken copy and visuals, and author the single-take `<short pause>` TTS script + verbatim `12–24` char subtitle clause list.
2. **Single-Take Voiceover & Sample-Accurate Mapping**: Generate the unified `Puck` WAV once, verify `voiced_dBFS` uniformity (`<= 3 dB` spread), extract exact clause/pause timestamps, and mix foley + stereo Lo-Fi BGM.
3. **Pre-Render QA Gate -> Full `60fps` Master Render & Drive Backup**: Inspect all-act QA stills via `view_file` to fix any tofu glyphs or layout overlaps first, encode the full `1920x1080 @ 60fps` (`CRF 19`) MP4 + source `.zip`, and upload a `<10MB` `720p @ 24fps` backup MP4 + `.zip` to Google Drive.
4. **MANDATORY Automatic Delivery Bundle (NEVER Wait to Be Asked!)**: Every time a full video is delivered, you MUST automatically generate and deliver ALL of the following together:
   - **Video & Files**: `1080p 60fps` master `.mp4`, storyboard overview sheet, source `.zip`, and Google Drive backup links via `google:show_file` / `drive:create_file`.
   - **Paired `4:3` Horizontal + `3:4` Vertical Covers (`双封面必出`)**: Generate the `3:4` vertical cover (`竖封面 3:4`) via `image_gen:generate_image` (with generous whitespace above Xeron's ear tips), then pass it in `image_references` to generate the matched `4:3` horizontal cover (`横封面 4:3`) and embed both inline in chat.
   - **Ready-to-Paste Titles, Descriptions & Hashtags (`标题 + 简介 + 话题必出`)**: Include one-click copyable blocks for (a) 3 candidate titles, (b) Douyin short title (`<= 20` chars) + compliant description + `#话题` tags, and (c) Bilibili title + sample-accurate chapter-timestamped description + tags.
