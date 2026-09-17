# -*- coding: utf-8 -*-
"""Recomprime as artes da campanha para WebP e gera subsets woff2 da Inter.

Entrada: os arquivos originais do bundle (assets-src/).
Saida:   assets/*.webp e assets/*.woff2, que e o que a pagina carrega.
"""
import io, os, sys
from PIL import Image
from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

SRC, OUT = "assets-src", "assets"

# q85 + method 6: visualmente indistinguivel nestes tamanhos de exibicao,
# e a arte e decorativa (fica atras do conteudo, desfocada em parte).
IMAGES = {
    "flor.png":        dict(quality=85, method=6),
    "girassol.png":    dict(quality=85, method=6),
    "bg-mensagem.png": dict(quality=85, method=6),
    "logos-white.png": dict(lossless=True, method=6),  # logo chapado: lossless sai menor
    "logos.png":       dict(lossless=True, method=6),
}

FONTS = ["Inter-Light.ttf", "Inter-Regular.ttf", "Inter-Medium.ttf", "Inter-SemiBold.ttf"]


def charset():
    """Latim completo + pontuacao + setas, mais tudo que o index.html ja usa.

    Latin-1 e Latin Extended-A entram inteiros de proposito: o campo de nome
    e digitado pelo usuario, entao nao da para subsetar so pelo texto fixo.
    """
    cps = set()
    cps |= set(range(0x0020, 0x007F))   # ASCII
    cps |= set(range(0x00A0, 0x0100))   # Latin-1 Supplement
    cps |= set(range(0x0100, 0x0180))   # Latin Extended-A
    cps |= set(range(0x2010, 0x2028))   # travessoes, aspas tipograficas, reticencias
    cps |= set(range(0x2030, 0x205F))   # ‰ ‹ › etc.
    cps |= set(range(0x2190, 0x2200))   # setas: → ↗ ⟳ ...
    with open("index.html", encoding="utf-8") as f:
        cps |= {ord(c) for c in f.read()}
    return cps


def main():
    if not os.path.isdir(SRC):
        sys.exit(f"falta a pasta {SRC}/ com os originais do bundle")
    before = after = 0

    for name, opts in IMAGES.items():
        src = os.path.join(SRC, name)
        dst = os.path.join(OUT, os.path.splitext(name)[0] + ".webp")
        im = Image.open(src).convert("RGBA")
        im.save(dst, "WEBP", **opts)
        b, a = os.path.getsize(src), os.path.getsize(dst)
        before += b; after += a
        print(f"{name:18} {b/1024:8.1f} KB -> {a/1024:7.1f} KB  ({100-a*100//b:2d}% menor)")

    cps = charset()
    for name in FONTS:
        src = os.path.join(SRC, name)
        dst = os.path.join(OUT, os.path.splitext(name)[0] + ".woff2")
        font = TTFont(src)
        o = Options()
        o.flavor = "woff2"
        o.desubroutinize = True
        o.layout_features = ["kern", "liga", "calt", "ccmp", "locl", "mark", "mkmk"]
        o.name_IDs = ["*"]
        o.notdef_outline = True
        s = Subsetter(options=o)
        s.populate(unicodes=cps)
        s.subset(font)
        font.flavor = "woff2"
        font.save(dst)
        font.close()
        b, a = os.path.getsize(src), os.path.getsize(dst)
        before += b; after += a
        print(f"{name:18} {b/1024:8.1f} KB -> {a/1024:7.1f} KB  ({100-a*100//b:2d}% menor)")

    print(f"\nTOTAL              {before/1024:8.1f} KB -> {after/1024:7.1f} KB"
          f"  ({100-after*100//before}% menor)")


if __name__ == "__main__":
    main()
