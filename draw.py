"""Draw the 24 November 2026 news image (1024x1024) with Pillow.

Layout, my own design for this day: a navy masthead, one large lead
panel (Russian jets over Korea), two mid panels (Seoul market rally,
SpaceX/Tesla merger talks) and three bottom panels (Malaysia data
centres, Hormuz tankers, Zelensky talks). Every picture is flat shapes
drawn from scratch; every headline is short, factual text.

Run:  python3 draw.py            (writes entry.png next to this file)
Needs Pillow (build time only); the entry program main.py does not.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24

PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (20, 49, 92)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
BORDER = (190, 182, 168)
MUTED = (90, 86, 76)

RED = (179, 38, 30)
GREEN = (18, 122, 70)
BLUE = (24, 96, 160)
TEAL = (14, 107, 107)
ORANGE = (214, 106, 24)
PURPLE = (94, 64, 140)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, word by word."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, x, y, text, fnt, color, max_width, leading):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def panel(draw, x, y, w, h, accent, kicker, headline, deck,
          art, headline_size=25, deck_size=17):
    """One story card: kicker strip, headline, deck, illustration."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=CARD, outline=BORDER, width=2)
    # kicker strip
    draw.rounded_rectangle([x, y, x + w, y + 28], radius=10, fill=accent)
    draw.rectangle([x, y + 14, x + w, y + 28], fill=accent)
    draw.rectangle([x, y, x + 14, y + 28], fill=accent)
    draw.text((x + 12, y + 5), kicker, font=SANS_B(15), fill=WHITE)
    tx = x + 14
    ty = y + 40
    ty = text_block(draw, tx, ty, headline, SANS_B(headline_size), INK,
                    w - 28, headline_size + 6)
    text_block(draw, tx, ty + 4, deck, SANS(deck_size), MUTED,
               w - 28, deck_size + 5)
    art(draw, x + 10, y + h - 108, w - 20, 96)


# ---------------- illustrations (flat shapes, no photo) ----------------

def art_jets(draw, x, y, w, h):
    """Two jets over the sea near an island, with an alert triangle."""
    draw.rectangle([x, y, x + w, y + h], fill=(178, 214, 235))
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(46, 130, 150))
    # island
    draw.polygon([(x + 30, y + h - 26), (x + 90, y + h - 62),
                  (x + 170, y + h - 26)], fill=(72, 140, 82))
    draw.polygon([(x + 82, y + h - 62), (x + 88, y + h - 78),
                  (x + 96, y + h - 62)], fill=(52, 110, 62))
    # jets: simple swept silhouettes, kept inside the art box
    for jx, jy, s in ((x + 12, y + 14, 0.85), (x + 150, y + 52, 0.7)):
        body = [(jx, jy), (jx + 150 * s, jy + 12 * s),
                (jx + 150 * s, jy + 20 * s), (jx, jy + 26 * s)]
        draw.polygon(body, fill=(40, 48, 60))
        draw.polygon([(jx + 60 * s, jy + 2 * s), (jx + 110 * s, jy - 16 * s),
                      (jx + 128 * s, jy + 4 * s)], fill=(40, 48, 60))
        draw.polygon([(jx + 60 * s, jy + 26 * s), (jx + 104 * s, jy + 42 * s),
                      (jx + 122 * s, jy + 24 * s)], fill=(40, 48, 60))
    # alert triangle
    cx, cy = x + w - 58, y + h - 30
    draw.polygon([(cx, cy - 26), (cx + 26, cy + 18), (cx - 26, cy + 18)],
                 fill=RED, outline=(255, 255, 255), width=2)
    draw.text((cx - 4, cy - 14), "!", font=SANS_B(22), fill=WHITE)


