# Assignment 2

### Part 1: Pikachu

#### Problem Formulation:

1) The game consists of a board NxN, where N>=7. It is a two player game consisting of black and white pieces. The white pieces/pichus are placed on 1st and 2nd row and the black placed on 2nd last and 3rd last row. If any one of the pichu reaches the opposite end of the board i.e for white the last row and for black the first row then that piece turns into a pikachu.
2) The goal is to predict the next best possible move for the max player given the initial board configuration. 
3) The possible moves for pichus include: moving forward, left, right by one position if the position is empty. 
4) The possible attacks of pichus include: moving forward, left, right by two positions on an empty block if there is an opponent piece one step forward, left, right respectively. Thus the opponent piece is killed in the process.
5) The possible moves for pikachu include: moving any number of steps forward, left, right on an empty block, given the blocks in between are also empty.
6) The possible attacks of pikachus include: moving any number of steps forward, left, right above an opponent piece, given the blocks after the opponent piece are empty. It can move to any block after the opponent piece, and killing the opponent in that process.
Thus, here our aim was to build 4 different methods for the moves and attacks of the pichu and pikachu i.e moves for white pichu, pikachu and moves for black pichu, pikachu.
7) Also, since the game tree can get pretty big, an evaluation function is important to judge the utility of the board for any given state, whether it favors black or white. So, if the max player is white then the utility should be positive for white so that it is likely to win. Thus, instead of going all down to the terminal state we traverse to a specific depth calculate the evaluation function and propagate it back up which selects the best possible move for the max player using the minimax algorithm
8) Inorder to further improve the efficiency of the game tree we also decided to implement alpha beta pruning which will basically prune the part of the tree for which alpha is greater than equal to beta

#### Program Description:

1) Inorder to generate the possible moves of pichus and pikachus there are 4 methods in the program:
pichu_move_w(board,N) - Calculates all the possible moves of white pichus on the board along with the attacking moves as well. This function consists of 6 components i) white pichu moving forward ii) white pichu moving left iii) white pichu moving right iv) white pichu moving two steps forward by killing the opponent piece in between v) white pichu moving two steps left by killing the opponent piece in between vi) white pichu moving two steps right by killing the opponent piece in between. It also converts the white pichu to pikachu if it reaches the last row of the board. 

pichu_move_b(board,N) - Calculates all the possible moves of black pichus on the board along with the attacking moves as well. This function consists of 6 components i) black pichu moving forward ii) black pichu moving left iii) black pichu moving right iv) black pichu moving two steps forward by killing the opponent piece in between v) black pichu moving two steps left by killing the opponent piece in between vi) black pichu moving two steps right by killing the opponent piece in between. It also converts the black pichu to pikachu if it reaches the last row of the board.

pikachu_move_w(board,N) - Calculates all the possible moves of white pikachus on the board along with the attacking moves as well. This function consists of 6 components i) white pikachu moving forwards any number of empty steps ii) white pikachu moving left any number of empty steps iii) white pikachu moving right any number of empty steps iv) white pikachu moving any number of empty steps forward by killing the opponent piece in between v) white pikachu moving any number of empty steps left by killing the opponent piece in between vi) white pikachu moving any number of empty steps right by killing the opponent piece in between

pikachu_move_b(board,N) - Calculates all the possible moves of black pikachus on the board along with the attacking moves as well. This function consists of 6 components i) black pikachu moving forwards any number of empty steps ii) black pikachu moving left any number of empty steps iii) black pikachu moving right any number of empty steps iv) black pikachu moving any number of empty steps forward by killing the opponent piece in between v) black pikachu moving any number of empty steps left by killing the opponent piece in between vi) black pikachu moving any number of empty steps right by killing the opponent piece in between

