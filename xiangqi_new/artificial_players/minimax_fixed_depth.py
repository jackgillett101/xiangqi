from artificial_players.artificial_player import ArtificialPlayer
from artificial_players.static_evaluation_functions.material_count import MaterialCount
from board.board import Board
from copy import deepcopy
from random import shuffle


# At each turn, fixed depth minimax runs asd N-depth look-forward search with leaves evaluated according
# to a specified evaluation function, and takes the best option found
class MinimaxFixedDepth(ArtificialPlayer):
    def __init__(self, colour, depth=3, leaf_evaluation_function=MaterialCount()):
        super().__init__(colour)

        self.leaf_evaluation_function = leaf_evaluation_function
        self.depth = depth
        self.counter = 0

    def make_move(self, board_layout):
        best_move, score = self.minimax(board_layout,
                                        depth=self.depth,
                                        colour_perspective=self.colour,
                                        remember_move=True)

        chosen_start, chosen_destination = best_move

        move_string = ArtificialPlayer.get_move_string_from_coords(chosen_start, chosen_destination)

        print("FixedDepthMinimax has run the numbers, and plays {}".format(move_string))
        self.counter = 0
        return move_string

    def minimax(self, board_layout, depth, colour_perspective, remember_move=False):
        self.counter += 1
        if self.counter % 1000 == 0:
            print("Minimax has evaluated {} positions so far".format(self.counter))

        if depth == 0:
            return self.leaf_evaluation_function.evaulate_board(board_layout)

        new_colour = 'red' if colour_perspective == 'black' else 'black'
        shadow_board = Board(board_layout)
        all_possible_moves = self.all_possible_moves(shadow_board, colour_perspective)
        shuffle(all_possible_moves)

        max_score = {colour_perspective: -1e6, new_colour: 1e6}
        best_move = None

        #if depth == 3:
            #all_possible_moves = list(filter(lambda x: x[0].get_occupant().piece_name == "炮" and (x[1].get_coords()[1] == 9 or x[1].get_coords()[1] == 3), all_possible_moves))

        for move in all_possible_moves:
            #if depth == 3 and move[0].get_occupant().piece_name == "炮" and (move[1].get_coords()[1] == 9 or move[1].get_coords()[1] == 2):
            #    print("interesting")
            #if depth == 2: # and (shadow_board.get_corner(1, 9).get_occupant().piece_name == "炮" or
            #                   shadow_board.get_corner(7, 9).get_occupant().piece_name == "炮"):
            #    print("interesting")

            new_layout, winning_colour = self.apply_move(board_layout, move)

            # Found a winning move - break here. Found a losing move - ignore it!
            if winning_colour is not None:
                if winning_colour == colour_perspective:
                    max_score = {colour_perspective: 1e8, new_colour: -1e8}
                    best_move = move
                    break
                else:
                    continue

            score = self.minimax(new_layout, depth=depth-1, colour_perspective=new_colour)

            #if depth == 3 and move[0].get_occupant().piece_name == "炮" and move[1].get_coords()[1] == 9:
            #    print("interesting")

            if score[colour_perspective] > max_score[colour_perspective]:
                max_score = score
                best_move = move

        if remember_move is True:
            return best_move, max_score
        else:
            return max_score

    def apply_move(self, board_layout, move):
        initial_corner, destination_corner = move

        winning_colour = None
        target_occupant = destination_corner.get_occupant()
        if target_occupant is not None:
            if target_occupant.piece_name == "帅":
                winning_colour = 'black'
            if target_occupant.piece_name == "将":
                winning_colour = 'red'

        from_x_location, from_y_location = initial_corner.get_coords()
        to_x_location, to_y_location = destination_corner.get_coords()

        new_layout = deepcopy(board_layout)
        new_layout[to_x_location][to_y_location] = new_layout[from_x_location][from_y_location]
        new_layout[from_x_location][from_y_location] = None, None

        return new_layout, winning_colour
