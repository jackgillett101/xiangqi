from abc import abstractmethod


class EvaluationFunction:
    def __init__(self):
        pass

    @abstractmethod
    def evaulate_board(self, board_layout, colour_perspective):
        pass
