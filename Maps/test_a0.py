# YOU SHOULD NOT MODIFY THIS FILE
# 
# a0_test.py version 2021.01.28
#
# Zoher Kachwala, based on code by Jagpreet Chawla
#

#importing student's scripts
import route_pichu
import arrange_pichus
from itertools import groupby
import re
import pytest

def navigate(mapX,moves):
	# Find my start position
	you_loc=[(row_i,col_i) for col_i in range(len(mapX[0])) for row_i in range(len(mapX)) if mapX[row_i][col_i]=="p"][0]
	# Find goal location
	goal_loc=[(row_i,col_i) for col_i in range(len(mapX[0])) for row_i in range(len(mapX)) if mapX[row_i][col_i]=="@"][0]    
	moves=moves.lower()
	try:
		you_row,you_col=you_loc
		for i,move in enumerate(moves):
			if move=='u':
				#moving up only row dimension (index position 0 of you_loc) updated
				you_row-=1
			elif move=='d':
				#moving down only row dimension (index position 0 of you_loc) updated
				you_row+=1
			elif move=='r':
				#moving right only col dimension (index position 1 of you_loc) updated
				you_col+=1
			elif move=='l':
				#moving left only col dimension (index position 1 of you_loc) updated
				you_col-=1
			if i == len(moves)-1:
				#True if Provided Path reaches the Goal
				return mapX[you_row][you_col]=='@'
			elif mapX[you_row][you_col]=='X':
				#Return False if Provided Path contains invalid moves
				return False
	except IndexError:
		#Moves go off the map
		return False

def seekthehidden(mapX,p_locs):
	#grouping ps by common row dimension
	row_groups=groupby(p_locs,lambda x:x[0])
	for _,row_group in row_groups:
		row_group=sorted(row_group)
		row=row_group[0][0]
		for i in range(len(row_group)-1):
			#checking the section between two consecutive ps in a row
			section=list(mapX[row,row_group[i][1]:row_group[i+1][1]])
			if 'X' not in section and '@' not in section:
				return False

	#grouping ps by common col dimension
	col_groups=groupby(p_locs,lambda x:x[1])

	for _,col_group in col_groups:
		col_group=sorted(col_group)
		col=col_group[0][1]
		for i in range(len(col_group)-1):
			#checking the section between two consecutive ps in a col
			section=list(mapX[col_group[i][0]:col_group[i+1][0],col])
			if 'X' not in section and '@' not in section:
				return False
	return True

#Part 1 needs to return the int:dist, str_list:moves
def check_solution1(mapX,dist_key):
	regex_moves=re.compile(r'^[UDRLudrl]+$')
	#function to search
	dist,moves=route_pichu.search(mapX)
	assert type(dist)==int,"Distance is not an integer"
	assert regex_moves.match(moves),"Moves contain invalid characters"
	assert dist==dist_key,"Wrong solution"
	assert dist==len(moves),"Distance and path length are not equal"
	assert navigate(mapX,moves)==True,"Path did not reach the goal"

#Part 2 needs to return the 2d_list: map,bool: if_solution_exists
def check_solution2(mapX,sol_exist_key,n):
	solved_map,sol_exist=arrange_pichus.solve(mapX,n)
	import numpy as np
	solved_map=np.array(solved_map)
	mapX=np.array(mapX)
	assert solved_map.shape==mapX.shape,"Shape of maps does not match"
	assert len(set([c for row in solved_map for c in row])-set(['.','X','p','@']))==0,"Map contains invalid characters"
	assert sol_exist==sol_exist_key,"Wrong solution"
	#replacing p on both maps
	solved_map_p=np.array([[c.replace('p','.') for c in row] for row in solved_map])
	mapX_p=np.array([[c.replace('p','.') for c in row] for row in mapX])
	assert np.array_equal(solved_map_p,mapX_p),"The buildings in the original map replaced"
	p_locs=[(row,col) for col in range(solved_map.shape[1]) for row in range(solved_map.shape[0]) if solved_map[row,col]=='p']
	assert len(p_locs)==n,"Wrong number of pichus placed"
	assert seekthehidden(mapX,p_locs)==True,"Pichus can see each other"

def load_maps():
	maps=[]
	for name in ['map.txt','map2.txt']:
		with open(name,"r") as file:
			mapX=[list(line) for line in file.read().splitlines()]
		with open(name + '.solution.txt',"r") as file:
			lines=file.read().splitlines()
			dist=int(lines[0])
			sol_exist=bool(lines[1])
			n=int(lines[2])
			maps.append((mapX,dist,sol_exist,n))
	return maps

@pytest.mark.timeout(30)
def test_question1_case1():
	maps=load_maps()
	mapX,dist_key,_,_=maps[0]
	check_solution1(mapX,dist_key)

@pytest.mark.timeout(30)
def test_question2_case1():
	maps=load_maps()
	mapX,_,sol_exist_key,n=maps[0]
	check_solution2(mapX,sol_exist_key,n)

@pytest.mark.timeout(30)
def test_question1_case2():
	maps=load_maps()
	mapX,dist_key,_,_=maps[1]
	check_solution1(mapX,dist_key)

@pytest.mark.timeout(30)
def test_question2_case2():
	maps=load_maps()
	mapX,_,sol_exist_key,n=maps[1]
	check_solution2(mapX,sol_exist_key,n)


