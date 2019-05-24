import re

from cartola_mn.utils.valorization import find_first_round_game, rodadas_desfalques, valorization
from cartola_mn.utils.cartola import Cartola
from django.shortcuts import render
from django.views.generic import View


class Player:
    rodada_atual = 6
    rodada_inicial = 1
    desfalques = 0
    preco: float
    media: float
    jogos: int
    ultima: float
    pontos: float
    id: int


class Players(View):
    response_template = 'player/player.html'

    def _calculate_valorization(self, price, last_pontuation):
        y = (price / 100) * 37
        z = y * 2
        total_points = z - last_pontuation
        return total_points

    def populate_scout(self, scout):
        if 'RB' not in scout:
            scout['RB'] = 0

        if 'DD' not in scout:
            scout['DD'] = 0

        if 'DP' not in scout:
            scout['DP'] = 0

        if 'GS' not in scout:
            scout['GS'] = 0

        return scout

    def get(self, request, **kwargs):
        c = Cartola()
        data = c.make_request('players')
        new_data = {'atletas': list()}

        for i in data['atletas']:
            i['status_nome'] = data['status'][str(i['status_id'])]['nome']
            i['status_id'] = data['status'][str(i['status_id'])]['id']

            if i['status_id'] != 7:
                continue
            position = data['posicoes'][str(i['posicao_id'])]['abreviacao']
            if request.GET.get('position'):
                if position != request.GET.get('position'):
                    continue

            i['position'] = position
            i['foto'] = re.sub(r'([FORMATO])\w+', '140x140', str(i['foto']))

            player = Player()
            player.desfalques = i['rodada_id'] - i['jogos_num']
            player.jogos = i['jogos_num']
            player.media = i['media_num']
            player.pontos = int(request.GET.get('points')) if request.GET.get('points') else 5
            player.ultima = i['pontos_num']
            player.preco = i['preco_num']
            player.id = i['atleta_id']
            rodada_inicial_num = find_first_round_game(player)
            player.rodada_inicial = rodada_inicial_num if rodada_inicial_num else player.rodada_atual
            player.desfalques = rodadas_desfalques(player)
            i['to_valorizate'] = valorization(player)

            if 'RB' not in i['scout']:
                i['scout']['RB'] = 0
            i['scout'] = self.populate_scout(i['scout'])

            new_data['atletas'].append(i)

        new_data['order_by'] = 'media_num'
        if request.GET.get('order_by'):
            new_data['order_by'] = request.GET.get('order_by')

        return render(request, self.response_template, {'data': new_data})


class Team(View):
    response_template = 'templates/my_team.html'

    def get(self, request):
        c = Cartola()
        data = c.make_request('my_team')

        return render(request, self.response_template, {'data': data})