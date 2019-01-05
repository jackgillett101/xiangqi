from artificial_players.artificial_player import ArtificialPlayer
from artificial_players.static_evaluation_functions.material_count import MaterialCount
from board.board import Board
from copy import deepcopy
from random import shuffle


# At each turn, variable depth minimax runs asd N-depth look-forward search with leaves evaluated according
# to a specified evaluation function. However, it will continue to evaluate some additional deeper branches
# based on some heuristics (eg. it will continue down branches where pieces are taken), before evaluating the
# static position at the bottom of each branch
class MinimaxVariableDepth(ArtificialPlayer):
    def __init__(self, colour, min_depth=3, max_depth=6, symmetry_check=True, leaf_evaluation_function=MaterialCount()):
        super().__init__(colour)

        self.leaf_evaluation_function = leaf_evaluation_function
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.symmetry_check = symmetry_check
        self.counter = 0
        self.top_level_counter = 0

    def make_move(self, board_layout):
        best_move, score = self.minimax(board_layout,
                                        depth=self.min_depth,
                                        colour_perspective=self.colour,
                                        remember_move=True)

        chosen_start, chosen_destination = best_move

        move_string = ArtificialPlayer.get_move_string_from_coords(chosen_start, chosen_destination)

        print("VariableDepthMinimax traverses a pruned tree, and digs out {}".format(move_string))
        self.counter = 0
        self.top_level_counter = 0
        return move_string

    def minimax(self, board_layout, depth, colour_perspective, remember_move=False):
        self.counter += 1

        if depth == self.min_depth - 1:
            self.top_level_counter += 1
            print("{} top-level evaluations".format(self.top_level_counter))

        if self.counter % 1000 == 0:
            print("Minimax has evaluated {} positions so far".format(self.counter))

        # If we've hit our max depth, break out of the loop here (otherwise trees can take a LONG time)
        termination_value = self.leaf_evaluation_function.evaulate_board(board_layout)
        if depth <= self.min_depth - self.max_depth:
            return termination_value

        # Creating a shadow board is the slow step, as it involves a deep copy of the current board. An alternative
        # faster approach would be to play out each tree on the existing board, but we'd have to be *very careful* to
        # reset it to the current position after each move
        new_colour = 'red' if colour_perspective == 'black' else 'black'
        shadow_board = Board(board_layout)
        all_possible_moves = self.all_possible_moves(shadow_board, colour_perspective)
        shuffle(all_possible_moves)

        max_score = {colour_perspective: -1e6, new_colour: 1e6}
        best_move = None

        # If symmetry check is set to true, we do a quick check here for reflectional symmetry on the board, and
        # remove equivalent moves if symmetric. This drastically speeds up the first move, but is unlikely to help
        # any subsequent moves - currently not sure if this is overall beneficial or not. Could restrict to first
        # move only if checking turns out to be costly
        if self.symmetry_check:
            symmetry = True
            for i in [0, 1, 2, 3]:
                if board_layout[i] != board_layout[-i-1]:
                    symmetry = False

            # If we're here, board is completely symmetrical about the central column - filter out moves on the RHS
            if symmetry:
                all_possible_moves = list(filter(lambda x: x[0].get_coords()[0] <= 4, all_possible_moves))

        for move in all_possible_moves:

            # Depth check is now done in here. Any moves involving captures are allowed to run their course,
            # other moves are cut off here if we're at or below max depth
            initial_corner, destination_corner = move
            if depth <= 0 and destination_corner.get_occupant() is None:
                score = termination_value
            # Also ignore soldier, advisor captures as there are many of these and they're low value
            elif depth <= 0 and destination_corner.get_occupant().piece_name in ["兵", "卒", "士"]:
                score = termination_value
            else:
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
