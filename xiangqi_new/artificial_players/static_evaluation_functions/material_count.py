from artificial_players.static_evaluation_functions.evaluation_function import EvaluationFunction
from pieces.piece_factory import PieceFactory
from pieces.soldier import Soldier
from pieces.cannon import Cannon
from pieces.car import Car
from pieces.horse import Horse
from pieces.elephant import Elephant
from pieces.guard import Guard
from pieces.general import General


class MaterialCount(EvaluationFunction):
    def __init__(self):
        pass

    def evaulate_board(self, board_layout):
        material_balance = 0

        for row in board_layout:
            for piece, colour in row:
                if piece is not None:
                    multiplier = 1 if colour == 'red' else -1
                    material_balance += multiplier * MaterialCount.evaluate_piece(piece)

        return {'red': material_balance, 'black': -1 * material_balance}

    @staticmethod
    def evaluate_piece(piece):
        piece_class = PieceFactory.names_to_subclasses[piece].__name__
        if piece_class == "Soldier":
            return 3
        if piece_class == "Cannon":
            return 7
        if piece_class == "Car":
            return 10
        if piece_class == "Horse":
            return 5
        if piece_class == "Elephant":
            return 3
        if piece_class == "Guard":
            return 2
        if piece_class == "General":
            return 1e8
