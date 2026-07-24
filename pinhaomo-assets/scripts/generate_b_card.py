from PIL import Image, ImageDraw, ImageFont
import os

# B-style design.md resource card generator (Ardot fallback)
# 视觉对齐「拼好模-教学种子资源」：正文/副标题用站酷快乐体(圆润柔和)，
# 强对比小标题(类型行/小节标签)用 Noto Sans SC 粗体，块间距与行距拉大→疏朗排布。
W = 1080
PAD = 56
CARD_PAD = 44
CARD_RADIUS = 24
CARD_GAP = 26        # 块间距（稀疏化：原16）
LINE_GAP = 16        # 行间距（稀疏化：原12）
LABEL_GAP = 14       # 小节标签到正文间距（原8）

COLORS = {
    "bg": "#16203A",
    "card": "#0E1830",
    "card_border": "#2B5CFF",
    "brand": "#2B5CFF",
    "warm": "#FF8A3D",
    "white": "#FFFFFF",
    "sub": "#DCE3F2",       # 副标题次白
    "src": "#9397A2",       # 来源 0.55 白混色
}

FONT_PATH = "C:/Windows/Fonts/NotoSansSC-VF.ttf"
# Ardot equivalent of ZCOOL QingKe HuangYou (黄油体), used for display title
FONT_TITLE_PATH = "C:/Users/79204/.kimi-work/bin/kimi-tools/fonts/19-ZCOOLQingKeHuangYou.ttf"
# Ardot equivalent of ZCOOL KuaiLe (站酷快乐体), used for body/subtitle — rounded & soft
FONT_BODY_PATH = "C:/Users/79204/.kimi-work/bin/kimi-tools/fonts/26-ZCOOL-KuaiLe.ttf"

def load_font(size, weight=400, path=FONT_PATH):
    try:
        return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)
    except Exception as e:
        print(f"font load error: {e}")
        return ImageFont.load_default()

