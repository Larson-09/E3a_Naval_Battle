"""
@author LAUDE Jordan and SARLAT Meven
"""

from Utils.Enums import State, Direction
import numpy as np


class Board:

    # CONSTRUCTOR ======================================================================================================

    def __init__(self, columns, rows):
        """ The Board initializer

        @param columns  The number of columns of the boards
        @param rows     The number of rows of the boards
        """

        self.columns = columns
        self.rows = rows

        self.layer1 = [[State.NONE for i in range(self.columns)] for j in range(self.rows)]
        self.layer2 = [[State.NONE for i in range(self.columns)] for j in range(self.rows)]
        self.layer3 = [[State.NONE for i in range(self.columns)] for j in range(self.rows)]
        self.layers = [self.layer1, self.layer2, self.layer3]

        self.forbidden_squares = []

    # GETTERS ==========================================================================================================

    def get_layers(self):
        """ Method used to get the array containing the layers squares

        @return layers
        """
        return self.layers

    def get_layer(self, layer_index):
        """ Method used to get a specific layer

        @return layer
        """
        return self.layers[layer_index]

    def get_square_content(self, row, col, layer):
        """ Method used to get the content of a square

        @param row      The row coordinate of the square to get the content
        @param col      The column coordinate of the square to get the content
        @param layer    The layer coordinate of the square to get the content
        """
        return self.layers[layer][row][col]

    # SETTERS ==========================================================================================================

    def set_square_content(self, row, col, layer, content):
        """ Method used to set the content of a square

        @param row      The row coordinate of the square to set the content
        @param col      The column coordinate of the square to set the content
        @param layer    The layer coordinate of the square to set the content
        @param content      The content to set in the square
        """
        self.layers[layer][row][col] = content

    # OTHERS ===========================================================================================================

    def place_a_submarine(self, y_coord, x_coord, layer_idx, size, direction):
        """ Method used to place a submarine on the ally board

        @param y_coord      The row coordinate of the head of the submarine
        @param x_coord      The column coordinate of the head of the submarine
        @param layer_idx    The layer coordinate of the submarine
        @param size         The number of squares of the submarine
        @param direction    The direction of the submarine
        """

        # Place the head of the submarine
        self.layers[layer_idx][y_coord][x_coord] = State.S

        # Place the rest of the submarine if the size is more than 1 square
        if size > 1:
            if direction == Direction.TOP:
                row = y_coord
                for i in range(size - 1):
                    row -= 1
                    self.layers[layer_idx][row][x_coord] = State.S

            elif direction == Direction.BOTTOM:
                row = y_coord
                for i in range(size - 1):
                    row += 1
                    self.layers[layer_idx][row][x_coord] = State.S

            elif direction == Direction.LEFT:
                col = x_coord
                for i in range(size - 1):
                    col -= 1
                    self.layers[layer_idx][y_coord][col] = State.S

            elif direction == Direction.RIGHT:
                col = x_coord
                for i in range(size - 1):
                    col += 1
                    self.layers[layer_idx][y_coord][col] = State.S

    def copy(self, destination):
        """ Method used to copy the content of the self board object in another

        @param destination  The board in which we want to copy the content of our self board
        """

        layer_idx = 0
        for layer in self.get_layers():

            destination.append(layer)

            nb_rows = np.shape(layer)[0]
            nb_columns = np.shape(layer)[1]

            for i in range(nb_rows):
                for j in range(nb_columns):
                    destination[layer_idx][i][j] = destination[layer_idx][i][j].value

            layer_idx += 1