// Monta img/mtw-pdf.webp (2560x1600): como abrir um PDF no Marca-texto Web.
// Usa as capturas pdf-popup.png (menu da extensão; no e-mail, o "an" foi trocado: fica só ***@gmail.com) e pdf-pagina.png (tela "Grife seus PDFs", sem a barra do Chrome, recortada no centro: x 250–1550, y 46–806 da captura de 1691x989).
// A janela de escolher arquivo é desenhada aqui (genérica, sem pastas reais do usuário).
// Uso (na raiz):  NODE_PATH=$(npm root -g) node src/capturas/pdf.js && python3 -c "from PIL import Image; Image.open('/tmp/mtw-pdf.png').convert('RGB').save('img/mtw-pdf.webp','WEBP',quality=85,method=6)"
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const uri = f => 'data:image/png;base64,' + fs.readFileSync(path.join(__dirname, f)).toString('base64');
const OUT = process.argv[2] || '/tmp/mtw-pdf.png';
const pdfIco = '<svg viewBox="0 0 20 24" width="18" height="22"><path d="M2 1h11l5 5v17H2z" fill="#fff" stroke="#C9CCD3"/><path d="M13 1v5h5" fill="none" stroke="#C9CCD3"/><rect x="0" y="12" width="14" height="7" rx="1.5" fill="#D93B30"/><text x="7" y="17.6" font-size="5.6" font-family="Arial" font-weight="700" fill="#fff" text-anchor="middle">PDF</text></svg>';
const html = `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
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
.pop{position:absolute;left:80px;top:150px;width:300px;border-radius:12px;overflow:hidden;border:1px solid #D2CEC8;box-shadow:0 24px 50px -24px rgba(70,50,0,.45)}
.pop img{display:block;width:100%}
.win{position:absolute;left:440px;top:150px;width:790px;border-radius:14px;overflow:hidden;background:#fff;border:1px solid #D2CEC8;box-shadow:0 24px 50px -24px rgba(70,50,0,.35)}
.bar{height:35px;background:#EDEDF0;display:flex;align-items:center;padding:0 14px;gap:7px;border-bottom:1px solid #DEDEE2}
.dot{width:11px;height:11px;border-radius:50%}
.url{margin-left:14px;height:22px;width:520px;border-radius:11px;background:#fff;display:flex;align-items:center;padding:0 12px;font:400 12.6px 'Instrument Sans';color:#505050}
.win img{display:block;width:100%}
.dlg{position:absolute;left:962px;top:455px;width:300px;border-radius:12px;background:#fff;border:1px solid #CFD3DA;box-shadow:0 30px 60px -20px rgba(20,30,60,.45);font-size:13px;color:#1F2937;overflow:hidden}
.dlg .t{padding:11px 16px;font-weight:600;border-bottom:1px solid #E5E7EB;background:#F7F8FA}
.dlg .path{padding:9px 16px;color:#6B7280;font-size:12px;border-bottom:1px solid #EEF0F3}
.dlg ul{list-style:none;margin:0;padding:6px}
.dlg li{display:flex;align-items:center;gap:10px;padding:7px 10px;border-radius:7px}
.dlg li.sel{background:#DCE7FF}
.dlg .bt{display:flex;justify-content:flex-end;gap:10px;padding:10px 16px 14px;border-top:1px solid #EEF0F3}
.dlg .b{padding:7px 18px;border-radius:7px;border:1px solid #CFD3DA;font-weight:600}
.dlg .b.p{background:#1E3A6E;border-color:#1E3A6E;color:#fff;position:relative}
.n{position:absolute;width:34px;height:34px;border-radius:50%;background:#1E3A6E;color:#fff;font:800 18px/30px 'Bricolage Grotesque';text-align:center;border:2px solid #F7D04A;box-shadow:0 6px 14px -6px rgba(0,0,0,.5);z-index:5}
.cur{position:absolute;width:22px;z-index:6}
</style></head><body>
<h1>Abra seus PDFs <mark>em poucos cliques</mark></h1>
<div class="sub">Ícone do Marca-texto → “Abrir PDF no Marca-texto” → escolha o arquivo no computador (ou arraste o PDF para a tela).</div>
<div class="logo"><svg viewBox="0 0 24 24" aria-hidden="true"><defs><clipPath id="cp"><rect x="3.4" y="3.4" width="17.2" height="17.2" rx="5.2"/></clipPath></defs><g transform="rotate(-14 12 12)"><g clip-path="url(#cp)"><rect x="3.4" y="3.4" width="17.2" height="17.2" fill="#FFB74D"/><polygon points="3.4,3.4 20.6,3.4 3.4,20.6" fill="#FFE066"/></g></g></svg>Marca-texto Web</div>
<div class="pop"><img src="${uri('pdf-popup.png')}" alt=""></div>
<div class="n" style="left:36px;top:${150 + 82 * 300 / 293 - 17}px">1</div>
<svg class="cur" style="left:${80 + 215 * 300 / 293}px;top:${150 + 88 * 300 / 293}px" viewBox="0 0 16 24"><path d="M1 1v19l5-5 3.5 7.5 3-1.4L9 13.8h7z" fill="#111" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/></svg>
<div class="win"><div class="bar"><span class="dot" style="background:#FA5E57"></span><span class="dot" style="background:#FBB42A"></span><span class="dot" style="background:#25C239"></span><div class="url">Marca-texto Web · Grife seus PDFs</div></div>
<img src="${uri('pdf-pagina.png')}" alt=""></div>
<div class="n" id="n2">2</div>
<div class="dlg"><div class="t">Abrir</div><div class="path">Documentos › Estudos</div>
<ul><li>${pdfIco}Apostila de Direito.pdf</li><li class="sel">${pdfIco}Edital do concurso.pdf</li><li>${pdfIco}Informativo STJ.pdf</li></ul>
<div class="bt"><span class="b">Cancelar</span><span class="b p">Abrir</span></div></div>
<div class="n" id="n3">3</div>
</body></html>`;
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 2 });
  const p = await ctx.newPage();
  await p.setContent(html, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  // números 2 e 3: ao lado do botão "Escolher PDF no computador" (posição na captura recortada) e do botão "Abrir"
  await p.evaluate(() => {
    const img = document.querySelector('.win img').getBoundingClientRect(), s = img.width / 1300;
    const n2 = document.getElementById('n2'); n2.style.left = (img.left + 576 * s - 44) + 'px'; n2.style.top = (img.top + 538 * s - 17) + 'px';
    const a = document.querySelector('.dlg .b.p').getBoundingClientRect(), n3 = document.getElementById('n3');
    n3.style.left = (a.left + a.width / 2 - 17) + 'px'; n3.style.top = (a.bottom + 14) + 'px';
  });
  await p.screenshot({ path: OUT }); await b.close();
})();
