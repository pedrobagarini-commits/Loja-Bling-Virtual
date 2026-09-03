#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera o pacote do tema a partir do ZIP ORIGINAL exportado pela Tray/Bling.

Em vez de montar um ZIP novo, este script reescreve o original entrada por
entrada, na mesma ordem e com os mesmos cabecalhos:

  * arquivos que a personalizacao nao tocou  -> copia byte a byte dos dados
    ja comprimidos, sem recomprimir;
  * arquivos alterados -> recomprimidos, mas herdando todos os campos de
    cabecalho da entrada original (versoes, flags, data, atributos externos,
    campo extra).

O resultado tem a mesma lista de entradas, na mesma ordem, com a mesma
estrutura de container. So mudam os bytes dos arquivos que precisavam mudar.

Uso:
    python3 patch-tema-zip.py ORIGINAL.zip PASTA_DO_TEMA SAIDA.zip
"""
import os, struct, sys, zipfile, zlib

LFH_SIG = b'PK\x03\x04'
CDH_SIG = b'PK\x01\x02'
EOCD_SIG = b'PK\x05\x06'


def ler_entrada_bruta(blob, info):
    """Devolve (nome, extra_local, dados_comprimidos) direto do cabecalho local."""
    off = info.header_offset
    assert blob[off:off + 4] == LFH_SIG, 'cabecalho local ausente em %s' % info.filename
    n_len, e_len = struct.unpack('<HH', blob[off + 26:off + 30])
    ini = off + 30 + n_len + e_len
    nome = blob[off + 30:off + 30 + n_len]
    extra = blob[off + 30 + n_len:ini]
    return nome, extra, blob[ini:ini + info.compress_size]


def main():
    original, pasta, saida = sys.argv[1], sys.argv[2], sys.argv[3]
    blob = open(original, 'rb').read()
    zin = zipfile.ZipFile(original)

    saida_bytes = bytearray()
    centrais = []
    copiados = recomprimidos = 0

    for info in zin.infolist():
        nome_b, extra_local, dados_orig = ler_entrada_bruta(blob, info)
        caminho = os.path.join(pasta, info.filename)
        if not os.path.exists(caminho):
            raise SystemExit('faltando na pasta do tema: %s' % info.filename)

        conteudo = open(caminho, 'rb').read()
        if zlib.crc32(conteudo) & 0xffffffff == info.CRC and len(conteudo) == info.file_size:
            # inalterado: reaproveita os bytes comprimidos originais
            dados, crc, tam_comp, tam_orig = dados_orig, info.CRC, info.compress_size, info.file_size
            copiados += 1
        else:
            crc = zlib.crc32(conteudo) & 0xffffffff
            tam_orig = len(conteudo)
            if info.compress_type == zipfile.ZIP_DEFLATED:
                c = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS)
                dados = c.compress(conteudo) + c.flush()
            else:
                dados = conteudo
            tam_comp = len(dados)
            recomprimidos += 1

        offset = len(saida_bytes)
        dt = info.date_time
        hora = (dt[3] << 11) | (dt[4] << 5) | (dt[5] // 2)
        data = ((dt[0] - 1980) << 9) | (dt[1] << 5) | dt[2]

        # cabecalho local: versao, flags, metodo, hora, data, crc, tamanhos, nomes
        saida_bytes += LFH_SIG + struct.pack(
            '<HHHHHIIIHH', info.extract_version, info.flag_bits,
            info.compress_type, hora, data, crc, tam_comp, tam_orig,
            len(nome_b), len(extra_local)) + nome_b + extra_local + dados

        # cabecalho central: quem criou, versao minima, flags, metodo, datas,
        # crc, tamanhos, nomes, disco, atributos e deslocamento
        centrais.append(CDH_SIG + struct.pack(
            '<HHHHHHIIIHHHHHII',
            (info.create_system << 8) | info.create_version,
            info.extract_version, info.flag_bits,
            info.compress_type, hora, data, crc, tam_comp, tam_orig,
            len(nome_b), len(info.extra), len(info.comment),
            0, info.internal_attr, info.external_attr, offset)
            + nome_b + info.extra + info.comment)

    inicio_cd = len(saida_bytes)
    for c in centrais:
        saida_bytes += c
    tam_cd = len(saida_bytes) - inicio_cd
    saida_bytes += EOCD_SIG + struct.pack(
        '<HHHHIIH', 0, 0, len(centrais), len(centrais), tam_cd, inicio_cd,
        len(zin.comment)) + zin.comment

    open(saida, 'wb').write(bytes(saida_bytes))
    print('entradas: %d  |  copiadas byte a byte: %d  |  recomprimidas: %d'
          % (len(centrais), copiados, recomprimidos))
    print('saida:', saida, '(%d bytes)' % len(saida_bytes))


if __name__ == '__main__':
    main()
