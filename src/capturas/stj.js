// Monta img/mtw-postit-stj.webp (2000x1310, mesma proporção e escala da foto do STF): art. 50 do Código Civil inteiro, como no Planalto, com o post-it verde do STJ ao lado.
// O texto do artigo é redesenhado (o print original cortava a lei); o post-it é recortado do print da extensão (stj-postit.png).
// Uso (na raiz): NODE_PATH=$(npm root -g) node src/capturas/stj.js /tmp/stj.png  e depois converter para webp.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const OUT = process.argv[2] || '/tmp/stj.png';
const post = 'data:image/png;base64,' + fs.readFileSync(path.join(__dirname, 'stj-postit.png')).toString('base64');
const html = `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>
*{box-sizing:border-box}
body{margin:0;width:2000px;height:1310px;background:#fff;font-family:Arial,"Liberation Sans",Helvetica,sans-serif;color:#000;position:relative;overflow:hidden}
.txt{position:absolute;left:70px;top:70px;width:1340px;font-size:37px;line-height:1.55;text-align:justify}
.txt p{margin:0 0 30px;text-indent:64px}
mark{background:#FCF1B7;color:inherit;padding:2px 0}
.chip{display:inline-block;text-indent:0;font:700 20px Arial,sans-serif;color:#1E6B3A;background:#D7F0E4;border-radius:8px;padding:2px 8px;margin:0 4px;vertical-align:3px;line-height:1.3}
a{color:#0000EE}
.post{position:absolute;left:1450px;top:150px;width:492px}
</style></head><body>
<div class="txt">
<p>Art. 49-A. A pessoa jurídica não se confunde com os seus sócios, associados, instituidores ou administradores. <a href="#">(Incluído pela Lei nº 13.874, de 2019)</a></p>
<p>Art. 50. Em caso de abuso da personalidade jurídica, <mark>caracterizado pelo desvio de finalidade ou pela confusão patrimonial</mark><span class="chip">STJ</span>, pode o juiz, a requerimento da parte, ou do Ministério Público quando lhe couber intervir no processo, desconsiderá-la para que os efeitos de certas e determinadas relações de obrigações sejam estendidos aos bens particulares de administradores ou de sócios da pessoa jurídica beneficiados direta ou indiretamente pelo abuso. <a href="#">(Redação dada pela Lei nº 13.874, de 2019)</a></p>
<p style="text-indent:0;text-align:center;color:#555">(...)</p>
</div>
<img class="post" src="${post}" alt="">
</body></html>`;
(async () => { const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 2000, height: 1310 } })).newPage();
  await p.setContent(html, { waitUntil: 'load' }); await p.waitForTimeout(300); await p.screenshot({ path: OUT }); await b.close(); })();
