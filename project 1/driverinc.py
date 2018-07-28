import sys
from collections import deque
import resource

class State():

    def __init__(self, boardip,parent = None):
        #argv returns a string so conv it into int for evaluation
        self.board_vals = boardip #in string
        self.board = map(lambda x: int(x), boardip.split(',')) # string to list conv, spliting using intermediate commas
        self.parent = parent
                
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth+1 # increases depth as a child is created from a separate parent in next level, 
                                        # this line ensures that depth increases only when a new level is created since siblings in 
                                        # same level have 1 parent  
class Solver():
    # deque is a special type of list which can both function as queue and stack
    def __init__(self,init_state,method):
        self.method = method
        self.init = init_state
        self.maxdepth = 0
        self.nodeexpanded = 0


    def methodsel(self):
        if self.method == "bfs":
            self.bfs_sol()
        elif self.method == "dfs":
            self.dfs_sol()

    def bfs_sol(self):
        frontier = deque()
        frontier.append(self.init)
        frontier_dict = {self.init.board_vals:0}
        explored_dict = {}

        while frontier:
            present = frontier.popleft()
            explored_dict[present.board_vals] = 0
            #print("\nFrontier before deletion:",present.board_vals)
            del frontier_dict[present.board_vals]

            if Board.is_goal(present):
                self.goalstate = present
                return
            self.nodeexpanded += 1
            #print("Node expanded:",self.nodeexpanded,"\n")
            for child in Board.children_udlr(present):
                if self.maxdepth < child.depth:
                    self.maxdepth = child.depth
                if child.board_vals not in frontier_dict and child.board_vals not in explored_dict:
                    frontier.append(child)
                    frontier_dict[child.board_vals] = 0
                
    def dfs_sol(self):
        
        frontier = deque()
        frontier.append(self.init)
        frontier_dict = {self.init.board_vals:0}
        explored_dict = {}
        
        while frontier:
            present = frontier.pop()
            explored_dict[present.board_vals] = 0
            #print("\nFrontier before deletion:",present.board_vals)
            del frontier_dict[present.board_vals]
            
            if Board.is_goal(present):
                self.goalstate = present
                return
            
            self.nodeexpanded += 1
            #print("Node expanded:",self.nodeexpanded,"\n")
            if self.maxdepth < present.depth:
                self.maxdepth = present.depth
            i = 0
            for child in Board.children_rldu(present):
                if child.board_vals not in frontier_dict and child.board_vals not in explored_dict:
                    i +=1
                    frontier.append(child)
                    frontier_dict[child.board_vals] = 0
                    #print("\n Child:",i," State:",child.board_vals)
    
        
    def result(self):
        path = []
        current = self.goalstate
        while current.parent != None:
            path.append(Board.actions(current))
            current = current.parent
        path = path[::-1]
        string_to_write = 'path_to_goal: [' + ', '.join(path) + ']\n'
        string_to_write += 'cost_of_path: ' + str(len(path)) + '\n'
        string_to_write += 'nodes_expanded: ' + str(self.nodeexpanded) + '\n'
        string_to_write += 'search_depth: ' + str(len(path)) + '\n'
        string_to_write += 'max_search_depth: ' + str(self.maxdepth) + '\n'
        usage_details = resource.getrusage(resource.RUSAGE_SELF)
        string_to_write += 'running_time: %.8f\n' % (usage_details.ru_utime + usage_details.ru_stime)
        string_to_write += 'max_ram_usage: %.8f\n' % (usage_details.ru_maxrss / 1024.0 ** 2)

        file = open('output.txt', 'w')
        file.write(string_to_write)
        file.close()
        

 
class Board():
    
    @classmethod # @classmethod specifies that it can use vars of instances accessing it  
    def is_goal(self,state):
        goal = [0,1,2,3,4,5,6,7,8]
        for i in range(9):
            if state.board[i] != goal[i]:
                return False
        return True
    @classmethod
    def zeros(self,state):
        for i in range(9):
            if state.board[i] == 0:
                return i
    @classmethod
    def actions(self,state):
        if state.parent is None:
            return None
        else:
            zero_parent = self.zeros(state.parent)
            zero_pre= self.zeros(state)
            pos = zero_parent - zero_pre
            if pos == 3:
                return "'Up'"
            elif pos == -3:
                return "'Down'"
            elif pos == -1:
                return "'Right'"
            elif pos == 1:
                return "'Left'"

    @classmethod
    def swap_pos_udlr(self,state):
        zero_pos= Board.zeros(state)
        #table stores swap position for each zero position in udlr order
        swap_lookup_table = {0: [1, 3], 1: [4, 0, 2], 2: [5, 1], 3: [0, 6, 4],
                             4: [1, 7, 3, 5], 5: [2, 8, 4], 6: [3, 7], 7: [4, 6, 8], 8: [5, 7]
                             }

        return swap_lookup_table[zero_pos]
    
    @classmethod
    def children_udlr(self,state):
        z= Board.zeros(state)
        swap_pts = self.swap_pos_udlr(state)
        children = []

        for pts in swap_pts:
            new = state.board[:]
            new[z] = state.board[pts]
            new[pts] = 0
            new = map(lambda x: str(x), new)#conv to string
            new = ",".join(new)
            children.append(State(new,state))#add new state with parent
        return children
    
    @classmethod
    def children_rldu(self,state):
        return self.children_udlr(state)[::-1]# for dfs it should swap in rldu , so reverse list obtained from chilred udlr



if __name__ == "__main__":
    #sys.argv returns each words typed in terminal to run a pgm. argv[0] is the program name itself 
    method = sys.argv[1]
    board = sys.argv[2]
    s = State(board) # instance of State created 
    g = Solver(s,method) #solver instace created , each solver istance contains vars of state which can be used with object of Solver 
    g.methodsel()
    g.result()












