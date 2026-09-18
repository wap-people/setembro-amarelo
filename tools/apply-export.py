# -*- coding: utf-8 -*-
"""Transforma o export cru do dc no index.html que vai pro Pages.

Uso:  python tools/apply-export.py "caminho/Setembro Amarelo.dc.html"

O export vem pedindo .ttf e .png e buscando o React no unpkg. Este script
reaplica, de forma idempotente, tudo o que a pagina publicada precisa. Rode
o tools/optimize.py depois, para (re)gerar assets/ a partir de assets-src/.
"""
import io, os, re, shutil, sys

DEST = "index.html"

HEAD = '''<link rel="preload" href="assets/Inter-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/Inter-Medium.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/Inter-SemiBold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/Inter-Light.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="vendor/react.production.min.js" as="script">
<link rel="preload" href="vendor/react-dom.production.min.js" as="script">
<script>
// O dc-runtime busca o React no unpkg, e so depois de ele proprio carregar.
// window.__resources e o gancho dele para trocar a URL: servindo da mesma
// origem, os dois baixam em paralelo com o support.js, sem DNS/TLS para
// terceiro. De quebra, definir __resources desliga o refetch de location.href
// que o runtime faz para atualizar o template (ver support.js, funcao boot) —
// aqui isso so rebaixava o HTML inteiro de novo, sem serventia.
window.__resources = {
  "https://unpkg.com/react@18.3.1/umd/react.production.min.js": "vendor/react.production.min.js",
  "https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js": "vendor/react-dom.production.min.js"
};
</script>
<script defer src="./support.js"></script>'''

TITLE = '<title>Setembro Amarelo · WAP</title>'
DESC = ('<meta name="description" content="Campanha Setembro Amarelo da WAP: '
        'escolha uma mensagem de cuidado, compartilhe e conheça boas práticas '
        'de bem-estar.">')

IMAGES = ("bg-mensagem", "girassol", "flor", "logos-white", "logos")


def main(src):
    s = io.open(src, encoding="utf-8").read()
    feito = []

    # 1. idioma
    if re.search(r"<html(?:\s[^>]*)?>", s) and 'lang=' not in s.split(">", 2)[1]:
        s = re.sub(r"<html>", '<html lang="pt-BR">', s, count=1)
        feito.append('lang="pt-BR"')

    # 2. title + description, logo depois do <script> do runtime
    if "<title>" not in s:
        s = s.replace("</head>", f"{TITLE}\n{DESC}\n</head>", 1)
        feito.append("title + description")

    # 3. preload, React local e defer — substitui a tag crua do runtime
    if "__resources" not in s:
        alvo = '<script src="./support.js"></script>'
        if alvo not in s:
            sys.exit(f"nao achei {alvo!r} no export; o formato mudou, revisar a mao")
        s = s.replace(alvo, HEAD, 1)
        feito.append("preload + React local + defer")

    # 4. extensoes otimizadas (tags <img> e as chamadas load() do saveImage)
    if ".ttf" in s or any(f"{n}.png" in s for n in IMAGES):
        s = s.replace('.ttf") format("truetype")', '.woff2") format("woff2")')
        for n in IMAGES:
            s = s.replace(f"assets/{n}.png", f"assets/{n}.webp")
        feito.append("woff2 + webp")

    sobrou = re.findall(r"assets/[\w-]+\.(?:ttf|png)", s)
    if sobrou:
        sys.exit(f"sobrou referencia nao otimizada: {sorted(set(sobrou))}")
    # As URLs do unpkg aparecem so como chave do mapa __resources, que e o
    # jeito de apontar para longe delas. Carregar de la, nao.
    if re.search(r"""src\s*=\s*["']https://unpkg""", s):
        sys.exit("o HTML ainda carrega algo direto do unpkg")

    if os.path.exists(DEST):
        shutil.copy(DEST, DEST + ".bak")
    io.open(DEST, "w", encoding="utf-8", newline="\n").write(s)
    print(f"{DEST} gerado de {src}")
    for f in feito:
        print("  aplicado:", f)
    print("\nAgora rode: python tools/optimize.py")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
