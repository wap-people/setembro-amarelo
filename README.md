# Setembro Amarelo — WAP

Página da campanha Setembro Amarelo: o visitante escolhe o que precisa hoje,
recebe uma mensagem de cuidado (com link para compartilhar e opção de salvar
como imagem), vê boas práticas de bem-estar e pode abrir o formulário de adesão
ao Zenklub.

No ar em: **https://wap-people.github.io/setembro-amarelo/**

## Quem publica

O Pages está em **Deploy from a branch** → `main`, pasta `/ (root)`. Não há
build nem GitHub Actions: **um push na `main` republica o site sozinho em ~1
minuto**. Na prática, quem tem permissão de escrita no repositório publica.

| Permissão | Dá para |
| --- | --- |
| **Write** | Editar, commitar, dar push — ou seja, publicar. Cobre o dia a dia. |
| **Admin** | Tudo acima, mais `Settings` (inclusive religar o Pages se alguém desligar) e dar acesso a outras pessoas. |

Convém mais de uma pessoa com **Admin**. Com Write, a campanha continua no ar
e atualizável, mas qualquer coisa em `Settings` volta a depender de uma pessoa
só — que é justamente o que se quer evitar numa campanha com data marcada.

Acesso se dá em `Settings` → `Collaborators and teams`. Numa org, preferir um
**time** a colaborador avulso: entra e sai gente pelo time, e o desligamento
de alguém não deixa acesso solto para trás.

## Primeira vez na máquina

```bash
git clone https://github.com/wap-people/setembro-amarelo.git
cd setembro-amarelo
pip install Pillow "fonttools[woff]" brotli   # só para os scripts de tools/
```

Para ver rodando local:

```bash
python -m http.server 8777
```

e abrir http://127.0.0.1:8777/. **Abrir o `index.html` com duplo clique não
funciona** — o runtime precisa de HTTP, pelo `file://` a página fica em branco.

## O ciclo completo, do export ao ar

1. Exportar o protótipo do dc (vem um `.zip`).
2. Conferir se as artes mudaram: comparar o `assets/` do zip com o
   `assets-src/` daqui. Nas duas últimas vezes só o HTML tinha mudado.
3. Se mudaram, substituir os originais em `assets-src/`.
4. ```bash
   python tools/apply-export.py "caminho/Setembro Amarelo.dc.html"
   python tools/optimize.py
   ```
5. Testar local (ver o checklist abaixo).
6. `git add -A && git commit && git push` — pronto, está no ar.
7. Abrir https://wap-people.github.io/setembro-amarelo/ com `?x=1` no fim da
   URL, para furar cache, e conferir.

### Checklist antes do push

- As três telas: menu, mensagem, boas práticas.
- O sheet "Enviar para alguém", e o **Salvar imagem** de fato gerando o PNG —
  é o caminho mais frágil, porque desenha as artes num canvas.
- Larguras 320, 375 e 430 px, sem barra de rolagem horizontal.
- Console sem 404. Se aparecer `.ttf` ou `.png` sendo pedido, o
  `apply-export.py` não rodou.

### Se a página abrir em branco

Quase sempre é o `support.js`: sem ele nada renderiza e **não aparece erro na
tela**, só no console. Conferir se o arquivo está na raiz e se o `<head>` do
`index.html` ainda o carrega.

## Estrutura

| Caminho | Para que serve |
| --- | --- |
| `index.html` | A página. Template (`<x-dc>`) + lógica (`class Component extends DCLogic`). |
| `support.js` | Runtime do protótipo (dc-runtime). Compila o template e monta o componente. **Sem ele a página fica em branco.** |
| `vendor/react*.js` | React 18.3.1 UMD, servido da mesma origem (ver abaixo). |
| `assets/*.woff2` | Inter 300/400/500/600, subsetada, usada com o nome `InterW`. |
| `assets/*.webp` | Artes da campanha. |
| `assets-src/` | O bundle cru: o export `.dc.html` como saiu do dc, e as artes/fontes em PNG e TTF. Nada aqui é servido na página — é a entrada dos scripts de `tools/`, e o que permite diferenciar um export novo do anterior. **Não edite o `.dc.html` daqui esperando ver mudança no site**; quem vai pro ar é o `index.html` da raiz. |
| `tools/apply-export.py` | Reaplica as mudanças da publicação sobre um export novo do dc. |
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

Os scripts de `tools/` precisam de:

```bash
pip install Pillow "fonttools[woff]" brotli
```

## Por que os scripts existem

O export do dc sempre volta pedindo `.ttf` e `.png` e buscando o React no
unpkg — ou seja, desfazendo a otimização a cada reexportação. Em vez de
repor as quatro mudanças na mão toda vez, o `tools/apply-export.py` reaplica
todas por cima do export cru, e o `tools/optimize.py` regenera `assets/`.

Os dois são idempotentes: rodar de novo não estraga nada. E o
`apply-export.py` **aborta** se sobrar referência a `.ttf`, `.png` ou ao
unpkg — se o formato do export mudar a ponto de ele não achar onde encaixar,
ele avisa em vez de gerar uma página quebrada e silenciosamente pesada.

## Fora do repositório

O bundle original (`Aplicativo setembro amarelo.zip`) traz também uma pasta
`uploads/` com os materiais de origem: o mockup `SETEMBRO AMARELO - MOBILE.pdf`
e as artes em alta. São ~27 MB e não fazem falta para a página rodar, então
ficaram de fora daqui.
