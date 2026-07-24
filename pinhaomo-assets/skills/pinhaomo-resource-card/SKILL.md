# 拼好模资源卡生成与发布

为「拼好模」QQ 频道生产并发布单张资源分享卡（海报图）。覆盖内容准备、视觉风格选择、Ardot 设计/导出、Pillow 代码生成兜底、PNG 校验、频道发布、异常帖删除的全流程。

## 适用场景

- 从开源项目/教程/提示词中提炼资源，做成一张学生向资源卡
- 需要发到 QQ 频道「资源精选」等子频道
- Ardot 适配器不稳定或导出失败时需要可靠 fallback

## 前置依赖

- 已安装 `tencent-channel-cli` 并完成个人号授权（`doctor` 全绿）
- 已知 guild-id `627624404088187935` 与目标 channel-id
- 视觉规范见项目根 `DESIGN.md`（v1.1+）
- Python 3.13+ 与隔离 venv（路径 `C:\Users\79204\.workbuddy\binaries\python\envs\default`）
- Pillow 已安装：`"$VENV/Scripts/python.exe" -m pip install Pillow pyyaml`

## 资源卡内容 8 字段（必须齐全）

1. 资源编号（如「资源 03」）
2. SkillSpector 风险 0–100（目前统一写 0/100，未接入自动评估）
3. 类型（如「设计系统规范 / 工具」）
4. 用途（一句话，学生向）
5. 核心机制（3–4 条，用 1. 2. 3.）
6. 怎么用（一句话场景）
7. 标签（2–4 个，# 前缀）
8. 来源（github 链接 + 星标数，禁用 ★，用「星标」文字）

## 风格选择（按内容重要度）

读取 `DESIGN.md` v1.1 的 `importanceMap`：

- 高 / 公告·置顶·重点 → **B_focus**（深蓝底 #16203A + 深卡 #0E1830 + 白字 + 品牌蓝 #2B5CFF + 暖橙 #FF8A3D 强调）
- 中 / 教学·陪练 → **A_companion**（浅蓝灰底 #EEF3FA + 白卡 + 品牌蓝 + 暖橙）
- 中低 / 技术资讯·数据 → **C_calm**（浅灰底 #F5F6F8 + 白卡 + 冷蓝 #1E6BFF）
- 低 / 快讯·Q&A → **D_quick**（近白底 #FAFBFC + 极少强调色）

## 路线一：Ardot 设计（首选）

1. 加载 `ardot-design-core` + `ardot-ui-design`（或 `ardot-poster`）。
2. 确保当前设计文件打开：`fetch_file_info`；若未打开则用 `open_design` 或 `create_design`。
3. 按选定风格的 token 搭建：frame → 卡片 → head/badge/risk → 标题 → 副标题 → 类型 → 用途 → 核心机制 → 怎么用 → 标签 → 来源。
4. 文字规范：
   - 全部字号 ≥28px
   - 禁用 emoji 与 U+2300–U+27BF 符号（★、①②③④ 等）；列表用「1. 2. 3.」，星标用文字「星标」
   - B 风格标题用 display 字体（ZCOOL QingKe HuangYou 黄油体）；正文/副标题用站酷快乐体（ZCOOL KuaiLe，圆润柔和，与「教学种子资源」统一调性）；强对比小标题（类型行/小节标签）用 Noto Sans SC 粗体——层级靠字族差异+字重差异表达（呼应 DESIGN.md v1.1）
5. 校验：`capture_layout` 零问题，`capture_screenshot` 可选（该接口可能超时，不阻塞）。
6. 导出：`export_nodes(fileId, nodeIds=[rootNode], outputDir="exports", format="png", scale=2)`。
7. 文件重命名：Ardot 默认导出名为 `<node-id>.png`，需改为中文名。

## 路线二：Pillow 代码生成（Ardot 导出失败时的兜底）

当 `export_nodes` 产出空白/纯色图、或 Ardot 适配器持续 NO_ADAPTER 时，切换到本脚本。

### 当前可用脚本

`scripts/generate_b_card.py`：生成 B_focus 风格的 design.md 资源卡。

### 扩展为通用卡片的步骤

1. 复制 `scripts/generate_b_card.py` 为 `scripts/generate_resource_card.py`。
2. 在脚本顶部定义 `theme`（A/B/C/D），读取 `DESIGN.md` 的 YAML token 自动填色/字号/圆角。
3. 字体 fallback 链：
   - 优先检查 Ardot 可用字体列表（`mcp__ardot__get_available_fonts`）
   - 若 Ardot 不可用，使用本机缓存的 Ardot 等价字体（实测可用）：
     - 黄油体（ZCOOL QingKe HuangYou，标题 display）：`C:/Users/79204/.kimi-work/bin/kimi-tools/fonts/19-ZCOOLQingKeHuangYou.ttf`
     - 站酷快乐体（ZCOOL KuaiLe，圆润柔和）：`C:/Users/79204/.kimi-work/bin/kimi-tools/fonts/26-ZCOOL-KuaiLe.ttf`
     - 思源黑体（Noto Sans SC，正文/标签）：`C:/Windows/Fonts/NotoSansSC-VF.ttf`（支持 100–900 字重）
   - 路径须用 `C:/` 前缀（Windows native Python），勿用 `/c/`
4. 渲染后必须校验：
   ```python
   px = list(img.getdata())
   non_bg = sum(1 for p in px if p[:3] != ImageColor.getrgb(theme.bg))
   assert non_bg / len(px) > 0.15, "图片内容可能为空"
   ```

## 发布到频道

```bash
tencent-channel-cli feed publish-feed \
  --guild-id 627624404088187935 \
  --channel-id <CHANNEL_ID> \
  --feed-type 1 \
  --image "C:/Users/79204/WorkBuddy/QQ频道/exports/<卡.png>" \
  --content "<简介 + hashtags>"
```

常用 channel-id：
- 公告：737383084
- 资源精选：737383095
- 提示词库：737383096
- 教程：737383097
- 技术资讯：737383099
- Q&A：737383110

## 处理异常帖（如黑屏、发错）

1. 找到 feed_id 与 create_time_raw：
   ```bash
   tencent-channel-cli feed get-channel-timeline-feeds --guild-id 627624404088187935 --channel-id <CHANNEL_ID> --count 10 -j
   ```
2. 删除：
   ```bash
   tencent-channel-cli feed del-feed \
     --guild-id 627624404088187935 \
     --channel-id <CHANNEL_ID> \
     --feed-id <FEED_ID> \
     --create-time <CREATE_TIME_RAW> \
     -y
   ```

## 质量门禁（发布前必做）

- [ ] 8 字段齐全
- [ ] 无 emoji / ★ / ①②③④ 等禁用符号
- [ ] 字号 ≥28px（海报场景）
- [ ] 目标风格与内容重要度匹配
- [ ] PNG 非空校验通过（非背景像素 >15%）
- [ ] 如用浅色风格，暖橙标签需改用兜底色 `#E2701A` 或 `#D9651A` 以满足 WCAG 大字号 3:1

## 已知坑

- Ardot `capture_screenshot` 接口常超时，但 `export_nodes` 通常正常；若 `export_nodes` 也黑屏，果断切 Pillow。
- Ardot 适配器会 NO_ADAPTER，重试 ≤3 次后仍失败则停止设计任务，切 Pillow。
- `tencent-channel-cli feed publish-feed` 图片路径用正斜杠 `/` 更稳。
- `del-feed` 必须带 `--create-time`。

## 版本

- v1.0 — 2026-07-24 — 初稿，沉淀 B_focus 卡片修复黑屏的完整流程。
