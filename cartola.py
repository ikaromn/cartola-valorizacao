import sys
import cartolaValorization as cv

player_name = sys.argv[1]
player_price = float(sys.argv[2])
player_pontuation = float(sys.argv[3])

a = cv.Cartola(player_name,player_price,player_pontuation)

b = a.calculateValorization()
print(b)