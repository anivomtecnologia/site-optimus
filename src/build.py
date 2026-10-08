#!/usr/bin/env python3
"""Monta o site da Optimus Aprendizado.

Uso (na raiz do repositório):  python3 src/build.py

Etapas:
  1. Injeta Ajuda, Política de Privacidade e Termos de Uso (src/docs/*.html)
     em marca-texto-web.html e gera as páginas avulsas
     privacidade-marca-texto-web.html e termos-marca-texto-web.html.
  2. Monta o corpo do site a partir de src/optimus-aprendizado.fonte.html:
     embute as imagens de img/ em base64 e embute a página do Marca-texto Web
     (CSS escopado em #marca-texto, classes com prefixo m-, ids com prefixo mtw-).
  3. Junta src/head.html + corpo e grava index.html na raiz.

Só usa a biblioteca padrão do Python. Pode rodar quantas vezes quiser (é idempotente).
"""
import os,re,base64
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rd(rel): return open(os.path.join(ROOT,rel),encoding='utf-8').read()
def wr(rel,txt): open(os.path.join(ROOT,rel),'w',encoding='utf-8').write(txt)

# ===================== 1. documentos =====================
p=os.path.join(ROOT,'marca-texto-web.html'); s=open(p,encoding='utf-8').read()
priv=rd('src/docs/privacidade.html'); termos=rd('src/docs/termos.html'); ajuda=rd('src/docs/ajuda.html'); psite=rd('src/docs/privacidade-site.html')
EMAIL='marcatextoweb@optimusaprendizado.com'
# bloco de ajuda
help_html=f'''<!--HELP--><div class="help">
        <div><span class="label">Precisa de ajuda?</span><p>Dúvidas, problemas ou pedidos sobre a extensão, a assinatura ou os seus dados? É só escrever para o nosso e-mail.</p></div>
        <a class="btn ghost" href="mailto:{EMAIL}">{EMAIL}</a>
      </div><!--/HELP-->
      '''
if '<!--HELP-->' in s: s=re.sub(r'<!--HELP-->.*?<!--/HELP-->\s*',lambda _:help_html,s,flags=re.S)
else: s=s.replace('<p class="disclaimer">',help_html+'<p class="disclaimer">',1)
# links no rodapé
old='<a href="https://www.instagram.com/marcatextoweb/" target="_blank" rel="noopener">Instagram @marcatextoweb</a><a href="./">Voltar para o site</a>'
# a Política de Privacidade abre a página avulsa (URL própria, para colar em formulários); Termos e Ajuda abrem em sobreposição
new='<a href="privacidade-marca-texto-web.html" target="_blank" rel="noopener" class="doclink">Política de Privacidade</a><a href="privacidade-optimus.html" target="_blank" rel="noopener" class="doclink">Privacidade do site</a><label for="doc-termos" class="doclink">Termos de Uso</label><label for="doc-ajuda" class="doclink">Ajuda</label><a href="https://www.instagram.com/marcatextoweb/" target="_blank" rel="noopener">Instagram @marcatextoweb</a><a href="./">Voltar para o site</a>'
if old in s and 'class="doclink"' not in s: s=s.replace(old,new)
# sobreposições dos documentos
def ov(i,title,body):
    return (f'<input type="checkbox" id="{i}" class="dcb" aria-label="Abrir {title}">'
            f'<div class="docov" role="dialog" aria-label="{title}"><div class="docbox">'
            f'<div class="dochead"><span>Marca-texto Web · {title}</span><label for="{i}" class="docclose" role="button" tabindex="0">Fechar ✕</label></div>'
            f'<article class="doc">{body}</article>'
            f'<div class="docfoot"><label for="{i}" class="btn ghost" role="button" tabindex="0">Fechar</label></div></div></div>')
