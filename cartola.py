import sys

player_name = sys.argv[1]
player_price = float(sys.argv[2])
player_pontuation = float(sys.argv[3])

def player_valorization(player_name, player_price, player_pontuation):
	y = (player_price / 100) * 37
	z = y * 2
	total_points = z - player_pontuation
	print('O jogador %s precisa fazer %s para valorizar' % (player_name, total_points))

player_valorization(player_name, player_price, player_pontuation)