import itertools
from random import randint


class Board(object):
    ''' Represents the grid '''
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        def create_coordinates(x: int, y: int):
            ''' Creates a board
                Size: x * y '''
               
            for i in range(x):
                for j in range(y):
                    yield (i, j)

        self.board_map = {}
        for elem in create_coordinates(self.width, self.height):
            self.board_map[elem] = {'neighbours': [], 'isBlocked': False}
            for x, y in itertools.product([elem[0]-1, elem[0], elem[0]+1], [elem[1]-1, elem[1], elem[1]+1]):
                # excluding out-of-bounds numbers
                if 0 <= x < self.width and 0 <= y < self.height and (x, y) != elem and (x == elem[0] or y == elem[1]):
                    self.board_map[elem]['neighbours'].append((x,y))

    def query_cell(self, location: tuple):
        '''prints cell information
           input must be tuple of integers'''

        #validating input
        if type(location) != tuple:
            return None
        if type(location[0]) != int or type(location[1]) != int:
            return None

        if not 0 <= location[0] <= self.width - 1 or not 0 <= location[0] <= self.height - 1:
            return None

        return self.board_map[location]['neighbours']

    def cell_block(self, cell: tuple):
        '''Makes the cell a blocked cell
           So it cannot be accessed'''

        self.board_map[cell]['isBlocked'] = True

    def cell_unblock(self, cell: tuple):
        '''Makes the cell an unblocked cell
           So it can be accessed again'''

        self.board_map[cell]['isBlocked'] = False

class Route(object):

    def __init__(self, board: object):
        self.board = board

    def FindShortestPathBFS(self, start_position: tuple, goal_position: tuple):
        '''Using the Breadth First Search algorithm this function
            finds the shortest route by keeping track of 
            the visited nodes and the nodes the agent moved from.
            
            [In]:
            start_position -> tuple of ints
            goal_position -> tuple of ints
            
            [Out]:
            shortest_route -> a list made by the embedded CalculateShortestRoute function'''
    
        def CalculateShortestRoute(ending_point: tuple, starting_point: tuple):
            '''Returns an ordered list of nodes that shows the shortest route
                between the starting point and the goal
                
                [In]:
                start_position -> tuple of ints
                goal_position -> tuple of ints
                [Out]:
                shortest_route -> list'''
            
            
            shortest_route = []
            shortest_route.insert(0, ending_point)
            while shortest_route[0] != starting_point:
                shortest_route.insert(0, node_parents[shortest_route[0]])
            return shortest_route        
        
        explored_nodes = []
        node_parents = {}
       
        queue = []
        queue.insert(0, start_position)

        # Unblock the goal position
        if self.board.board_map[goal_position]['isBlocked'] == True:
            self.board.cell_unblock(goal_position)
        
        while len(queue) != 0:
            current_node = queue.pop()
            explored_nodes.append(current_node)
            
            if current_node == goal_position:
                return CalculateShortestRoute(current_node, start_position)
            
            #look up viable routes (nodes)
            nodes = self.board.board_map[current_node]['neighbours']
            
            for node in nodes:
                if self.board.board_map[node]['isBlocked'] == False:
                    if node not in explored_nodes:
                        #mark node as explored
                        explored_nodes.append(node)
                        
                        #store a reference to the previous node
                        node_parents[node] = current_node
                        
                        #add node to queue
                        queue.insert(0, node)

