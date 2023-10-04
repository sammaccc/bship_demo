import random as rand

class Ship:

    def __init__(self, length, orientation, startPoint):

        self.length = length
        # 0=facing right, 1=down, 2=left, 3=up
        self.orientation = orientation
        # (x,y) starting coordinates
        self.startPoint = startPoint

        #shipCoords (x,y) x,y coordinates, with True/False for if coordinate has been hit
        self.shipCoords = {}
        for i in range(length):
            if self.orientation == 0:
                self.shipCoords[(startPoint[0]+i, startPoint[1])] = False
            if self.orientation == 1:
                self.shipCoords[(startPoint[0], startPoint[1]+i)] = False
            if self.orientation == 2:
                self.shipCoords[(startPoint[0]-i, startPoint[1])] = False
            if self.orientation == 3:
                self.shipCoords[(startPoint[0], startPoint[1]-i)] = False


    def get_coordinates(self):
                
        return self.shipCoords.keys()


    def coord_in_ship(self, coord):
        if coord in self.get_coordinates():
            return True
        return False
    
    def coord_is_hit(self, coord):

        return self.shipCoords.get(coord)

    def set_coord_hit(self, coord):
        self.shipCoords[coord] = True

    def ship_sunk(self):
        for hitStatus in self.shipCoords.values():
            if hitStatus is False:
                return False
        return True            
        
                          
    
class Board:

    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.ships = []

        i = 5
        while i >= 2:
            
            self.__place_ship(i)
            i -= 1
            
        self.__place_ship(3)
    

    # add a ship of given size within boundaries of board
    def __place_ship(self, length):
        
        # if true, we found a clear start point/orientation for the ship
        clearWaters = False

        while clearWaters is False:
            orientation = rand.randint(0,3)
            xCoord = rand.randint(0, self.width - 1)
            yCoord = rand.randint(0, self.height - 1)


            ship = Ship(length, orientation, (xCoord, yCoord))
            if ( (self.__ship_in_range(ship) is True)
                and (self.__ship_intersects(ship) is False) ):
                
                clearWaters = True
                self.ships.append(ship)
                    

    def __ship_in_range(self, ship):

        for point in ship.get_coordinates():
            if ( (point[0] < 0) or (point[0] >= self.width) or
                 (point[1] < 0) or (point[1] >= self.height) ):
                return False
        return True

    # check if the given ship intersects with any existing ships
    def __ship_intersects(self, ship):

        for coordinate in ship.get_coordinates():
            if self.__coordinate_occupied(coordinate):
                return True
        return False


    def print_board(self):

        boardPrint = ""
        for y in range(self.height):
            for x in range(self.width):

                if self.__coordinate_hit((x,y)):
                    boardPrint += "X"
                elif self.__coordinate_occupied((x,y)):
                    boardPrint += "O"
                else:
                    boardPrint += "."
                    
                if x == (self.width - 1):
                    boardPrint += "\n"
                else:
                    boardPrint += " "
        print(boardPrint)


    # check if given (x,y) coordinate is occupied by any ship
    def __coordinate_occupied(self, coord):

        for ship in self.ships:
            if ship.coord_in_ship(coord):
                return True
        return False

    def __coordinate_hit(self, coord):
        for ship in self.ships:
            if ship.coord_is_hit(coord):
                return True
        return False

    def all_ships_sunk(self):
        for ship in self.ships:
            if ship.ship_sunk() is False:
                return False
        return True

    def handle_coord_guess(self, coord):
        for ship in self.ships:
            if ship.coord_in_ship(coord) is True:
                ship.set_coord_hit(coord)
                break
        
                
                








    
