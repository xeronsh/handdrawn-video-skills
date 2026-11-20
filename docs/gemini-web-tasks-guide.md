# Gemini Web Tasks 完整实操与排障手册

> 本文档面向在 **Gemini Web Tasks** 中运行 `handdrawn-video-skills` 四件套的创作者，覆盖从**平铺 ZIP 打包、Skills UI 导入、工具能力映射、对谈采写、3-Zoom 审片门禁、双封面生成顺序**到**常见故障排查**的全流程操作。
>
> 若需将角色 IP、视觉配色或运行环境迁移到自有品牌 / Claude Code / Codex / 本地 `uv`，请参阅 [自定义 IP 与多运行时移植指南](./ip-porting-guide.md)。

---

## 1. 前置准备：打包平铺根目录 Skill ZIP

Gemini Web Tasks 的 Skills 导入器要求每个 `.zip` 包的**压缩根目录直接存放 `SKILL.md`**（以及同级的 `references/`、`scripts/` 子目录），不能多套一层外层目录。

仓库内置了零外部依赖的打包脚本 [`scripts/package_zips.py`](../scripts/package_zips.py)，直接运行即可自动校验并生成标准压缩包：

```bash
# 打包 Track A：通用可移植四件套（推荐）
uv run scripts/package_zips.py --track generic --out dist

# 打包 Track B：原版黑猫四件套预设
uv run scripts/package_zips.py --track xeron --out dist

# 一次性打包全部轨道
uv run scripts/package_zips.py --track all --out dist
```

### 打包产物与用途对照

| 轨道 | 独立上传 `.zip`（逐个导入 Gemini Web Tasks Skills UI） | 归档合集 `.zip`（仅用于备份或本地解压） |
| :--- | :--- | :--- |
| **Track A（通用版）** | `dist/generic/selfmedia-pipeline.zip`<br>`dist/generic/script-storyboard.zip`<br>`dist/generic/mascot-illustrations.zip`<br>`dist/generic/handdrawn-motion.zip` | `dist/generic/handdrawn-video-skills-generic-suite.zip` |
| **Track B（原版预设）** | `dist/xeron/xeron-selfmedia-pipeline.zip`<br>`dist/xeron/xeron-script-storyboard.zip`<br>`dist/xeron/xeron-cat-illustrations.zip`<br>`dist/xeron/xeron-cat-motion.zip` | `dist/xeron/xeron-skills-suite.zip` |

> **注意**：请上传 **4 个独立 `.zip`**，不要直接把 `*-suite.zip` 合集包上传到 Skills UI。

---

## 2. 在 Gemini Web Tasks Skills UI 中导入与更新

1. 打开 Gemini Web Tasks，进入 **Skills 管理面板**。
2. 点击上传，**依次导入同一轨道下的全部 4 个独立 `.zip`**：
   - 总控编排：`selfmedia-pipeline.zip`（或 `xeron-selfmedia-pipeline.zip`）
   - 脚本分镜：`script-storyboard.zip`（或 `xeron-script-storyboard.zip`）
   - 插画双封面：`mascot-illustrations.zip`（或 `xeron-cat-illustrations.zip`）
   - 手绘动画引擎：`handdrawn-motion.zip`（或 `xeron-cat-motion.zip`）
3. **为什么必须 4 个一起上传？**
   总控 Skill（`selfmedia-pipeline`）会在执行过程中通过 `lookup_skills` 和 `get_skill_resources` 自动加载 `handdrawn-motion`（3 个 PyCairo 渲染脚本 + 导演规范）和 `mascot-illustrations`（视觉 DNA + 双封面提示词模板）。缺少任意一个都会导致风格退化或无法出封面。
4. **后续增量更新**：修改某个 Skill 文件后，重新执行 `uv run scripts/package_zips.py`，只需在 Skills UI 中重新上传发生变动的那个 `.zip` 即可。

---

## 3. Gemini Web Tasks 工具能力映射

总控 Skill 在 YAML frontmatter 中声明了 `allowed-tools: text_to_speech image_gen drive google default_api`。各阶段调用的原生能力如下：

