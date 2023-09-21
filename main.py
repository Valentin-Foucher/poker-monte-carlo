from poker_monte_carlo import stack
from poker_monte_carlo.combinations import find_best_combination, compare_combinations
from poker_monte_carlo.parser import parse_board, parse_hand

s = stack.generate_stack()

first_player_hand = parse_hand(stack.draw_hand(s))
second_player_hand = parse_hand(stack.draw_hand(s))

print(f'first player hand: {first_player_hand}')
print(f'Second player hand: {second_player_hand}\n')

board = stack.draw_flop(s)
parsed_board = parse_board(board)
print(f'Board: {parsed_board}')
print(f'first player hand: {find_best_combination(first_player_hand, parsed_board).combination} - '
      f'{find_best_combination(first_player_hand, parsed_board).cards}')
print(f'Second player hand: {find_best_combination(second_player_hand, parsed_board).combination} - '
      f'{find_best_combination(second_player_hand, parsed_board).cards}\n')


board = stack.draw_turn(s, board)
parsed_board = parse_board(board)
print(f'Board: {parsed_board}')
print(f'first player hand: {find_best_combination(first_player_hand, parsed_board).combination} - '
      f'{find_best_combination(first_player_hand, parsed_board).cards}')
print(f'Second player hand: {find_best_combination(second_player_hand, parsed_board).combination} - '
      f'{find_best_combination(second_player_hand, parsed_board).cards}\n')

board = stack.draw_river(s, board)
parsed_board = parse_board(board)
print(f'Board: {parsed_board}')
print(f'first player hand: {find_best_combination(first_player_hand, parsed_board).combination} - '
      f'{find_best_combination(first_player_hand, parsed_board).cards}')
print(f'Second player hand: {find_best_combination(second_player_hand, parsed_board).combination} - '
      f'{find_best_combination(second_player_hand, parsed_board).cards}\n')


result = compare_combinations(find_best_combination(first_player_hand, parsed_board),
                              find_best_combination(second_player_hand, parsed_board))

if result == 1:
    print('Player 1 wins')
elif result == -1:
    print('Player 2 wins')
else:
    print('Draw')