docs='<!--DOCS-->\n'+ov('doc-termos','Termos de Uso',termos)+'\n'+ov('doc-ajuda','Ajuda',ajuda)+'\n<!--/DOCS-->'
if '<!--DOCS-->' in s: s=re.sub(r'<!--DOCS-->.*?<!--/DOCS-->',lambda _:docs,s,flags=re.S)
else: s=s.replace('</footer>','</footer>\n'+docs,1)
css='''/*DOCCSS*/
.help{margin-top:16px;display:flex;flex-wrap:wrap;gap:12px 24px;align-items:center;justify-content:space-between;background:var(--surface);border:1px solid var(--line);border-radius:24px;padding:clamp(20px,3vw,28px)}
.help p{font:700 clamp(18px,2vw,22px)/1.25 var(--f-display);letter-spacing:-.01em;margin-top:6px}
.help .btn{white-space:normal;overflow-wrap:anywhere;text-align:center}
.doclink{cursor:pointer;text-decoration:underline}
.dcb{position:absolute;width:1px;height:1px;opacity:0;overflow:hidden;pointer-events:none}
.docov{display:none;position:fixed;inset:0;z-index:400;background:rgba(8,13,22,.62);overflow-y:auto;overscroll-behavior:contain;padding:clamp(12px,4vw,48px) 12px}
.dcb:checked + .docov{display:block}
.docbox{max-width:780px;margin:0 auto;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:22px;box-shadow:0 30px 80px -20px rgba(0,0,0,.5)}
.dochead{position:sticky;top:0;z-index:1;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:14px clamp(18px,3vw,28px);background:var(--surface);border-bottom:1px solid var(--line);border-radius:22px 22px 0 0;font:600 14px var(--f-body);color:var(--muted)}
.docclose{cursor:pointer;font-weight:600;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:999px;padding:6px 12px;white-space:nowrap}
.doc{padding:clamp(20px,3vw,32px) clamp(18px,4vw,40px) 8px;font-size:16px;line-height:1.65}
.doc h2{font-size:clamp(26px,3vw,34px)}
.doc h3{font-size:18px;letter-spacing:-.01em;margin-top:26px}
.doc p,.doc ul{margin:10px 0}
.doc ul{padding-left:22px}
.doc li{margin:4px 0}
.doc a{color:var(--accent);overflow-wrap:anywhere}
.doc-meta{color:var(--muted);font-size:14px}
.doc-mail{font:700 clamp(17px,2.2vw,22px)/1.3 var(--f-display);overflow-wrap:anywhere}
.docfoot{padding:8px clamp(18px,4vw,40px) 28px}
.docfoot .btn{cursor:pointer}
/*/DOCCSS*/
'''
if '/*DOCCSS*/' in s: s=re.sub(r'/\*DOCCSS\*/.*?/\*/DOCCSS\*/\n',lambda _:css,s,flags=re.S)
else: s=s.replace('footer{padding-block',css+'footer{padding-block',1)
open(p,'w',encoding='utf-8').write(s)

# páginas avulsas (para o link da Chrome Web Store)
head=s.split('<style>')[0]
head=re.sub(r'<!--GTAG-->.*?<!--/GTAG-->\s*','',head,flags=re.S)  # a tag do Google Ads não vai nas páginas legais (Privacidade e Termos)
style=re.search(r'<style>.*?</style>',s,re.S).group(0)
for fn,title,body in [('privacidade-marca-texto-web.html','Política de Privacidade',priv),('termos-marca-texto-web.html','Termos de Uso',termos)]:
    h=head.replace('<title>Marca-texto Web · Optimus Aprendizado</title>',f'<title>{title} · Marca-texto Web</title>')
    page=(h+style+'\n<style>.docbox{margin:clamp(16px,4vw,48px) auto}.pg-wrap{padding:0 12px}</style>\n</head>\n<body>\n<div class="pg-wrap"><div class="docbox">'
          f'<div class="dochead"><span>Marca-texto Web · {title}</span><a class="docclose" href="marca-texto-web.html" style="text-decoration:none">Voltar</a></div>'
          f'<article class="doc">{body}</article><div class="docfoot"></div></div></div>\n</body>\n</html>\n')
    wr(fn,page)
# política de privacidade do SITE (tag do Google Ads, fontes do Google): página avulsa com as cores da Optimus e "Voltar" para o site
SITE_CSS=('<style>:root{--bg:#F4F5F7;--surface:#FCFCFD;--ink:#15192B;--muted:#626A7A;--faint:#B4BAC6;--line:#DEE2E9;--accent:#2B5BD7}'
          '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#10131C;--surface:#181C28;--ink:#E8ECF4;--muted:#98A2B5;--faint:#485165;--line:#262C3A;--accent:#86A6F7}}'
          '.docbox{margin:clamp(16px,4vw,48px) auto}.pg-wrap{padding:0 12px}</style>')
