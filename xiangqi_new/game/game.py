from board.board import Board
from pieces.soldier import Soldier
from pieces.cannon import Cannon
from pieces.car import Car
from pieces.horse import Horse
from pieces.elephant import Elephant
from pieces.guard import Guard
from pieces.general import General
import time


class Game:
    def __init__(self):
        self.whose_turn = 'red'

        self.board = Board()
        self.setup_board(self.board)
        print(self.board)

        self.artificial_players = {'red': None, 'black': None}

    def add_artificial_player(self, player):
        if self.artificial_players[player.get_colour()] is not None:
            raise KeyError("Already have an artificial player for {}!".format(player.get_colour()))

        self.artificial_players[player.get_colour()] = player
        self.artificial_players_take_turns(True, None, self.whose_turn, self.board)

    def setup_board(self, board):
        for team in [{'colour': 'red', 'back_row': 0, 'cannon_row': 2, 'soldier_row': 3},
                     {'colour': 'black', 'back_row': 9, 'cannon_row': 7, 'soldier_row': 6}]:

            for x in [0, 2, 4, 6, 8]:
                soldier = Soldier(x, team['soldier_row'], team['colour'], board)

            for x in [+1, -1]:
                cannon = Cannon(4 + x * 3, team['cannon_row'], team['colour'], board)
                car = Car(4 + x * 4, team['back_row'], team['colour'], board)
                horse = Horse(4 + x * 3, team['back_row'], team['colour'], board)
                elephant = Elephant(4 + x * 2, team['back_row'], team['colour'], board)
                guard = Guard(4 + x * 1, team['back_row'], team['colour'], board)

            general = General(4, team['back_row'], team['colour'], board)

    def artificial_player_takes_turn(self):
        if self.artificial_players[self.whose_turn] is not None:
            move_string = self.artificial_players[self.whose_turn].make_move(self.board.machine_readable_layout())

            return self.move(move_string)
        else:
            return None

    def artificial_players_take_turns(self, game_continues, losing_team, whose_turn, board):
        while game_continues:
            artificial_turn = self.artificial_player_takes_turn()

            if artificial_turn is None:
                break
            else:
                game_continues, losing_team, whose_turn, board = artificial_turn

        return game_continues, losing_team, whose_turn, board

    def move(self, move_string):
        game_continues, losing_team, whose_turn, board = self.move_action(move_string)

        game_continues, losing_team, whose_turn, board = \
            self.artificial_players_take_turns(game_continues, losing_team, whose_turn, board)

        return game_continues, losing_team, whose_turn, board

    def move_action(self, move_string):
        # move_string must be of the format 'A3-A5', for piece on A3 moves to A5
        start_location, finish_location = move_string.split('-')

        start_column, start_row = Board.location_string_to_corner(start_location)
        finish_column, finish_row = Board.location_string_to_corner(finish_location)

        start_corner = self.board.get_corner(start_column, start_row)

        if not start_corner.is_occupied():
            raise KeyError("Corner {} is unoccupied, so can't move from here!".format(start_location))

        if start_corner.colour_of_occupant() != self.whose_turn:
            raise KeyError("It's {}'s turn but piece on {} is {}"
                           .format(self.whose_turn, start_location, start_corner.colour_of_occupant()))

        game_continues, losing_team = start_corner.get_occupant().move_piece(finish_column, finish_row)

        if self.whose_turn == 'red':
            self.whose_turn = 'black'
        else:
            self.whose_turn = 'red'

        print(self.board)
        time.sleep(2)

        return game_continues, losing_team, self.whose_turn, self.board
