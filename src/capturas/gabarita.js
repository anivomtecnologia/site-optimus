// Monta img/gab-questao.webp (2560x1600): exemplo de questão do gabaritaPDF (Certo ou Errado com gabarito e trecho do material).
// Desenho em HTML (não é captura da tela), com o exemplo do próprio "Como usar" do gabaritaPDF (métodos de interpretação da Constituição).
// Uso (na raiz):  NODE_PATH=$(npm root -g) node src/capturas/gabarita.js /tmp/gab.png
//   e depois:     python3 -c "from PIL import Image; Image.open('/tmp/gab.png').convert('RGB').save('img/gab-questao.webp','WEBP',quality=88,method=6)"
const { chromium } = require('playwright');
const OUT = process.argv[2] || '/tmp/gab.png';
const html = `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,600;0,700;1,600;1,700&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap">
<style>
*{box-sizing:border-box}
body{margin:0;width:1280px;height:800px;overflow:hidden;font-family:'Instrument Sans',sans-serif;color:#242120;
  background:radial-gradient(700px 320px at 100% 0%,#F3E3E6 0%,rgba(243,227,230,0) 100%),#F8F5EE;position:relative}
.bar{position:absolute;left:0;top:0;bottom:0;width:14px;background:#6E1A2B}
.brand{position:absolute;left:64px;top:44px;font:700 30px 'Lora',serif;letter-spacing:-.01em}.brand i{color:#6E1A2B;font-style:italic}
.crumb{position:absolute;right:64px;top:52px;font:500 15px 'JetBrains Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#7A6E66}
.card{position:absolute;left:64px;right:64px;top:150px;background:#fff;border:1px solid #E7DED2;border-radius:24px;box-shadow:0 30px 60px -30px rgba(80,30,40,.35);padding:38px 46px;display:grid;gap:22px;align-content:start}
.tag{display:flex;gap:10px;align-items:center;font:600 14px 'JetBrains Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:#6E1A2B}
.tag span{background:#F4ECEE;border:1px solid #E5CDD2;border-radius:999px;padding:6px 12px}
.q{font:600 29px/1.38 'Lora',serif;color:#242120;max-width:1040px}
.opts{display:flex;gap:14px}
.o{font:600 19px 'Instrument Sans';padding:12px 26px;border-radius:14px;border:1.5px solid #E1D7CB;color:#4A3F35;background:#FBF8F3}
.o.ok{background:#6E1A2B;border-color:#6E1A2B;color:#fff}
.res{display:grid;grid-template-columns:auto 1fr;gap:12px 18px;align-items:start;background:#FBF8F3;border:1px solid #EFE6DA;border-radius:18px;padding:22px 26px}
.gab{font:700 17px 'JetBrains Mono',monospace;color:#6E1A2B;letter-spacing:.04em;text-transform:uppercase;padding-top:3px}
.why{font:400 20px/1.5 'Instrument Sans';color:#3B342F}
.why b{font-weight:600;color:#242120}
.src{grid-column:1/-1;border-left:5px solid #6E1A2B;background:#fff;border-radius:10px;padding:14px 18px;font:400 19px/1.5 'Lora',serif;font-style:italic;color:#3B342F}
.src mark{background:linear-gradient(transparent 55%,#F6E27A 55%,#F6E27A 92%,transparent 92%);color:inherit}
.src small{display:block;font:600 13px 'JetBrains Mono',monospace;font-style:normal;letter-spacing:.08em;text-transform:uppercase;color:#7A6E66;margin-bottom:6px}
</style></head><body>
<div class="bar"></div>
<div class="brand">gabarita<i>PDF</i></div>
<div class="crumb">Direito Constitucional · Interpretação</div>
<div class="card">
  <div class="tag"><span>Questão 3</span><span>Certo ou Errado</span></div>
  <div class="q">No método tópico-problemático, a interpretação parte da norma constitucional para o problema concreto.</div>
  <div class="opts"><span class="o">Certo</span><span class="o ok">Errado ✓</span></div>
  <div class="res">
    <span class="gab">Gabarito: Errado</span>
    <div class="why"><b>Por quê:</b> no método tópico-problemático, parte-se do <b>problema concreto para a norma</b> (método indutivo). Partir da norma para o problema é o caminho do método hermenêutico-concretizador.</div>
    <div class="src"><small>Trecho do seu material</small>“Do problema concreto para a norma (<mark>método indutivo</mark>), com a Constituição como sistema aberto e a escolha dos topoi.”</div>
  </div>
</div>
</body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 2 })).newPage();
  await p.setContent(html, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  await p.screenshot({ path: OUT }); await b.close();
})();
