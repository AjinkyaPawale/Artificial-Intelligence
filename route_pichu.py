#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : [Ajinkya Pawale, ajpawale]
#
# Based on skeleton code provided in CSCI B551, Spring 2021.


import sys
import json

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]

# Return a string with the board rendered in a human/pichu-readable format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)

def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

	# Return only moves that are within the board and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]
    
#This function will compare the move popped out of the fringe with the next move esitimated and return the path it traversed    
def path(curr_move,move,move_string):
    if curr_move[0] - move[0] == 1:
        move_string = move_string+'U'
    elif curr_move[0] - move[0] == -1:
        move_string = move_string+'D'
    elif curr_move[1] - move[1] == 1:
        move_string = move_string+'L'
    elif curr_move[1] - move[1] == -1:
        move_string =  move_string+'R'
    return move_string
        
        


# Perform search on the map

# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# move_count is the number of moves required to navigate from start to finish, or -1
# if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)
#
def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        fringe=[(pichu_loc,0,"")]  # Initializing the fringe with a third parameter(string) for the path variable       
        move_string = ''  # it will keep the track of the path traversed
        visit_node=[]     # to keep a track of the visited nodes so that they are not looked in the search again
        move_count = 0    # to keep a track of the number of nodes traveresed to the goal
        
        while fringe:
                (curr_move, curr_dist,curr_path)=fringe.pop()  # curr_path is the varaible which is added to keep a track of the popped out path
                visit_node.append(curr_move)  # keep a track of the visited nodes
                #print(curr_move)
                #print(curr_dist)
                for move in moves(house_map,*curr_move):
                       #print(visit_node)
                       #print(move)
                       #print(house_map[move[0]][move[1]])
                        if house_map[move[0]][move[1]]=="@":
                                move_count = curr_dist+1
                                move_string = path(curr_move,move,curr_path)  
                                return (move_count, move_string)
                        elif move not in visit_node: # check if the move is visited and consider only the non-visited moves
                                move_count = curr_dist+1
                                move_string = path(curr_move,move,curr_path)
                                fringe.append((move, move_count, move_string))
                                #print(fringe)

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Routing in this board:\n" + printable_board(house_map) + "\n")
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + str(solution[1]))

