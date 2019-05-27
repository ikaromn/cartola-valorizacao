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
            player.pontos = float(request.GET.get('points')) if request.GET.get('points') else 5
            player.ultima = i['pontos_num']
            player.preco = i['preco_num']
            player.id = i['atleta_id']
            rodada_inicial_num = find_first_round_game(player)
            player.rodada_inicial = rodada_inicial_num if rodada_inicial_num else player.rodada_atual
            player.desfalques = rodadas_desfalques(player)
            i['to_valorizate'] = valorization(player)

            i['scout'] = self.populate_scout(i['scout']) if i['scout'] else []

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


class PartialScore(View):
    response_template = 'player/partial.html'

    def get(self, request):
        c = Cartola()
        data = c.make_request('partial_score')
        new_data = {'atletas': list()}

        for _, value in data['atletas'].items():
            value['foto'] = re.sub(r'([FORMATO])\w+', '140x140', str(value['foto']))

            new_data['atletas'].append(value)

        return render(request, self.response_template, {'data': new_data})


class TeamPartialScore(View):
    response_template = 'player/team-partial.html'
    template_error = 'error.html'

    def get(self, request):
        c = Cartola()
        team = request.GET.get('team_name')
        round_num = request.GET.get('round')

        try:
            data = c.make_request('team_partial_score', team_name=team, round=round_num)
            scores = c.make_request('partial_score')
        except Exception as e:
            return render(request, self.template_error, {'data': str(e)})

        new_data = {
            'atletas': list(),
            'total_score': 0,
        }
        for i in data['atletas']:
            i['foto'] = re.sub(r'([FORMATO])\w+', '140x140', str(i['foto']))
            try:
                i['pontos_num'] = scores['atletas'][str(i['atleta_id'])]['pontuacao']
            except KeyError:
                i['pontos_num'] = 0
            new_data['total_score'] += i['pontos_num']
            new_data['atletas'].append(i)
        return render(request, self.response_template, {'data': new_data})
