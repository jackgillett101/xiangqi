from abc import abstractmethod
from itertools import product


class ArtificialPlayer:
    def __init__(self, colour):
        self.colour = colour

    @abstractmethod
    def make_move(self, board_layout):
        pass

    # Several sub-classes will want a list of all possible moves, so generate it here
    def all_possible_moves(self, board, colour_perspective):
        my_pieces = board.get_pieces_for_colour(colour_perspective)
        possible_moves = []

        for piece in my_pieces:
            current_location = [piece.get_location()]
            valid_moves = piece.valid_moves()

            possible_moves += list(product(current_location, valid_moves))

        return possible_moves

    @staticmethod
    def get_move_string_from_coords(start_corner, finish_corner):
        return "{}-{}".format(start_corner.get_pretty_coords(), finish_corner.get_pretty_coords())

    def get_colour(self):
        return self.colour