| 生产阶段 | Gemini Web Tasks 原生能力 | 关键参数与硬性约束 |
| :--- | :--- | :--- |
| **技能发现与资源读取** | `lookup_skills`、`get_skill_resources` | 动态读取 `references/*.md` 与 `scripts/*.py` |
| **一镜到底口播配音** | `text_to_speech:generate_speech` | 单次合成全片（`<= 5 min`），默认 `language_code="cmn-CN"`、`voice="Puck"`；用 `<short pause>` 控制气口停顿，英文缩写拆字母拼写（如 `S O P`） |
| **音频与动画渲染** | 内置 Linux Python 沙盒 | 运行 `cairo_handdrawn.py`、`chibi_watercolor_kit.py`、`motion_rig_kit.py`（或 Track B 对应脚本）及 `ffmpeg` 多进程编码 |
| **3-Zoom 视觉审片** | `view_file` | 编码前查看接触表、Look Frames 与 `1:1` 裁切 PNG，人工+模型双重把关 |
| **插画与配对双封面** | `image_gen:generate_image` | 支持 `aspect_ratio`（`3:4` / `4:3` / `16:9`）与 `image_references` 角色一致性锁图 |
| **交付展示与云端备份** | `google:show_file`、`drive:create_file` | 内嵌展示成片与双封面，并将 `<10MB` `720p @ 24fps` 备份视频与源码 `.zip` 存入 Google Drive |

> **音频铁律**：严禁分幕多次调用 TTS 再拼接，也严禁使用 `pydub` 切气口或 `ffmpeg atempo` 变速。单次 `<short pause>` 配音 + `align_subs_on_raw_vowel_peaks` 原生对齐是保证全片音色、语速和重音咬合 100% 统一的前提。

---

## 4. 标准端到端实操流程

### 阶段一：对谈采写与合规分镜（`script-storyboard`）

如果你只有一个想法或粗纲，先不要直接让模型渲染视频，先触发 `script-storyboard`：

1. **选题定调**：Agent 会给出 3–4 个具象物理比喻切入角度（例如烧水壶 `20°C -> 100°C`、折手牌、过筛子、拉手刹），选定最贴合你真实经历的一个。
2. **2 轮轻量对谈（“grill me”）**：每轮 2–3 个聚焦问题，榨出你的真实案例、边界条件与自然口语，拒绝“AI 鸡汤味”和 `——` 书面破折号。
3. **声画同构与单一刻度体检**：确保口播里的比喻与画面道具 1:1 对应，且全片只用一套物理刻度（绝不把抽象 `%` 和 `°C` 混在一幕里）。
4. **平台多模态前置排雷**：在录音和画图前，预先清洗语音 ASR、画面 OCR 和文案中的风控敏感词（如赌博/漏洞/绕过风控/导流竞品/境外 IP 等）。
5. **验收标准**：确认最终输出的 `一、提词器纯净连读版` 与 `二、完整视听分镜大纲` 中的台词做到 **100% 逐字一致**。

### 阶段二：一镜到底配音与音频母带

脚本锁定后，交给 `selfmedia-pipeline` 执行音频阶段：

- **单次生成 WAV**：插入 `<short pause>` 段落/乐句停顿标记后一次生成，校验各段落 `voiced_dBFS` 波动 `<= 3 dB`。
- **三级声画时间戳提取**：调用 `align_subs_on_raw_vowel_peaks`，基于未剪辑 WAV 的 `280–3200 Hz` 元音音核峰值与 `-38.0 dB` 气口谷值，精确对齐每条 `12–24` 字的 `40px` 字幕及特效瞬态触发帧。
- **混音母带**：在关键转折帧混入轻量拟声音效，并铺入立体声 Karplus-Strong 吉他 Lo-Fi BGM（人声段 `0.28`，气口停顿段自动抬升至 `0.58`）。

### 阶段三：3-Zoom 审片门禁（全片 `60fps` 渲染前必看！）

**切勿跳过审片直接跑 2 分钟 `60fps` 全片编码。** 渲染脚本会先跑确定性 `f(t)` 采样与 `lint_and_render_3zoom_qa`，并通过 `view_file` 展示 3 层质检图：

1. **Gate 1 — 自动指标 Lint + 3 张 `1920x1080` Look Frames**：
   - 确认所有道具/舞台地板停留在 `y <= 850`（确保 `y = 956` 的 `40px` 字幕安全带背景墨水密度 `< 16%`）。
   - 检查是否出现 `☐` 缺字豆腐块（常见于不支持的特殊符号 `↻`、`✗`、`♠`、`♦`）。
   - 确认 `#FAF8F3` 冷压纸质感、湿边水彩晕染与角色 2.5 头身比例自然。
2. **Gate 2 — 全幕接触表 + `0.10s` `8–10` 帧运动条（默认 `strip_count=8`，`qa_motion_strip.png`）**：
   - 检查核心动作是否具备 `预备反拉 -> 快速爆发 -> 停顿回味` 节奏。
   - 检查 `+16.7ms` 相邻帧稳定性（`< 5.0%` 像素跳变），防止整屏闪烁。
