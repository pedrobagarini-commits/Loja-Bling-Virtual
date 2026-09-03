#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monta uma escada de pacotes para descobrir o que o importador do Bling recusa.

Cada pacote parte do ZIP ORIGINAL e aplica um subconjunto das alteracoes,
sempre pelo mesmo empacotador (patch-tema-zip.py), que preserva a estrutura
do container. Enviando os pacotes em ordem, o primeiro que falhar aponta o
grupo de arquivos responsavel.

Uso: python3 bisecar-zip.py ORIGINAL.zip PASTA_COM_ALTERACOES PASTA_SAIDA
"""
import os, shutil, subprocess, sys, zipfile

RAIZ = os.path.dirname(os.path.abspath(__file__))

TEMPLATES = ['elements/header.html', 'elements/horizontal-nav.html',
             'elements/showcase.html', 'elements/showcase-best-sellers.html',
             'elements/snippets/newsletter.html', 'elements/snippets/search.html']
SECOES    = ['layouts/default.html', 'pages/home.html']
ESTILO    = ['css/custom.css.html']
CONFIGS   = ['configs/settings.json', 'configs/settings.html']

ETAPAS = [
    ('0-nenhuma-alteracao',   []),
    ('1-templates',           TEMPLATES),
    ('2-secoes-da-home',      TEMPLATES + SECOES),
    ('3-com-o-css',           TEMPLATES + SECOES + ESTILO),
    ('4-completo',            TEMPLATES + SECOES + ESTILO + CONFIGS),
]

def main():
    original, alterados, saida = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(saida, exist_ok=True)
    for nome, arquivos in ETAPAS:
        tmp = os.path.join(saida, '_tmp')
        if os.path.isdir(tmp): shutil.rmtree(tmp)
        os.makedirs(tmp)
        # parte sempre da arvore original
        with zipfile.ZipFile(original) as z:
            z.extractall(tmp)
        # aplica so o subconjunto desta etapa
        for rel in arquivos:
            shutil.copyfile(os.path.join(alterados, rel), os.path.join(tmp, rel))
        destino = os.path.join(saida, 'teste-%s.zip' % nome)
        subprocess.run([sys.executable, os.path.join(RAIZ, 'patch-tema-zip.py'),
                        original, tmp, destino], check=True,
                       stdout=subprocess.DEVNULL)
        shutil.rmtree(tmp)
        print('  teste-%-22s %2d arquivo(s) alterado(s)  %7d bytes'
              % (nome + '.zip', len(arquivos), os.path.getsize(destino)))

if __name__ == '__main__':
    main()
