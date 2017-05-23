class Cartola(object):
	
	def __init__(self, player, price, last_pontuation):
		self.player = player
		self.price = price
		self.last_pontuation = last_pontuation

	def calculateValorization(self):
		y = (self.price / 100) * 37
		z = y * 2
		total_points = z - self.last_pontuation
		str_to_return = 'O jogador {} precisa fazer {} para valorizar'.format(self.player, total_points)
		return str_to_return