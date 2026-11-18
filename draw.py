#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news infographic (1024x1024 PNG).

Stories (all reported on 18 Nov 2026, corroborated across several outlets):
 1. Gulf: US struck an Iranian missile site on Qeshm Island; Iran hit
    Kuwait (Ali Al Salem Air Base) and Bahrain in reply.
 2. Ukraine hit the Kerch Bridge to Crimea again; part of the road span
    collapsed into the strait.
 3. Xi Jinping met Vladimir Putin in Shenzhen ahead of Thursday's
    three-way talks with Donald Trump.
 4. Democrat Mary Peltola won the Alaska Senate seat; Democrats take
    the Senate 56-44.
Also: Ebola in DR Congo passes 11,000 cases; US loses measles-free
status after 26 years; Nvidia posts a record $115.8B quarter;
Category 5 Cyclone Xavier hits the Cook Islands.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (14, 30, 51)          # deep navy
PANEL = (24, 46, 74)       # panel navy
PANEL_EDGE = (58, 96, 140)
WHITE = (245, 247, 250)
GOLD = (212, 175, 55)
MUTED = (168, 184, 204)
RED = (192, 57, 43)
BLUE = (36, 113, 163)
DARKBLUE = (31, 97, 141)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def burst(d, cx, cy, r1, r2, n=12, color=(255, 176, 32)):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=color)


