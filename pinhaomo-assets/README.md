# 拼好模 · 运营资产（pinhaomo-assets）

本目录沉淀「拼好模」QQ 频道智能体学习社区的**自有运营资产**，与仓库根的策展列表（`README.md`）互补：那里是**外部资源策展**，这里是**社区自有资产**。

## 目录结构

- `DESIGN.md` — 资源卡视觉规范真源（沿用 google-labs/design.md 格式：YAML token + 设计叙事）。定义 4 套风格（A 柔和陪伴 / B 焦点高能 / C 冷静专业 / D 轻量速读）、字号梯度、配色与禁用项，消除多卡片设计漂移。
- `scripts/generate_b_card.py` — B 风格资源卡生成器（Pillow）。当 Ardot 导出异常时的可靠兜底，可扩展为通用资源卡生成器。
- `exports/` — 已发布到频道的资源卡 PNG（2x）：
  - `拼好模-教学种子资源卡.png` — `/teach` + `/writing-great-skills` 学生向种子卡（资源精选）
  - `拼好模-DESIGN.md资源卡.png` — Google Labs `DESIGN.md` 项目卡（资源精选）
  - `拼好模-open-image-prompts资源卡.png` — NanmiCoder/open-image-prompts 可溯源视觉提示词归档卡（资源精选）
- `skills/pinhaomo-resource-card/SKILL.md` — 资源卡制作项目级 skill（双路线：Ardot 设计 / Pillow 代码生成）。

## 使用

- 新增资源卡：照 `DESIGN.md` 选风格 → Ardot 设计或 `scripts/generate_b_card.py` 生成 → `tencent-channel-cli feed publish-feed --image` 发「资源精选」（channel `737383095`）。
- 频道标识：guild-id `627624404088187935`，展示号 `pd38005630`。
- 字体：Ardot 等价中文字体缓存于本机 `C:/Users/79204/.kimi-work/bin/kimi-tools/fonts/`（黄油体 `19-ZCOOLQingKeHuangYou.ttf`、站酷快乐体 `26-ZCOOL-KuaiLe.ttf`）。
