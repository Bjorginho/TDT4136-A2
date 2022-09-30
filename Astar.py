from Map import Map_Obj
from Node import Node 

"""

                Authors
    Frede Berdal (fredekb@stud.ntnu.no) 
    André Bjørgum (anbjorg@stud.ntnu.no)
    
"""

def heuristic(from_node: Node, to_node: Node):
    """
    Finds the Manhattan distance between two nodes on the map. 
    """
    row1, col1 = from_node.location
    row2, col2 = to_node.location
    return abs(row1 - row2) + abs(col1 - col2)

def get_neighbours(location: list[int, int], map: Map_Obj) -> list[Node]: 
    """
    Returns a list of all walkable neighbours / adjacent cells to the current node. We ignore the diagonal cells. 
    """    
    row, col = location 
    north = (row - 1, col)
    south = (row + 1, col)
    east = (row, col + 1)
    west = (row, col - 1)

    directions = [east, west, north, south]
    neighbours = [] 
    for dir in directions: 
        if valid_location(dir, map):
            neighbours.append(Node(list(dir), map))
    
    return neighbours

def valid_location(loc: list[int, int], map: Map_Obj):
    """
    Checks if the location is valid, i.e. in bounds and not a wall. 
    """
    row, col = loc 
    if row < 0 or col < 0: 
        return False 
    elif row > len(map.get_maps()[0]) or col > len(map.get_maps()[0][0]):
        return False 
    elif map.get_cell_value([row, col]) == -1:  # obstacle / wall 
        return False 
    else: 
        return True 

def draw(map: Map_Obj, current: Node, open: list[Node], closed: list[Node], goal: Node):
    """
    Helper method for drawing the path (used in debugging)
    """
    for node in open:
        map.replace_map_values(pos=node.location, value=3, goal_pos=goal.location) # blackish 
    for node in closed:
        map.replace_map_values(pos=node.location, value=4, goal_pos=goal.location) # mørkegrå
    map.replace_map_values(pos=current.location, value=1, goal_pos=goal.location) # whiteish

def printInfo(current: Node, open: list[Node], closed: list[Node], start: Node, goal: Node):
    """
    Helper method for displaying information (used in debugging)
    """
    print("Start: ", start.location)
    print("Goal: ", goal.location)
    print("")
    print("Current: ", (current.location, current.f_cost))
    print("Open nodes: ", [(node.location, node.f_cost) for node in open])
    print("Closed nodes: ", [(node.location, node.f_cost) for node in closed])

def astar(map: Map_Obj):
    """
    Implementation of the A* algorithm. Takes a Map_Obj as input and returns the shortest path from start and goal location (in map object)

    """
    # Fetches the start and goal position and adds them into Node objects. 
    start: Node = Node(tuple(map.get_start_pos()), map)
    goal: Node = Node(tuple(map.get_goal_pos()), map)

    # Create two empty lists: One for visited nodes and one for the nodes which are opened, but not yet expanded. 
    OPEN: list[Node] = [start] # Open nodes 
    CLOSED: list[Node] = [] # Closed nodes / expanded

    # Loops and checks each node in OPEN 
    while len(OPEN) > 0:
        OPEN = sorted(OPEN, key= lambda n : n.f_cost) # Sort the OPEN list based on the element's f-values : (g + h)
        current = OPEN[0] # We take the the node with least f value 

        OPEN.remove(current) # Remove the selected node from OPEN 
        CLOSED.append(current) # Add the selected node into CLOSED 

        # If the selected node is on the goal location --> We have found a path 
        if current.location == goal.location:
            print("Reached location")
            path = [] # Create empty path 
            node = current 
            while node is not None and node.parent is not None: # The initial node has parent: None 
                path.append(node)
                map.replace_map_values(pos=node.location, value=4, goal_pos=goal.location) # Draw the node into the map so we can see the full path after  
                node = node.parent # Go to next node, which is mapped as best parent
            # draw(map, current=current, open=OPEN, closed=CLOSED, goal=goal)    
            return path[::-1] # Shortest path with the least cost from start to goal 
        else: 
            successors: list[Node] = get_neighbours(list(current.location), map)
            for successor in successors: # Loop through neighbours and add to OPEN
                closed_locations = [node.location for node in CLOSED]
                if successor.location not in closed_locations: #  If neighbour has not been expanded to yet.
                    new_g = current.g_cost + successor.cost
                    open_locations =  [node.location for node in OPEN]
                    if successor.location not in open_locations: # If neighbour has not been expanded to yet, and not in OPEN.
                        # Calculate costs of the neighbour
                        successor.g_cost = current.g_cost + successor.cost
                        successor.h_cost = heuristic(successor, goal)
                        successor.f_cost = successor.g_cost + successor.h_cost
                        successor.parent = current
                        # Add to OPEN list, then validate afterwards 
                        OPEN.append(successor)
                    else:
                        if new_g < successor.g_cost:
                            successor.g_cost = current.g_cost + successor.cost
                            successor.h_cost = heuristic(successor, goal)
                            successor.f_cost = successor.g_cost + successor.h_cost
                            successor.parent = current
                            OPEN.append(successor)
    return [] # No path was found. 

def main():
    # Select task (1,2,3 and 4) - Part 3 not implemented. 
    selected_map = Map_Obj(task=1)
    path = astar(selected_map)
    selected_map.show_map()


if __name__ == "__main__":
    main()