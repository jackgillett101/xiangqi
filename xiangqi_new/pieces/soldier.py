from pieces.piece import Piece


class Soldier(Piece):
    def __init__(self, x_location, y_location, colour, board):
        super().__init__(x_location, y_location, colour, board)

        if colour == 'red':
            self.movement = +1
        else:
            self.movement = -1

        if self.colour == 'red':
            self.piece_name = "兵"
        else:
            self.piece_name = "卒"

    def valid_moves(self):
        valid_cells = []

        if 0 <= self.y_location + self.movement < 9:
            valid_cells.append(self.board.get_corner(self.x_location, self.y_location + self.movement))

        if (self.y_location >= 5 and self.colour == 'red') or (self.y_location <= 4 and self.colour == 'black'):
            if self.x_location > 0:
                valid_cells.append(self.board.get_corner(self.x_location - 1, self.y_location))
            if self.x_location < 8:
                valid_cells.append(self.board.get_corner(self.x_location + 1, self.y_location))

        valid_cells = super().remove_cells_containing_ally(valid_cells)
        return valid_cells

    def __repr__(self):
        return "Solder at {}".format(self.current_location)
