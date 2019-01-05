from pieces.piece import Piece


class Guard(Piece):
    def __init__(self, x_location, y_location, colour, board):
        super().__init__(x_location, y_location, colour, board)

        self.piece_name = "士"

    def valid_moves(self):
        valid_cells = []

        for x_direction, y_direction in [(+1, +1), (+1, -1), (-1, +1), (-1, -1)]:
            x_current, y_current = self.x_location + x_direction, self.y_location + y_direction

            if self.board.check_indices(x_current, y_current):
                if 3 <= x_current <= 5 and (0 <= y_current <= 2 and self.colour == 'red'\
                                            or 7 <= y_current <= 9 and self.colour == 'black'):
                    cell = self.board.get_corner(x_current, y_current)
                    valid_cells.append(cell)

        valid_cells = super().remove_cells_containing_ally(valid_cells)
        return valid_cells

    def __repr__(self):
        return "Guard at {}".format(self.current_location)
