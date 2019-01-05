from pieces.piece import Piece


class Cannon(Piece):
    def __init__(self, x_location, y_location, colour, board):
        super().__init__(x_location, y_location, colour, board)

        if self.colour == 'red':
            self.piece_name = "炮"
        else:
            self.piece_name = "砲"

    def valid_moves(self):
        valid_cells = []

        for x_direction, y_direction in [(+1, 0), (-1, 0), (0, +1), (0, -1)]:
            jump_count = 0
            x_current, y_current = self.x_location + x_direction, self.y_location + y_direction

            while self.board.check_indices(x_current, y_current):
                cell = self.board.get_corner(x_current, y_current)
                if not cell.is_occupied() and jump_count == 0:
                    valid_cells.append(cell)
                elif cell.is_occupied() and jump_count == 1:
                    valid_cells.append(cell) # Don't need to check colour as ally pieces are filtered later
                    break
                elif cell.is_occupied():
                    # We can jump the piece and take the next one, if it's an enemy
                    jump_count += 1
                    if jump_count > 1:
                        break

                x_current, y_current = x_current + x_direction, y_current + y_direction

        valid_cells = super().remove_cells_containing_ally(valid_cells)
        return valid_cells

    def __repr__(self):
        return "Cannon at {}".format(self.current_location)
