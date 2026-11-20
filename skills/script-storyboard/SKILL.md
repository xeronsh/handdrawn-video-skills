---
name: script-storyboard
description: Interactive interview-driven video scriptwriting and 16:9 hand-drawn storyboard workflow for creator mascot IPs across Douyin, Xiaohongshu, Bilibili, and YouTube, with metaphor-first 1:1 audio-visual alignment, single unified scale auditing, configurable platform compliance desensitization, and fast-paced multi-beat visual choreography. Use whenever the user wants to discuss a new video topic, brainstorm video angles, audit or polish a video script, asks to be interviewed ("grill me") to extract their own words, or requests a hand-drawn Chibi watercolor storyboard.
---
# Script & Storyboard

Co-create authentic, logically airtight, platform-compliant video scripts and fast-paced `16:9` hand-drawn watercolor storyboards through structured interviewing and metaphor-first causal auditing.

> **IP & Platform Slot**: Read `ip-profile.yaml` (see `templates/ip-profile.example.yaml`) if present to fill `{{MASCOT_NAME}}`, `{{ACCENT_HEX}}` (default `#2EE59D`), `{{BRAND_NAME}}`, and `platform.preset` (`douyin` | `xiaohongshu` | `bilibili` | `youtube`).

## Core Principles

1. **Preserve Authentic Creator Voice (Never Cliché Ghostwriting)**: Extract or audit the creator's own thoughts without erasing their candid phrasing, rhythm, or closing catchphrases (avoiding `——` dashes and preachy filler).
2. **Metaphor-First 1:1 Audio-Visual Parity & Single Scale (`声画同构 + 单一物理刻度`)**: Ensure spoken copy explicitly introduces the concrete visual metaphor shown on screen (e.g., boiling a glass kettle `20°C -> 100°C`, clearing a game boss pit, folding a weak starting hand), and eliminate conflicting dual scales (never mix invented `70%/80%` percentages alongside a `100°C` boiling scale).
3. **Fast-Paced Multi-Beat Sub-Scene Rhythm (`每幕 2–4 拍景别递进 + 气口横移转场`)**: Break every act into crisp `[拍1]..[拍4]` causal beats (`Setup -> Side-by-Side Proof -> X-Ray/Review Ledger -> Threshold Breakthrough`) using pure 2.5-head Chibi mascot poses (avoiding props like two-wheeled crank bicycles that stretch chibi legs unnaturally).
4. **Hand-Drawn Draftsman Callouts & Easter Eggs (NEVER Heavy PPT Term Cards)**: Pair visual cause-and-effect with light curved-arrow hand-drawn margin notes (`手绘引线批注`, `2–6` chars) and corner Easter eggs (yellow Debug Rubber Duck, peeking mini mascot, achievement toasts).
5. **Configurable Platform Compliance Pre-Desensitization (`创作阶段前置排雷`)**: Scrub high-risk phrasing **before** TTS synthesis according to the active target platform:
   - **Douyin (`douyin`, default)**: Rephrase gambling terms (`别赌博梭哈` -> `千万别上头梭哈`), public proxy/IP digits (`203.0.113.x`), anti-fraud bypass terms (`防风控`, `群控`, `养号`), competitor platform names in automation contexts (`小红书/闲鱼/微信`), and exploit/grey-market words (`爆漏洞`, `破解`, `白嫖`, `躺赚`).
   - **Xiaohongshu (`xiaohongshu`)**: Scrub off-platform traffic funnels (`加微`, `私信领`), absolute ad-law superlatives (`全网第一`, `绝对`), and grey-market triggers.
   - **Bilibili (`bilibili`)**: Preserve authentic technical precision while scrubbing grey-market bypass instructions and planning clean chapter timestamps.
   - **YouTube (`youtube`)**: Ensure advertiser-friendly terminology, copyright-safe audio cues, and crisp `00:00` chapter anchors.
6. **100% Verbatim Parity**: Every word in Section II act dialogue must match Section I teleprompter copy word-for-word, and clauses should sit comfortably in `12–24` characters for single-line `40px` subtitles.

## Steps

1. **Load Profile & Propose 3–4 Focused Metaphor Angles (or Audit Existing Draft)**: Check for scale clashes, delayed metaphors, detour sentences, and platform ASR/OCR risk words.
2. **Run a Concise Interview When Starting Fresh**: Ask 2 to 3 focused questions per round to capture real stories, concrete numbers, and sharp boundaries in the creator's own voice.
3. **Choreograph Multi-Beat Watercolor Storyboard**: Design 2 to 4 `[拍]` beats per act with `{{MASCOT_NAME}}` acting poses, `{{ACCENT_HEX}}` threshold payoff cues, draftsman callouts, corner Easter eggs, and `{{BRAND_NAME}}` signatures.
4. **Output the Standard Two-Part Deliverable**:
   - `## 一、提词器纯净连读版（完整口播逐字稿）` (marked cleanly for `<short pause>` breath valleys)
   - `## 二、完整视听分镜大纲（逐字稿 × 16:9 二头身水彩手绘画面、批注与彩蛋）`
