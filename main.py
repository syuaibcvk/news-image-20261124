#!/usr/bin/env python3
"""The World in One Day — Tuesday 24 November 2026.

A deterministic newspaper front page drawn from scratch with Pillow.
Lead: seven Ukrainian sea drones sank the Russian corvette Merkury at
Benghazi naval base, Libya, in the early hours of Sunday 22 November;
President Zelensky confirmed it on Monday 23 November, calling it an
"exemplary mission". Libyan officials described the ship as severely
damaged; satellite images showed most of it submerged, bow above
water. The cargo ship MV Angara was also hit and a Ka-27 helicopter
aboard was destroyed. The UN called for an inquiry, Russia promised
a response, and Tripoli demanded an explanation from Kyiv.

Grid: Nvidia's board unanimously reinstated Jensen Huang as CEO on
Monday after pressure from President Trump and shareholders, sending
the stock up about 31-33%, the Nasdaq up 6.51% and the S&P 500 up
4.73%; stocks soared while Bitcoin faded from $64,500 on Monday to
about $60,880-61,250 on Tuesday morning, with Fear & Greed at 11
(Extreme Fear), $4.14 billion of spot Bitcoin ETF outflows in
November to 20 November, and US October PCE due Wednesday 25 November
at 08:30 ET; Russia warned Estonia of "open war" as Estonia prepares
to close its land border from 1 December for at least six months; and
14 nations — the UK, Spain, Canada, Australia and ten others —
recognised the ICJ's Rohingya genocide ruling.

In brief: Gaza, the Nepal 5.6 earthquake, Virginia and Oregon suing
SpaceX over Grok, Russian jets in South Korea's air defence zone,
and Iran and the Gulf.

Sources were cross-checked on 24 November 2026 against Reuters, CNN,
AP, the WSJ and other reporting named in the research brief. Weekend
and Monday events are dated honestly in the text. No network, no
clock, no randomness: two runs write byte-identical PNGs.
Output: $MAKEFUN_OUTPUT_DIR/entry.png, or ./entry.png beside this
file when the variable is unset.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
MARGIN = 38
CONTENT = SIDE - 2 * MARGIN

NEWSROOM = (248, 244, 236)
BLACK = (24, 22, 18)
CRIMSON = (139, 28, 28)
MUTED = (112, 104, 92)
RULE_GREY = (203, 195, 178)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
FIXED = "DejaVuSansMono.ttf"


def face(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def fit_lines(canvas, text, font, width):
    out, current = [], ""
    for word in text.split():
        candidate = word if not current else current + " " + word
        if canvas.textlength(candidate, font=font) <= width:
            current = candidate
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


class Page:
    def __init__(self):
        self.sheet = Image.new("RGB", (SIDE, SIDE), NEWSROOM)
        self.pen = ImageDraw.Draw(self.sheet)
        self.cursor = 16

    def rule(self, thick=2, colour=BLACK, left=MARGIN, right=SIDE - MARGIN):
        self.pen.rectangle([left, self.cursor, right, self.cursor + thick - 1],
                           fill=colour)
        self.cursor += thick

    def space(self, n):
        self.cursor += n

    def block(self, text, font, leading, width=CONTENT, x=MARGIN,
              colour=BLACK, centred=False):
        for line in fit_lines(self.pen, text, font, width):
            at = x
            if centred:
                at = x + (width - self.pen.textlength(line, font=font)) / 2
            self.pen.text((at, self.cursor), line, font=font, fill=colour)
            self.cursor += leading


def header(page):
    page.rule(5)
    page.space(3)
    page.rule(1)
    page.space(8)
    page.block("THE WORLD IN ONE DAY", face(SERIF_B, 42), 50, centred=True)
    page.space(2)
    page.block("Tuesday 24 November 2026  ·  The day's world news on a "
               "single page  ·  No. 24", face(SANS, 14), 19, colour=MUTED,
               centred=True)
    page.space(5)
    page.block("MONDAY CLOSE:  NASDAQ +6.51%   ·   S&P 500 +4.73%   ·   "
               "DOW +3.01%   ·   NVIDIA +~31-33%", face(FIXED, 13), 17,
               centred=True)
    page.space(5)
    page.rule(1)
    page.space(3)
    page.rule(4)
    page.space(7)
    page.block("INSIDE — Ukraine sinks Russian corvette in Libya  ·  Huang "
               "back at Nvidia  ·  Russia warns Estonia  ·  Rohingya ruling",
               face(SANS_B, 12), 16, colour=CRIMSON, centred=True)
    page.space(7)


def lead_story(page):
    top = page.cursor
    page.pen.rectangle([MARGIN, top, SIDE - MARGIN, top + 2], fill=CRIMSON)
    page.cursor = top + 12
    page.block("LIBYA  ·  BENGHAZI  —  SANK SUNDAY, CONFIRMED MONDAY",
               face(SANS_B, 12), 15, width=CONTENT - 28, x=MARGIN + 14,
               colour=CRIMSON)
    page.space(4)
    page.block("Ukraine sinks Russian warship in Libya",
               face(SERIF_B, 30), 35, width=CONTENT - 28, x=MARGIN + 14)
    page.space(4)
    page.block(
        "Seven Ukrainian sea drones sank the Russian corvette Merkury "
        "at Benghazi naval base in the early hours of Sunday 22 "
        "November, President Zelensky confirmed on Monday, calling it "
        "an \u201cexemplary mission\u201d. The new corvette, commissioned in "
        "2023, was left mostly submerged, only its bow above water in "
        "satellite images. Libyan officials said the ship was "
        "\u201cseverely damaged\u201d rather than sunk. The cargo ship MV "
        "Angara, used to carry weapons, was also hit, a Ka-27 "
        "helicopter aboard was destroyed, and ten Russians and Libyans "
        "were lightly wounded. The UN called for an inquiry, Tripoli "
        "demanded an explanation from Kyiv, Libya condemned the "
        "attack, and Russia promised to respond.",
        face(SERIF, 14), 18, width=CONTENT - 28, x=MARGIN + 14)
    page.space(5)
    page.block("7 SEA DRONES  ·  SUNDAY 22 NOV, BENGHAZI  ·  ZELENSKY: "
               "\u201cSUNK\u201d  ·  LIBYA: \u201cSEVERELY DAMAGED\u201d",
               face(FIXED, 12), 16, width=CONTENT - 28, x=MARGIN + 14,
               colour=MUTED)
    page.cursor += 8
    bottom = page.cursor
    page.pen.rectangle([MARGIN, top, SIDE - MARGIN, bottom], outline=BLACK,
                       width=1)
    page.pen.rectangle([MARGIN, top, MARGIN + 5, bottom], fill=CRIMSON)
    page.space(12)


def one_story(page, x, width, kicker, headline, body):
    start = page.cursor
    page.block(kicker, face(SANS_B, 11), 12, width=width, x=x, colour=CRIMSON)
    page.space(2)
    page.block(headline, face(SERIF_B, 16), 17, width=width, x=x)
    page.space(2)
    page.block(body, face(SERIF, 12), 14, width=width, x=x)
    return page.cursor - start


def story_row(page, pair):
    between = 22
    col = (CONTENT - between) // 2
    tallest = 0
    for i, item in enumerate(pair):
        x = MARGIN + i * (col + between)
        saved = page.cursor
        used = one_story(page, x, col, item[0], item[1], item[2])
        tallest = max(tallest, used)
        page.cursor = saved
        if i:
            divider = x - between // 2
            page.pen.line([divider, saved + 2, divider, saved + tallest - 4],
                          fill=RULE_GREY, width=1)
    page.cursor += tallest


GRID = [
    [
        ("NVIDIA  ·  MONDAY",
         "Huang is back: Nvidia board reinstates its founder",
         "Nvidia\u2019s board voted unanimously on Monday to bring back "
         "Jensen Huang as CEO, effective immediately, 11 days after he "
         "stepped down and after pressure from President Trump and "
         "shareholders. The stock jumped about 31\u201333%; the Commerce "
         "Department blacklisted Singapore chip firm Megaspeed the "
         "same day."),
        ("MARKETS  ·  BITCOIN",
         "Stocks soar, Bitcoin fades as fear stays extreme",
         "Monday\u2019s rebound lifted the Nasdaq 6.51% to 24,089.56 and "
         "the S&P 500 4.73% to 7,237.90. Bitcoin touched $64,500 on "
         "Monday, then slipped to about $60,880\u201361,250 on Tuesday "
         "morning. Fear & Greed sat at 11 (Extreme Fear); spot Bitcoin "
         "ETFs saw $4.14bn of outflows in November to 20 Nov. US "
         "October PCE is due Wednesday 25 Nov at 08:30 ET."),
    ],
    [
        ("ESTONIA  ·  RUSSIA",
         "Russia warns Estonia of \u201copen war\u201d over border closure",
         "Russia\u2019s foreign ministry on Monday accused Estonia of "
         "hostile acts \u201con the verge of triggering open war\u201d, after "
         "Tallinn said it will close its land border with Russia from "
         "1 December for at least six months, citing an alleged "
         "Russian-backed arson attempt on a defence firm. Estonia "
         "denied its territory is used for Ukrainian operations."),
        ("MYANMAR  ·  THE HAGUE",
         "Rohingya: 14 nations back the ICJ genocide ruling",
         "The United Kingdom, Spain, Canada, Australia and ten other "
         "nations said on Monday that they recognise last week\u2019s "
         "International Court of Justice ruling finding a genocide of "
         "the Rohingya by Myanmar \u2014 a joint backing that raises the "
         "pressure on Myanmar\u2019s rulers to comply."),
    ],
]

SHORTS = [
    ("GAZA",
     "Israeli strikes killed at least three people, including an "
     "UNRWA worker."),
    ("NEPAL",
     "A magnitude 5.6 earthquake struck Koshi province, near the "
     "border with China."),
    ("UNITED STATES",
     "Virginia and Oregon sued SpaceX over alleged child-abuse images "
     "generated by Grok."),
    ("SOUTH KOREA",
     "Russian warplanes entered South Korea\u2019s air defence zone on "
     "Monday; Seoul issued an emergency warning for Ulleung Island."),
    ("IRAN  ·  GULF",
     "Iran stepped up strikes on Gulf sites amid a $290bn lawsuit, as "
     "the US tightened sanctions and its naval blockade."),
]


def brief_section(page, items):
    page.block("IN BRIEF", face(SANS_B, 13), 16, colour=CRIMSON)
    page.space(3)
    for place, text in items:
        page.block(place + " — " + text, face(SERIF, 13), 16)
        page.space(1)


def glance_box(page):
    """A ruled 'at a glance' strip filling the foot of the page with
    the day's verified figures, so the sheet reads as a full page."""
    top = page.cursor
    page.pen.rectangle([MARGIN, top, SIDE - MARGIN, top + 2], fill=CRIMSON)
    page.cursor = top + 12
    page.block("THE DAY AT A GLANCE", face(SANS_B, 12), 15,
               width=CONTENT - 28, x=MARGIN + 14, colour=CRIMSON)
    page.space(4)
    page.block("MERKURY — sunk Sunday at Benghazi, Zelensky said; "
               "\u201cseverely damaged\u201d, Libya said  ·  NVIDIA — Huang back, "
               "stock +~31\u201333%  ·  BITCOIN — $64,500 Monday, "
               "~$60,880\u201361,250 Tuesday, Fear & Greed 11  ·  ESTONIA — "
               "land border closes 1 Dec, \u22656 months  ·  ROHINGYA — 14 "
               "nations back the ICJ ruling  ·  NEXT — US PCE, Wed 25 "
               "Nov, 08:30 ET", face(SERIF, 13), 17, width=CONTENT - 28,
               x=MARGIN + 14)
    page.cursor += 8
    bottom = page.cursor
    page.pen.rectangle([MARGIN, top, SIDE - MARGIN, bottom], outline=BLACK,
                       width=1)
    page.pen.rectangle([MARGIN, top, MARGIN + 5, bottom], fill=CRIMSON)
    page.space(12)


def colophon(page):
    page.rule(2)
    page.space(5)
    page.block("Sources: Reuters · CNN · AP · WSJ · Al Jazeera · "
               "Defense News · The Times · Fox News",
               face(SANS, 11), 14, colour=MUTED, centred=True)
    page.space(3)
    page.block("Figures as reported on 23\u201324 November 2026. Weekend "
               "events are dated in the text. Drawn with Pillow — no "
               "network, no photograph.", face(SANS, 11), 14, colour=MUTED,
               centred=True)


def assemble():
    page = Page()
    header(page)
    lead_story(page)
    for index, pair in enumerate(GRID):
        story_row(page, pair)
        page.space(4)
        if index < len(GRID) - 1:
            page.rule(1, colour=RULE_GREY)
            page.space(4)
    brief_section(page, SHORTS)
    page.space(6)
    glance_box(page)
    colophon(page)
    print("content ends at y=%d of %d" % (page.cursor, SIDE))
    return page.sheet


def main():
    image = assemble()
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or
                   Path(__file__).resolve().parent)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    image.save(target, format="PNG", optimize=True)
    print("wrote %s (%d bytes)" % (target, target.stat().st_size))


if __name__ == "__main__":
    main()