def art_market(draw, x, y, w, h):
    """Rising bars and a big green arrow, with +6%."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 244, 234))
    bars = [22, 34, 30, 46, 58, 74, 88]
    bw = w // len(bars) - 8
    for i, bh in enumerate(bars):
        bx = x + 8 + i * (bw + 8)
        draw.rectangle([bx, y + h - 10 - bh, bx + bw, y + h - 10],
                       fill=GREEN)
    draw.polygon([(x + w - 170, y + 44), (x + w - 40, y + 44),
                  (x + w - 40, y + 58), (x + w - 170, y + 58)],
                 fill=GREEN)
    draw.polygon([(x + w - 40, y + 30), (x + w - 40, y + 72),
                  (x + w - 10, y + 51)], fill=GREEN)
    draw.text((x + 12, y + 8), "+6%", font=SANS_B(34), fill=GREEN)


def art_rocket(draw, x, y, w, h):
    """A rocket lifting off beside a simple car, on a dark sky."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 24, 44))
    for sx, sy in ((x + 20, y + 14), (x + 90, y + 40), (x + 200, y + 10),
                   (x + 300, y + 34), (x + 380, y + 16), (x + 250, y + 62)):
        draw.ellipse([sx, sy, sx + 4, sy + 4], fill=WHITE)
    # rocket body
    rx = x + 60
    draw.polygon([(rx, y + 8), (rx + 18, y + 8), (rx + 18, y + 56),
                  (rx, y + 56)], fill=(235, 235, 235))
    draw.polygon([(rx - 2, y + 8), (rx + 9, y - 12), (rx + 20, y + 8)],
                 fill=RED)
    draw.polygon([(rx - 10, y + 56), (rx, y + 44), (rx, y + 60)],
                 fill=RED)
    draw.polygon([(rx + 28, y + 56), (rx + 18, y + 44), (rx + 18, y + 60)],
                 fill=RED)
    draw.ellipse([rx + 4, y + 20, rx + 14, y + 30], fill=BLUE)
    draw.polygon([(rx + 2, y + 62), (rx + 8, y + 62), (rx + 5, y + 82),
                  (rx - 2, y + 78)], fill=ORANGE)
    draw.polygon([(rx + 10, y + 62), (rx + 16, y + 62), (rx + 20, y + 78),
                  (rx + 13, y + 82)], fill=(255, 190, 60))
    # simple car
    cx = x + w - 190
    cy = y + h - 34
    draw.rounded_rectangle([cx, cy - 16, cx + 150, cy + 2], radius=8,
                           fill=(200, 210, 220))
    draw.polygon([(cx + 30, cy - 16), (cx + 48, cy - 34),
                  (cx + 100, cy - 34), (cx + 118, cy - 16)],
                 fill=(200, 210, 220))
    draw.ellipse([cx + 22, cy - 4, cx + 46, cy + 16], fill=(20, 20, 20))
    draw.ellipse([cx + 104, cy - 4, cx + 128, cy + 16], fill=(20, 20, 20))


def art_servers(draw, x, y, w, h):
    """Server racks with a red cut across them."""
    draw.rectangle([x, y, x + w, y + h], fill=(228, 232, 238))
    for i in range(3):
        rx = x + 16 + i * 100
        draw.rectangle([rx, y + 8, rx + 84, y + h - 8], fill=(38, 48, 64))
        for row in range(5):
            ry = y + 16 + row * 16
            draw.rectangle([rx + 8, ry, rx + 76, ry + 10], fill=(70, 84, 104))
            draw.ellipse([rx + 12, ry + 3, rx + 17, ry + 8], fill=(90, 220, 130))
    draw.line([x + 10, y + h - 12, x + w - 10, y + 12], fill=RED, width=10)
    draw.line([x + 10, y + 12, x + w - 10, y + h - 12], fill=RED, width=10)


def art_tanker(draw, x, y, w, h):
    """A tanker on the sea with a blast above it."""
    draw.rectangle([x, y, x + w, y + h], fill=(20, 60, 110))
    draw.rectangle([x, y + h - 30, x + w, y + h], fill=(12, 44, 84))
    # tanker hull and boxes
    hx = x + 30
    draw.polygon([(hx, y + h - 46), (hx + 220, y + h - 46),
                  (hx + 200, y + h - 22), (hx + 14, y + h - 22)],
                 fill=(30, 30, 34))
    for i, col in enumerate((RED, GOLD, (220, 220, 220), BLUE)):
        bx = hx + 26 + i * 48
        draw.rectangle([bx, y + h - 72, bx + 42, y + h - 46], fill=col)
    draw.rectangle([hx + 222, y + h - 66, hx + 244, y + h - 46],
                   fill=(200, 200, 200))
    # explosion starburst
    ex, ey = x + w - 70, y + 34
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 12, 34
        a = math.radians(ang)
        draw.line([ex, ey, ex + r2 * math.cos(a), ey + r2 * math.sin(a)],
                  fill=(255, 190, 60), width=7)
    draw.ellipse([ex - 16, ey - 16, ex + 16, ey + 16], fill=ORANGE)
    draw.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(255, 230, 120))