2) To calculate the utility value for a particular depth of the game tree created an evaluation function:
evaluation_function(board,max_player) - Calculates the utility value for a particular board and the given max player. As the utility value will change depending on the max player. It has the following components: 
5 x (number of pichus of max player - number of pichus of min player)
25 x (number of pikachus of max player - number of pikachus of min player)
10 x (number of pichus of max player in opponent half - number of pikachus of min player in opponent hald) - here for white the opponent half will be 2nd last and 3rd last row and for black it will be 2nd and 3rd row
0.5 x (mobility of max player - mobility of min player) - mobility is nothing but the number of possible moves it can make 

3) There is a successor function which combines the moves of white pieces and black pieces:
successor(board,player) - Returns the successors of white and black depending on the player passed. For white: pichu_move_w(board,N)+pikachu_move_w(board,N)
And for black: pichu_move_b(board,N)+pikachu_move_b(board,N)

4) There is a method which checks for the terminal state of the board i.e. when the white pieces are over or black pieces are over.
terminal(board,player) - If max player is white and if the sum of black pieces is zero then it returns true. If the max player is black and if the sum of white pieces is zero then it returns true. Otherwise it returns false.

5) The main function calls the find_best_move(board,player,timelimit,depth) iteratively for a depth ranging from 3 to 10. It returns the best possible move.

6) The find_best_move(board,player,timelimit,depth) basically sets the max and min player depending on the input and passes the results to aplha_beta_result(board,max_player,min_player,depth)

7) aplha_beta_result(board,max_player,min_player,depth) sets the alpha and beta value as -inf and inf respectively and calls the min_method(board,max_player,min_player,alpha,beta,depth) and tries to maximize the value it returns.

8) min_method(board,max_player,min_player,alpha,beta,depth) checks if the board has reached terminal state or the required depth otherwise calls the max_method(board,max_player,min_player,alpha,beta,depth) it returns the value for which the minimum is taken and stored in v. The alpha beta check is applied and if alpha is greater than or equal to beta then the branch is pruned. 

9) max_method(board,max_player,min_player,alpha,beta,depth) checks if the board has reached terminal state or the required depth otherwise calls the min_method(board,max_player,min_player,alpha,beta,depth) it returns the value for which the maximum is taken and stored in v. The alpha beta check is applied and if alpha is greater than or equal to beta then the branch is pruned.

#### Problems Faced:

Faced difficulties with generating the successors of the board for white and black. Since we took it as a 1D list it was a little tedious but through conditions and slicing it was possible to formulate all the game rules into the problem.
Setting the weights for the evaluation function was a bit confusing as there was no proper direction as to which weights to pick. Tried a different bunch of combinations and finally decided to go with the ones mentioned above.



### Part 2: The Game of Sebastian

#### Problem Statement: 

Implement a program that plays Sebastian as well as possible, i.e. getting the highest possible score. Your goal is to achieve as high an average score as possible.

#### Brief Approach:

As this game consists of both luck as well as skill, it comes under the category of Games of Chance. We have implemented a combination of Greedy as well Expectimax Algorithm for the game of Sebastian. The problem with only using Expectimax algorithm is that it has a time complexity of O(n^5). Our greedy approach might not always be the best, but it still reduces the search space and also could give a higher probability of getting a higher score and also tries to use all categories possible.

#### Initial State:

The initial state is dice configurations which consists of a 5 dice which have been rolled.

#### Goal State:

The Goal State is when the game is finished and we try and achieve the highest possible score of Sebastian within the constraints.

#### State Space:

The state space for the Brute Force Expectimax algorithm is a search for the entire tree, i.e. of all possible reroll configurations, i.e. 2^5=32. This can yield to minimum 6^5 calculations, there by increasing the time complexity. 

The state space for the Greedy approach is much lesser as depending on the count of dice values for that particular configurations, we decide to not try to check all the configurations, instead simply reroll those dice which have lower counts from above. It will explained in more detail in the approach below.

#### Approach:

The program written in sebastian.py runs for 100 times, and within each iteration, the following steps take place:

Step 1. Initially 5 dice are rolled created a set of 5 values between 1 and 6. Based on these values we need to make a judgement if we need to reroll a dice or any subset of dice or not, such that we could get a higher score.

