// Compõe título + logo + moldura de navegador + captura e salva PNG 2560x1600 (chamado por gerar.py)
const { chromium } = require('playwright');
const path = require('path');
const TELAS = {
  sumario: { titulo: 'Sumário navegável <mark>nas leis do Planalto</mark>', sub: 'Livros, títulos, capítulos e artigos ao lado do texto — e um “você está em” que acompanha a leitura.' },
  busca:   { titulo: 'Ache qualquer artigo <mark>em segundos</mark>', sub: 'Busque pelo número (1.238, 44-A) ou por palavra (promessa de fato) e vá direto ao dispositivo.' },
  margens: { titulo: 'Leia do seu jeito: <mark>3 margens</mark>', sub: 'Estreita, Normal ou Larga — e a mesma margem vale na hora de imprimir em A4.' },
};
const html = (t, img, cw, ch) => `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=Instrument+Sans:wght@400..700&display=swap">
<style>
*{box-sizing:border-box}
body{margin:0;width:1280px;height:800px;overflow:hidden;position:relative;font-family:'Instrument Sans',system-ui,sans-serif;
  background:radial-gradient(760px 300px at 100% 0%,#FFF2C9 0%,rgba(255,242,201,0) 100%),linear-gradient(180deg,#FAF5EA 0%,#F9F4EA 100%)}
h1{position:absolute;left:50px;top:22px;margin:0;font:800 37.1px/1.15 'Bricolage Grotesque';letter-spacing:-.025em;color:#1B2B4B;white-space:nowrap}
h1 mark{background:linear-gradient(transparent 52%,#FDE27D 52%,#FDE27D 94%,transparent 94%);color:inherit;padding:0 6px;margin:0 -6px}
.sub{position:absolute;left:50px;top:72px;font:400 17.5px/1.3 'Instrument Sans';color:#4E5566;white-space:nowrap}
.logo{position:absolute;right:50px;top:34px;display:flex;align-items:center;gap:9px;font:700 15.5px 'Bricolage Grotesque';letter-spacing:-.01em;color:#14213D}
.logo svg{width:20px;height:20px;display:block}
.win{position:absolute;left:${50 + (1180 - (cw + 2)) / 2}px;top:140px;width:${cw + 2}px;border-radius:14px;overflow:hidden;background:#fff;border:1px solid #D2CEC8;box-shadow:0 24px 50px -24px rgba(70,50,0,.35)}
.bar{height:35px;background:#EDEDF0;display:flex;align-items:center;padding:0 14px;gap:7px;border-bottom:1px solid #DEDEE2}
.dot{width:11px;height:11px;border-radius:50%}
.url{margin-left:14px;height:22px;width:640px;border-radius:11px;background:#fff;display:flex;align-items:center;gap:7px;padding:0 12px;font:400 12.6px 'Instrument Sans';color:#505050}
.url svg{width:10px;height:11px}
.shot{display:block;width:${cw}px;height:${ch}px}
</style></head><body>
<h1>${t.titulo}</h1><div class="sub">${t.sub}</div>
<div class="logo"><svg viewBox="0 0 24 24" aria-hidden="true"><defs><clipPath id="cp"><rect x="3.4" y="3.4" width="17.2" height="17.2" rx="5.2"/></clipPath></defs><g transform="rotate(-14 12 12)"><g clip-path="url(#cp)"><rect x="3.4" y="3.4" width="17.2" height="17.2" fill="#FFB74D"/><polygon points="3.4,3.4 20.6,3.4 3.4,20.6" fill="#FFE066"/></g></g></svg>Marca-texto Web</div>
<div class="win"><div class="bar"><span class="dot" style="background:#FA5E57"></span><span class="dot" style="background:#FBB42A"></span><span class="dot" style="background:#25C239"></span>
<div class="url"><svg viewBox="0 0 10 11" fill="#6B6B6B"><path d="M5 0a2.6 2.6 0 0 0-2.6 2.6V4H1.6C1 4 .5 4.5.5 5.1v4.3c0 .6.5 1.1 1.1 1.1h6.8c.6 0 1.1-.5 1.1-1.1V5.1C9.5 4.5 9 4 8.4 4h-.8V2.6A2.6 2.6 0 0 0 5 0zm-1.4 4V2.6a1.4 1.4 0 0 1 2.8 0V4H3.6z"/></svg>planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm</div></div>
<img class="shot" src="${img}" alt=""></div>
</body></html>`;

(async () => {
  const dir = process.argv[2];                       // pasta de trabalho (recebida de gerar.py)
  const quais = process.argv.slice(3).length ? process.argv.slice(3) : Object.keys(TELAS);
  const browser = await chromium.launch();
  for (const nome of quais) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 2 });
    const page = await ctx.newPage();
    const arq = path.join(dir, `prep-${nome}.png`);
    const buf = require('fs').readFileSync(arq);
    const cw = buf.readUInt32BE(16) / 2, ch = buf.readUInt32BE(20) / 2;   // tamanho da captura em px CSS (o canvas é 2x)
    const uri = 'data:image/png;base64,' + buf.toString('base64');
    await page.setContent(html(TELAS[nome], uri, cw, ch), { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(400);
    // largura real do título e do subtítulo (para conferir contra as imagens antigas)
    const med = await page.evaluate(() => { const r = s => { const e = document.querySelector(s); const b = e.getBoundingClientRect(); return Math.round(b.width); }; return { titulo: r('h1'), sub: r('.sub') }; });
    await page.screenshot({ path: path.join(dir, `novo-${nome}.png`) });
    console.log(nome, 'medidas CSS px', JSON.stringify(med));
    await ctx.close();
  }
  await browser.close();
})();
