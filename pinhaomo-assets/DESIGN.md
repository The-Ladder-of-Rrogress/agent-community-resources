---
# 拼好模（PinHaoMo）资源卡设计系统规范 v1.1
# 给 coding agent 读的「视觉真源」：YAML token（机器可读）+ 下方 prose（设计叙事）。
# 用途：拼好模 QQ 频道资源卡（提示词 / Skill / 教程 索引卡）的统一视觉约束，
#       消除多卡片、多生成器之间的「设计漂移（design drift）」。
name: 拼好模 PinHaoMo
version: 1.1.0

# ===== 核心原则：抓眼而不伤眼，强可读 =====
principle:
  core: "抓眼而不伤眼，可读性强"
  eyeCatching:          # 怎么「抓眼」
    - "对比：字号差 ≥1.2 倍、强调色块、关键信息 Hero 放大"
    - "字体个性：圆体/黑体/显示体等不同字族制造第一眼记忆点"
    - "聚焦：用留白与色块把视线引到主信息，而非满屏喧哗"
  notStraining:         # 怎么「不伤眼」
    - "字号硬下限 28px（手机小屏远观场景），任何文字不得低于此值"
    - "对比度达标：普通文字 ≥4.5:1，大字号(≥24px) ≥3:1（WCAG）"
    - "主色 ≤3 种 + 强调色 ≤1 种，避免多字色乱飞"
    - "克制字重/字号种类，同屏层级 ≤5 级，避免视觉噪音"
    - "留白充足、信息成组，不拥挤"
  readable:             # 怎么「可读」
    - "左对齐为主（符合左→右阅读习惯，体验最佳）"
    - "层级精简规范，避免一个卡片内字号/颜色种类过多"
    - "亲密性：用留白/分割线/色块把相关信息成组"
    - "数字格式化：千分位、百分比一位小数、金额缩写、带符号增长率"

# ===== 字体库（不锁定单一字体，按风格与角色选用）=====
# 可用性以 Ardot get_available_fonts 校验为准；每类给候选 + 兜底。
fonts:
  library:
    rounded:            # 圆润柔和，陪伴感
      - "ZCOOL KuaiLe"        # 站酷快乐体（首选圆体）
      - "LXGW WenKai"         # 霞鹜文楷（人文楷体，柔）
    boldDisplay:        # 力量/显示体，抓眼
      - "ZCOOL QingKe HuangYou"  # 站酷庆科黄油体（厚实）
      - "Smiley Sans"           # 得意黑（窄黑潮，字怀紧）
    sans:               # 现代无衬线，正文通用
      - "Sarasa Gothic SC"      # 更纱黑体
      - "Noto Sans SC"
      - "HarmonyOS Sans SC"
    serif:              # 人文衬线，冷静专业
      - "Noto Serif SC"
    mono:               # 等宽/数据，Hero 数字
      - "Sarasa Mono SC"
      - "JetBrains Mono"
  roleBinding:          # 角色→字族（每风格内再定）
    title: "标题字族（可圆/可黑/可衬线，按风格）"
    body: "正文字族（优先 sans，保证长文可读）"
    data: "数字字族（mono 类，Hero 数字更利落）"

# ===== 多套风格（按内容重要度/类型选）=====
themes:
  A_companion:                       # 风格A·柔和陪伴（默认 / 中重要度 / 教学·陪练）
    name: "柔和陪伴"
    when: "教学种子卡、Skill 介绍、陪伴学习类（默认风格）"
    fonts: { title: "ZCOOL KuaiLe", body: "ZCOOL KuaiLe", data: "Sarasa Gothic SC" }
    weight: 400
    colors: { bg: "#EEF3FA", brand: "#2B5CFF", warm: "#FF8A3D", ink: "#16203A", card: "#FFFFFF" }
    scale: { h1: 88, h2: 56, h3: 42, h4: 36, body: 32, caption: 28 }
    rounded: { card: 28, badge: 999 }
    shadow: "0 12px 28px rgba(13,20,36,0.12)"

  B_focus:                           # 风格B·焦点高能（高重要度 / 公告·置顶·重点）
    name: "焦点高能"
    when: "公告、置顶、核心发布、重点资源（最高重要度）"
    fonts: { title: "ZCOOL QingKe HuangYou", body: "Sarasa Gothic SC", data: "Sarasa Mono SC" }
    weight: 700
    colors: { bg: "#16203A", brand: "#2B5CFF", warm: "#FF8A3D", ink: "#FFFFFF", card: "#0E1830" }
    # 深色卡 + 白字，品牌蓝/暖橙作强调，对比极强
    scale: { h1: 100, h2: 64, h3: 46, h4: 38, body: 32, caption: 28 }
    rounded: { card: 24, badge: 999 }
    shadow: "0 16px 36px rgba(0,0,0,0.35)"

  C_pro:                             # 风格C·冷静专业（中低重要度 / 技术资讯·数据·教程）
    name: "冷静专业"
    when: "技术资讯、数据卡、教程目录（信息密度高）"
    fonts: { title: "Noto Sans SC", body: "Sarasa Gothic SC", data: "JetBrains Mono" }
    weight: 700
    colors: { bg: "#F4F6F9", brand: "#2B5CFF", warm: "#FF8A3D", ink: "#16203A", card: "#FFFFFF" }
    scale: { h1: 80, h2: 52, h3: 40, h4: 34, body: 30, caption: 28 }
    rounded: { card: 16, badge: 8 }
    shadow: "0 6px 18px rgba(13,20,36,0.08)"
    layout: "网格化、左对齐严谨、强调色克制（暖橙少用）"

  D_light:                           # 风格D·轻量速读（低重要度 / 快讯·Q&A·日常）
    name: "轻量速读"
    when: "Q&A、快讯、轻量提示（最低重要度，快速扫读）"
    fonts: { title: "Sarasa Gothic SC", body: "Sarasa Gothic SC", data: "Sarasa Mono SC" }
    weight: 400
    colors: { bg: "#EEF3FA", brand: "#2B5CFF", warm: "#FF8A3D", ink: "#16203A", card: "#FFFFFF" }
    scale: { h1: 72, h2: 48, h3: 38, h4: 32, body: 28, caption: 28 }
    rounded: { card: 20, badge: 999 }
    shadow: "0 4px 12px rgba(13,20,36,0.06)"
    layout: "极少强调色，靠留白与字号拉层级，小尺寸"

