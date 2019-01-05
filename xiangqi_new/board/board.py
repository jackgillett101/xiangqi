from board.corner import Corner
from pieces.piece_factory import PieceFactory


class Board:
    horizontal_labels = Corner.horizontal_labels

    def __init__(self, layout=None):
        self.corners = [[[] for y in range(0, 10)] for x in range(0, 9)]

        for x in range(0, 9):
            for y in range(0, 10):
                self.corners[x][y] = Corner(self, x, y)

                # If a layout was passed in, set it up now
                if layout is not None:
                    piece_name, colour = layout[x][y]
                    if piece_name is not None:
                        piece = PieceFactory.create_piece_from_name(piece_name, x, y, colour, self)
                        #self.corners[x][y].register_piece(piece)

    def check_indices(self, x_location, y_location):
        if 0 > x_location or 0 > y_location or 9 <= x_location or 10 <= y_location:
            return False
        else:
            return True

    def get_corner(self, x_location, y_location):
        if self.check_indices(x_location, y_location):
            return self.corners[x_location][y_location]
        else:
            raise KeyError("The cell requested is out of range of the board")

    def get_pieces_for_colour(self, colour):
        pieces = []
        for row in self.corners:
            for corner in row:
                if corner.is_occupied():
                    if corner.colour_of_occupant() == colour:
                        pieces.append(corner.get_occupant())

        return pieces

    @staticmethod
    def location_string_to_corner(location_string):
        if len(location_string) != 2 or location_string[0] not in Board.horizontal_labels \
                or int(location_string[1]) < 0 or int(location_string[1]) > 9:
            raise KeyError("location_strings must be of format C4, first letter A-I and second number 0-9")

        column_number = Board.horizontal_labels.index(location_string[0])
        row_number = int(location_string[1])

        return column_number, row_number

    # Returns a list-of-lists for each corner, with (occupant_name, colour) for each
    def machine_readable_layout(self):
        output = [[[] for y in range(0, 10)] for x in range(0, 9)]
        for x in range(0, 9):
            for y in range(0, 10):
                occupant = self.corners[x][y].get_occupant()
                colour = None if occupant is None else occupant.colour
                occupant_name = None if occupant is None else occupant.piece_name
                output[x][y] = occupant_name, colour

        return output

    def __repr__(self):
        visual_representation = list(map(list, zip(*self.corners)))

        col_indices = ["０", "１", "２", "３", "４", "５", "６", "７", "８", "９"]
        rows = ""
        for i, corners in enumerate(visual_representation):
            row = "－".join(list(map(lambda x: x.pretty_print(), corners)))
            rows = row + "\u3000" + col_indices[i] + "\n" + rows

            if i == 4:
                # rows = rows + "－－－－－－－－－－－－－－－－－\n"
                rows = "｜\u3000\u3000\u3000楚河\u3000\u3000\u3000\u3000\u3000漢界\u3000\u3000\u3000｜\n" + rows
                # rows = rows + "－－－－－－－－－－－－－－－－－\n"

        rows = rows + "Ａ\u3000Ｂ\u3000Ｃ\u3000Ｄ\u3000Ｅ\u3000Ｆ\u3000Ｇ\u3000Ｈ\u3000Ｉ"
        return rows
