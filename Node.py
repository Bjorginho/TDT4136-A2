from Map import Map_Obj

class Node(): 
    """
    Class to represent a location on the map. Fetch the cost of each cell
    """
    def __init__(self, loc: list[int, int], map: Map_Obj) -> None:
        self.location = tuple(loc) 
        self.g_cost = 0 
        self.h_cost = 0
        self.f_cost = 0
        self.parent = None 
        self.cost = map.get_cell_value(loc) 