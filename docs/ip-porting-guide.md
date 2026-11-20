# 自定义 IP、平台合规与多运行时移植指南

> 本文档说明如何基于 **Track A（[`skills/`](../skills/selfmedia-pipeline/SKILL.md) 通用可移植四件套）**，在 15 分钟内完成：
> 1. 替换成你自己的吉祥物 IP、主强调色、书法签名水印与口播音色；
> 2. 切换抖音 / B 站 / 小红书 / YouTube 平台合规与封面规格；
> 3. 将同一套 Skills 迁移到 **Gemini Web Tasks、Claude Code、Codex 或本地 `uv` 环境**。
>
> 若你打算直接使用默认工作流在 Gemini Web Tasks 中出片，请先查看 [Gemini Web Tasks 实操手册](./gemini-web-tasks-guide.md)。

---

## 1. 移植架构总览

通用四件套将“可变配置”清晰拆为 **3 层**，无需重写核心 PyCairo 渲染引擎即可完成整套品牌换肤：

| 定制层级 | 核心文件 | 负责内容 |
| :--- | :--- | :--- |
| **第 1 层 · IP 与平台档案** | [`templates/ip-profile.example.yaml`](../templates/ip-profile.example.yaml) | 单一事实源：角色设定、色板、水印文案、TTS 音色、目标平台预设、字幕高亮词表 |
| **第 2 层 · 静态画风与动画 `BrandConfig`** | [`skills/mascot-illustrations/references/ip-and-style-dna.md`](../skills/mascot-illustrations/references/ip-and-style-dna.md)<br>[`skills/handdrawn-motion/scripts/cairo_handdrawn.py`](../skills/handdrawn-motion/scripts/cairo_handdrawn.py)<br>[`skills/handdrawn-motion/scripts/chibi_watercolor_kit.py`](../skills/handdrawn-motion/scripts/chibi_watercolor_kit.py)<br>[`skills/handdrawn-motion/scripts/motion_rig_kit.py`](../skills/handdrawn-motion/scripts/motion_rig_kit.py) | 插画提示词视觉锁定、动画 `BrandConfig` 参数与 `draw_brand_signature` 签名、2.5 头身水彩角色绘制、C/S 脊柱骨骼与跨平台字体发现 |
| **第 3 层 · 平台合规与运行时适配** | [`skills/script-storyboard/SKILL.md`](../skills/script-storyboard/SKILL.md)<br>[`skills/selfmedia-pipeline/SKILL.md`](../skills/selfmedia-pipeline/SKILL.md) | 多模态敏感词替换规则、封面宽高比组合，以及不同 Agent 平台的 TTS / 生图 / 存储工具映射 |

---

## 2. 第一步：配置你的 IP 档案（`templates/ip-profile.example.yaml`）

复制 [`templates/ip-profile.example.yaml`](../templates/ip-profile.example.yaml) 为你的项目档案（如 `ip-profile.yaml`），模板已按 8 个顶层区块组织（支持零外部依赖直接被 `BrandConfig.from_file()` 读取）：

- **`brand`（品牌与水印）**：填写 `name`（书法签名与署名）、`watermark_text`（右下角 `15%` 呼吸透明度水印）与 `tagline`。
- **`mascot`（角色物种与剪影锁定）**：配置 `name`、`species`、`personality`、`primary_hex`、`eye_hex`、`inner_ear_hex` 与 `visual_lock_prompt`。确定 3–5 个**永不改变的视觉锚点**（例如纯色躯干 + 特征耳型 + 标志性眼神），锚点越少越锐利，生图与代码绘制的一致性越高；并在 `forbidden_props` 中列出破坏二头身比例的禁用道具。
- **`palette`（“单色单义”色板）**：
  - `ink_hex`：暖墨黑（`#151618`）配 `2B` 铅笔灰（`#5D6066`）。
  - `accent_hex`（默认 `#2EE59D`）：唯一英雄强调色，**只用于阈值突破、核心高亮、激活状态或角色瞳孔**，常见高辨识度备选如琥珀橙 `#F59E0B`、钴蓝 `#3B82F6`、珊瑚红 `#F43F5E`。
  - `paper_hex`：水彩视频模式与 Mode 3.0 封面固定使用暖冷压棉纸 `#FAF8F3`，Mode 1.0 文章插画使用纯白 `#FFFFFF`。
