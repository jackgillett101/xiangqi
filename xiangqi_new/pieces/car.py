from pieces.piece import Piece


class Car(Piece):
    def __init__(self, x_location, y_location, colour, board):
        super().__init__(x_location, y_location, colour, board)

        self.piece_name = "车"

    def valid_moves(self):
        valid_cells = []

        for x_direction, y_direction in [(+1, 0), (-1, 0), (0, +1), (0, -1)]:
            x_current, y_current = self.x_location + x_direction, self.y_location + y_direction

            while self.board.check_indices(x_current, y_current):
                cell = self.board.get_corner(x_current, y_current)
                valid_cells.append(cell)

                if cell.is_occupied():
                    break

                x_current, y_current = x_current + x_direction, y_current + y_direction

        valid_cells = super().remove_cells_containing_ally(valid_cells)
        return valid_cells

    def __repr__(self):
        return "Car at {}".format(self.current_location)
