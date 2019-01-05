from game.game import Game
from artificial_players.random_chancer import RandomChancer
from artificial_players.minimax_fixed_depth import MinimaxFixedDepth
from artificial_players.minimax_variable_depth import MinimaxVariableDepth

artificial_player_1 = RandomChancer('red')
artificial_player_2 = RandomChancer('black')
artificial_player_3 = MinimaxVariableDepth('red')
artificial_player_4 = MinimaxFixedDepth('black', depth=3)

game = Game()

game.add_artificial_player(artificial_player_3)
game.add_artificial_player(artificial_player_4)

