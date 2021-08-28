## Part 1:

The basic idea behind this question is to arrange tiles of a board consisting of 20 tiles.

#### Intital State: 
A 4X5 board with 20 tiles with no empty spaces. The tiles can be arranged in any order.

#### Goal State: 
Short sequence of moves to restore the canonical configuration of the board.

#### Successor Function: 
There are several ways the tiles can be moved in order to attain the goal state.The tiles can be moved in the following ways
      i)The first and third rows can only be slid left
      ii)The second and fourth rows can only be slid right
      iii)The first,third and fifth columns can be slid upwards
      iv)The second and fourth can be slid downwards
      So there are 9 possible successor functions.
      There is a succ[] array which takes the board configuration and the path and the heuristic. The successor function depends on the path followed. 
      
 
#### Challenges: 
One of the main approaches we had tried before was to consider the misplaced tiles. But the evaluation function turned out same.Hence the code kept falling into an infinite loop each time the code ran. Hence we had to devise a better heuristic.

 
#### Heuristic used:
A heuristic is defined. The admissible heuristic is the misplaced tiles/length.If the path is upwards or downwards the length /heuristic is 4 or else it is 5. 
  
#### Working : 
In this problem,we have converted the board which is in tuple format as a list.The fringe consists of the heuristic,the board configuration and the path.Then using 'heapq'.The elements with lowest priority is popped out first.The lowest priority means the one with the least heuristic. In the successors() function. 9 states are created as copies. A for loop is run to traverse the columns.So while the states will have columns constant as i and the rows keep changing.Now in the first case we can see that the first and third rows can be slid to the left so we implement it in the following manner:

For the first row

 If we have to move left. We consider the value of i and the modulus symbol(%) indicates the remainder. It moves to the position obtained ((i+1)%5)
for i in range(0,COLS):
   state1[0][i]=state[0][(i+1)%5)

Now since it is moved in a circular fashion.If it is at the fifth position(that is when i=1),when slid right it will go back to the first postion.For eg
for i in range(0,COLS):
   state3[1][i]=state[0][(i+4)%5] 

This same thing can be implemented for columns. The columns have upwards and downward movements.
      If we have to move upwards
for i in range(0,ROWS):
   state5[i][0] = state[(i+1)%4][0]. 

Similarly if we have to move down
for i in range(0, ROWS):
   state8[i][1] = state[(i-1)%4][1]

An array called visited[] is also declared.This keeps updating the nodes when they get visited.A variable called succ will keep popping out the least heuristic value and the same time the cost function increments by 1.if it is at goal state we print succ[2] which is the path. if it not we keep repeating the process of pushing and popping using the heap queue until the goal state is found. This is given in the solve() function. The solve() function has an array called visited[] which maintains a list of visited nodes. The heap pops out the one with the lowest heuristic in the following manner:

'heapq.heappop(fringe)' and it increments the cost function given by the variable c_s.The successor function is given in form of an array which takes         elements heuristic,board configuration and the path. Hence the final_path where the path will be stored. The final path is succ[2]. Now we are checking if succ[1] that is the board configuration is the goal state. If it is the final path which is stored in succ[2] is printed else the visited node is appended each time. In order to perform this we use heappush which will keep pushing the heuristic function and the cost function. 
  
     

## Part 2: 

The problem statement was to find the shortest driving distance between pair of given cities.

In this problem two datasets have been provided to us. One dataset consists of major highway segments of United States(also includes parts of Southern Canada and Northern Mexico).This datasets include highway names,distances,speed limits.A second dataset is created with the latitude and longititude postions.The cost function can be one of the following. 
           i)segments:-finds the path with fewer number of segments
           ii)distance: Tries to find a route with shortest final distance
           iii)time:-finds the fastest route assuming one drives the speed limit
           iv)safe:-tries to find the safest driving route.he one that minimizes the probability of having an accident.Assume that the rate of accidents is 1 per  
           millions driving for the US State highway.
           
