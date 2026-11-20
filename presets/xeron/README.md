# Xeron 自媒体四件套原版预设（Track B — v14 二头身水彩 & 双封面自动交付版）

本目录完整保留 **Xeron `#2EE59D` 薄荷绿眼黑猫 IP** 原版四件套 Skills（100% 向后兼容，已完成隐私与个人硬编码脱敏，并补充跨平台路径与字体回退），可直接打包上传至 **Gemini Web Tasks** 使用，也支持在 **Claude Code / Codex / 本地 Agent CLI** 中复用。

## 包含的 4 个核心 Skill

1. **`xeron-cat-illustrations`**：纯白与冷压水彩手绘插画、抖音 `4:3` 横版 + `3:4` 竖版成对双封面模板、Xeron 黑猫 IP 视觉锁定卡与审片清单（含 `references/` 两份规范文档）。
2. **`xeron-script-storyboard`**：对谈式口播提炼、比喻前置声画同构体检、单一物理刻度校验、抖音风控前置脱敏与多拍分镜规范。
3. **`xeron-cat-motion`（v11.1）**：四层去 AI 味手绘动画架构，完整内含三套核心 Python 渲染引擎：
   - `scripts/v14_chibi_watercolor_kit.py`（纯正 2.5 头身极简平涂粗线条手绘小黑猫、冷压水彩纸纹理、预加密湿边水彩晕染、100°C 玻璃烧水壶、Skill 模块卡、筹码塔、复利飞轮、手绘引线批注与 Debug 鸭彩蛋库）
   - `scripts/cairo_handdrawn.py`（v5.0 蘸水笔压感、12fps 独立抖动、一镜连续摄像机与三倍率 QA 门禁）
   - `scripts/xeron_clean_rig.py`（v7/v8 立体声 Karplus-Strong 吉他 Lo-Fi BGM 合成器、元音音核零漂移字幕对齐、多进程极速 H.264 编码器与 AI 产品线框图组件）
4. **`xeron-selfmedia-pipeline`（v3.1）**：端到端自媒体出片总控流水线，内置一镜到底 `<short pause>` Puck 配音、抖音多模态防雷盾，以及**每次出完视频强制默认交付 `4:3 + 3:4` 双封面 + 标题/简介/话题包 + Google Drive 云端备份**标准。

## 一键打包 `.zip`（用于 Gemini Web Tasks 上传）

在仓库根目录执行：

```bash
uv run scripts/package_zips.py --track xeron
```

将在 `dist/xeron/` 下生成 4 个扁平根目录单包（`SKILL.md` 直接位于压缩包根目录）以及 1 个合集包：

- `dist/xeron/xeron-selfmedia-pipeline.zip`
- `dist/xeron/xeron-script-storyboard.zip`
- `dist/xeron/xeron-cat-illustrations.zip`
- `dist/xeron/xeron-cat-motion.zip`
- `dist/xeron/xeron-skills-suite.zip`（完整合集归档）

## 导入方式

- **Gemini Web Tasks（推荐）**：打开 Gemini Web Tasks 的 **Skills 管理界面**，将上述 4 个独立 `.zip` 文件逐个上传导入即可开箱触发。
- **跨平台复用（Claude Code / Codex / 本地 Agent CLI）**：直接将本目录下的 4 个子文件夹复制到 `.claude/skills/` 或本地 Agent 的 `skills/` 目录即可调用。
- **跨系统字体配置（本地渲染可选）**：脚本默认优先匹配 Gemini Linux 沙盒的 Debian Noto CJK 字体路径，并自动回退至常见 Linux / macOS / Windows 字体；也可通过环境变量 `HANDDRAWN_FONT_REGULAR`、`HANDDRAWN_FONT_BOLD`、`HANDDRAWN_FONT_SERIF` 手动指定字体路径。
