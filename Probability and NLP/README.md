# Assignment 3: Probability and Statistical Learning

### Part I: Part-of-speech tagging 

#### Problem:

To calculate the parts of speech of words in a given sentence using 3 algorithms: 
1) Simplified Bayes Model
2) HMM
3) MCMC 


#### Training:

Calculating transition, emission, initial probabilities for the training corpus. Maintained a dictionary for each one of them. Apart from them calculated initial probability value for all parts of speech, word count probability and also the parts of speech count probability in the training set. Finally, calculated the Bayes probability for each word in the training set. 

Here is the screen shot of the dictionaries of all the probabilities in the training set:

[![Screen-Shot-2021-04-30-at-9-52-49-PM.png](https://i.postimg.cc/mgm6r9xQ/Screen-Shot-2021-04-30-at-9-52-49-PM.png)](https://postimg.cc/jDJhgLS5)

#### Emission Probability:
The emission probability of each word and pos is calculated and stored in a dictionary with a tuple of word and pos as key and its probability as the value which again is normalized for each word.
##### i.e P(w_i= beautiful | s_i=adjective)

#### Transition Probability:
The transition probability is calculated for 12 x 12 POS. It has a tuple of previous_pos and current_pos as keys and its count as values. Later the count is normalized using the total counts. 
##### i.e P(s_{i+1}=verb | s_i=adverb)

#### Initial Probability:
The initial probability distribution for the first word in every sentence is calculated using their POS. It is again normalized for the first word and used as it is.


#### Simplified Bayes Net:
The Bayes net probability was calculated and stored in a dictionary. We stored the probability for each word and all the possible POS's of that word, later they were normalized for each of the words. If the testing label exists in the training dictionary, we use the most probable POS from the training data. Else we consider it as a foreign word( 'x' ).


#### Viterbi:
We store the respective combinations of initial distribution and emission probability for the first word. For all the next words we calculate the respective products of emission probability, previous probability and transition probability. While iterating through all the 12 POS we consider the pos with the maximum probability. We append this value to the current distribution. We append such values for all 12 POS up to the length of the sentence. While calculating the probability for the first POS, if the word doesn't exist we append the most frequent first character in the initial probability. While iterating through the second word if we don't find any combination of a word with all of the 12 pos, only then we consider the exception case of using the transition probability, previous probability and a scaling constant because of not having an emission probability.
Backtracking for the last word, we chose the maximum probability for all the 12 POS. After choosing this POS we backtrack from the last word and use the maximum transition probability for that POS. For backtracking, if we don't find a combination of word and pos in the current distribution we consider the transition probability as an alternative. Then we reverse the list because the list was appended in the reverse format and return it.

#### MCMC:
Generate an initial particle, for each subsequent particle, for each variable Si, re-sample Si from the conditional distribution that holds all other variables at their present values. For example, for S2, you would sample a new part of speech from:
P(S2 | S1, S3, ..., Sn, W1, W2, ... Wn)
Computing that distribution will involve the factors of the posterior that involve S2, i.e. P(S2|S1), P(W2|S1,S2) and P(W3|S2,S3).
For Gibbs sampling, we store the emission probabilities for the 12 POS. If the POS doesn't exist we replace it with a downscaled value among all the minimum values. Then we randomly iterate for 20000 times and based on a range of probability it lies in. We do this for all the words in the sentence. Then we store the last of all the POS and return it.


#### Posterior Probability:
Over here, the sum of the probabilities for the part of speech of the given word is calculated and normalized. The posterior probability is calculated using the emission probability calculated in the training function. In this implementation the log probabilities are considered, ie. log(ab) = log(a)+log(b). 
For the simplified bayes net we calculate the probability using the sum(since log is used) of the emission probabilities for all the words. 
For the Viterbi algorithm we use emission probability and the transition probability to calculate the posterior probability, thus adding up both of the probabilities for each word in the sentence. 
For the Gibbs sampling, we calculate the probability using the emission, transition probability and using the part of speech count which has been normalized for the training data. If the pos for a word is not present in the training corpus then we chose a constant using the minimum possible product. We sum up these probabilities and return for the respective model.

#### Challenge:
Handling all the exceptions whenever the testing data had some new words or the length of sentence was exceptionally small was one challenge. This program in particularly required a lot of dictionaries to be maintained which created a confusion to update and use them.


### Part2: Mountain finding

#### Problem: To detect the edge line of a mountain in an image using Bayes Net and Hidden Markov Model.

1. The simple_mode() function gives us the solution for the 1st approach towards solving the problem. As we have the image contrast values, it would mean that higher the contrast, higher the probability that the ridge line will be present over there.
So, we implement it in the form of Bayes net, by returning the maximum value's index for each column in the edge_strength matrix. Since I have converted it into a transpose, hence we return the maximum value's index from each row. These index values are stored in ridge.

It produced decent outputs only for mountain.jpg, mountain5.jpg and mountain8.jpg.

2. We have implemented the Viterbi algorithm to solve this problem.They require Transmission and Emmision probabilities.

a. To calculate the Transition probability, we have designed the calculate_transition_probabilty() function. It is used to calculate the transition probabiities for the Hidden Markov Models for approach 2 and 3.

Whenever we have a maximum value from the previous row to be used for transition state, to ensure smoothness in the curve, we need to consider the indices which are just besides the previous maximum index. We have consider values starting from previous index-10 to index+10, i.e. 20 values.

So those indices which are near the previous value of ridge, that value is set with higher probability(0.5) and as we go further away, it is will be decreased. After doing some experimentaion, it was observed that for increasing gradient(climbing upwards), the probability value required was higher. Hence we have not used Uniform Probability Distributions.

For rising slope, we set those values to 0.35, and for downhill it has been set to 0.2. Further away, the probabilities are set to 0.1. And all the remaining transition probabilities are set to 0 as there is no chance that a pixel will reach such steep values.

For example: if the previous element of the ridge is 100, so we initialize the transition probabilities with 0.0. After this, we set the values of indices of 100-2=(98) to 100+1(101) to 0.5, indicating maximum probability. Then we set the probability of indices: 100-5(95) to 100-3(97) to 0.35. Then we set the probability of indices 100+2(102) to 100+4(104) to 0.2.
After this we set the values of 100-10(90) to 100-6(94) and 100+5(105) to 100+10(110) with probablity of 0.1. All the remaining transition probabilities are set to 0. List t_p is returned.


b. To calculate the Emmision probability, we have designed the calculate_emmission_probability() function. It returns the list of emmision probabiities of a particular column(in case of transpose the row). The emmision probabilities have been set to a normalized values for of the edge_strength values.
This is done to ensure that it ranges from 0 to 1, i.e. becomes scalable in terms of probability.


c. The hmm_viterbi() function is the function which evaluates the solution for the second approach. We have implemented a Hidden Markov Model, in which column to column transition is treated as transition probabilities, whereas the image gradient from edge strength has been treated as emmision probabilities.

d. So initially we take the transpose of the edge_strength matrix.

e. For initial probability, we have made some modifications. If we obeserve all the test images, all the mountains are starting in the 1st half of the image from middle to top. So for initializing this, the bottom 40% values of the 1st row of transpose are muliplied by 0.25 to reduce their probability. We took top 60% to ensure flexibility among test cases and not exactly at half.

f. From this list n, we select the value with highest gradient as 1st element in Ridge. We further initialize the initial probability p0 with 1. 

g .We then iterate from 1 to number of rows of transpose_gradient, generate the transition and emmision probability for each row of transpose_gradient. We multiply these values for each index together and futher multiply it with p0, implementing the Viterbi algorithm. These products are stored in viterbi_product list. Then we set the max value of this list to p0. The index of p0 from viterbi_product is stored in the ridge.

h. Thus we continue our algorithm till all rows of the transpose_gradient are visited.

i. Our code ran well for all test images except for mountain2.jpg, mountain3.jpg and mountain7.jpg, but all the images are smooth. mountain2.jpg, mountain3.jpg failed because the initial index went wrong, hence all the remaining ridge indices for those 3 images didn't go correctly.

3. a. The hmm_viterbi_human() function is used to implement the third approach with human feedback of row and column. We first convert the string value of row and column to integer.

b. The implementation is quite similar to the hmm_viterbi(), except that we need to implement this from current column(as it is true for the ridge line), till the end and again implement it from current column in a reverse manner till we reach column 0.

c. As we are converting it into a transpose_gradient matrix, the operations will run on rows instead on columns. Thus it produces a more accurate output than the 2nd approach.

d. We ran the following ridge line coordinates for all images, which gave very good outputs.

mountain.jpg- 74 77
mountain2.jpg-56 152
mountain3.jpg-42 190
mountain4.jpg-55 141
mountain5.jpg-59 93
mountain6.jpg-72 95
mountain7.jpg-20 83
mountain8.jpg-64 125
mountain9.jpg-70 169

We got perfect superimpositions for mountain.jpg, mountain5.jpg and mountain8.jpg.

#### Challenges faced, Assumptions and Design Choices:

1. One of the biggest challenges was clouds in the image, as they also have high edge strength. Similarly trees in maps like mountain2.jpg, create a bad start for the implementation.
2. The only way to solve the above problem was tweaking the probability values such that it has higher chance towards increasing slope of than the mountain as compared to downward slope.
3. Another assumption was that all test images have mountains in the tope half of the image. So for flexibility, we have reduced the values of bottom 40% row values of 1st column by multiplying it with 0.25. This helps us detecting the ridge start correctly.

### Part3: Reading text
#### Problem
Optical Character Recognition using a simple Bayes Net and HMM with MAP inference (Viterbi Decoding)

#### Text Preprocessing
Given a text file with input of the form "WORD POS_TAG WORD POS_TAG ...." remove the POS tags and unnecessary special characters to generate cleaner text.

#### Calculate Probability Distribution
<b>Initial Probability Distribution:</b> Generte a dictionary that holds the key ie. letter 'l', whose value is the number of times a sentence begins with the letter 'l'
```
{
	'A': count1/totalcount, 
	'B': count2/totalcount, 
	'C': count3/totalcount,
	.....
}
```
Additional step performed while estimating initial probability distribution:
Remove all unecessary keys from the initial distribution dictionary because it is assumed that the documents only have the 26 uppercase latin characters, the 26 lowercase characters, the 10 digits, spaces, and 7 punctuation symbols, (),.-!?'".

<b>Transition Probability Distribution:</b> Generate a dictionary of the form where each key in the dictionary is the letter l whose value is dictionary with the counts of each letter k that will follow the letter l

```
{
    'A' : {'t': count1/totalcountofA, 'l': count2/totalcountofA, ......}
    'B' : .............. ,
    'C' : .............. ,
    ........
}
```
    
<b> Emission Probability Distribution:</b> For estimating the emission probabilities we use a simple Naive Bayes classifier. If we assume that m% of the pixels are noisy, then a naive Bayes classifier could assume that each pixel of a given noisy image of a letter will match the corresponding pixel in the reference letter with probability (100 - m)%.

#### Generating Text Sequence
<b>Naive bayes classifier:</b> Each letter in the noisy image is compared with every actual letter image and the emission probability is computed. The letter whose probability is the largest among the ones computed previously determines the letter that will appear in the final text sequence.

<b> HMM with MAP inference (Viterbi Decoding): </b>
Performed as follows:
1. Compute the initial probabilities for all hidden states(actual letters) for the first observed letter(noisy image letter)
2. Recursively find the most probable sequence of hidden states by doing the following:
    a. Find the probabilities of the probable paths from state q(t-1) to q(t) --> vi(t-1)
    b. Compute max(1<=i<=N) vi(t-1) *  TP[i,j]
    c. vi(t) = emission_prob[j,t] * max(1<=i<=N) vi(t-1) *  TP[i,j]
3. To find most probable sequence of letters, trace back is performed iteratively as follows:
    - start from state t, find the hidden state corresponding to the highest probability, then state t-1 and so on until t=0
    - add all the hidden states to form a sequence of letter.
4. In this implementation the log probabilties are considered, ie. log(ab) = log(a)+log(b)


#### Assumptions and Design Choices
1. Dictionaries are used for easy look up operations.
2. When there is a missing transition probability of letter l to letter k, the count of the l -> k is assigned 1. When the counts are normalized, the probability of transition from l->k is now 1/totalcount. This ensures that the decoded sequence obtained after traceback is sensible ans helps get good results.
3. Documents only have the 26 uppercase latin characters, the 26 lowercase characters, the 10 digits, spaces, and 7 punctuation symbols, (),.-!?'".