Step 2. So first the first_roll() function is called. We initially convert the dice configuration from String input to a List input using the convert_dice_to_list() function.

The first_roll() function receives the inputs as dice and the current scorecard. We initially convert the string formatted dice, eg. 1 2 4 5 3 into list of dice results using convert_dice_to_list() function. We then check the count of dice values of the current dice configuration. eg. for [1,2,3,1,2], we have dice_dict as {1:2,2:2,3:1,4:0,5:0,6:0}. Then we find out the max_key over here, which contains the maximum value of the dice_dict.

2a. calculate_remaining():

The calculate_remaining() function returns the indices of those dice numbers which need to be rerolled whenever this is called. eg. for [1,2,2,5,2], we know that max_key is 2, so we return the indices of 1 and 5(not in max_key). The returned list in this case is [0,3].

2b. max_layer()

Within the max_layer() function, we take all the possible values of whether we can reroll a dice or a subset of dice from the current categories or not. So we iterate over 5 times for each roll of the dice by selecting either True(reroll it) or False(Don't reroll it). We have 2^5==32 possibilities here if we can choose to reroll a dice or not.

For each particular case, it calls the expectation() function, and for each layer and same subtree in the expectimax tree, it returns the total expectation value. 
Thus at every layer we can return the maximum expectation value(using max_so_far variable). Based on this max_so_far value, we generate the reroll list and use it as a decision to reroll.

2c. The expectation() function will help us to evaluate the expectation values of every category of reroll. For a set of 5 dice, We have 2^5=32 different possibilities of either roll or not roll. 

Based on these values, we generate the outcome_count, which we be using to evaluate the expectation value. The exp value will store the result maximum score returned from total_score() function. We calculate the sum of the exp values to generate the total expectation value of that particular level from the expectimax tree. The expection value is returned when we multiply the exp value by 1.0 and divide it by the outcome_count.

As there is no fixed method to get a high score, we try to use a greedy approach. If the constraint doesn't allow us with the greedy approach, we use the expectimax algorithm. We generate the max_key value using the dice_dict dictionary, as mentioned above.

1. If we get the maximum value in dice_dict as 3 or greater than 3, we could try to achieve the first 6 categories, squadron, triplex, quadrupla or quintuplicatam. To achieve this, we could use the calculate_remaining() function and only reroll the dice elements apart from the max_key.

2. We also need to try to achieve the bonus of 35 points. So to achieve that, we try and check which value is the max_value and if its particular value isn't in scorecard.scorecard.keys(). eg. if max_key is 6, we need to check if "sextus" is not present in scorecard.scorecard.keys(). If not, then we will reroll those dice where 6 is not present. In the worst case, a "triplex" is guaranteed (assuming that triplex hasn't been used, otherwise, we could yield "sextus"). However, we have ignored the "primus" category,as it doesn't make much difference in the total score(max achievable is 5).

3. Now the max achievable value from "sextus" is 6*5=30 and "quintus" is 5*5=25, whereas for squadron the value is 25. So we keep this above "secundus", "tertium" and "quartus".  For dice_dict[max_key]==3, we will reroll the remaining dice where key is not equal to max_key, hoping to get "squadron".

4. If none of the categories from 2 to 5 or "squadron" is available in scorecard.scorecard(), i.e. if len of reroll_list is 0, we try to achieve "quintuplicatam", "quadrupla", "triplex" by rerolling the remaining dice. If still we don't fulfill any criteria, we call the max_layer() function.

5. We could also check in the dice_dict[key]==2. If such is the case, we try to check for the "secundus" to "quintus" categories, as it might help us to give the bonus.

6. Apart from these, we could also check for "company" and "prattle", by doing individual checks of each element of dice set in a similar manner. If that category is possible, we return an empty list to reroll, of course only if it has not been used in the current scorecard.
   
7. If none of the above categories are possible, we call the max_layer() function to evaluate based on the expectation values.