def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def wrap_text(text, font, max_w, draw):
    """CJK-aware word wrap: split on spaces, break over-long tokens by character."""
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for w in words:
            if text_size(draw, w, font)[0] > max_w:
                if cur:
                    lines.append(cur); cur = ""
                ccur = ""
                for ch in w:
                    if text_size(draw, ccur + ch, font)[0] <= max_w:
                        ccur += ch
                    else:
                        lines.append(ccur); ccur = ch
                cur = ccur
                continue
            test = (cur + " " + w).strip()
            if text_size(draw, test, font)[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def main():
    # Fonts
    f_badge = load_font(30, 700)                              # Noto 粗体
    f_risk = load_font(38, 700)                               # Noto 粗体
    f_title = load_font(100, 400, path=FONT_TITLE_PATH)       # 黄油体
    f_sub = load_font(46, 400, path=FONT_BODY_PATH)           # 站酷快乐体(圆润)
    f_type = load_font(38, 900)                               # Noto Black 强对比小标题
    f_label = load_font(38, 700)                              # Noto Bold 小节标签
    f_body_bold = load_font(32, 400, path=FONT_BODY_PATH)     # 站酷快乐体 + 暖橙强调
    f_body = load_font(32, 400, path=FONT_BODY_PATH)          # 站酷快乐体 正文
    f_tags = load_font(28, 700)                               # Noto 粗体
    f_src = load_font(28, 400)                                # Noto 常规

    tmp = Image.new("RGB", (W, 3000), COLORS["bg"])
    draw = ImageDraw.Draw(tmp)

    content_w = W - PAD * 2 - CARD_PAD * 2

    badge_w, badge_h = text_size(draw, "资源 03", f_badge)
    risk_w, risk_h = text_size(draw, "风险 0/100", f_risk)
    head_h = max(badge_h, risk_h)

    title_lines = wrap_text("让 AI 生成 UI 不跑偏", f_title, content_w, draw)
    title_h = sum(text_size(draw, ln, f_title)[1] for ln in title_lines) + LINE_GAP * (len(title_lines) - 1)

    sub_lines = wrap_text("Google Labs 开源 · DESIGN.md 设计规范", f_sub, content_w, draw)
    sub_h = sum(text_size(draw, ln, f_sub)[1] for ln in sub_lines) + LINE_GAP * (len(sub_lines) - 1)

    type_h = text_size(draw, "类型：设计系统规范 / 工具", f_type)[1]

    label_use_h = text_size(draw, "用途", f_label)[1]
    use_lines = wrap_text("用一份 Markdown 描述视觉识别，让 coding agent 自动遵循，消灭跨页面「设计漂移」。", f_body_bold, content_w, draw)
    use_h = sum(text_size(draw, ln, f_body_bold)[1] for ln in use_lines) + LINE_GAP * (len(use_lines) - 1)

    label_mech_h = text_size(draw, "核心机制", f_label)[1]
    mech_lines = wrap_text("1. YAML token（颜色/字体/间距）机器可读；2. Markdown 叙事人类可读；3. CLI 支持 lint/diff/export/spec；4. 9 条 lint 规则（对比度/断链等）。", f_body, content_w, draw)
    mech_h = sum(text_size(draw, ln, f_body)[1] for ln in mech_lines) + LINE_GAP * (len(mech_lines) - 1)

    label_how_h = text_size(draw, "怎么用", f_label)[1]
    how_lines = wrap_text("在仓库根放 DESIGN.md，AI 编程助手自动读取遵循；npx @google/design.md 一键用。拼好模已把自身规范写成 DESIGN.md。", f_body, content_w, draw)
    how_h = sum(text_size(draw, ln, f_body)[1] for ln in how_lines) + LINE_GAP * (len(how_lines) - 1)

    tags_h = text_size(draw, "#设计系统 #AI生成UI #不跑偏 #GoogleLabs", f_tags)[1]
    src_lines = wrap_text("来源 github.com/google-labs-code/design.md（21.7万 星标）｜拼好模 QQ频道", f_src, content_w, draw)
    src_h = sum(text_size(draw, ln, f_src)[1] for ln in src_lines) + LINE_GAP * (len(src_lines) - 1)

    card_inner_h = (
        head_h
        + CARD_GAP
        + title_h
        + CARD_GAP
        + sub_h
        + CARD_GAP
        + type_h
        + CARD_GAP
        + label_use_h
        + LABEL_GAP
        + use_h
        + CARD_GAP
        + label_mech_h
        + LABEL_GAP
        + mech_h
        + CARD_GAP
        + label_how_h
        + LABEL_GAP
        + how_h
        + CARD_GAP
        + tags_h
        + CARD_GAP
        + src_h
    )
    H = PAD * 2 + card_inner_h + CARD_PAD * 2

    img = Image.new("RGB", (W, H), COLORS["bg"])
    draw = ImageDraw.Draw(img)

    shadow_offset = 12
    card_rect = [PAD, PAD, W - PAD, PAD + card_inner_h + CARD_PAD * 2]
    draw.rounded_rectangle(
        [card_rect[0] + shadow_offset, card_rect[1] + shadow_offset, card_rect[2] + shadow_offset, card_rect[3] + shadow_offset],
        radius=CARD_RADIUS, fill="#0a1220"
    )
    draw.rounded_rectangle(card_rect, radius=CARD_RADIUS, fill=COLORS["card"], outline=COLORS["card_border"], width=3)

    y = PAD + CARD_PAD

    badge_rect = [PAD + CARD_PAD, y, PAD + CARD_PAD + badge_w + 36, y + head_h + 8]
    draw.rounded_rectangle(badge_rect, radius=999, fill=COLORS["brand"])
    draw.text((PAD + CARD_PAD + 18, y + 4), "资源 03", font=f_badge, fill=COLORS["white"])
    draw.text((W - PAD - CARD_PAD - risk_w, y), "风险 0/100", font=f_risk, fill=COLORS["warm"])
    y += head_h + CARD_GAP

    for ln in title_lines:
        draw.text((PAD + CARD_PAD, y), ln, font=f_title, fill=COLORS["white"])
        y += text_size(draw, ln, f_title)[1] + LINE_GAP
    y += CARD_GAP - LINE_GAP

    for ln in sub_lines:
        draw.text((PAD + CARD_PAD, y), ln, font=f_sub, fill=COLORS["sub"])
        y += text_size(draw, ln, f_sub)[1] + LINE_GAP
    y += CARD_GAP - LINE_GAP

    draw.text((PAD + CARD_PAD, y), "类型：设计系统规范 / 工具", font=f_type, fill=COLORS["brand"])
    y += type_h + CARD_GAP

    draw.text((PAD + CARD_PAD, y), "用途", font=f_label, fill=COLORS["brand"])
    y += label_use_h + LABEL_GAP
    for ln in use_lines:
        draw.text((PAD + CARD_PAD, y), ln, font=f_body_bold, fill=COLORS["warm"])
        y += text_size(draw, ln, f_body_bold)[1] + LINE_GAP
    y += CARD_GAP - LINE_GAP

    draw.text((PAD + CARD_PAD, y), "核心机制", font=f_label, fill=COLORS["brand"])
    y += label_mech_h + LABEL_GAP
    for ln in mech_lines:
        draw.text((PAD + CARD_PAD, y), ln, font=f_body, fill=COLORS["white"])
        y += text_size(draw, ln, f_body)[1] + LINE_GAP
    y += CARD_GAP - LINE_GAP

    draw.text((PAD + CARD_PAD, y), "怎么用", font=f_label, fill=COLORS["brand"])
    y += label_how_h + LABEL_GAP
    for ln in how_lines:
        draw.text((PAD + CARD_PAD, y), ln, font=f_body, fill=COLORS["white"])
        y += text_size(draw, ln, f_body)[1] + LINE_GAP
    y += CARD_GAP - LINE_GAP

    draw.text((PAD + CARD_PAD, y), "#设计系统 #AI生成UI #不跑偏 #GoogleLabs", font=f_tags, fill=COLORS["warm"])
    y += tags_h + CARD_GAP

    for ln in src_lines:
        draw.text((PAD + CARD_PAD, y), ln, font=f_src, fill=COLORS["src"])
        y += text_size(draw, ln, f_src)[1] + LINE_GAP

    out = "C:/Users/79204/WorkBuddy/QQ频道/exports/拼好模-DESIGN.md资源卡.png"
    img2x = img.resize((W * 2, H * 2), Image.Resampling.LANCZOS)
    img2x.save(out, "PNG")
    print(f"saved: {out} ({W*2}x{H*2})")

    px = list(img2x.getdata())
    bg = (22, 32, 58)
    non_bg = sum(1 for p in px if p[:3] != bg)
    print(f"non-background pixels: {non_bg} / {len(px)} ({100*non_bg/len(px):.1f}%)")

if __name__ == "__main__":
    main()
