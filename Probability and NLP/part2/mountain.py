#!/usr/local/bin/python3
#
# Authors: ajpawale-cdeshpa-svogiral
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, April 2021
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
import copy

# calculate "Edge strength map" of an image
#
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

"""
The calculate_transpose() function creates the transpose of the egde strength matrix. The purpose of doung this is to make accessing index of the 2-Dimensional list easier.

"""

def calculate_transpose(input_image):
    x=edge_strength(input_image)
    transpose_gradient=list(map(list, zip(*x)))
    return transpose_gradient

"""
The simple_mode() function gives us the solution for the 1st approach towards solving the problem. As we have the image contrast values, it would mean that higher the contrast, higher the probability that the ridge line will be present over there.
So, implement it in the form of Bayes net, by returning the maximum value's index for each column in the edge_strength matrix. Since I have converted it into a transpose, hence we return the maximum value's index from each row. These index values are stored in ridge.
"""

def simple_mode(input_image):
    transpose_gradient=calculate_transpose(input_image)
    ridge=[]
    for i in transpose_gradient:
        ridge.append(i.index(max(i)))

    return ridge

"""
The is_valid() function is used to ensure that no array indices go out of bounds. It will be used to check during the transitional probability calculation.
"""

def is_valid(max_size,index):
    return index<max_size

"""
The calculate_transition_probabilty() is used to calculate the transition probabiities for the Hidden Markov Models for approach 2 and 3.
Whenever we have a maximum value from the previous row to be used for transition state, to ensure smoothness in the curve, we need to consider the indices which are just besides the previous maximum index. We have consider values starting from previous index-10 to index+10, i.e. 20 values.
So those indices which are near the previous value of ridge, that value is set with higher probability(0.5) and as we go further away, it is will be decreased. After doing some experimentaion, it was observed that for increasing gradient(climbing upwards), the probability value required was higher. Hence we have not used Uniform Probability Distributions.
For rising slope, we set those values to 0.35, and for downhill it has been set to 0.2. Further away, the probabilities are set to 0.1. And all the remaining transition probabilities are set to 0 as there is no chance that a pixel will reach such steep values.

For example: if the previous element of the ridge is 100, so we initialize the transition probabilities with 0.0. After this, we set the values of indices of 100-2=(98) to 100+2(102) to 0.5, indicating maximum probability. Then we set the probability of indices: 100-5(95) to 100-3(97) to 0.35. Then we set the probability of indices 100+3(103) to 100+4(104) to 0.2.
After this we set the values of 100-10(90) to 100-6(94) and 100+5)105) to 100+10(110) with probablity of 0.1. All the remaining transition probabilities are set to 0. List t_p is returned.
"""

def calculate_transition_probabilty(index,a):
    t_p=[0]*len(a)

    
    for i in range(index-10,index-5):
        if is_valid(len(t_p),i):
            t_p[i]=0.1

    
    for i in range(index-5,index-2):
        if is_valid(len(t_p),i):
            t_p[i]=0.35
    
    for i in range(index-2,index+2):
        if is_valid(len(t_p),i):
            t_p[i]=0.5

    for i in range(index+2,index+5):
        if is_valid(len(t_p),i):
            t_p[i]=0.2

    
    for i in range(index+5,index+11):
        if is_valid(len(t_p),i):
            t_p[i]=0.1
	
    return t_p


"""
The calculate_emmission_probability() returns the list of emmision probabiities of a particular column(in case of transpose the row). The emmision probabilities have been set to a normalized values for of the edge_strength values.
This is done to ensure that it ranges from 0 to 1, i.e. becomes scalable in terms of probability.

"""

def calculate_emmission_probability(array):

    max_size=max(array)
    min_size=min(array)
    for i in range(len(array)):
        array[i]=(array[i]-min_size)/(max_size-min_size)

    return array
    
