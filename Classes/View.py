"""
@author LAUDE Jordan and SARLAT Meven
"""

from Utils.Enums import State
from Classes.Player import Player
from Classes.Board import Board
import numpy as np

class View:

    # CONSTRUCTOR ======================================================================================================

    def __init__(self):
        """ The View constructor
        """

    def display_welcome_message(self):
        print()
        print("            WELCOME TO SEA BATTLE !!\n")
        print("                     _")
        print("                    | \\")
        print("                     '.|")
        print("     _-   _-    _-  _-||    _-    _-  _-   _-    _-    _-")
        print("       _-    _-   - __||___    _-       _-    _-    _-")
        print("    _-   _-    _-  |   _   |       _-   _-    _-")
        print("      _-    _-    /_) (_) (_\        _-    _-       _-")
        print("              _.-'           `-._      ________       _-")
        print("        _..--`                   `-..'       .'")
        print("    _.-'  o/o                     o/o`-..__.'        ~  ~")
        print(" .-'      o|o        ESEO         o|o      `.._.  // ~  ~")
        print(" `-._     o|o                     o|o        |||<|||~  ~")
        print("     `-.__o\o                     o|o       .'-'  \\ ~  ~")
        print("          `-.______________________\_...-``'.       ~  ~")
        print("                                    `._______`.\n")

        print("Rules :\n"
              "- You will be playing turn by turn\n"
              "- Type STOP at any time after submarine placement to stop the game \n "
              "(it will be saved and you will be able to reload this game next time just by selecting the saving file in Saves/Year/Month/Day/File)\n")

    # DISPLAY METHODS ==================================================================================================

    def display_player_to_play(self, current_player):
        """ Display the name of the player who is about to play a turn

        @param current_player the player who is about to play a turn
        """

        print("=======================", current_player.name.upper(), "===============================================")

    def display_boards(self, board_to_display):
        """ Display the content of boards

        @param board_to_display the board to display
        """

        # Get values of the enum
        board_to_display_cpy = Board(10, 5)
        layer_idx = 0

        for layer in board_to_display_cpy.get_layers():

            nb_rows = np.shape(layer)[0]
            nb_columns = np.shape(layer)[1]
            for i in range(nb_rows) :
                for j in range(nb_columns):
                    layer[i][j] = board_to_display.get_layers()[layer_idx][i][j].value

            layer_idx += 1

        # Print layers
        col_indexes = ""
        for col_idx in range(nb_columns):
            col_indexes += "    " + str(col_idx)

        layer_idx = 0
        for layer in board_to_display_cpy.get_layers():

            # display the depth of the sea
            layer_idx += 1
            print(str(layer_idx * 100) + "m sea")

            # display the columns index
            print(col_indexes)

            # display the rows
            for i in range(len(layer)):
                print(i, layer[i])
            print()

    def display_out_of_bound_input(self):
        print()
        print("You chose a value which is out of the board range, please select another value")


    def display_wrong_input_type(self):
        print()
        print("You chose a non-integer value, please select another value")


    def display_result(self, winner):
        """ Display the result of the game

        @param winner the player who won the game
        """

        print("The game is finished, the winner is", winner.name + " !!")

