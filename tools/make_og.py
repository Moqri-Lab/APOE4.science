"""Draw og.png, the link-preview image, into the repository root."""
import pathlib
from PIL import Image, ImageDraw, ImageFont

OUT = pathlib.Path(__file__).resolve().parent.parent / "og.png"
BG, INK, MUTED, E4 = "#f6f7f9", "#14181f", "#4a5260", "#b0234f"


def font(names, size):
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            pass
    return ImageFont.load_default()


serif = ["DejaVuSerif-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"]
sans = ["DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
mono = ["DejaVuSansMono-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"]

im = Image.new("RGB", (1200, 630), BG)
d = ImageDraw.Draw(im)
d.rectangle((0, 0, 1200, 12), fill=E4)
d.text((80, 70), "apoe", font=font(mono, 40), fill=INK)
x = 80 + d.textlength("apoe", font=font(mono, 40))
d.text((x, 70), "4", font=font(mono, 40), fill=E4)
x += d.textlength("4", font=font(mono, 40))
d.text((x, 70), ".science", font=font(mono, 40), fill=INK)
d.text((72, 170), "ε4/ε4", font=font(serif, 210), fill=E4)
d.text((80, 450), "A community resource on APOE ε4 homozygosity", font=font(sans, 40), fill=INK)
d.text((80, 510), "Evidence · Data resources · Papers · Trials · Drugs", font=font(sans, 32), fill=MUTED)
im.save(OUT)
print("wrote", OUT)
