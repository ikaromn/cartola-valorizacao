import re

from cartola_mn.utils.cartola import Cartola
from django.shortcuts import render
from django.views.generic import View


class Players(View):
    response_template = 'player.html'

    def _calculate_valorization(self, price, last_pontuation):
        y = (price / 100) * 37
        z = y * 2
        total_points = z - last_pontuation
        return total_points

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
            i['to_valorizate'] = self._calculate_valorization(i['preco_num'], i['pontos_num'])
            new_data['atletas'].append(i)

        return render(request, self.response_template, {'data': new_data})


class Team(View):
    response_template = 'templates/my_team.html'

    def get(self, request):
        c = Cartola()
        data = c.make_request('my_team')

        # sorted = {'atletas': list()}
        # most_valueble = 0
        # for i in data['atletas']:

        return render(request, self.response_template, {'data': data})
