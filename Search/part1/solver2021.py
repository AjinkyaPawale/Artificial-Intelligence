#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: Ajinkya Pawale 2000701032
#
# Based on skeleton code by D. Crandall, January 2021
#

import sys
import copy
import heapq

ROWS=4
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]
 
#heuristic that calculates the number of misplaced tiles. At the end the heuristic is divided by 4 if there is a column shift or divided by 5 it it is a row shift.                                                                  
def heuristic(board,path,goal):
    h_s=0
    if path=='U1'or path=='U3'or path=='D2' or path=='D4': 
        leng=4
    else:
        leng=5
    for i in range(0,ROWS):
        for j in range(0,COLS):
            if board[i][j]==goal[i][j]:
                h_s= h_s+0
            else:
                h_s= h_s+1
    h_s = h_s/leng
    return h_s

# return a list of possible successor states
def successors(state):
    state1 = copy.deepcopy(state)
    state2 = copy.deepcopy(state)
    state3 = copy.deepcopy(state)
    state4 = copy.deepcopy(state)
    state5 = copy.deepcopy(state)
    state6 = copy.deepcopy(state)
    state7 = copy.deepcopy(state)
    state8 = copy.deepcopy(state)
    state9 = copy.deepcopy(state)
    
    for i in range(0, COLS):
        state1[0][i] = state[0][(i+1)%5]  # to slid the first row left
    for i in range(0, COLS):
        state2[2][i] = state[2][(i+1)%5]  # to slid the third row left
    for i in range(0, COLS):
        state3[1][i] = state[1][(i+4)%5]  # to slid the second row right
    for i in range(0, COLS):
        state4[3][i] = state[3][(i+4)%5]  # to slid the forth row right
    for i in range(0, ROWS):
        state5[i][0] = state[(i+1)%4][0]  # to slid the first column up
    for i in range(0, ROWS):
        state6[i][2] = state[(i+1)%4][2]  # to slid the third column up
    for i in range(0, ROWS):
        state7[i][4] = state[(i+1)%4][4]  # to slid the fifth column up
    for i in range(0, ROWS):
        state8[i][1] = state[(i-1)%4][1]  # to slid the second column down
    for i in range(0, ROWS):
        state9[i][3] = state[(i-1)%4][3]  # to slid the orth column down
    
    return [(state1,'L1'),(state2,'L3'),(state3,'R2'),(state4,'R4'),(state5,'U1'),(state6,'U3'),(state7,'U5'),(state8,'D2'),(state9,'D4')]

# check if we've reached the goal
def is_goal(state):
    goal = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20]]
    if state == goal:
        return True
    else:
        return False

def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    initial_board = list(initial_board)
    goal = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20]]
    board = []
    fringe=[[4,board,'']]
    heapq.heapify(fringe)
    final_path= ''
    c_s=0
    j=0
    for i in range(0,ROWS):
           board.append(initial_board[j:COLS+j])
           j=j+5
    print(board)
    visited=[]  # maintaining a list of visited nodes
    while len(fringe)!=0:
        succ = heapq.heappop(fringe)  # popping out the board with the least heuristic value
        c_s=c_s+1  # incrementing the cost function 
        final_path = succ[2]
        if is_goal(succ[1]): # checking the goal state
            return(succ[2])
        for  move in successors(succ[1]): # generating successors
            if move not in visited:
                heapq.heappush(fringe,[c_s + heuristic(move[0],move[1],goal),move[0],final_path+move[1]])
                visited.append(move)

            


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]
            

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    if route == "Invalid Start State":
        print ("Solution not found since inital board configuration is wrong")
    else:  
        print("Solution found in " + str(len(route)//2) + " moves:" + "\n" + "".join(route))
