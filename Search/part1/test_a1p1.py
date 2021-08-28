# !/usr/bin/env python3
# YOU SHOULD NOT MODIFY THIS FILE
# 
# test_a1p1.py version 2021.02.24
#
# Vibhas Vats


'''
###################################################################################################
############################# IMPORTANT CHANGES ###################################################
###################################################################################################
####### Running solver2021.py alone #######

To run solver2021.py through terminal you will have to use test_board.txt. The command should look like 
python3 solver2021.py test_board.txt 

#### Testing instruction ####

1. Copy paste both the files 'test_case.txt' and test_puzzle_a1.py in Part1 directory. 
2. Run: python3 -m pytest -v
3. It should display how are you performing in testing. 


## About test board:  'test_case.txt'

# THE BOARD PROVIDED WITH THE A1 RELEASE WILL NOT BE USED FOR TESTING. USE THIS BOARD INSTEAD.

1. There is only one test board named: test_case.txt
2. First line of the .txt file is the correct solution. 
3. The given solution may not be the shortest solution, but you will get full grade if you could get a better or same output. 

Post your doubts on InScribe!!
'''

#importing student's scripts
import solver2021
from collections import defaultdict
import pytest

############ Tests ############
canonical_state = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20]]
valid_moves_set = set('LRUD12345')
valid_moves_dict = {"R": [2,4], "L": [1,3], "U": [1,3,5], "D": [2,4]}

def get_string_output(list_):
    output = ""
    for move in list_:
        output += move
    return output

def collect_moves(move_str):
    all_moves = defaultdict(list)
    for idx in range(0, len(move_str), 2):
        if move_str[idx] in ["L", "R", "U", "D"]:
            all_moves[move_str[idx]].append(int(move_str[idx+1]))
    return all_moves


def move_right(board, row):
  """Move the given row to one position right"""
  board[row] = board[row][-1:] + board[row][:-1]
  return board

def move_left(board, row):
  """Move the given row to one position left"""
  board[row] = board[row][1:] + board[row][:1]
  return board

def transpose_board(board):
  """Transpose the board --> change row to column"""
  return [list(col) for col in zip(*board)]

def path_finder(board, path_):
  """Uses the output of student's path to reach canonical state"""
  for idx in range(0, len(path_), 2): 
    direction, index = path_[idx], int(path_[idx+1]) - 1
    if direction == "R":
      board = move_right(board, index)
    elif direction == "L":
      board = move_left(board, index)
    elif direction == "U": 
      board = transpose_board(move_left(transpose_board(board), index))
    else: 
      board = transpose_board(move_right(transpose_board(board), index))
  return board

def get_map_as_list(map_):
  ##Converts list of list into a single list for map
    map_out = []
    for row in map_:
        map_out.extend(row)
    return map_out


## Check the output of the puzzle
def check_puzzle(mapX,path_corr):
    logs= get_string_output(solver2021.solve(get_map_as_list(mapX)))
    print(get_map_as_list(mapX))
    path_found = logs.strip()
    ans_move_dict = collect_moves(path_found)
    assert logs != None, "Output is Empty!"
    assert logs != " ", "Output is Empty String!"
    ## Total length of path should be even
    assert len(path_found)%2 == 0, "Invalid Number of moves, total moves length should be an even number"
    ## valid path should be subset
    assert set(path_found).issubset(valid_moves_set), f"Invalid moves: {list(set(path_found) - valid_moves_set)}"
    ## Check for odd even rule
    for move_name, m in ans_move_dict.items():
        assert set(m).issubset(set(valid_moves_dict[move_name])), "Right moves not made! follow odd even restriction for rows and columns."
    ## Solution found should be equal in length or less
    assert len(path_corr) >= len(path_found), "Not the shortest path!"
    ## Retrace to canonical form using student's output.
    assert canonical_state == path_finder(mapX, path_found), "Canonical form doesn't match. Path found was wrong!"


def load_maps():
    maps=[]
    for name in ['test_case.txt']:
        with open(name,"r") as file:
            lines=file.read().splitlines()
            correct_path=lines[0]
            mapX=[[int(i) for i in line.split()] for line in lines[1:]]
            maps.append((mapX,correct_path))
    return maps


time_ = 30

@pytest.mark.timeout(time_)
def test_puzzle_2021_case1():
    maps=load_maps()
    mapX,corr_path=maps[0]
    check_puzzle(mapX,corr_path)




