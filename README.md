## Route_Pichu Report:


1. The goal is to find the shortest path between the agent “p” and goal “@”. The agent can move one square at a time in any of the four principal compass directions, and the code should find the shortest distance between the two points and then output a string of letters (L, R, D, and U for left, right, down, and up) indicating that solution. 

2. The code was getting caught in an infinite loop since it was revisiting the visited states again and again and getting stuck in it.

3. In-order to keep a track of the visited states, I have added a variable named visit_node which stores the popped out path from the fringe, so that the fringe.append function only considers the non visited successors.

4. Here the initial state is the initial configuration of the map with p at the bottom left corner. The successors are the moves of p I,e up, down, left or right. Cost is the number of steps needed to reach the goal state “@“. 

5. By adding the logic of keeping a track of visited states, the fringe append and pop is implemented in a depth first search strategy, since in the code a list is used to pop and append elements, which has functionality same as the stack.

6. The variable “curr_dist” keeps the track of the steps covered to reach the goal. It is stored in the move_count variable and thus it returns the cost to reach the goal. 

7. In the code, initially the fringe has the position of p and the length of the path traversed which is 0 at the start. I added an extra parameter to the fringe for the path traversed, which is initialized as empty string.

8. In-order to calculate the path, I have added the function “path” which has the three parameters as inputs: the “curr_move” which is returned during pop, the move taken by the successor node and finally the appended list of the path traversed i.e. move_string. Thus by subtracting the values of “curr_move” and “move” varaible, we get the value of the path taken i.e. U,R,L,D.

9. Thus, the above “path” function returns the path traversed which is stored in “move_string”.

10. Once the goal state is reached, the “path” function returns the final path string to reach the goal and the move_count returns the length of the path traversed.

## Arrange_Pichus Report:

1. The goal of this part is to arrange pichus on the map configuration in such a way that there is no row/column conflict except for the case where there is an X in between pichus. User inputs the parameter k which specifies the number of pichus to be arranged on the board with the above condition.

2. Here the initial state is the configuration of the board with 1 pichu (k=1). Successor states are the configurations of the map with k = 2,3,4..n. Cost function can be neglected in this case as we are arranging the pichus one by one such that it satisfies the condition. Goal state is the configuration of all the k pichus on the board with the condition satisfied. The search abstraction used over here is depth first search as a "list" is used to append and pop the element. List is pretty similar to stack as it works in a LIFO manner.

3. The solve function in the original code appends all the possible successor nodes. Rather than doing that I have added a “check” function which checks if the successor satisfies the condition or not and then only it appends it to the fringe. It then breaks and moves on to the next succesor which in turn returns the next valid state. 

4. The logic of the “check” function works in such a way that it checks the row validity and then it checks the column validity.

5. Row validity consists of nested for-loop with outer for loop traversing through the row and the inner for loop traversing through the column. Initially the flag is set as false and there is a list “log” which gets updated if the passed successor state "s" is invalid. The column validity works in a similar way with  nested for-loop with outer for loop traversing through the column and the inner for loop traversing through the row.

6. If the “check” function encounters ‘p’ then it checks the flag, if it’s false then it sets the flag as true. If it encounters ‘x’ then it sets the flag as false and if it encounters ‘.’ then it continues through the loop. Finally,  if the element is ‘p’ and flag is true then it appends “Invalid” to the log list. In this way the validity check is applied and the above goal condition is verified.

7. Finally, when the search reaches the successor state where k=n, the same “check” function logic is applied and thus we get the goal state.

8. In the main function where the “solve” method is called, if k=1 then it just returns the initial configuration of the map and for k>1 it enters the “solve” method. Lastly, when k is out of bound, “None” is returned.
