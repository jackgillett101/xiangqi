from artificial_players.artificial_player import ArtificialPlayer
from board.board import Board
import random


# At each turn, random chancer plays a random move uniformly chosen from the valid possibilities
class RandomChancer(ArtificialPlayer):
    def __init__(self, colour):
        super().__init__(colour)

    def make_move(self, board_layout):
        board = Board(layout=board_layout)

        possible_moves = self.all_possible_moves(board, self.colour)

        (chosen_start, chosen_destination) = random.choice(possible_moves)

        move_string = ArtificialPlayer.get_move_string_from_coords(chosen_start, chosen_destination)

        print("RamdomChancer has a master plan, and plays {}".format(move_string))
        return move_string
