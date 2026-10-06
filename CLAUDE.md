# CLAUDE.md: site da Optimus Aprendizado

Instruções para o Claude (Claude Code) trabalhar neste repositório. Leia antes de qualquer mudança.

## O que é

Site institucional da **Optimus Aprendizado**, marca da **ANIVOM TECNOLOGIA LTDA** (CNPJ 69.199.407/0001-96). Funciona como vitrine das ferramentas de estudo da empresa. A primeira ferramenta publicada é o **Marca-texto Web**, uma extensão do Chrome para grifar e organizar estudos. Outras virão, por exemplo o Gabarita PDF (gabaritapdf.com.br).

- No ar em **https://www.optimusaprendizado.com.br**. O endereço sem `www` redireciona para ele.
- Hospedagem: **Vercel**, time "Optimus Aprendizado", projeto `site-optimus`, ligado à branch `main` deste repositório. Todo push na `main` é publicado sozinho em 1 ou 2 minutos.
- Site 100% estático, sem framework e sem build na Vercel. Os arquivos da raiz são servidos como estão.

## Estrutura

```
index.html                         GERADO: site completo (imagens e página do Marca-texto embutidas)
marca-texto-web.html               FONTE e página avulsa do Marca-texto Web (também é servida)
privacidade-marca-texto-web.html   GERADO: Política de Privacidade avulsa (URL usada na Chrome Web Store)
termos-marca-texto-web.html        GERADO: Termos de Uso avulsos
img/                               imagens .webp (galeria 1280x800 e prints dos post-its)
src/optimus-aprendizado.fonte.html FONTE da página principal
src/docs/                          FONTE dos textos: privacidade.html, termos.html, ajuda.html
src/head.html                      FONTE do <head> do index.html (title, description, og, favicon)
src/build.py                       monta tudo (só usa a biblioteca padrão do Python)
src/check.py                       conferência rápida (ids, âncoras, labels, imagens)
.vercelignore                      impede que src/, CLAUDE.md e README.md sejam publicados
```

## Como fazer uma mudança

1. Edite **só as fontes**: `src/optimus-aprendizado.fonte.html`, `marca-texto-web.html`, `src/docs/*.html`, `src/head.html` ou `img/`.
   - **Nunca edite `index.html` à mão.** Ele é sobrescrito pelo build.
   - Em `marca-texto-web.html`, os trechos entre `<!--HELP-->…<!--/HELP-->`, `<!--DOCS-->…<!--/DOCS-->` e `/*DOCCSS*/…/*/DOCCSS*/` são gerados a partir de `src/docs/`. Edite os textos em `src/docs/`, não ali.
2. Rode `python3 src/build.py` e depois `python3 src/check.py`.
3. Se possível, abra `index.html` num navegador, por exemplo com Playwright, e confira no computador e no celular (390px). Teste também **com JavaScript desligado**.
4. Faça o commit **das fontes e dos arquivos gerados juntos** e dê push na `main`.

## Regras técnicas (aprendidas na prática, não quebrar)

- **Tudo que é essencial funciona sem JavaScript.** No navegador do dono do site, o JavaScript chegou a não rodar. Por isso:
  - A página do Marca-texto Web abre **dentro do site** por um checkbox oculto (`#mtw-open`) e `label for="mtw-open"`. O CSS é `.mtw-cb:checked + .product-panel{display:block}`. Não usar `:target`, Shadow DOM, `fetch` nem `<template>` para isso.
  - A galeria de 4 abas usa radios (`.m-gr`) e labels. O zoom das fotos dos post-its usa checkbox (`.zcb`), e Ajuda, Privacidade e Termos também (`.dcb`).
  - As animações (o topo "ruído → foco", "Uma hora de estudo, dois jeitos" e o marca-texto azul animado da missão) são **só CSS**.
  - O JavaScript existe apenas como melhoria: botões Ruído/Foco, tecla Esc, palavras da missão acendendo na rolagem, copiar e-mail.
