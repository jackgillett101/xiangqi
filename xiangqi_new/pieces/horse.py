from pieces.piece import Piece


class Horse(Piece):
    def __init__(self, x_location, y_location, colour, board):
        super().__init__(x_location, y_location, colour, board)

        self.piece_name = "马"

    def valid_moves(self):
        valid_cells = []

        for x_direction, y_direction in [(+1, 0), (-1, 0), (0, +1), (0, -1)]:
            x_blocking, y_blocking = self.x_location + x_direction, self.y_location + y_direction

            if self.board.check_indices(x_blocking, y_blocking):
                blocking_cell = self.board.get_corner(x_blocking, y_blocking)

                if not blocking_cell.is_occupied():
                    x_location, y_location = 2 * x_direction, 2 * y_direction

                    for z in [+1, -1]:
                        x_move = x_location if x_location != 0 else z
                        y_move = y_location if y_location != 0 else z
                        x_move_coords, y_move_coords = self.x_location + x_move, self.y_location + y_move

                        if self.board.check_indices(x_move_coords, y_move_coords):
                            cell = self.board.get_corner(x_move_coords, y_move_coords)
                            valid_cells.append(cell)

        valid_cells = super().remove_cells_containing_ally(valid_cells)
        return valid_cells

    def __repr__(self):
        return "Horse at {}".format(self.current_location)
