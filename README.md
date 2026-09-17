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

| Arquivo | Para que serve |
| --- | --- |
| `index.html` | A página. Template (`<x-dc>`) + lógica (`class Component extends DCLogic`). |
| `support.js` | Runtime do protótipo (dc-runtime). Compila o template e monta o componente; carrega React 18 do unpkg. **Sem ele a página fica em branco.** |
| `assets/Inter-*.ttf` | Fonte Inter (300/400/500/600), usada com o nome `InterW`. |
| `assets/*.png` | Artes da campanha: fundo da tela de mensagem, girassol, flor e o lockup de logos (`logos-white.png` na tela, `logos.png` é a variante escura, não usada hoje). |
| `.nojekyll` | Desliga o Jekyll no Pages — serve os arquivos como estão. |

`index.html` é o export do protótipo sem alterações, exceto por três linhas
somadas no `<head>`: `lang="pt-BR"`, `<title>` e `<meta name="description">`.
Ao reexportar, vale repor essas três.

## Rodar local

```bash
python -m http.server 8777
```

Depois abra http://127.0.0.1:8777/. Abrir o `index.html` com `file://` não
funciona — o runtime precisa de HTTP.

## Fora do repositório

O bundle original (`Aplicativo setembro amarelo.zip`) traz também uma pasta
`uploads/` com os materiais de origem: o mockup `SETEMBRO AMARELO - MOBILE.pdf`
e as artes em alta. São ~27 MB e não fazem falta para a página rodar, então
ficaram de fora daqui.
