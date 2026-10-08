#!/usr/bin/env python3
"""Gera as imagens da galeria do Marca-texto Web: img/mtw-sumario.webp, mtw-busca.webp e
mtw-margens.webp (2560x1600), a partir das capturas de tela originais desta pasta.

Uso (na raiz do repositório):  python3 src/capturas/gerar.py

Para trocar uma imagem: salve a nova captura aqui com o mesmo nome (sumario.png, busca.png ou
margens.png; quanto maior a captura, mais nítida a imagem) e rode o comando. Depois rode
python3 src/build.py e python3 src/check.py como sempre.

Título, subtítulo, logo e moldura do navegador vêm do modelo em compor.js (texto de verdade,
não imagem). Se mudar o texto de uma tela, mude lá.

Precisa de: Pillow (pip install pillow), Node e Playwright (npm i -g playwright). Não faz parte
do build do site (o build usa só a biblioteca padrão) e esta pasta não é publicada (.vercelignore).
"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
NOMES = ['sumario', 'busca', 'margens']
W, H = 2358, 1250          # área útil da janela do navegador no canvas 2560x1600 (já em 2x)

def preparar(nome, pasta):
    """Ajusta a captura à janela (cobre a área, corta a sobra à direita/embaixo) com LANCZOS,
    para o navegador não precisar esticar a imagem."""
    im = Image.open(os.path.join(AQUI, nome + '.png')).convert('RGBA')
    fundo = Image.new('RGBA', im.size, (255, 255, 255, 255)); fundo.alpha_composite(im); im = fundo.convert('RGB')
    s = max(W / im.width, H / im.height)
    up = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    up = up.filter(ImageFilter.UnsharpMask(radius=1.0, percent=60, threshold=2)).crop((0, 0, W, H))
    up.save(os.path.join(pasta, f'prep-{nome}.png'))
    print(f'{nome}: captura {im.size[0]}x{im.size[1]} (escala {s:.2f}x)')

def main():
    try:
        node_path = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        sys.exit('Precisa de Node/npm com Playwright instalado (npm i -g playwright).')
    env = dict(os.environ, NODE_PATH=node_path)
    with tempfile.TemporaryDirectory() as pasta:
        for n in NOMES: preparar(n, pasta)
        subprocess.run(['node', os.path.join(AQUI, 'compor.js'), pasta] + NOMES, check=True, env=env)
        for n in NOMES:
            destino = os.path.join(RAIZ, 'img', f'mtw-{n}.webp')
            Image.open(os.path.join(pasta, f'novo-{n}.png')).convert('RGB').save(destino, 'WEBP', quality=85, method=6)
            print(f'img/mtw-{n}.webp: {os.path.getsize(destino) // 1024} KB')

if __name__ == '__main__':
    main()