def art_talks(draw, x, y, w, h):
    """Four flags around a table: UA, RU, US, EU."""
    draw.rectangle([x, y, x + w, y + h], fill=(233, 230, 222))
    draw.ellipse([x + 30, y + h - 44, x + w - 30, y + h - 6], fill=(150, 104, 62))
    flags = (("UA", (0, 91, 159)), ("RU", (200, 40, 40)),
             ("US", (30, 60, 120)), ("EU", (0, 51, 153)))
    fw = 62
    gap = (w - 4 * fw) // 5
    for i, (label, col) in enumerate(flags):
        fx = x + gap + i * (fw + gap)
        draw.rectangle([fx, y + 12, fx + fw, y + 44], fill=col,
                       outline=(255, 255, 255), width=2)
        draw.text((fx + 14, y + 18), label, font=SANS_B(18), fill=WHITE)
        draw.line([fx + fw // 2, y + 44, fx + fw // 2, y + h - 40],
                  fill=(90, 86, 76), width=3)


# ---------------- page ----------------

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 108], fill=NAVY)
    d.rectangle([0, 108, W, 114], fill=GOLD)
    d.text((MARGIN, 12), "THE WORLD IN ONE DAY",
           font=SERIF_B(56), fill=WHITE)
    d.text((MARGIN, 72), "TUESDAY, 24 NOVEMBER 2026",
           font=SANS_B(28), fill=GOLD)

    # lead story: Russian jets
    lx, ly, lw, lh = MARGIN, 128, W - 2 * MARGIN, 296
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10,
                        fill=CARD, outline=BORDER, width=2)
    d.rounded_rectangle([lx, ly, lx + lw, ly + 30], radius=10, fill=RED)
    d.rectangle([lx, ly + 15, lx + lw, ly + 30], fill=RED)
    d.rectangle([lx, ly, lx + 15, ly + 30], fill=RED)
    d.text((lx + 12, ly + 6), "SECURITY  ·  KOREA", font=SANS_B(15), fill=WHITE)
    text_block(d, lx + 16, ly + 44,
               "Russian jets enter Korea's air zone — Ulleung Island alert",
               SANS_B(33), INK, 560, 40)
    text_block(d, lx + 16, ly + 132,
               "Seoul scrambles fighters as Russian warplanes cross into the "
               "air defence zone. The island warning is lifted in five "
               "minutes; no airspace is violated.",
               SANS(20), MUTED, 560, 26)
    d.text((lx + 16, ly + 236), "SEOUL · TUESDAY MORNING",
           font=SANS_B(16), fill=RED)
    art_jets(d, lx + 600, ly + 44, lw - 624, lh - 60)

    # middle row
    mid_y, mid_h = 440, 252
    panel(d, MARGIN, mid_y, 480, mid_h, GREEN, "MARKETS  ·  SEOUL",
          "Seoul stocks soar as Nvidia brings back Huang",
          "KOSPI +6%, SK hynix +8% in Tuesday's rebound.",
          art_market, headline_size=25)
    panel(d, 520, mid_y, 480, mid_h, BLUE, "BUSINESS  ·  MUSK",
          "SpaceX and Tesla name directors for merger talks",
          "Five directors to lead committees, FT reports.",
          art_rocket, headline_size=25)

    # bottom row
    bot_y, bot_h = 708, 260
    bw = 317
    panel(d, MARGIN, bot_y, bw, bot_h, TEAL, "TECH  ·  MALAYSIA",
          "Malaysia: data centres must shun blacklisted firms",
          "Seven firms on the US Entity List.",
          art_servers, headline_size=22, deck_size=16)
    panel(d, 353, bot_y, bw, bot_h, ORANGE, "ENERGY  ·  GULF",
          "Iran says three tankers hit mines in Hormuz",
          "IRGC reports blasts and fires in the strait.",
          art_tanker, headline_size=22, deck_size=16)
    panel(d, 682, bot_y, bw, bot_h, PURPLE, "DIPLOMACY  ·  UKRAINE",
          "Zelensky urges four-party peace talks",
          "Kyiv says it is ready to meet as early as Tuesday.",
          art_talks, headline_size=22, deck_size=16)

    # footer
    d.text((MARGIN, 978),
           "Six stories first reported on Tuesday 24 November 2026  ·  Drawn with Python + Pillow",
           font=SANS(16), fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