h=head.replace('<title>Marca-texto Web · Optimus Aprendizado</title>','<title>Política de Privacidade do site · Optimus Aprendizado</title>')
h=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="Política de Privacidade do site da Optimus Aprendizado: cookies, Google Ads e seus direitos.">',h)
wr('privacidade-optimus.html',h+style+'\n'+SITE_CSS+'\n</head>\n<body>\n<div class="pg-wrap"><div class="docbox">'
   '<div class="dochead"><span>Optimus Aprendizado · Política de Privacidade do site</span><a class="docclose" href="./" style="text-decoration:none">Voltar</a></div>'
   f'<article class="doc">{psite}</article><div class="docfoot"></div></div></div>\n</body>\n</html>\n')
print('documentos: ok')

# ===================== 2. montagem =====================
def uri(name):
    return 'data:image/webp;base64,'+base64.b64encode(open(os.path.join(ROOT,'img',name),'rb').read()).decode()
# As capturas grandes da galeria ficam como arquivos em img/ (loading=lazy: só baixam quando precisam)
# em vez de embutidas em base64; senão o index.html passa de 4 MB. As imagens pequenas continuam embutidas.
SOLTAS={'mtw-grifos.webp','mtw-sumario.webp','mtw-busca.webp','mtw-margens.webp'}
def inline_imgs(t):
    def tag(m):
        im=m.group(0); n=re.search(r'src="img/([\w-]+\.webp)"',im)
        if not n: return im
        if n.group(1) in SOLTAS:
            return im if 'loading=' in im else re.sub(r'\s*/?>$',' loading="lazy" decoding="async">',im)
        return im.replace(n.group(0),'src="'+uri(n.group(1))+'"').replace(' loading="lazy"','')
    return re.sub(r'<img\b[^>]*>',tag,t)

P='#marca-texto'
def split_top(css):
    """devolve lista de (cabeçalho, corpo) no nível atual"""
    out=[];i=0;n=len(css)
    while i<n:
        j=css.find('{',i)
        if j<0: break
        head=css[i:j].strip(); depth=1;k=j+1
        while k<n and depth:
            if css[k]=='{': depth+=1
            elif css[k]=='}': depth-=1
            k+=1
        out.append((head,css[j+1:k-1])); i=k
    return out
def split_commas(sel):
    parts=[];d=0;cur=''
    for ch in sel:
        if ch in '([': d+=1
        if ch in ')]': d-=1
        if ch==',' and d==0: parts.append(cur);cur=''
        else: cur+=ch
    parts.append(cur); return [p.strip() for p in parts if p.strip()]
def map_sel(p):
    if p.startswith(':root'):
        if p.startswith(':root[data-theme="dark"]'): return P+'.force-dark'
        return re.sub(r'^:root(:not\(\[data-theme="light"\]\))?',P,p)
    if p in ('html','body'): return P
    if p.startswith('html ') or p.startswith('body '): p=p.split(' ',1)[1]
    if p.startswith('*') or p.startswith(':'): out=P+' '+p
    else: out=P+' '+p
    return re.sub(r'\.([A-Za-z_][\w-]*)',r'.m-\1',out)
def scope(css):
    css=re.sub(r'/\*.*?\*/','',css,flags=re.S)
    res=[]
    for head,body in split_top(css):
        if head.startswith('@media') or head.startswith('@supports'):
            res.append(head+'{'+scope(body)+'}')
        elif head.startswith('@'):
            res.append(head+'{'+body+'}')
        else:
            res.append(','.join(map_sel(p) for p in split_commas(head))+'{'+body+'}')
    return '\n'.join(res)

s=rd('src/optimus-aprendizado.fonte.html')
s=inline_imgs(s)
m=rd('marca-texto-web.html')
style=re.search(r'<style>(.*?)</style>',m,re.S).group(1)
body=re.search(r'<body>(.*)</body>',m,re.S).group(1)
body=re.sub(r'<script>.*?</script>','',body,flags=re.S)
body=inline_imgs(body)

