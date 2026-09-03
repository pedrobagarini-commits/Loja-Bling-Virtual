#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera o pacote do tema para envio ao Bling.

O repositorio mantem a personalizacao em arquivos separados, que e mais facil
de manter:

    css/redesign.css              camada visual
    elements/benefits-bar.html    faixa de vantagens
    elements/category-grid.html   grade de categorias
    elements/how-it-works.html    passo a passo

Alguns importadores so aceitam o conjunto de arquivos que o tema ja tinha.
Este script produz uma variante equivalente sem nenhum arquivo novo: o CSS vai
para dentro de css/custom.css.html e as tres secoes sao embutidas nos
templates que as chamam. O resultado tem exatamente os mesmos 106 nomes de
arquivo do tema exportado pela Tray.

Uso:
    python3 build-tema-bling.py                 # gera dist/tema-bling.zip
    python3 build-tema-bling.py --com-extras    # mantem os arquivos separados
"""
import io, os, re, shutil, sys, zipfile

RAIZ  = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(RAIZ, 'dist')
PASTAS = ['configs', 'css', 'elements', 'img', 'js', 'layouts', 'pages']

EXTRAS = ['css/redesign.css', 'elements/benefits-bar.html',
          'elements/category-grid.html', 'elements/how-it-works.html']

def ler(p):  return io.open(p, encoding='utf-8').read()
def escrever(p, s): io.open(p, 'w', encoding='utf-8', newline='').write(s)

def montar_arvore(tmp, embutir):
    if os.path.isdir(tmp): shutil.rmtree(tmp)
    os.makedirs(tmp)
    for pasta in PASTAS:
        shutil.copytree(os.path.join(RAIZ, pasta), os.path.join(tmp, pasta))
    if not embutir:
        return

    # 1) CSS da camada de personalizacao entra no fim do custom.css.html
    css = ler(os.path.join(RAIZ, 'css/redesign.css'))
    alvo = os.path.join(tmp, 'css/custom.css.html')
    escrever(alvo, ler(alvo) + '\n\n' + css)

    # 2) tira o <link> do redesign.css, que agora nao existe mais como arquivo
    lay = os.path.join(tmp, 'layouts/default.html')
    s = ler(lay)
    s = re.sub(r'\n *<!-- camada de personalizacao da loja \(carregada por ultimo\) -->'
               r'\n *<link rel="stylesheet" href="\{\{ asset\(\'css/redesign\.css\'\) \}\}"[^>]*>\n',
               '\n', s)
    assert 'redesign.css' not in s, 'link do redesign.css nao foi removido'
    escrever(lay, s)

    # 3) as tres secoes passam a ser embutidas onde eram chamadas
    for elemento, arquivo in (('benefits-bar',  'layouts/default.html'),
                              ('category-grid', 'pages/home.html'),
                              ('how-it-works',  'pages/home.html')):
        corpo = ler(os.path.join(RAIZ, 'elements/%s.html' % elemento)).strip()
        alvo  = os.path.join(tmp, arquivo)
        s = ler(alvo)
        chamada = re.compile(r"\{%\s*element\s+'" + re.escape(elemento) + r"'\s*%\}")
        assert chamada.search(s), 'chamada de %s nao encontrada em %s' % (elemento, arquivo)
        s = chamada.sub(lambda _m: corpo, s, count=1)
        escrever(alvo, s)

    # 4) remove os arquivos que foram embutidos
    for rel in EXTRAS:
        os.remove(os.path.join(tmp, rel))

def empacotar(tmp, destino):
    """Replica os metadados do ZIP exportado pela Tray: sem entradas de
    diretorio, tudo deflated, create_version 6.3, extract_version 2.0 e
    permissoes 0666."""
    arquivos = []
    for pasta in PASTAS:
        for dirpath, dirnames, filenames in os.walk(os.path.join(tmp, pasta)):
            dirnames.sort()
            for fn in sorted(filenames):
                full = os.path.join(dirpath, fn)
                arquivos.append((os.path.relpath(full, tmp).replace(os.sep, '/'), full))
    arquivos.sort()
    with zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for arc, full in arquivos:
            info = zipfile.ZipInfo(arc, date_time=(2026, 9, 2, 17, 34, 0))
            info.compress_type   = zipfile.ZIP_DEFLATED
            info.create_system   = 3
            info.create_version  = 63
            info.extract_version = 20
            info.external_attr   = 0o100666 << 16
            z.writestr(info, open(full, 'rb').read())
    return len(arquivos)

def main():
    embutir = '--com-extras' not in sys.argv
    os.makedirs(SAIDA, exist_ok=True)
    tmp = os.path.join(SAIDA, '_tema')
    destino = os.path.join(SAIDA, 'tema-bling.zip')
    montar_arvore(tmp, embutir)
    n = empacotar(tmp, destino)
    shutil.rmtree(tmp)
    print('%s  |  %d arquivos  |  %s' % (
        'sem arquivos novos' if embutir else 'com arquivos separados',
        n, destino))

if __name__ == '__main__':
    main()