- **Animações com `prefers-reduced-motion`:** as seções com classe `km` (hero, "Uma hora de estudo" e a frase da missão) continuam animando de propósito, porque são lentas e decorativas. O resto respeita a preferência.
- **Nunca deixe a sequência `</` dentro do `<script>`.** O build já escapa para `<\/`, mas não reintroduza na mão. Um `</body>` dentro de string chegou a cortar o script inteiro.
- A página do Marca-texto embutida no `index.html` tem o CSS escopado em `#marca-texto`, classes com prefixo `m-` e ids com prefixo `mtw-`. Quem faz isso é o build: escreva a fonte com nomes normais.
- Fontes (Google Fonts): Bricolage Grotesque (títulos), Instrument Sans (texto) e JetBrains Mono (rótulos).

## Identidade visual

- **Site da Optimus:** azul `#2B5BD7`, cinza `#626A7A`, off-white `#F4F5F7`, texto `#15192B`, azul-claro de grifo `#C4D6FF`. Tem modo escuro (tokens em `:root`). O visual deve ser sóbrio e tecnológico, nunca infantil, e sem cores demais.
- **Logo:** um "O" em traço com um ponto azul no alto à direita, seguido de "Optimus" e "Aprendizado".
- **Amarelo é exclusivo do Marca-texto Web**: `#F2C230` e `#F7D04A`, com azul-marinho `#1E3A6E`. Não usar amarelo no restante do site.
- Post-it do **STF em azul** e do **STJ em verde**, como na extensão.

## Decisões de conteúdo já tomadas pelo dono

- Missão: "Facilitar o processo de **aprendizagem**, para que **seu tempo de estudo renda mais**…" A frase em negrito tem o marca-texto azul animado.
- Público ("Para"): estudantes · quem aprende ao longo da vida · concurseiros · vestibulandos · professores.
- Lista do topo: Objetivo claro, Fonte confiável, Prática ativa, Métodos que funcionam, Progresso visível.
- Removidos a pedido do dono: seção "Como pensamos o aprendizado", selo "NOVO" e Instagram no rodapé do site principal (ele fica só no Marca-texto).
- E-mails: **educa@optimusaprendizado.com** (site) e **marcatextoweb@optimusaprendizado.com** (suporte do Marca-texto). Atenção: os e-mails são `.com`, e o site é `.com.br`.
- Termos de Uso **sem** seção de direito de arrependimento, por escolha do dono. A Política de Privacidade **não** nomeia encarregado (DPO).
- Preços do Marca-texto Web: teste de 48h; R$ 9,90/mês; R$ 89,90/ano. O pagamento é feito via ExtensionPay/Stripe, e as marcações ficam só no navegador do usuário.
- Tom: direto, prático, sem jargão, em português do Brasil.

## Pendências

- [ ] Trocar os 3 links "Testar grátis" e "Começar o teste grátis" (hoje `https://chromewebstore.google.com/search/Marca-texto%20Web`) pelo link real da extensão na Chrome Web Store.
- [ ] Revisão jurídica da Política de Privacidade e dos Termos de Uso.
- [ ] Quando o Gabarita PDF puder ser divulgado, adicionar um card na seção "Uma ferramenta para cada área de estudo".
- [ ] Opcional: limpar CSS sem uso na fonte (blocos `/* MÉTODO */` e `/* FUNDADOR */`, de seções que foram removidas).

## Domínio e DNS (Registro.br): não mexer sem necessidade

DNS do Registro.br, em modo avançado:

- `A` `optimusaprendizado.com.br` → `216.198.79.1`
- `A` `www.optimusaprendizado.com.br` → `216.198.79.1`
- `TXT` `www.optimusaprendizado.com.br` → `anthropic-domain-verification-…` **NUNCA APAGAR**. Por causa dele, o `www` usa registro A em vez de CNAME.
