# Setembro Amarelo — WAP

Página da campanha Setembro Amarelo: o visitante escolhe o que precisa hoje,
recebe uma mensagem de cuidado (com link para compartilhar e opção de salvar
como imagem), vê boas práticas de bem-estar e pode abrir o formulário de adesão
ao Zenklub.

Publicado em: **https://wap-people.github.io/setembro-amarelo/**

## Como publicar no GitHub Pages

1. `Settings` → `Pages`
2. **Source**: `Deploy from a branch`
3. **Branch**: `main`, pasta `/ (root)` → `Save`
4. Aguarde ~1 minuto e acesse a URL acima.

Não é preciso build: é HTML estático puro.

## Estrutura

| Arquivo | Para que serve |
| --- | --- |
| `index.html` | A página. Template (`<x-dc>`) + lógica (`class Component extends DCLogic`). |
| `support.js` | Runtime do protótipo (dc-runtime). Compila o template e monta o componente; carrega React 18 do unpkg. **Sem ele a página fica em branco.** |
| `assets/Inter-*.ttf` | Fonte Inter (400/500/600) usada como `InterW`. |
| `.nojekyll` | Desliga o Jekyll no Pages — serve os arquivos como estão. |

## Artes pendentes

Estes quatro PNGs são referenciados pelo `index.html` e **ainda não estão no
repositório** (não vieram no export). Enquanto faltarem, um `onerror` no
`<head>` esconde a imagem em vez de mostrar o ícone de erro do navegador — a
página funciona, mas sem a arte de fundo e sem o logo:

- `assets/bg-mensagem.png` — fundo da tela de mensagem (cover, tela inteira)
- `assets/girassol.png` — girassol grande do canto inferior direito
- `assets/flor.png` — florzinha usada em vários cantos
- `assets/logos-white.png` — lockup Wap · WAAW by Alok · freso (versão branca)

Basta commitar os quatro em `assets/` com esses nomes. Nada mais precisa mudar.

## Rodar local

```bash
python -m http.server 8777
```

Depois abra http://127.0.0.1:8777/. Abrir o `index.html` com `file://` não
funciona — o runtime precisa de HTTP.
