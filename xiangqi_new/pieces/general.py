from pieces.piece import Piece


class General(Piece):
    def __init__(self, x_location, y_location, colour, board):
        super().__init__(x_location, y_location, colour, board)

        if self.colour == 'red':
            self.piece_name = "帅"
        else:
            self.piece_name = "将"

    # General overrides the die method - if general dies, the game is over!
    def die(self):
        print("{} loses the game as their general falls".format(self.colour))

        return False, self.colour

    def valid_moves(self):
        valid_cells = []

        for x_direction, y_direction in [(+1, 0), (-1, 0), (0, +1), (0, -1)]:
            x_current, y_current = self.x_location + x_direction, self.y_location + y_direction

            if self.board.check_indices(x_current, y_current):
                if 3 <= x_current <= 5 and 0 <= y_current <= 2:
                    cell = self.board.get_corner(x_current, y_current)
                    valid_cells.append(cell)

        # TODO: Flying general move here...

        valid_cells = super().remove_cells_containing_ally(valid_cells)
        return valid_cells

    def __repr__(self):
        return "General at {}".format(self.current_location)