Thus, this is how the first_roll() function operates.

Step 3. We then call the second_roll() function. The second_roll() function does the same tasks which first_roll() function, but only on a new set of dice outcomes. Thus we call the first_roll function again, and return a new reroll_list for the 3rd round.

Step 4. Then we call the third_roll() function. The third_roll() function will eventually calculate the maximum score which can be generated from the categories after the last reroll. The curr_categories will show the scores of all categories for the current dice configuration after we call the total_score() function. 
The problem with everytime using the maximum score is that we may end up utilizing a category which has already been used in the game. To solve this problem, we create a duplicate of scorecard.scorecard, named temp. Within temp, we delete all the categories which have already been utilized, and we delete those categories from curr_categories.

Another problem that we face is especially towards the end, when the score of the remaining categories might be of value 0, so instead of not picking up any category, it randomly chooses a category with value 0, which we won't be able to utilize for a further round. The solution to that is to delete all categories with scorecard.scorecard equal to 0 before we process any further by using a list named delete_empty. In such a case, we will never select any 0 valued entry and skip to the next round.

Thus the expectation() and max_layer() functions deal with the Brute force state space evaluation of the expectimax algorithm whereas the use of calculate_remaining() function helps us with a greedy approach.



### Part 3: Document classification

#### Problem Statement: 

Estimate the Naive Bayes parameters from training data (where the
correct label is given), and then use these parameters to classify new text objects. 

#### Loading Data

The data is initially loaded into a dictionary of the form:

```
{
"objects": objects, 
"labels": labels, 
"classes": list(set(labels))
}
```
The training data and testing data are read into a Pandas dataframe.
The train data dataframe has columns : Tweet, Label and the test data dataframe has columns: Tweet.

#### Text Preprocessing:

Procedure:
1. Lower case each tweet in the **training and test data**
2. Obtain a list of tokens in each tweet using the space delimiter.
3. Ignore the tokens that are special characters and numbers.
4. Remove stop words.
5. Join all the filtered tokens to form a string of the tweet where each filtered token is separated by a space.

The cleaned train tweets are added into a column called "Clean Text" into the train data dataframe and similarly the cleaned test tweets are added as a column to the test data dataframe.

#### Creating word-count-to-label matrix

Procedure:
1. Consider all the "Clean Text" tweets from the training data.
2. Split the train data dataframe by label to create 2 dataframes for the labels "EastCoast" and "WestCoast".
3. Create two dictionaries, one with unique words and their counts in all the tweets associated with "EastCoast" and a similar one for "WestCoast".

#### Classification of test data

Given a test tweet of the form w1 w2 w3 ... wn, the posterior probabilities of both labels are computed as follows:

P("EastCoast" | w1 w2 w3 ... wn) = P(w1 | "EastCoast) * P(w2 | "EastCoast") * ... * P( wn | "EastCoast") * P("EastCoast")

P("EastCoast" | w1 w2 w3 ... wn) = Posterior Probability

P(wn | "EastCoast) = Likelihood [Obtained from the two previously created dictionaries of unique words for both labels]

P("EastCoast") = Prior Probability [Calculated as number of tweets with East Coast Label / Total number of tweets]

The posterior probabilities for WestCoast label are computer in a similar manner.

In order to classify the tweet into either of the labels, the concept of "Odds Ratio" is utilized:

odds ratio = (P("EastCoast" | w1 w2 w3 ... wn)) / P("WestCoast" | w1 w2 w3 ... wn)

If the odds ratio > 1 then the tweet is classified as "EastCoast" and "WestCoast" otherwise.

#### Special Case: Laplace Smoothing

Suppose a word wk does not exist in the unique words dictionary for either labels, then the likelihood for this word give the label is zero.
In order to avoid the "zero probability" case, the word wk is assigned a small probability value as follows:

P(wk | "EastCoast") = 1 / (total number of unique words in east coast + total number of unique words across all documents)

P(wk | "WestCoast") is computed in a similar manner.