#### Intial State: 
The start city and the destination city
 
#### Goal State: 
Path till the destination city from the start city

#### Successor Function:
Lets consider a place. All the places which is separated by a single segment or which is the closest can be considered as successor function. For instance in the dataset given to us, if we start at Bloomington_Indiana one of it's successors would be Martinsville_Indiana.

#### Challenges: 
We tried calculating the heuristic using Euclidean Distance for longitude and latitude but it did not return correct values hence we decided to go ahead with the haversine distance. Additionally, we faced issues while popping out values which had the same heuristic value, in such a case we decided to consider a second priority element i.e in our case the distance, so that incase of a tie if the heuristic value it will pop out the node with the lowest distance value in the fringe.

#### Heuristic Used: 
We eventually used Haversine formula where the distance can be calculated by using latitude and longitude. For the segment cost function we used the haversine distance divided by the average segment length (average segment length = total distance/total segments). For the distance cost function we used the haversine distance. For the time cost function we used the haversine distance divided by the average/mean speed limit. For the safe cost function we used the haversine distance in two halves: one half is divided by the interstate accident probability and the other half is divided by the noninterstate accident probability.

#### Working:
Here intinally we have used a data frame to read the road segments and the city gps data frame. In the road segments data frame we have added the time column which is calculated as distance/speel_limit. Additionaly, the probability for road accidents is calculated for each data point by considering the interstate probaility and non interstate probabilty and multiplying it by the distance covered. The calculate_heuristic function returns the haversine distance between latitudes and longitudes. 

There are 4 functions that calculate the path from start city to destination city. They all have the same logic except for the cost and heuristic function. Here are the steps involved in the calculate_min_heuristic:
1) Consider an empty fringe with values: cost+heuristic, distance, city,path
2) The fringe is converted to heap queue so that we can pop out the least heuristic element
3) Here, we are using the A* search, hence the goal state check will be outside the successor function
4) The fringe is popped out at the start and the goal state is checked, if not then it continues to the successor function which generates the succesors with neighbouring cities/highways path. The popped out cities are saved in the visited_node to avoid infinite loop problem
5) The heurisitic is caculated using the haversine distance
6) For each of the 4 functions f=cost+heuristics is different
7) Each successor is pushed and the process goes on till we find the destination city

Finally, the get_route funtion takes the cost as the input and caculates the sum of distances, time, accident probability and route. It is returned to the main function

 

## Part 3: 
The problem statement involves choosing teams for a project. An electronic survey is circulated where the following questions are asked.
i)The IU username
ii)How would you like to work 
a)You would like to work alone.Enter your userid
b)You  would like to work with 2 or 3 people and already have teammates in mind.All have agreed to work with each other.Enter all the userids                         in the following format userid1-userid2 or userid1-userid2-userid3
c)You would like to work with  2 or 3 people but dont have any specific teams in your mind.In this case you have to enter the userids in the                        following formats userid-zzz,userids-zzz-zzz.
d)You would like to work with 3 people and you have one person in mind and not the other.so give it like userid1-userid2-zzz.
iii)Enter the people you do not want to work with enter their userids here.
                             
In this problem we have to assign students to teams in such a way the complaints get minimized.It should take an input file as input which contains the students response in a single line separated by spaces.
                     
#### SOLUTION:

This problem can be solved using a combination of Local Search as well as Brute Force method. The input file contains of User_IDs, and each of them puts in the preference of their teammates that they would like to work with along with the names with whom they don't want to work with. 

#### Initial State:

For initial state, we have assigned no teams, and each individual member works alone. We have calculated the cost of this order of the teams which will be used for our comparison throughout the "yield" operation.

#### Goal State:

The goal state will always produce a state which will have lower cost than the initial state. The state will consist of a combination of groups, such that the cost is lower than the previous goal's state. There is no fixed goal state in this search problem. Our search problem keeps on finding a better solution until it times out. 

