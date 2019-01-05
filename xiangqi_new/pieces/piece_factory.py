from pieces.soldier import Soldier
from pieces.cannon import Cannon
from pieces.car import Car
from pieces.horse import Horse
from pieces.elephant import Elephant
from pieces.guard import Guard
from pieces.general import General


class PieceFactory:

    names_to_subclasses = {
        "炮": Cannon,
        "砲": Cannon,
        "车": Car,
        "相": Elephant,
        "象": Elephant,
        "帅": General,
        "将": General,
        "士": Guard,
        "马": Horse,
        "兵": Soldier,
        "卒": Soldier
    }

    # A static factory method to create pieces from their names. Should centralise this soon
    @staticmethod
    def create_piece_from_name(piece_name, x_location, y_location, colour, board):
        piece_type = PieceFactory.names_to_subclasses[piece_name]

        return piece_type(x_location, y_location, colour, board)