def draw_explosion(d, x, y, w, h):
    # dark sky
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 46))
    # missile arcs rising from the lower left toward the burst
    d.arc([x + 6, y + 30, x + 190, y + 150], start=200, end=330,
          fill=(255, 120, 40), width=4)
    d.arc([x + 40, y + 44, x + 220, y + 160], start=205, end=335,
          fill=(255, 200, 60), width=4)
    # explosion burst
    burst(d, x + w // 2 + 30, y + h // 2 + 6, 46, 20, color=(255, 176, 32))
    burst(d, x + w // 2 + 30, y + h // 2 + 6, 28, 12, color=(255, 90, 30))
    d.ellipse([x + w // 2 + 18, y + h // 2 - 6, x + w // 2 + 42,
               y + h // 2 + 18], fill=(255, 240, 180))
    # smoke puffs near the burst
    for sx, sy, sr in [(x + w // 2 - 8, y + 18, 14),
                       (x + w // 2 + 78, y + 26, 16)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 124, 140))


def draw_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 52, 84))
    # water
    for i in range(3):
        yy = y + h - 26 + i * 9
        d.line([x + 14, yy, x + w - 14, yy], fill=(90, 160, 210), width=3)
    # towers
    d.rectangle([x + 56, y + 28, x + 72, y + h - 30], fill=(200, 208, 216))
    d.rectangle([x + w - 72, y + 28, x + w - 56, y + h - 30],
                fill=(200, 208, 216))
    # deck, left and right spans intact, middle span collapsed
    d.line([x + 20, y + 62, x + w // 2 - 46, y + 62], fill=(230, 236, 242),
           width=6)
    d.line([x + w // 2 + 46, y + 62, x + w - 20, y + 62],
           fill=(230, 236, 242), width=6)
    # collapsed span: two diagonals falling into the water
    d.line([x + w // 2 - 46, y + 62, x + w // 2 - 8, y + h - 34],
           fill=(255, 120, 40), width=6)
    d.line([x + w // 2 + 46, y + 62, x + w // 2 + 8, y + h - 34],
           fill=(255, 120, 40), width=6)
    # cables
    d.line([x + 64, y + 28, x + w // 2 - 46, y + 62], fill=(150, 164, 180),
           width=2)
    d.line([x + w - 64, y + 28, x + w // 2 + 46, y + 62],
           fill=(150, 164, 180), width=2)


def draw_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(32, 40, 56))
    # three flags on poles: China, Russia, USA
    flags = [
        ("CN", (204, 0, 0), None),
        ("RU", None, [(255, 255, 255), (0, 57, 166), (213, 0, 50)]),
        ("US", None, "us"),
    ]
    fw, fh, gap = 92, 58, 26
    total = 3 * fw + 2 * gap
    x0 = x + (w - total) // 2
    y0 = y + 22
    for i, (code, solid, stripes) in enumerate(flags):
        fx = x0 + i * (fw + gap)
        # pole
        d.line([fx + fw // 2, y0 - 8, fx + fw // 2, y0 + fh + 26],
               fill=(200, 200, 200), width=3)
        if solid:
            d.rectangle([fx, y0, fx + fw, y0 + fh], fill=solid)
            for sx, sy in [(fx + 14, y0 + 12), (fx + 26, y0 + 20),
                           (fx + 14, y0 + 28)]:
                d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3],
                          fill=(255, 222, 0))
        elif stripes == "us":
            for s in range(7):
                col = (178, 34, 52) if s % 2 == 0 else (255, 255, 255)
                d.rectangle([fx, y0 + s * (fh // 7), fx + fw,
                             y0 + (s + 1) * (fh // 7)], fill=col)
            d.rectangle([fx, y0, fx + 38, y0 + 30], fill=(60, 59, 110))
            for r in range(3):
                for c in range(3):
                    d.ellipse([fx + 6 + c * 11, y0 + 6 + r * 9,
                               fx + 9 + c * 11, y0 + 9 + r * 9],
                              fill=(255, 255, 255))
        else:
            for s, col in enumerate(stripes):
                d.rectangle([fx, y0 + s * (fh // 3), fx + fw,
                             y0 + (s + 1) * (fh // 3)], fill=col)
        d.text((fx + fw // 2, y0 + fh + 34), code, font=font(20, True),
               fill=MUTED, anchor="mt")


def draw_capitol(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 58, 92))
    cx = x + w // 2
    # dome
    d.pieslice([cx - 52, y + 8, cx + 52, y + 92], start=180, end=360,
               fill=(235, 240, 245))
    d.rectangle([cx - 56, y + 48, cx + 56, y + 58], fill=(235, 240, 245))
    d.rectangle([cx - 3, y - 2, cx + 3, y + 12], fill=(235, 240, 245))
    # columns
    for i in range(5):
        colx = cx - 64 + i * 32
        d.rectangle([colx, y + 58, colx + 12, y + 108],
                    fill=(215, 222, 230))
    d.rectangle([cx - 72, y + 108, cx + 72, y + 118], fill=(235, 240, 245))
    # ballot box
    bx, by = x + w - 108, y + h - 52
    d.rectangle([bx, by, bx + 78, by + 40], fill=(212, 175, 55))
    d.rectangle([bx + 8, by - 8, bx + 70, by], fill=(170, 140, 40))
    d.line([bx + 14, by + 20, bx + 32, by + 34, bx + 64, by + 6],
           fill=(255, 255, 255), width=5)


def panel(d, x, y, w, h, tag, accent, headline, sub, pic):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=PANEL,
                        outline=PANEL_EDGE, width=2)
    # tag band
    d.rounded_rectangle([x, y, x + w, y + 44], radius=14, fill=accent)
    d.rectangle([x, y + 30, x + w, y + 44], fill=accent)
    d.text((x + 18, y + 22), tag, font=font(21, True), fill=WHITE,
           anchor="lm")
    # pictogram
    pic(d, x + 16, y + 56, w - 32, 122)
    # headline (kept to two lines so the subtext fits inside the panel)
    lines = wrap(d, headline, font(28, True), w - 36)[:2]
    yy = y + 190
    for ln in lines:
        d.text((x + 18, yy), ln, font=font(28, True), fill=WHITE)
        yy += 34
    # subtext
    slines = wrap(d, sub, font(19), w - 36)[:2]
    for ln in slines:
        d.text((x + 18, yy + 4), ln, font=font(19), fill=MUTED)
        yy += 24


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # masthead
    d.text((W // 2, 34), "THE WORLD IN ONE IMAGE", font=font(24, True),
           fill=GOLD, anchor="mt")
    d.text((W // 2, 96), "WEDNESDAY 18 NOVEMBER 2026",
           font=font(52, True), fill=WHITE, anchor="mm")
    d.line([40, 140, W - 40, 140], fill=GOLD, width=3)

    px, py, pw, ph, gap = 24, 158, 476, 330, 24
    panel(d, px, py, pw, ph, "MIDDLE EAST  ·  WAR", RED,
          "Iran hits Kuwait & Bahrain after US strike",
          "Tehran answers the US strike on Qeshm with drones and "
          "missiles at Gulf targets.", draw_explosion)
    panel(d, px + pw + gap, py, pw, ph, "UKRAINE  ·  WAR", BLUE,
          "Kerch Bridge hit again — road span collapses",
          "Second day of strikes on the Crimea bridge; part of the "
          "span falls into the strait.", draw_bridge)
    panel(d, px, py + ph + gap, pw, ph, "CHINA  ·  SUMMIT", (155, 125, 10),
          "Xi meets Putin in Shenzhen ahead of talks with Trump",
          "The two leaders coordinate one day before the three-way "
          "summit on Thursday.", draw_flags)
    panel(d, px + pw + gap, py + ph + gap, pw, ph,
          "UNITED STATES  ·  POLITICS", DARKBLUE,
          "Peltola wins Alaska — Democrats take Senate 56–44",
          "The Alaska result flips the chamber; Israel's parliament "
          "elects a new speaker.", draw_capitol)

    # also-today strip
    y0 = py + 2 * ph + 2 * gap + 6
    d.rounded_rectangle([24, y0, W - 24, y0 + 104], radius=12,
                        fill=(20, 38, 62), outline=PANEL_EDGE, width=2)
    d.text((44, y0 + 16), "ALSO ON 18 NOVEMBER", font=font(20, True),
           fill=GOLD)
    d.text((44, y0 + 48),
           "Ebola in DR Congo passes 11,000 cases  ·  US loses measles-free "
           "status after 26 years",
           font=font(21), fill=WHITE)
    d.text((44, y0 + 76),
           "Nvidia posts a record $115.8B quarter  ·  Cyclone Xavier hits "
           "the Cook Islands",
           font=font(21), fill=WHITE)

    # footer
    d.text((W // 2, H - 22),
           "18 NOVEMBER 2026  ·  One day's world news, drawn from reports "
           "of the day",
           font=font(18), fill=MUTED, anchor="mm")

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
