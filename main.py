from poker_monte_carlo.combinations import find_best_combination
from poker_monte_carlo.parser import parse_board, parse_hand

hand = parse_hand('2c 2s')
board = parse_board('Ac 3s 6h 3d 4d')


print(find_best_combination(hand, board))
