#!/usr/bin/env python3
"""Conferência rápida do site montado. Uso: python3 src/check.py

Verifica, sem precisar de navegador:
  - ids duplicados;
  - links internos (#algo) e labels (for="...") sem alvo;
  - "</" dentro do <script> (quebra o script em alguns visualizadores);
  - imagens apontando para arquivos que não existem;
  - restos de marcação provisória ([preencher], NOVO, TODO).
Sai com código 1 se encontrar problema.
"""
import os, re, sys, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
problems = []

def check(name):
    html = open(os.path.join(ROOT, name), encoding='utf-8').read()
    ids = re.findall(r'\bid="([^"]+)"', html)
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    if dup: problems.append(f'{name}: ids duplicados {dup}')
    idset = set(ids)
    for h in set(re.findall(r'href="#([^"]+)"', html)):
        if h not in idset: problems.append(f'{name}: âncora sem alvo #{h}')
    for f in set(re.findall(r'\bfor="([^"]+)"', html)):
        if f not in idset: problems.append(f'{name}: label sem alvo for="{f}"')
    for m in re.finditer(r'<script>(.*?)</script>', html, re.S):
        if '</' in m.group(1): problems.append(f'{name}: "</" dentro de <script>')
    for src in re.findall(r'src="([^"]+)"', html):
        if src.startswith(('data:', 'http')): continue
        if not os.path.exists(os.path.join(ROOT, src)): problems.append(f'{name}: imagem não encontrada {src}')
    for t in ('[preencher]', '>NOVO<'):
        if t in html: problems.append(f'{name}: contém "{t}"')
    if re.search(r'\bTODO\b', html): problems.append(f'{name}: contém "TODO"')

for n in ('index.html', 'marca-texto-web.html', 'privacidade-marca-texto-web.html', 'termos-marca-texto-web.html'):
    check(n)

if problems:
    print('\n'.join(problems)); sys.exit(1)
print('ok: nenhum problema encontrado')
