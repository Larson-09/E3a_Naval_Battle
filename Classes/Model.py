"""
@author LAUDE Jordan and SARLAT Meven
"""

from Classes.Player import Player
from Classes.View import View
from Classes.Board import Board
from Utils.Enums import State, Direction

from datetime import datetime
import sys
import os
import csv
from tkinter import *
from tkinter.filedialog import askopenfilename

class Model:

    # CONSTRUCTOR ======================================================================================================

    def __init__(self, nb_columns, nb_rows, nb_submarines):
        """ The model constructor

        @param player_1_name the name of the first player
        @param player_2_name the name of the second player
        """

        # Init boards parameters
        self.nb_columns = nb_columns
        self.nb_rows = nb_rows
        self.nb_submarines = nb_submarines

        # Init view
        self.view = View()

        # Init the end of game marker
        self.is_game_finished_marker = False

        # Init players parameters
        player_1_name = input("What is your name player 1 ?")
        player_2_name = input("What is your name player 2 ?")

        self.player1 = Player(player_1_name, nb_columns, nb_rows)
        self.player2 = Player(player_2_name, nb_columns, nb_rows)
        self.players = [self.player1, self.player2]

        # Create the saving file
        self.saving_file_path = "Saves"
        year = datetime.now().strftime("%Y")
        month = datetime.now().strftime("%B")
        day = datetime.now().strftime("%d")
        dir_names = [year, month, day]

        for dir_name in dir_names :
            # Add the directory name to the path
            self.saving_file_path += "/" + dir_name

            # Check if the year directory already exists
            if not os.path.isdir(self.saving_file_path):
                os.mkdir(self.saving_file_path)

        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        date = date.replace(" ", "_")
        date = date.replace("/", "-")
        self.saving_file_path += "/" + player_1_name.upper() + "_vs_" + player_2_name.upper() + "_" + date + ".csv"

        # Display welcome message
        self.view.display_welcome_message()

        # Ask if the players want to reload a game
        resp = ""
        while resp != "Y" and resp != "y" and resp != "N" and resp != "n" and resp != "STOP":
            resp = input("Do you want to reload a saving file ? (Y/N)\n")

        if resp == "Y" or resp == "y":
            self.is_old_game_to_be_reload = True
            root = Tk()
            root.withdraw()
            self.backup_file_path = askopenfilename()
            root.destroy()

            # If the user close the window without selecting a file
            if self.backup_file_path == ():
                # Continue without loading a backup file
                self.is_old_game_to_be_reload = False

        elif resp == "N" or resp == "n":
            self.is_old_game_to_be_reload = False
        elif resp == "STOP":
            self.stop_the_game()

    # GETTERS / SETTERS ================================================================================================

    def get_player(self, idx_player):
        """ Method used to get a player

        @param idx_player the index of the player to return

        @return a player
        """
        return self.players[idx_player]

    # GLOBAL METHOD ====================================================================================================

    def launch_game(self):
        """ Manage the game
        """

        # If players want to reload an old game
        if self.is_old_game_to_be_reload:
            # Reload the selected game boards
            with open(self.backup_file_path) as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == "sbm_placement":
                        # Reload submarine placements
                        self.reload_saved_sbm(int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]), row[6])
                    elif row[0] == "make_a_shot":
                        # Reload shots
                        self.make_a_shot(int(row[1]), int(row[2]), int(row[3]), int(row[4]))

            # Display boards for player 1
            self.view.display_player_to_play(self.player1)
            print("There are your reloaded boards\n")
            self.view.display_boards(self.player1.ally_board)

            resp = "0"
            while resp != "":
                resp = input("Press [Enter] to see " + self.player2.get_name() + " reloaded submarine placement\n")

            # self.clear_console()

            # Display boards for player 2

            self.view.display_player_to_play(self.player2)
            print("There are your reloaded boards\n")
            self.view.display_boards(self.player2.ally_board)

            resp = "0"
            while resp != "":
                resp = input("Press [Enter] to go to the attacking phase\n")

            # self.clear_console()

        # Else, if players want to start a new game from scratch
        else :
            # Place submarines
            self.place_submarines(self.player1)
            self.view.display_boards(self.player1.ally_board)

            self.place_submarines(self.player2)
            self.view.display_boards(self.player2.ally_board)

        # Initialize the first player to play
        current_player = self.get_player(1)

        # Launch the game process
        while not self.is_game_finished_marker:

            # Play a turn
            self.one_turn(current_player)

            # Switch player if the game is not finished
            if not self.is_game_finished_marker:
                current_player = self.change_player(current_player)

        # Display who is the winner at the end of the game
        self.view.display_result(current_player)

    # TURN MANAGEMENT METHODS ==========================================================================================

    def one_turn(self, current_player):
        """ Manage a player turn

        @param current_player the current player
        """

        # Display the current player
        self.view.display_player_to_play(current_player)

        # Display that the player is in the attacking phase
        print("You are attacking !!")

        # Display the ally board
        print("Ally board after the enemy attack :")
        self.view.display_boards(current_player.ally_board)

        # Display the enemy board before the attack
        print("Enemy board before your attack :")
        self.view.display_boards(current_player.enemy_board)

        # Define the player under attack
        if current_player == self.player1:
            player_under_attack = self.player2
            player_under_attack_number = "2"
        elif current_player == self.player2:
            player_under_attack = self.player1
            player_under_attack_number = "1"

        # Make a shot
        row, col, layer = self.choose_coordinates_to_attack()
        while player_under_attack.get_ally_board().get_square_content(row, col, layer) == State.C:
            row, col, layer = self.choose_coordinates_to_attack()

        self.make_a_shot(player_under_attack_number, row, col, layer)

        # Display the enemy board after the attack
        print("Enemy board after the attack :")
        self.view.display_boards(current_player.enemy_board)

        # check if the game is finished

        if self.is_game_finished(player_under_attack):
            self.is_game_finished_marker = True

    def place_submarines(self, player):
        """ Allow players to place their submarines

        @param player The player who is placing his submarines
        """

        # Display who is placing his submarines
        print()
        self.view.display_player_to_play(player)
        print("Submarine placements")

        # Submarine placement
        for i in range(self.nb_submarines):
            size = i + 1
            print()
            print("--- SIZE " + str(size) + " SUBMARINE PLACEMENT ---")

            is_submarine_correctly_placed = False
            while not is_submarine_correctly_placed:

                # Ask for the row coordinate of the submarine
                row = -1

                print()
                while row not in range(self.nb_rows) or type(row) != int:
                    try:
                        row = int(input("Row for the submarine of size " + str(size) + " (between 0 and " + str(
                            self.nb_rows - 1) + ") : "))
                        if row not in range(self.nb_rows):
                            print()
                            self.view.display_out_of_bound_input()
                    except:
                        self.view.display_wrong_input_type()

                # Ask for the column coordinate of the submarine
                col = -1

                print()
                while col not in range(self.nb_columns):
                    try:
                        col = int(input("Column for the submarine of size " + str(size) + " (between 0 and " + str(
                            self.nb_columns - 1) + ") : "))
                        if col not in range(self.nb_columns):
                            self.view.display_out_of_bound_input()
                    except:
                        self.view.display_wrong_input_type()

                # Ask for the layer coordinate of the submarine
                layer = -1

                print()
                while layer not in range(3):
                    try:
                        layer = int(
                            input("layer for the submarine of size " + str(size) + " (0 : 100m, 1 : 200m, 2 : 300m)"))
                        if layer not in range(3):
                            self.view.display_out_of_bound_input()
                    except:
                        self.view.display_wrong_input_type()

                # Check that the chosen square is not already used
                player_layer = player.get_ally_board().get_layer(layer)
                if player_layer[row][col] != State.NONE:
                    print()
                    print("This square is already used, please select another one")
                    continue

                # Ask for the direction if the size of the submarine is more than 1 square
                if size == 1:
                    direction = Direction.NONE
                    is_submarine_correctly_placed = True

                else:
                    is_direction_set = False
                    while not is_direction_set:

                        is_direction_set = True

                        # Choose a direction
                        direction = 0
                        while direction not in ["T", "B", "R", "L"]:
                            direction = input("Direction of the submarine of size " + str(
                                size) + " \n - T = TOP \n - R = RIGHT \n - B = BOTTOM \n - L = LEFT")

                        # TOP Direction
                        if direction == "T":
                            for j in range(size):

                                # Check that the submarine is not overflowing the board
                                if row - j < 0:
                                    is_direction_set = False
                                    print(
                                        "A part of the submarine is out of the board, please select another direction")

                                # Check that the other squares are available
                                elif player_layer[row - i][col] != State.NONE:
                                    is_direction_set = False
                                    print("There is no space to place a", size,
                                          "squares submarines there. Select another direction")

                            if is_direction_set:
                                direction = Direction.TOP
                                is_submarine_correctly_placed = True

                        # BOTTOM Direction
                        elif direction == "B":
                            for j in range(size):

                                # Check that the submarine is not overflowing the board
                                if row + j > self.nb_rows - 1:
                                    is_direction_set = False
                                    print(
                                        "A part of the submarine is out of the board, please select another direction")

                                # Check that the other squares are available
                                elif player_layer[row + j][col] != State.NONE:
                                    is_direction_set = False
                                    print("There is no space to place a", size,
                                          "squares submarines there. Select another direction")

                            if is_direction_set:
                                direction = Direction.BOTTOM
                                is_submarine_correctly_placed = True

                        # RIGHT Direction
                        elif direction == "R":
                            for j in range(size):

                                # Check that the submarine is not overflowing the board
                                if col + j > self.nb_columns - 1:
                                    is_direction_set = False
                                    print(
                                        "A part of the submarine is out of the board, please select another direction")

                                # Check that the other squares are available
                                elif player_layer[row][col + j] != State.NONE:
                                    is_direction_set = False
                                    print("There is no space to place a", size,
                                          "squares submarines there. Select another direction")

                            if is_direction_set:
                                direction = Direction.RIGHT
                                is_submarine_correctly_placed = True

                        # LEFT Direction
                        elif direction == "L":
                            for j in range(size):

                                # Check that the submarine is not overflowing the board
                                if col - j < 0:
                                    is_direction_set = False
                                    print(
                                        "A part of the submarine is out of the board, please select another direction")

                                # Check that the other squares are available
                                elif player_layer[row][col - j] != State.NONE:
                                    is_direction_set = False
                                    print("There is no space to place a", size,
                                          "squares submarines there. Select another direction")

                            if is_direction_set:
                                direction = Direction.LEFT
                                is_submarine_correctly_placed = True

            # Everything is ok, we can place the submarine
            player.ally_board.place_a_submarine(row, col, layer, size, direction)
            player.add_sbm(row, col, layer, size, direction)

            # Save the submarine placement
            if player == self.player1 :
                player_number = "1"
            elif player == self.player2 :
                player_number = "2"
            else :
                raise Exception("submarine_placement ERROR : incorrect player")

            self.save_submarine_placement(player_number, row, col, layer, size, direction)

    def change_player(self, previous_player):
        """ Switch between players
        @param previous_player the player who played the previous turn
        """

        if previous_player == self.player1:
            return self.player2
        elif previous_player == self.player2:
            return self.player1
        else:
            print("change_player Exception : incorrect previous player")

    def is_game_finished(self, last_player_attacked):
        """ Check if the game is finished

        @param last_player_attacked the last player under attack
        @return true if each submarine of the attacked player is down, else return false
        """

        # Check if there is any submarine in the boards
        for sbm in last_player_attacked.get_submarines():
            if not sbm.get_is_down():
                return False

        return True

    # ATTACK METHODS ===================================================================================================

    def make_a_shot(self, player_under_attack_number, row, col, layer):
        """ Method used to make a shot on the enemy board

        @param player_under_attack_number   The number of the player who is under attack
        @param row                          The row coordinate of the attacked square
        @param col                          The column coordinate of the attacked square
        @param layer                        The layer coordinate of the attacked square
        """

        # Transform the attacked player number from string to integer
        player_under_attack_number = int(player_under_attack_number)

        # Load players regarding the player under attack number
        if player_under_attack_number == 1:
            player_under_attack = self.player1
            attacking_player = self.player2
        elif player_under_attack_number == 2:
            player_under_attack = self.player2
            attacking_player = self.player1
        else:
            raise Exception("make_a_shot Exception : The player number is not correct")

        # process the shot
        square_content = player_under_attack.get_ally_board().get_square_content(row, col, layer)

        # if no target found
        if square_content != State.S:

            # check content of squares around
            is_submarine_seen = False

            for col_idx in [col - 1, col + 1]:
                if player_under_attack.get_ally_board().get_square_content(row, col_idx, layer) == State.S:
                    is_submarine_seen = True

            for row_idx in [row - 1, row + 1]:
                if player_under_attack.get_ally_board().get_square_content(row_idx, col, layer) == State.S:
                    is_submarine_seen = True

            for layer_idx in [layer - 1, layer + 1]:

                if layer_idx < 0 or layer_idx > 2:
                    continue

                if player_under_attack.get_ally_board().get_square_content(row, col, layer_idx) == State.S:
                    is_submarine_seen = True

            # update the board
            if is_submarine_seen:
                self.update_states_after_shot(attacking_player, row, col, layer, State.V)
            elif not is_submarine_seen:
                self.update_states_after_shot(attacking_player, row, col, layer, State.R)

        # if a target is found
        elif square_content == State.S:

            # get the submarine on the attacked square
            under_attack_sbm_coordinates = [row, col, layer]

            # for each submarine
            for sbm in player_under_attack.get_submarines():
                # for each square of the submarine
                for i in range(sbm.get_size()):
                    if sbm.get_squares_coordinates()[i] == under_attack_sbm_coordinates:
                        sbm_under_attack = sbm

            # update square states
            attacking_player.enemy_board.set_square_content(row, col, layer, State.T)
            player_under_attack.ally_board.set_square_content(row, col, layer, State.T)
            sbm_under_attack.set_dictionary_state(under_attack_sbm_coordinates, State.T)

            # if the sbm is down
            is_sbm_down = sbm_under_attack.is_sbm_down()
            if is_sbm_down:
                # update states to C for all sbm coordinates in both attacking_player.enemy_board
                # and layer_under_attack.ally_board
                for coord in sbm_under_attack.get_squares_coordinates():
                    attacking_player.get_enemy_board().set_square_content(coord[0], coord[1], coord[2], State.C)
                    player_under_attack.get_ally_board().set_square_content(coord[0], coord[1], coord[2], State.C)
            else:
                # update the state of the attack square to T in both  attacking_player.enemy_board
                # and layer_under_attack.ally_board
                attacking_player.get_enemy_board().set_square_content(row, col, layer, State.T)
                player_under_attack.get_ally_board().set_square_content(row, col, layer, State.T)

        # save the shot
        self.save_shot(player_under_attack_number, row, col, layer)

    def choose_coordinates_to_attack(self):
        """ Method used to choose coordinates for a shot

        @ return row        The row coordinate of the attacked square
        @ return col        The column coordinate of the attacked square
        @ return layer      The layer coordinate of the attacked square
        """

        # Ask for the row coordinate of the submarine
        print()
        msg = "Choose a row between 0 and " + str(self.nb_rows - 1) + ") : "
        row = self.check_input_validity(self.nb_rows, msg)

        # Ask for the column coordinate of the submarine
        print()

        msg = "Choose a column between 0 and " + str(self.nb_columns - 1) + ") : "
        col = self.check_input_validity(self.nb_columns, msg)

        # Ask for the layer coordinate of the submarine
        print()

        msg = "Choose a layer as --> 0 : 100m, 1 : 200m, 2 : 300m)"
        layer = self.check_input_validity(3, msg)

        # return coordinates
        return row, col, layer

    def check_input_validity(self, max_range, input_msg):
        """ Method used to ask a coordinate and check its validity

        @param max_range    The range in which the value must be
        @param input_msg    The msg displayed to the user when he must choose a value

        @return value       The verified selected value
        """

        value = -1
        while value not in range(max_range):
            value = input(input_msg)

            if value == "STOP":
                self.stop_the_game()

            try:
                value = int(value)
                if value not in range(max_range):
                    print()
                    self.view.display_out_of_bound_input()
            except:
                self.view.display_wrong_input_type()

        return value

    def update_states_after_shot(self, attacking_player, row, col, layer, content):
        """ Method used to update states of the squares around the target square in the enemy board of
        attacking player

        @param attacking_player     The player who is attacking
        @param row                  The row coordinate of the square to update
        @param col                  The column coordinate of the square to update
        @param layer                The layer coordinate of the square to update
        @param content              The new content of the square to update
        """

        self.protected_square_update(attacking_player, row, col, layer, content)
        self.protected_square_update(attacking_player, row + 1, col, layer, content)
        self.protected_square_update(attacking_player, row - 1, col, layer, content)
        self.protected_square_update(attacking_player, row, col + 1, layer, content)
        self.protected_square_update(attacking_player, row, col - 1, layer, content)

        for layer_idx in [layer - 1, layer + 1]:

            if layer_idx < 0 or layer_idx > 2:
                continue

            self.protected_square_update(attacking_player, row, col, layer_idx, content)

    def protected_square_update(self, attacking_player, row, col, layer, content):
        """ Method used in update_states_after_shot() to update a square only it is different from State.T

        @param attacking_player     The player who is attacking
        @param row                  The row coordinate of the square to update
        @param col                  The column coordinate of the square to update
        @param layer                The layer coordinate of the square to update
        @param content              The new content of the square to update
        """
        square_content = attacking_player.get_enemy_board().get_square_content(row, col, layer)
        if square_content != State.T and square_content != State.C:
            attacking_player.get_enemy_board().set_square_content(row, col, layer, content)

    # SAVING METHODS ===================================================================================================

    def save_submarine_placement(self, player_number, row, col, layer, size, direction):
        """ Method used to save submarine placments coordinates in a csv file

        @param player_number    The player who was placing his submarine
        @param row              The row coordinate of the head of the submarine
        @param col              The column coordinate of the head of the submarine
        @param layer            The layer coordinate of the head of the submarine
        @param size             The size of the submarine
        @param direction        The direction of the submarine
        """
        # Create the line
        values = ["sbm_placement", player_number, row, col, layer, size, direction]

        # Write the line in the saving file
        with open(self.saving_file_path, "a") as file:
            writer = csv.writer(file)
            line = writer.writerow(values)

    def save_shot(self, player_under_attack_number, row, col, layer):
        """ Method used to save shots coordinates in a csv file

        @param player_under_attack_number       The number of the player who was under attack
        @param row                              The row coordinate of the attacked square
        @param col                              The column coordinate of the attacked square
        @param layer                            The layer coordinate of the attacked square
        """
        # Create the line
        values = ["make_a_shot", player_under_attack_number, row, col, layer]

        # Write the line in the saving file
        with open(self.saving_file_path, "a") as file:
            writer = csv.writer(file)
            line = writer.writerow(values)

    def reload_saved_sbm(self, player_number, row, col, layer, size, direction):
        """ Method used to reload a submarine

        @param player_number    The number of the player who owns the submarine
        @param row              The row coordinate of the head of the submarine
        @param col              The column coordinate of the head of the submarine
        @param layer            The layer coordinate of the head of the submarine
        @param size             The size of the submarine
        @param direction        The direction of the submarine
        """

        # Transform string value of direction to Enum value
        if direction == "Direction.TOP":
            direction = Direction.TOP
        elif direction == "Direction.RIGHT":
            direction = Direction.RIGHT
        elif direction == "Direction.BOTTOM":
            direction = Direction.BOTTOM
        elif direction == "Direction.LEFT":
            direction = Direction.LEFT
        else :
            raise Exception("reload_saved_sbm ERROR : the direction is incorrect")

        # Replace submarine
        if player_number == 1:
            self.player1.ally_board.place_a_submarine(row, col, layer, size, direction)
            self.player1.add_sbm(row, col, layer, size, direction)
        elif player_number == 2:
            self.player2.ally_board.place_a_submarine(row, col, layer, size, direction)
            self.player2.add_sbm(row, col, layer, size, direction)

    # OTHER METHODS ====================================================================================================

    def clear_console(self):
        """ Method used to clear the console after a player turn"""

        clear = lambda :os.system("clear")
        clear()

    def stop_the_game(self):
        """ Mehod used to stop the game if a players type "STOP"
        """

        print()
        print("The game has been interrupted")
        print("To reload this game, select this file next time : " + self.saving_file_path)
        sys.exit()