#### Successor Function:

The successor states are combinations in which the students can be grouped together. However there is a constraint in the size of the team. No team can have more than 3 members. We have used the itertools library of Python to generate the successor states. With this library we can generate various combinations in which teams can be formed. The overall successor function takes several string manupulation operations to generate it.

#### Cost Function:
The cost function utilizes the above mentioned dictionaries in the following ways:

a. In case of incorrect team size, the respective member increments the cost by 1.

b. In case of incorrect team members, the respective member increments the cost by number of people that wasn't assigned correctly.

c. In case of unwanted team members, the respective member increments the cost by 2.

The total cost of an individual will be the sum of above 3, and the total cost of the state is the sum of everybody's cost.

#### Challenges:

a. We faced several challenges for this assignment right from the beginning, i.e. to identify what the initial state was. We could have 2 ways:

1. We can make an individual member as his team, i.e. team size of 1 for each member.

2. We could randomly generate a team and then try to find the successors of it.

However the problem with the second approach is that, it is very difficult to generate the successor functions of it, as we cannot define it in a single way and that is keeps changing every time we run the program once again.

By using individual member as a team, our task to generate the successor function becomes quite easy using itertools.

b. There was another method if we randomly keep generating teams and keep checking cost, but that wasn't a proper "Search" problem, hence we decided to drop this approach.

#### Working:

1. Initially we convert the details of the input file into 3 arrays: keys(containing individual names), requested(containing the team members which are requested), not_wanted(containing names of team members they want to work with) and indices(containing the indices of keys to track the count of cost function. This has been handles using fopen in Python.

2. Along with this we have also initialized some dictionaries:

a. dictionary: To store the information about the person along with his requested teammates and non-wanted teammates.

b. dictionary_cost: To keep a track of the cost generated by each person(mails).

c. dictionary_cost_features: To keep a track of the length of the team members requested, team members requested (used to evaluate cost function) and not wanted team members.

3. The cost function utilizes the above mentioned dictionaries in the following ways:

a. In case of incorrect team size, the respective member increments the cost by 1.

b. In case of incorrect team members, the respective member increments the cost by number of people that wasn't assigned correctly.

c. In case of unwanted team members, the respective member increments the cost by 2.

4. We generate the successors using the itertools library in Python. We used the module to generate the combinations of several team members and we recursively call them our 1st state space is generated.

a. We use the '+' character to initially join 2 names of group of names to differentiate between already available teams and state space teams.

b. After doing some string manipulation, we replace the '+' with '-' to form a new team.

c. Thus the successor function returns a list of final_teams.

5. As the input to the cost function is a 2-D array, we have to convert it into a 1-D array to perform our operations. Hence we have also defined a two_d_list function.

6. In the solve function we first generate the cost of the initial state. After that we try to generate states(teams) which will reduce the cost. As there is not optimal solution for this problem, we have implemented a Local Search until we find the minimum value in a group of states. After sometime, if the system doesn't find an optimal state, it will get halted.

7.We also have set constraints like checking the current cost, and we keep running the while loop till it is greater than 0. We keep running the while loop till we reach a stage when the next team formed will have a minimum size of 4, which is not allowed. eg. if number of people in list are: 13, so we keep iterating till the number of teams becomes greater than 13//3+1, i.e. 5. Once the number of teams reduces down to five we halt. It is possible that the latest output shows more than 5 teams in the above example. That could happen if there is no state with lesser cost than the previous optimal one.

8. We then generate all the successor states inside this while loop.

9. We initialize 2 more dictionaries: cost_dict (To store all costs of each state) and dict_indices (To connect those costs with the states, as lists cannot be hashed).

10. Then we calculate the minumum cost of the state space and we compare it with previous one. If it is greater than or equal to the old one, we do not yield it, instead generate the successors of that state to search for a better state.

11. Thus if a new set of teams is formed with lesser cost after the search, we yield that value.

            
   
   
