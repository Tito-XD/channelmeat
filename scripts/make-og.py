# -*- coding: utf-8 -*-
"""生成 channelme.at 的方形 Open Graph 封面图 (1200x1200)。"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(ROOT, "public", "assets", "logo-meat.jpg")
OUT = os.path.join(ROOT, "public", "assets", "og-cover.png")

W = H = 1200
BG = (236, 236, 236)
INK = (29, 29, 31)
RED = (242, 64, 47)
GRAY = (136, 136, 136)

FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---- 半调网点背景（与网页 CSS 同款两层网点）----
for i, (size, gap, offset, alpha_col) in enumerate([
    (3, 44, 0, (210, 210, 210)),
    (2, 34, 17, (222, 222, 222)),
]):
    y = offset
    while y < H:
        x = offset
        while x < W:
            d.ellipse([x - size, y - size, x + size, y + size], fill=alpha_col)
            x += gap
        y += gap

# ---- （OG 图不放 M 水印，保持主体清晰）----

# ---- LOGO：圆角 + 白边贴纸感 ----
logo_size = 500
border = 18
logo = Image.open(LOGO).convert("RGB").resize((logo_size, logo_size), Image.LANCZOS)

mask = Image.new("L", (logo_size, logo_size), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([0, 0, logo_size, logo_size], radius=90, fill=255)

card = Image.new("RGB", (logo_size + border * 2, logo_size + border * 2), (255, 255, 255))
card.paste(logo, (border, border))
card_mask = Image.new("L", card.size, 0)
cd = ImageDraw.Draw(card_mask)
cd.rounded_rectangle([0, 0, card.size[0], card.size[1]], radius=104, fill=255)

card = card.rotate(2.5, expand=True, resample=Image.BICUBIC, fillcolor=None)
card_mask = card_mask.rotate(2.5, expand=True, resample=Image.BICUBIC)

# 贴纸投影
shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sx = (W - card.size[0]) // 2 + 10
sy = 130 + 14
sd.bitmap((sx, sy), card_mask, fill=(0, 0, 0, 40))
shadow = shadow.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(14))
img.paste(shadow, (0, 0), shadow)

lx = (W - card.size[0]) // 2
ly = 130
img.paste(card, (lx, ly), card_mask)

# ---- 标题 ----
title_font = ImageFont.truetype(FONT_BOLD, 112)
d.text((W // 2, 800), "肉食狗小分队", font=title_font, fill=INK, anchor="mm")

# ---- 红色胶囊 CHANNEL MEAT ----
pill_font = ImageFont.truetype(FONT_BOLD, 44)
text = "CHANNEL MEAT"
# 手动加字距
spacing = 10
widths = [d.textlength(ch, font=pill_font) for ch in text]
total_w = sum(widths) + spacing * (len(text) - 1)
pad_x, pad_y = 42, 18
pill_w = int(total_w + pad_x * 2)
pill_h = 44 + pad_y * 2
pill_y = 880
d.rounded_rectangle([(W - pill_w) // 2, pill_y, (W + pill_w) // 2, pill_y + pill_h],
                    radius=pill_h // 2, fill=RED)
cx = W // 2 - total_w / 2
for ch, wch in zip(text, widths):
    d.text((cx, pill_y + pill_h // 2), ch, font=pill_font, fill=(255, 255, 255), anchor="lm")
    cx += wch + spacing

# ---- slogan ----
slogan_font = ImageFont.truetype(FONT_BOLD, 32)
d.text((W // 2, 1000), "SEEK FOR MEAT · STAY FOR MEET", font=slogan_font, fill=GRAY, anchor="mm")

# ---- 底部域名 ----
domain_font = ImageFont.truetype(FONT_BOLD, 40)
d.text((W // 2, 1105), "channelme.at", font=domain_font, fill=RED, anchor="mm")

img.save(OUT, "PNG", optimize=True)
print("saved:", OUT, img.size)