# ---- HTML: classes, ids, fechar, galeria
body=re.sub(r'class="([^"]*)"',lambda mm:'class="'+' '.join('m-'+c for c in mm.group(1).split())+'"',body)
body=re.sub(r'\bid="([^"]+)"',r'id="mtw-\1"',body)
body=re.sub(r'\bfor="([^"]+)"',r'for="mtw-\1"',body)
body=body.replace('href="#preco"','href="#mtw-preco"')
# fechar: links para o site viram labels que desmarcam o checkbox
body=re.sub(r'<a class="([^"]*)" href="\./"( aria-label="[^"]*")?>(.*?)</a>',lambda mm:'<label class="'+mm.group(1)+' m-closer" for="mtw-open" role="button" tabindex="0"'+(mm.group(2) or '')+'>'+mm.group(3)+'</label>',body,flags=re.S)
body=body.replace('<a href="./">Voltar para o site</a>','<label class="m-closer m-closelink" for="mtw-open" role="button" tabindex="0">Voltar para o site</label>')
assert 'href="./"' not in body
# galeria: abas por radio (CSS puro)
tabs=re.findall(r'<button type="button" role="tab"[^>]*>(.*?)</button>',body)
assert len(tabs)==4
radios=''.join(f'<input type="radio" name="mtwg" id="mtwg{i}" class="m-gr"'+(' checked' if i==0 else '')+f' aria-label="{t}">' for i,t in enumerate(tabs))
body=re.sub(r'<div class="m-tabs"[^>]*>.*?</div>','<div class="m-tabs" aria-label="Telas do Marca-texto Web">'+''.join(f'<label for="mtwg{i}" class="m-gt">{t}</label>' for i,t in enumerate(tabs))+'</div>',body,count=1,flags=re.S)
body=body.replace('<div class="m-gallery">','<div class="m-gallery">'+radios,1)
body=re.sub(r' aria-hidden="true"( width="1280" height="800")',r'\1',body)
CAPS=['8 cores, sublinhado, círculo, colchetes, “Revisar” e post-its do STF e STJ. Tudo fica salvo na página.','Livros, títulos, capítulos e artigos ao lado do texto, e um “você está em” que acompanha a leitura.','Busque pelo número (1.238, 44-A) ou por palavra (promessa de fato) e vá direto ao dispositivo.','Estreita, Normal ou Larga. A mesma margem vale na hora de imprimir em A4.']
body=re.sub(r'<p class="m-caption"[^>]*>.*?</p>','<p class="m-caption">'+''.join(f'<span>{c}</span>' for c in CAPS)+'</p>',body,count=1,flags=re.S)
body=re.sub(r'<div class="m-frame"[^>]*>','<div class="m-frame">',body,count=1)

# ---- CSS escopado
css=scope(style)
extra='\n'.join([
 P+' .m-gr{position:absolute;width:1px;height:1px;opacity:0;overflow:hidden}',
 P+' .m-gt{font:500 14px var(--f-body);border:1px solid var(--line);background:var(--surface);color:var(--muted);padding:9px 16px;border-radius:999px;cursor:pointer;transition:all .25s}',
 P+' .m-frame img{opacity:0}',
 P+' .m-caption span{display:none}',
 P+' .m-closer{cursor:pointer}',
 P+' .m-closelink{text-decoration:underline}',
]+[
 f'{P} .m-gr:nth-of-type({k}):checked ~ .m-tabs .m-gt:nth-child({k}){{background:var(--ink);color:var(--bg);border-color:var(--ink)}}\n'
 f'{P} .m-gr:nth-of-type({k}):checked ~ .m-frame img:nth-child({k}){{opacity:1}}\n'
 f'{P} .m-gr:nth-of-type({k}):checked ~ .m-caption span:nth-child({k}){{display:inline}}\n'
 f'{P} .m-gr:nth-of-type({k}):focus-visible ~ .m-tabs .m-gt:nth-child({k}){{outline:2px solid var(--accent);outline-offset:3px}}'
 for k in range(1,5)])
tpl=('<!--TPL-MTW-->\n<input type="checkbox" id="mtw-open" class="mtw-cb" aria-label="Abrir ou fechar a página do Marca-texto Web">'
     '<div id="marca-texto" class="product-panel" role="dialog" aria-modal="true" aria-label="Marca-texto Web"><style>'+css+'\n'+extra+'</style>'+body+'</div>\n<!--/TPL-MTW-->')
s=re.sub(r'<!--TPL-MTW-->.*?<!--/TPL-MTW-->',lambda _:tpl,s,flags=re.S)
# --- etapa 3: cabeçalho + corpo -> index.html
# o visualizador e alguns parsers cortam scripts em "</": garante que não haja "</" dentro do <script>
a=s.index('<script>')+8; z=s.rindex('</script>')
s=s[:a]+s[a:z].replace('</','<\\/')+s[z:]
s=re.sub(r'^\s*<title>.*?</title>\s*','',s,count=1)  # o <title> fica só no head.html
out=rd('src/head.html')+s.lstrip('\n')+'\n</body>\n</html>\n'
wr('index.html',out)
print('index.html:',len(out),'bytes')