# ===== 内容重要度 → 风格映射（生成时据此选风格）=====
importanceMap:
  high:   "B_focus"     # 公告/置顶/核心发布
  mid:    "A_companion" # 教学/资源/教程（默认）
  midlow: "C_pro"       # 技术资讯/数据
  low:    "D_light"     # 快讯/Q&A/日常

# ===== 通用禁用（与风格无关）=====
forbidden:
  emoji: true
  symbols:              # 禁用 U+2300–U+27BF 区间字符
    - "★"
    - "①②③④"
  substitute:
    orderedList: "1. 2. 3."
    starWord: "星标"
---

# 拼好模资源卡设计系统 v1.1

## Overview（设计理念）

圆润、柔和、有陪伴感，但**不牺牲可读性**。拼好模是面向**学生群体**的智能体学习社区，主张兴趣驱动下的陪伴学习、共同进步（学习搭子）。资源卡像「学习搭子递来的便签」——既要第一眼抓人，又不能花哨到刺眼、挤到读不懂。

本规范是资源卡视觉的**唯一真源**。v1.1 起做三处升级（相对 v1.0 的单一圆体锁死）：
1. **字体不再限定**——建立字体库，按风格与角色（标题/正文/数据）自由选用，用字族与字重拉层级。
2. **准备多套风格**（A 柔和陪伴 / B 焦点高能 / C 冷静专业 / D 轻量速读），覆盖不同内容类型与重要度。
3. **核心原则显式化为「抓眼而不伤眼，强可读」**，并给出内容重要度 → 风格的映射，生成时照此选风格。

## 核心原则：抓眼而不伤眼，强可读

（以下原则综合自视觉层级理论与 WCAG 可读性底线，详见 prose 末「原则来源」。）

- **抓眼**：靠*对比*——字号差 ≥1.2 倍、强调色块、关键信息的 Hero 放大；靠*字体个性*——圆体/黑体/显示体制造第一眼记忆；靠*聚焦*——用留白与色块把视线引到主信息，而非满屏喧哗。
- **不伤眼**：字号硬下限 **28px**（手机小屏远观场景，低于此在小图上会糊）；对比度达标（普通文字 ≥4.5:1，大字号 ≥24px 或 18.66px bold ≥3:1，WCAG）；主色 ≤3 + 强调色 ≤1，避免多字色乱飞；同屏层级 ≤5 级、字重/字号种类克制，避免视觉噪音；留白充足、信息成组不拥挤。
- **可读**：左对齐为主（符合左→右阅读习惯，体验最佳；居中偏严肃、仅信息少时用）；层级精简规范，避免一个卡片里字号/颜色种类过多；亲密性——用留白/分割线/色块把相关信息成组；数字格式化（千分位、百分比一位小数、金额缩写、带符号增长率）。

## 字体系统（不锁定，按角色与风格选用）

字体库分五类，可用性以 Ardot `get_available_fonts` 校验为准，每类给候选 + 兜底：
- **rounded 圆润柔和**（陪伴感）：ZCOOL KuaiLe（站酷快乐体，首选）、LXGW WenKai（霞鹜文楷）。
- **boldDisplay 力量显示体**（抓眼）：ZCOOL QingKe HuangYou（黄油体，厚实）、Smiley Sans（得意黑，窄黑潮）。
- **sans 现代无衬线**（正文通用）：Sarasa Gothic SC（更纱黑体）、Noto Sans SC、HarmonyOS Sans SC。
- **serif 人文衬线**（冷静专业）：Noto Serif SC。
- **mono 等宽/数据**（Hero 数字）：Sarasa Mono SC、JetBrains Mono。

