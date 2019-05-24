import json
from os import listdir, path
# simple version for working with CWD


def find_first_round_game(player):
    BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
    rodadas_dir = path.join(BASE_DIR, 'rodadas')
    rodadas_num = len([name for name in listdir(rodadas_dir) if path.isfile(path.join(rodadas_dir, name))])

    for x in range(1, rodadas_num+1):
        file = f'{rodadas_dir}/rodada-{x}.json'
        with open(file, 'r') as rodada:
            json_rodada = json.load(rodada)
            for atleta in json_rodada['atletas']:
                if atleta['atleta_id'] == player.id:
                    if atleta['pontos_num'] != 0 and atleta['variacao_num'] != 0:
                        return atleta['rodada_id']

            rodada.close()


def rodadas_desfalques(player):
    BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
    rodadas_dir = path.join(BASE_DIR, 'rodadas')
    rodadas_num = len([name for name in listdir(rodadas_dir) if path.isfile(path.join(rodadas_dir, name))])

    desfalque_total = 0
    for x in range(rodadas_num,  0, -1):
        file = f'{rodadas_dir}/rodada-{x}.json'
        with open(file, 'r') as rodada:
            json_rodada = json.load(rodada)
            for atleta in json_rodada['atletas']:
                if atleta['atleta_id'] == player.id:
                    if atleta['pontos_num'] == 0 and atleta['variacao_num'] == 0:
                        desfalque_total += 1
                    else:
                        return desfalque_total


def valorization(player):
    r = player.rodada_atual
    r0 = player.rodada_inicial
    d = player.desfalques

    c = player.preco
    a = player.media
    g = player.jogos
    u = player.ultima
    p = player.pontos

    a0 = 0
    if g > 1:
        a0 = (a * g - u) / (g - 1)

    dr = r
    if r0 > 1:
        dr = r - r0

    if g == 0:
        d = dr - 1

    if d < 0:
        d = 0

    cr = 0
    pr = 0
    ur = 0

    if dr > 0:
        cr = c / dr
        pr = p / dr
        ur = u / dr

    cdr = cr * d
    udr = ur * d

    var = 0

    if dr == 1:
        if r0 == 1:
            var = 0.6890 * p - 0.3110 * c
        elif r0 >= 2:
            var = 0.4188 * p - 0.2125 * c
    elif dr == 2:
        if r0 == 1:
            var = 0.4221 * p - 0.2964 * c + 0.2813 * u
        elif r0 >= 2 and d == 1:
            var = 0.3589 * p - 0.2272 * c
        elif r0 >= 2 and d == 0:
            var = 0.3551 * p - 0.1137 * c - 0.0284 * u
    elif dr == 3:
        if r0 == 1 and d >= 1:
            var = 0.3301 * p - 0.2930 * c + 0.1882 * u
        elif r0 == 1 and d == 0:
            var = 0.3299 * p - 0.1440 * c - 0.0237 * u + 0.0471 * a0
        elif r0 >= 2:
            var = 0.2975 * p - 0.0764 * c - 0.0861 * u + 0.0007 * a0 - 0.2553 * cdr + 0.2943 * udr
    elif dr == 4:
        if r0 == 1 and d >= 2:
            var = 0.2939 * p - 0.2654 * c + 0.1469 * u
        elif r0 == 1 and d == 1:
            var = 0.2940 * p - 0.1621 * c + 0.0001 * u + 0.0490 * a0
        elif r0 == 1 and d == 0:
            var = 0.2936 * p - 0.0564 * c - 0.0827 * u + 0.0222 * a0
        elif r0 >= 2:
            var = 0.2762 * p - 0.0568 * c - 0.1088 * u + 0.0083 * a0 - 0.2462 * cdr + 0.2157 * udr
    else:
        if r0 == 1:
            var = 0.1580 * p + 0.0040 * c - 0.1588 * u + 0.0064 * a0 - 0.2358 * cdr + 0.1865 * udr + 0.5140 * pr - 0.3134 * cr + 0.2803 * ur
        elif r0 >= 2:
            var = 0.1608 * p - 0.0004 * c - 0.1599 * u + 0.0047 * a0 - 0.2240 * cdr + 0.1737 * udr + 0.4748 * pr - 0.2198 * cr + 0.2322 * ur

    if c + var < 0.7:
        var = 0.7 - c

    return var