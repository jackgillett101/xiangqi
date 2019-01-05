class Corner:
    horizontal_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    def __init__(self, board, x_location, y_location):
        self.board = board

        self.x_location = x_location
        self.y_location = y_location

        self.current_occupant = None

    def get_coords(self):
        return self.x_location, self.y_location

    def get_pretty_coords(self):
        return "{}{}".format(Corner.horizontal_labels[self.x_location], self.y_location)

    def register_piece(self, piece):
        if self.current_occupant is not None:
            raise KeyError("{} is already occupied!".format(self))
        else:
            self.current_occupant = piece

    def remove_piece(self):
        if self.current_occupant is None:
            raise KeyError("Can't remove piece from {} - no piece exists there!".format(self))

        self.current_occupant = None

    def new_piece_arrives(self, piece):
        game_state = (True, None)

        if self.current_occupant is not None:
            print("{} arrives and eats {} currently on the corner!"
                  .format(piece.pretty_print(), self.current_occupant.pretty_print()))

            game_state = self.current_occupant.die()

        self.current_occupant = piece

        return game_state

    def is_occupied(self):
        return self.current_occupant is not None

    def get_occupant(self):
        return self.current_occupant

    def colour_of_occupant(self):
        if self.current_occupant is None:
            return None
        else:
            return self.current_occupant.get_colour()

    def pretty_print(self):
        if self.is_occupied():
            return self.current_occupant.pretty_print()
        else:
            return "＋"

    def __repr__(self):
        return "Cell: {}, {}".format(self.x_location, self.y_location)