层级不再靠"单字重"硬扛（那是无字体选择时的妥协）。现在可用**字族差异 + 字重差异**共同表达重要度——例如风格 B 标题用黄油体 700、正文用更纱黑体 400，既抓眼又不糊。

## 多套风格与选用

| 风格 | 名称 | 重要度/类型 | 字体组合（标题/正文/数据） | 主色逻辑 |
|---|---|---|---|---|
| A | 柔和陪伴（默认） | 中 / 教学·陪练 | 站酷快乐体 / 站酷快乐体 / 更纱黑体 | 浅蓝灰底+白卡+品牌蓝+暖橙 |
| B | 焦点高能 | 高 / 公告·置顶·重点 | 黄油体700 / 更纱黑体 / 更纱等宽 | **深色卡+白字**，品牌蓝/暖橙强调，对比极强 |
| C | 冷静专业 | 中低 / 技术资讯·数据 | Noto Sans SC700 / 更纱黑体 / JetBrains Mono | 浅灰底+白卡+单一强调色，网格严谨 |
| D | 轻量速读 | 低 / 快讯·Q&A·日常 | 更纱黑体 / 更纱黑体 / 更纱等宽 | 极少强调色，靠留白与字号 |

**选风格 = 看内容重要度**（见 YAML `importanceMap`）：
- 高（公告/置顶/核心发布）→ **B 焦点高能**
- 中（教学/资源/教程，默认）→ **A 柔和陪伴**
- 中低（技术资讯/数据）→ **C 冷静专业**
- 低（快讯/Q&A/日常）→ **D 轻量速读**

风格 B 用深色底是为了在频道信息流里"跳"出来（高重要度需要强对比抓眼），但正文白字压深蓝仍满足 ≥4.5:1；其余风格保持浅底，避免大面积深块造成信息流疲劳（不伤眼）。

## 卡片字段规范（资源卡必有结构，与风格无关）

1. 资源编号（胶囊徽章）2. 风险值（0/100）3. 类型 4. 用途 5. 核心机制（「1. 2. 3.」序号）6. 怎么用 7. 标签 8. 来源（页脚半透明）。
卡片外观由所选风格 token 决定（圆角/描边/投影/底）；画布整页用该风格 `colors.bg`，页边距随风格 `rounded`/间距微调，卡片间距 18px 起。

## 禁用与兜底（通用）

- 禁用 emoji 与 U+2300–U+27BF 区间符号（★、①②③④ 等）。
- 序号用「1. 2. 3.」；星标含义用「星标」二字。
- 任何文字 ≥28px；导出统一 2x PNG（Ardot `export_nodes`，文件名按中文语义重命名）。

## 适用边界

当前卡片在 Ardot 手工制作，本文件作为**人类可审阅的规范真源**与**质量门禁**。接入代码生成管线（内容→HTML/SVG→PNG→推送）时，coding agent 应**读取本 DESIGN.md**：先查 `importanceMap` 定风格，再套该风格 token，从根本上消除跨卡片漂移；届时可跑 `design.md` 的 `lint`/`spec` 做 CI 校验（预期暖橙对比度会报 warning，属刻意取舍，可选加深至 `#E2701A` 兜底）。

## 对比度校验记录（2026-07-24，自定义 WCAG 门禁）

官方 `@google/design.md` 的 `lint` 在本环境无法运行（沙箱无网络/格式不兼容），故以自写脚本解析本文件 4 套配色做 WCAG 校验，作为实际 CI 门禁：

- **全部「文字压底」组合达标**（≥4.5:1）；B 焦点高能（深色卡）全绿，暖橙压深卡 7.51:1。
- **唯一 FAIL**：暖橙 `#FF8A3D` 压白底（浅色风格 A/C/D 的标签）仅 2.35:1，低于大字号 3:1 门槛——属文档已注明的刻意取舍。
- **已验证兜底**：浅色风格标签改用 `#E2701A`（压白底 3.20:1，达大字号门槛）或 `#D9651A`（3.60:1）即可合规，同时保留 `#FF8A3D` 作深色卡/大装饰强调。

## 原则来源（research-backed）

- 视觉层级四要素：Size / Color / Typeface / Space+Alignment（penpot、medium 视觉层级文）。
- "避免一个卡片内采用过多不同大小字号和颜色去表现信息层级，尽量使层级精简与规范"（站酷ZCOOL 信息卡片设计文）。
- 对齐：左对齐阅读体验最佳；居中传递严肃正式感、信息少时用（同上）。
- 亲密性：用留白/分割线/色块成组（同上）。
- WCAG：普通文字对比 4.5:1；大字号（18pt≈24px 或 14pt bold≈18.66px bold）放宽至 3:1（ixdf、boia、text2infographic）。
- UI 卡正文可读下限 14–16px（web 场景）；本规范因手机海报远观设为 28px（alfdesigngroup、design4users）。