- **`voiceover` / `platform` / `subtitles` / `audio` / `fonts`**：分别控制单次 `<short pause>` 配音（`provider` / `language_code` / `voice_name`）、平台预设与双封面模式（`preset` / `cover_ratios` / `cover_mode` / `custom_scrub_rules`）、字幕安全带（`baseline_y: 956` / `font_size_px: 40` / `highlight_keywords`）、BGM 闪避增益（`0.28 / 0.58`）与自定义字体路径。

---

## 3. 第二步：同步静态插画与双封面规则（`skills/mascot-illustrations/`）

1. **更新视觉锁定文档**：编辑 [`skills/mascot-illustrations/references/ip-and-style-dna.md`](../skills/mascot-illustrations/references/ip-and-style-dna.md)，将模板中的 `{{IP_PROFILE}}` 与 `{{ACCENT_HEX}}` 占位符替换为你自己的角色描述，并按你的垂直赛道扩充“低科技手绘道具词典”（如硬件开发可加入示波器/面包板，金融科普可加入天平/账本，设计科普可加入色卡/裁纸刀）。
2. **核对 3 种画布模式**：编辑 [`skills/mascot-illustrations/references/prompt-templates-and-qa.md`](../skills/mascot-illustrations/references/prompt-templates-and-qa.md)，确认三种模式的槽位已对齐你的 IP：
   - **Mode 1.0（纯白概念插画，`16:9`）**：纯 `#FFFFFF` 留白 `>= 45%`，无左上角标题，3–4 个手写短标注（`2–5` 字）。
   - **Mode 2.0（暖水彩 / 实物混搭场景，`16:9`）**：暖水彩背景或桌面实物摄影 + 扁平 2D 手绘角色交互。
   - **Mode 3.0（二头身水彩双封面，`3:4` + `4:3`）**：先出 `3:4` 竖版封面检查耳尖/头顶留白，再传入 `image_references` 生成配对 `4:3` 横版封面。

---

## 4. 第三步：定制动画引擎 `BrandConfig`、签名与字体

### 4.1 注入 `BrandConfig`

Track A 的 [`skills/handdrawn-motion/scripts/cairo_handdrawn.py`](../skills/handdrawn-motion/scripts/cairo_handdrawn.py) 提供轻量级 `BrandConfig` 数据类，支持 **`BrandConfig.from_file()`（无需安装 PyYAML 也可解析 YAML/JSON）**、`BrandConfig.from_dict()` 与 `BrandConfig.from_env()` 三种加载方式，通过 `set_brand_config(cfg)` 即可全局生效于全部 3 个渲染脚本：

```python
from cairo_handdrawn import BrandConfig, set_brand_config

# 方式 A：直接从你的 IP 档案加载
cfg = BrandConfig.from_file("templates/ip-profile.example.yaml")
set_brand_config(cfg)

# 方式 B：在代码中直接覆盖关键品牌参数
cfg = BrandConfig(
    brand_name="InkCraft",
    watermark_text="InkCraft",
    accent_hex="#F59E0B",
    mascot_primary_hex="#0D0D0D",
    mascot_eye_hex="#F59E0B",
    subtitle_keywords=["工作流", "临界点", "自动化", "护栏"],
)
set_brand_config(cfg)
```

核心字段一览：

| 字段名 | 说明 | 示例值 |
| :--- | :--- | :--- |
| `brand_name` | 品牌 / 创作者名称，用于书法签名与元数据 | `"InkCraft"` |
| `watermark_text` | 右下角常驻水印文本 | `"InkCraft"` |
| `accent_hex` | 核心强调色（仅用于突破阈值、眼睛与荧光笔高亮） | `"#2EE59D"`（可改为 `"#F59E0B"` 等） |
| `mascot_primary_hex` | 吉祥物主体墨色 / 毛色 | `"#0D0D0D"` |
| `mascot_eye_hex` | 吉祥物标志性瞳孔 / 眼部高亮色 | `"#2EE59D"` |
| `subtitle_keywords` | 字幕自动触发强调色高亮的关键词列表（`list[str]`） | `["工作流", "临界点", "自动化", "护栏"]` |

