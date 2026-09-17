# Setembro Amarelo — WAP

Página da campanha Setembro Amarelo: o visitante escolhe o que precisa hoje,
recebe uma mensagem de cuidado (com link para compartilhar e opção de salvar
como imagem), vê boas práticas de bem-estar e pode abrir o formulário de adesão
ao Zenklub.

No ar em: **https://wap-people.github.io/setembro-amarelo/**

## Como publicar no GitHub Pages

1. `Settings` → `Pages`
2. **Source**: `Deploy from a branch`
3. **Branch**: `main`, pasta `/ (root)` → `Save`

Não é preciso build: é HTML estático puro. Um push na `main` republica sozinho
em ~1 minuto.

## Estrutura

| Caminho | Para que serve |
| --- | --- |
| `index.html` | A página. Template (`<x-dc>`) + lógica (`class Component extends DCLogic`). |
| `support.js` | Runtime do protótipo (dc-runtime). Compila o template e monta o componente. **Sem ele a página fica em branco.** |
| `vendor/react*.js` | React 18.3.1 UMD, servido da mesma origem (ver abaixo). |
| `assets/*.woff2` | Inter 300/400/500/600, subsetada, usada com o nome `InterW`. |
| `assets/*.webp` | Artes da campanha. |
| `assets-src/` | Os originais do bundle (PNG e TTF). Não são servidos na página; existem para dar de comer ao `tools/optimize.py`. |
| `tools/optimize.py` | Gera `assets/` a partir de `assets-src/`. |
| `.nojekyll` | Desliga o Jekyll no Pages — serve os arquivos como estão. |

## Peso da página

A primeira versão publicada baixava **3,0 MB** e a arte grande (`flor.png`,
1,4 MB sozinha) monopolizava a banda. Hoje a mesma página baixa **~570 KB**,
sem mudar nada do visual:

| | Antes | Depois |
| --- | ---: | ---: |
| Artes | 2,5 MB PNG | 275 KB WebP |
| Fontes | 1,34 MB TTF | 86 KB WOFF2 subsetado |
| React | unpkg, em série | mesma origem, em paralelo |
| Requisições | 12 | 11 |

O que foi feito:

- **PNG → WebP** com qualidade 85 (`logos*` em lossless, que sai menor por ser
  arte chapada). As dimensões não mudaram.
- **TTF → WOFF2 subsetado**: Latin-1 + Latin Extended-A + pontuação + setas.
  Latin inteiro entra de propósito, porque o campo de nome é digitado pelo
  usuário e não dá para subsetar pelo texto fixo.
- **`<link rel="preload">`** das fontes e do React, para saírem junto com o
  `support.js` em vez de depois dele.
- **React servido daqui**, via `window.__resources` — o gancho do próprio
  dc-runtime para trocar a URL do CDN. Isso também desliga um refetch de
  `location.href` que o runtime faz quando `__resources` não está definido, e
  que só rebaixava o HTML inteiro sem serventia.
- **`defer`** no `support.js`. O runtime já trata os dois casos (`readyState`
  ou `DOMContentLoaded`), então é seguro.

Os arquivos em `vendor/` foram conferidos contra os hashes SRI que o próprio
`support.js` carrega para essas URLs.

### Mexeu nas artes ou nas fontes?

Ponha os originais em `assets-src/` e rode:

```bash
pip install Pillow "fonttools[woff]" brotli
python tools/optimize.py
```

## Rodar local

```bash
python -m http.server 8777
```

Depois abra http://127.0.0.1:8777/. Abrir o `index.html` com `file://` não
funciona — o runtime precisa de HTTP.

## Se reexportar o protótipo

O `index.html` é o export do dc, com estas mudanças por cima. Reexportando,
é preciso repor:

1. `lang="pt-BR"`, `<title>` e `<meta name="description">` no `<head>`
2. o bloco de `<link rel="preload">` e o `window.__resources`
3. `defer` no `<script src="./support.js">`
4. as extensões: `.ttf` → `.woff2` e `.png` → `.webp` (nas tags `<img>` **e**
   nas chamadas `load()` dentro do `saveImage`)

## Fora do repositório

O bundle original (`Aplicativo setembro amarelo.zip`) traz também uma pasta
`uploads/` com os materiais de origem: o mockup `SETEMBRO AMARELO - MOBILE.pdf`
e as artes em alta. São ~27 MB e não fazem falta para a página rodar, então
ficaram de fora daqui.
