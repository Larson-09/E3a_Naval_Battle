"""
@author LAUDE Jordan and SARLAT Meven
"""

from Classes.Submarine import Submarine
from Classes.Board import Board

class Player():

    # CONSTRUCTOR ======================================================================================================

    def __init__(self, name, nb_columns, nb_rows):
        """ The PLayer initializer

        @param name         The name of the player
        @param nb_columns   The number of columns for the boards
        @param nb_rows      The number of rows for the boards
        """

        self.name = name
        self.ally_board = Board(nb_columns, nb_rows)
        self.enemy_board = Board(nb_columns, nb_rows)

        self.submarines = []

    # GETTERS ==========================================================================================================

    def get_name(self):
        return self.name

    def get_ally_board(self):
        return self.ally_board

    def get_enemy_board(self):
        return self.enemy_board

    def get_submarines(self):
        return self.submarines

    def get_submarine(self, index):
        return self.submarines[index]

    # OTHERS ===========================================================================================================

    def add_sbm(self, row, col, layer, size, direction):
        """ Methode used to create and initialize a new player's submarine

        @param row          The row coordinate of the head of the submarine
        @param col          The column coordinate of the head of the submarine
        @param layer        The layer of the submarine
        @param size         The number of squares of the submarine
        @param direction    The direction of the submarine
        """

        sbm = Submarine(row, col, layer, size, direction)
        self.submarines.append(sbm)
