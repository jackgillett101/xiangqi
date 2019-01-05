from pieces.piece import Piece


class Elephant(Piece):
    def __init__(self, x_location, y_location, colour, board):
        super().__init__(x_location, y_location, colour, board)

        if self.colour == 'red':
            self.piece_name = "相"
        else:
            self.piece_name = "象"

    def valid_moves(self):
        valid_cells = []

        for x_direction, y_direction in [(+2, +2), (+2, -2), (-2, +2), (-2, -2)]:
            x_current, y_current = self.x_location + x_direction, self.y_location + y_direction
            x_blocking, y_blocking = self.x_location + int(x_direction / 2), self.y_location + int(y_direction / 2)

            if self.colour == 'red' and y_current <= 4 or self.colour == 'black' and y_current >= 5:
                if self.board.check_indices(x_current, y_current):
                    cell = self.board.get_corner(x_current, y_current)
                    blocking_cell = self.board.get_corner(x_blocking, y_blocking)

                    if not blocking_cell.is_occupied():
                        valid_cells.append(cell)

        valid_cells = super().remove_cells_containing_ally(valid_cells)
        return valid_cells

    def __repr__(self):
        return "Elephant at {}".format(self.current_location)