3. **Gate 3 — `420x420` `1:1` 像素接触裁切（`qa_crops_1to1.png`）**：
   - 放大检查角色眼部眼神、爪子与道具的接触点、手绘引线箭头和耳尖是否发生穿帮或悬空。

发现任何微瑕，直接指出幕号和位置让 Agent 微调重出 QA 图；全部确认无误后再放行多进程分片编码（`encode_turbo_film`，`1920x1080 @ 60fps, CRF 19`）。

### 阶段四：双封面生成顺序（严格遵循 `3:4` -> `4:3`）

视频编码完成后，总控会自动调用 `mascot-illustrations` 生成成对双封面，**顺序不能颠倒**：

1. **先出 `3:4` 竖版封面（`aspect_ratio="3:4"`）**：
   - 上半区留足手写大字主标题（2 行、每行 `4–7` 字 + 主强调色荧光笔底纹）与紧凑副标题。
   - **耳尖留白检查（Ear-Clearance Check）**：确认顶部文字与角色耳尖之间有宽裕的纯净留白，绝不压头或切耳。若出现触碰，立即把该图传入 `image_references` 做 1 次外科手术式微调（主体缩至约 `90%` 并略微下移）。
2. **再出 `4:3` 横版封面（`aspect_ratio="4:3"`）**：
   - 将审核通过的 `3:4` 竖版封面 ID 传入 `image_references`，锁定同一角色五官、笔触、纸张底色与道具元素，重排为横向视觉重心。
   - 两张封面会自动内嵌在对话中供你核对和下载。

### 阶段五：自动交付包验收与发布前提醒

每次成片交付时，确认你已收到以下全部 4 类产出：

- [ ] `1920x1080 @ 60fps (CRF 19)` 母片 `.mp4` + 分镜总览图 + 完整工程源码 `.zip`
- [ ] `<10MB` `720p @ 24fps` 压缩预览版 `.mp4` 与源码包的 Google Drive 备份链接
- [ ] 成对 `3:4` 竖版 + `4:3` 横版高清封面（无错别字、无外边框、耳尖留白干净）
- [ ] 一键复制文案包：3 个候选标题、抖音短标题（`<= 20` 字）+ 合规简介 + `#话题`、B 站标题 + 精确到秒的章节时间戳简介与标签

> **抖音发布实操提醒**：上传前请确认使用**国内直连网络（关闭代理）**，并在发布页勾选 **`自主声明 -> 内容由 AI 生成`**。

---

## 5. 常见故障排查（Troubleshooting）

| 现象 / 报错 | 常见原因 | 解决方案 |
| :--- | :--- | :--- |
| 画面文字出现 `☐` 缺字豆腐块 | 文本中混入了 `NotoSansCJK` 未收录的特殊符号（如 `↻`、`✗`、`♠`、`♦`）或系统字体路径异常 | 用矢量手绘图形/笔刷划叉替代特殊字符；检查 `HANDDRAWN_FONT_REGULAR` / `BOLD` / `SERIF` 环境变量或开启 `fontTools` 字符集预检 |
| 字幕与口播明显错拍，或声音发紧发机械 | 分段生成了多个 TTS 音频后拼接，或误用了 `atempo` 变速 / 自动剪气口 | 强制回归单次 `<short pause>` 配音，并直接对原始未剪辑 WAV 调用 `align_subs_on_raw_vowel_peaks` |
| 封面出现陌生左上角小标题，或文字碰到角色耳尖 | 生图模型自动补了标题栏，或角色构图偏大 | 将原图放入 `image_references`，发出定向编辑指令：“仅移除左上角多余标题并用纯背景无缝补齐”或“将角色与道具整体缩至 90% 并下移，保持其余文字不变” |
| 沙盒报 `ModuleNotFoundError` 找不到引擎脚本 | 上传了嵌套子目录的 `.zip`（根目录不是 `SKILL.md`），或脚本硬编码了旧沙盒路径 | 使用 `uv run scripts/package_zips.py` 重新打包平铺根目录 `.zip`；确认脚本通过 `Path(__file__).resolve().parent` 解析同级模块 |
| `60fps` 全片渲染超时或成品文件过大难以预览 | 单进程顺序渲染，或直接传输高码率 1080p 母片 | 使用 `encode_turbo_film` 多进程分片渲染（依赖纯函数 `f(t)` 确定性）；先看自动生成的 `<10MB` `720p @ 24fps` 预览版再下载母片 |
| `selfmedia-pipeline` 执行时找不到配图或动画规范 | 只上传了总控 `.zip`，漏传了另外 3 个配套 Skill | 确认同一轨道下的全部 4 个独立 `.zip` 均已在 Skills UI 中启用，且未混搭 Track A 与 Track B 的不同命名 |