注入 `BrandConfig` 后，引擎会自动：
- 统一替换湿边水彩高亮、荧光笔底纹、图标激活色与字幕关键词高亮色；
- 用动态生成的书法签名 **`draw_brand_signature(ctx, ..., brand_name=..., accent_rgb=...)`** 替代硬编码签名笔划，无需手算贝塞尔路径坐标。

### 4.2 替换角色绘制函数时的 4 条防劣化底线

如果你要修改 [`skills/handdrawn-motion/scripts/chibi_watercolor_kit.py`](../skills/handdrawn-motion/scripts/chibi_watercolor_kit.py) 中的 `draw_chibi_mascot`（或 [`motion_rig_kit.py`](../skills/handdrawn-motion/scripts/motion_rig_kit.py) 中的 `draw_mascot_actor`），将其从默认墨水吉祥物改成你自己的物种（如小狐狸、小猫头鹰、极简机器人），请保留以下四层去 AI 味规范：

1. **闭合剪影原则（One shape, one outline）**：头、躯干、四肢用平滑闭合轮廓绘制，禁止用零散直角矩形和生硬线条拼装。
2. **禁止破坏二头身比例的道具**：不要把 2.5 头身短手短脚角色强行塞进需要长腿的机械道具（如双轮脚踏车），改用操作台、拉杆、烧水壶、飞轮、滑板或浮空卡片等自然交互道具。
3. **叠加四道自然介质**：保留 `make_paper_stage`（`#FAF8F3` 冷压纸）、`pencil_underdraw`（2B 铅笔底稿）、`wet_watercolor_wash`（偏移湿边水彩）与 `brush_stroke`（压感蘸水笔 + 独立 `12fps` `boil_offset_xy` 抖动）。
4. **保留相位错峰与字幕安全区**：动作遵循 `眼 -> 头(+3f) -> 躯干(+6f) -> 肢体(+8f) -> 耳尾(+12f)` 错峰，且所有道具和地面严格停留在 `y <= 850`，绝不侵入 `y = 956` 的 `40px` 字幕安全带。

### 4.3 跨操作系统 CJK 字体配置

渲染脚本默认优先检查 Debian/Ubuntu Noto CJK 路径（与 Gemini Linux 沙盒一致），并依次回退到系统常见字体。在 macOS / Windows / NixOS 本地运行时，推荐通过环境变量显式锁定字体文件，彻底避免 `☐` 缺字方块：

```bash
# Linux (Noto CJK)
export HANDDRAWN_FONT_REGULAR="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
export HANDDRAWN_FONT_BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
export HANDDRAWN_FONT_SERIF="/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"

# macOS（示例：思源黑体 / PingFang）
export HANDDRAWN_FONT_REGULAR="/System/Library/Fonts/PingFang.ttc"
export HANDDRAWN_FONT_BOLD="/System/Library/Fonts/STHeiti Medium.ttc"
```

---

## 5. 第四步：切换发布平台合规与封面预设

根据你的主发平台，调整 `templates/ip-profile.example.yaml` 及 [`skills/script-storyboard/SKILL.md`](../skills/script-storyboard/SKILL.md) 中的合规与交付策略：

| 目标平台 | 推荐封面规格与生成顺序 | 合规审查重点 | 文案包与发布策略 |
| :--- | :--- | :--- | :--- |
| **抖音（Douyin）** | 强制配对 **`3:4` 竖版 -> `4:3` 横版**（先校验 `3:4` 顶部耳尖留白再锁图生成 `4:3`） | **严格多模态（ASR + OCR + 简介）防雷**：禁涉赌/漏洞破解/白嫖躺赚、禁防风控/群控/指纹浏览器、禁竞品自动化导流词、禁真实境外公网 IP（示例 IP 一律用 RFC 5737 `203.0.113.x`） | 短标题 `<= 20` 字 + 合规简介 + `#话题`；直连网络上传并勾选“内容由 AI 生成” |
| **B 站（Bilibili）** | 主推 **`16:9` 横版**（或沿用 `4:3` 横版），标题大字居中偏上、强化概念道具对比 | 保持技术表述客观克制，规避违规灰产与夸大收益承诺，可正常保留技术名词与开源生态讨论 | 深度信息量标题 + **精确到秒的章节时间戳简介** + 技术/知识分区标签 |
| **小红书（Xiaohongshu）** | 优先 **`3:4` 竖版主封面**，可复用 `Mode 1.0` / `Mode 3.0` 批量生成配套信息图滑动卡片 | 规避“私信领资料 / 站外导流 / 绝对化用语（第一、100% 有效）”等社区限流词 | 痛点钩子短标题 + 精炼分段笔记 + 场景化标签 |
| **YouTube / Shorts** | 长视频用 **`16:9` 高对比缩略图**（最多 3–4 个粗体英文关键词）；Shorts 裁切 `9:16` 安全中区 | 遵循版权与社区准则；若做英文/双语频道，切换 TTS `language_code`（如 `en-US`）并调小拉丁字幕字号/行宽 | `00:00` 起始的英文/双语章节标记 + 置顶评论要点总结 |