"""
The hmm_viterbi() function is the function which evaluates the solution for the second approach. We have implemented a Hidden Markov Model, in which column to column transition is treated as transition probabilities, whereas the image gradient from edge strength has been treated as emmision probabilities.

So initially we take the transpose of the edge_strength matrix.

For initial probability, we have made some modifications. If we obeserve all the test images, all the mountains are starting in the 1st half of the image from middle to top. So for initializing this, the bottom 40% values of the 1st row of transpose are muliplied by 0.25 to reduce their probability. We took top 60% to ensure flexibility among test cases and not exactly at half.
From this list n, we select the value with highest gradient as 1st element in Ridge. We further initialize the initial probability p0 with 1. 
We then iterate from 1 to number of rows of transpose_gradient, generate the transition and emmision probability for each row of transpose_gradient. We multiply these values for each index together and futher multiply it with p0, implementing the Viterbi algorithm. These products are stored in viterbi_product list. Then we set the max value of this list to p0. The index of p0 from viterbi_product is stored in the ridge.
Thus we continue our algorithm till all rows of the transpose_gradient are visited.
"""



def hmm_viterbi(input_image):

    transpose_gradient=calculate_transpose(input_image)

    n=copy.deepcopy(transpose_gradient)

    for i in range(3*len(n[0])//5,len(n[0])):
        n[0][i]=n[0][i]*0.25

    ridge=[n[0].index(max(n[0]))]

    p0=1

    for i in range(1,len(transpose_gradient)):
        t_p=calculate_transition_probabilty(ridge[i-1],transpose_gradient[i])
        e_p=calculate_emmission_probability(transpose_gradient[i])
        viterbi_product=[]
        for j in range(len(t_p)):
            viterbi_product.append(t_p[j]*e_p[j]*p0)
        
        p0=max(viterbi_product)
        ridge.append(viterbi_product.index(p0))
        
    return ridge
        

"""
The hmm_viterbi_human() function is used to implement the third approach with human feedback of row and column. We first convert the string value of row and column to integer.

The implementation is quite similar to the hmm_viterbi(), except that we need to implement this from current column(as it is true for the ridge line), till the end and again implement it from current column in a reverse manner till we reach column 0.
As we are converting it into a transpose_gradient matrix, the operations will run on rows instead on columns. Thus it produces a more accurate output than the 2nd approach.

"""


def hmm_viterbi_human(input_image,row,column):

    new_column=int(column)
    new_row=int(row)

    transpose_gradient=calculate_transpose(input_image)
    
    ridge=[0]*len(transpose_gradient)
    
    ridge[new_column]=new_row

    p0=1
   
    for i in range(new_column+1,len(transpose_gradient)):
        t_p=calculate_transition_probabilty(ridge[i-1],transpose_gradient[i])
        e_p=calculate_emmission_probability(transpose_gradient[i])
        viterbi_product=[0]*len(t_p)
        
        for j in range(len(t_p)):
            viterbi_product[j]+=(t_p[j]*e_p[j]*p0)
        
        p0=max(viterbi_product)
        ridge[i]=viterbi_product.index(p0)
        
    for i in range(new_column-1,-1,-1):
        t_p=calculate_transition_probabilty(ridge[i+1],transpose_gradient[i])
        e_p=calculate_emmission_probability(transpose_gradient[i])
        viterbi_product=[0]*len(t_p)

        for j in range(len(t_p)):
            viterbi_product[j]+=(t_p[j]*e_p[j]*p0)

        p0=max(viterbi_product)
        ridge[i]=viterbi_product.index(p0)


    return ridge        





# main program
#
gt_row = -1
gt_col = -1
if len(sys.argv) == 2:
    input_filename = sys.argv[1]
elif len(sys.argv) == 4:
    (input_filename, gt_row, gt_col) = sys.argv[1:]
else:
    raise Exception("Program requires either 1 or 3 parameters")

# load in image 
input_image = Image.open(input_filename)

ridge=simple_mode(input_image)

ridge2=hmm_viterbi(input_image)

ridge3=hmm_viterbi_human(input_image,gt_row,gt_col)






# compute edge strength mask
edge_strength = edge_strength(input_image)
imageio.imwrite('edges.jpg', uint8(255 * edge_strength / (amax(edge_strength))))

# You'll need to add code here to figure out the results! For now,
# just create a horizontal centered line.
#ridge = simple_mode(input_image)
#print(ridge)


# output answer
imageio.imwrite("output.jpg", draw_edge(input_image, ridge,(255, 0, 0), 5))
imageio.imwrite("output.jpg", draw_edge(input_image, ridge2,(0, 0, 255), 5))
imageio.imwrite("output.jpg", draw_edge(input_image, ridge3,(0, 255, 0), 5))
