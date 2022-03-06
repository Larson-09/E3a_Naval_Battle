"""
@author LAUDE Jordan and SARLAT Meven
"""

from Utils.Enums import State, Direction

class Submarine:

    # CONSTRUCTOR ======================================================================================================

    def __init__(self, row, col, layer, size, direction):
        """ The submarine constructor

        @param row          The row coordinate of the head of the submarine
        @param col          The column coordinate of the head of the submarine
        @param layer        The layer of the submarine
        @param size         The number of squares of the submarine
        @param direction    The direction of the submarine
        """
        
        self.size = size
        self.is_down = False
        self.direction = direction

        # init coordinates of the submarine
        self.squares = {}
        self.squares_coordinates = []

        for i in range(size):

            if direction == Direction.TOP:
                self.squares_coordinates.append([row - i, col, layer])

                coordinates_str = str(row - i) + str(col) + str(layer)
                self.squares[coordinates_str] = State.S

            elif direction == Direction.BOTTOM:
                self.squares_coordinates.append([row + i, col, layer])

                coordinates_str = str(row + i) + str(col) + str(layer)
                self.squares[coordinates_str] = State.S

            elif direction == Direction.LEFT:
                self.squares_coordinates.append([row, col - i, layer])

                coordinates_str = str(row) + str(col - i) + str(layer)
                self.squares[coordinates_str] = State.S

            elif direction == Direction.RIGHT:
                self.squares_coordinates.append([row, col + i, layer])

                coordinates_str = str(row) + str(col + i) + str(layer)
                self.squares[coordinates_str] = State.S

            elif direction == Direction.NONE:
                print()
                coordinates_str = str(row) + str(col + i)
                self.squares_coordinates.append([row, col, layer])
                self.squares[coordinates_str] = State.S

            else:
                raise Exception("submarine_init Exception : the direction coordinate is not valid")

    # GETTERS ==========================================================================================================

    def get_size(self):
        return self.size
    
    def get_squares_coordinates(self):
        return self.squares_coordinates

    def get_dictionary_state(self, coordinates):
        coordinates_str = ""
        for coord in coordinates:
            coordinates_str += str(coord)

        return self.squares[coordinates_str]

    def get_is_down(self):
        return self.is_down

    # SETTERS ==========================================================================================================

    def set_dictionary_state(self, coordinates, content):
        coordinates_str = ""
        for coord in coordinates:
            coordinates_str += str(coord)

        self.squares[coordinates_str] = content

    # OTHERS ===========================================================================================================
    def is_sbm_down(self):
        """ Method used to know if the sbm is donw or not. If the sbm is down, this method also updates values of the
        sbm from State.T to State.C

        @return True if the sbm is down, Falss if it is not
        """

        # Check if the sbm is down
        for square_state in self.squares.values():
            if square_state != State.T :
                return False

        # Update values if the sbm is down
        for key in self.squares.keys():
            self.squares[key] = State.C

        # Update is down statement
        self.is_down = True

        return True