---

## 6. 第五步：迁移到多 Agent 运行时与本地 `uv`

本仓库的 Skill 遵循通用 `SKILL.md` + `references/` + `scripts/` 规范，可在以下 4 种环境中运行：

### 6.1 运行时工具映射对照表

| 能力环节 | Gemini Web Tasks（默认） | Claude Code | Codex | 本地 `uv` 命令行工作流 |
| :--- | :--- | :--- | :--- | :--- |
| **Skill 加载方式** | Skills UI 上传 4 个平铺 `.zip`（`lookup_skills`） | 复制 `skills/*` 到 `.claude/skills/` | 复制 `skills/*` 到 `~/.codex/skills/` 或项目 `skills/` | 直接读取 `skills/` 文档与 Python 模块 |
| **一镜到底 TTS** | `text_to_speech:generate_speech` | 接入 MCP TTS 或本地 CLI（Gemini TTS API / Edge-TTS / CosyVoice / OpenAI TTS）生成单条 WAV | 同左（输出标准单声道/立体声 WAV） | 任意 TTS 脚本导出 `vo_raw.wav` 传入 `align_subs_on_raw_vowel_peaks` |
| **插画与双封面** | `image_gen:generate_image`（原生支持 `image_references`） | 接入生图 MCP 或 API 脚本（Gemini Image / Imagen / GPT-Image / Flux 参考图编辑） | 同左 | 调用对应生图 API，先生成 `3:4` 再带参考图生成 `4:3` |
| **3-Zoom 审片** | `view_file` | 内置 `Read` 工具直接读取 QA PNG 图像 | 图像读取工具或终端提示人工打开 PNG | 直接在本地看图器检查 `qa_look_*.png`、`qa_motion_strip.png`、`qa_crops_1to1.png` |
| **云端归档备份** | `drive:create_file` / `google:show_file` | 本地 `dist/` 或 `rclone copy` 同步到云盘/对象存储 | 同左 | `rclone` / S3 / 本地目录归档 |

### 6.2 本地 `uv` 环境快速初始化

在本地开发、调试动画脚本或验证自定义 `BrandConfig` 时，推荐全程使用 `uv`：

```bash
# 1. 确保系统已安装 ffmpeg、cairo 与 Noto CJK 字体（详见 README 系统依赖章节）
ffmpeg -version

# 2. 同步虚拟环境与核心渲染依赖（可选 --extra fonts 开启 fontTools 缺字检查）
uv sync --extra fonts

# 3. 验证 Python 渲染套件可正常导入与解析同级模块
uv run python -c "
import sys, pathlib
sys.path.insert(0, str(pathlib.Path('skills/handdrawn-motion/scripts').resolve()))
import cairo_handdrawn, motion_rig_kit, chibi_watercolor_kit
print('All 3 motion engine modules imported cleanly!')
"

# 4. 修改完自定义 IP 后，一键重新打包上传用 ZIP
uv run scripts/package_zips.py --track generic --out dist
```

> **提示**：如果你同时维护多个垂直频道（例如科技频道 + 读书频道），只需保留一套通用 `skills/` 底座，为每个频道维护一份独立的 `ip-profile.yaml` 与轻量 `BrandConfig` 覆盖，即可在几分钟内切换完整画风与口播人设。
