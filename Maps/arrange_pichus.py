#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : [PUT YOUR NAME AND USERNAME HERE]
#
# Based on skeleton code in CSCI B551, Spring 2021
#


import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]

# Count total # of pichus on board
def count_pichus(board):
    return sum([ row.count('p') for row in board ] )

# Return a string with the board rendered in a human-pichuly format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])

# Add a pichu to the board at the given position, and return a new board (doesn't change original)
def add_pichu(board, row, col):
    return board[0:row] + [board[row][0:col] + ['p',] + board[row][col+1:]] + board[row+1:]

#This function checks the validity of the successor state and returns true if the successor state is valid
def check(board):
    log = [] # It gets updated if the passed successor state is invalid
    # The below logic checks if there is any row conflict along with the 'X' node taken into consideration
    for rowno in range(0,len(board)):
        flag = False 
        for colno in range(0,len(board[0])):
            if board [rowno][colno] == 'p' and flag == True:
                log.append("Invalid")
                break   
            elif board[rowno][colno] == 'X': 
                flag = False
            elif board[rowno][colno] == '.':
                continue
            elif board [rowno][colno] == 'p' and flag ==False:
                flag = True
    # The below logic checks if there is any column conflict along with the 'X' node taken into consideration            
    for colno in range(0,len(board[0])):
        flag = False
        for rowno in range(0,len(board)):
            if board [rowno][colno] == 'p' and flag == True:
                log.append("Invalid")
                break   
            elif board[rowno][colno] == 'X': 
                flag = False
            elif board[rowno][colno] == '.':
                continue
            elif board [rowno][colno] == 'p' and flag ==False:
                flag = True
    # If any of the above conflict(i.e row/column) does not contain an invalid state then return True            
    if 'Invalid' not in log:
        return True
        

# Get list of successors of given board state
def successors(board):
   # print(board) 
    return [ add_pichu(board, r, c) for r in range(0, len(board)) for c in range(0,len(board[0])) if(board[r][c] == '.')]

# check if board is a goal state
def is_goal(board, k):
    return count_pichus(board) == k 


# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_map, success), where:
# - new_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_board, k):

    fringe = [initial_board]
   # print(fringe)
    while len(fringe) > 0:
        for s in successors(fringe.pop()):
            print(s)
            if is_goal(s, k) and check(s): # added a conditional check which returns True if the last state is a valid successor or not
                return(s,True)
            elif check(s):  # added a conditional check which returns True if the state is a valid successor or not
                fringe.append(s) 
                break
    return ([],False)

# Main Function
if __name__ == "__main__": 
    house_map=parse_map(sys.argv[1])

    # This is K, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial board:\n" + printable_board(house_map) + "\n\nLooking for solution...\n")
    if k==1: # if k equals 1 then by default the code will return the inital state 
        newboard, success = house_map, True
    else: # if k >=1 then apply the solve function and compute
        (newboard, success) = solve(house_map, k)
    print ("Here's what we found:")
    print (printable_board(newboard) if success else "None")


