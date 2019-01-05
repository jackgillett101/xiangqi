from abc import abstractmethod


class Piece:
    def __init__(self, x_location, y_location, colour, board):
        self.x_location = x_location
        self.y_location = y_location

        if colour not in ['red', 'black']:
            raise KeyError("Colour must be 'red' or 'black', '{}' not valid".format(colour))
        else:
            self.colour = colour

        self.board = board
        self.current_location = self.board.get_corner(x_location, y_location)
        self.current_location.register_piece(self)

    def move_piece(self, x_location, y_location):
        valid_moves = self.valid_moves()

        new_location = self.board.get_corner(x_location, y_location)
        if new_location not in valid_moves:
            raise KeyError("Can't move to {}, not a valid move!".format((x_location, y_location)))

        game_state = new_location.new_piece_arrives(self)

        self.current_location.remove_piece()
        self.current_location = new_location

        self.x_location = x_location
        self.y_location = y_location

        return game_state

    def die(self):
        return True, None

    def get_colour(self):
        return self.colour

    def get_location(self):
        return self.current_location

    @abstractmethod
    def valid_moves(self):
        pass

    def pretty_print(self):
        if self.colour == 'red':
            return "\x1b[1;30;41m{}\x1b[0m".format(self.piece_name)
        else:
            return "{}".format(self.piece_name)

    def remove_cells_containing_ally(self, valid_cells):
        return list(filter(lambda x: x.colour_of_occupant() != self.colour, valid_cells))
