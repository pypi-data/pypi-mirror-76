# 2-Opt Search Algorithm 

In optimization, 2-opt is a simple local search algorithm with special swapping mechanism that suits well to solve the 
traveling salesman problem. This algorithm is sensitive to the initial point of search, i.e., its final results get 
changed by different initial points. 2-opt runs very fast such that a tsp with 120 cities can be solved in less than 
5 sec on the intel core i7. To get a more reliable result, you should run the 2-opt with different randomized initial 
points for enough number of times. One more thing, the travelling salesman problem has many applications in real world 
such as logistic planning or DNA sequencing. So, having a fast and simple method to solve the TSP is valuable. 

 
## Library
The library requires the following libraries:

* Numpy
* Random
* Time

## Install

It can be installed using pip:
'''
pip install py2opt
'''
Alternatively it can be intalled via conda:

'''
conda install -c conda-forge py2opt
'''

## Usage

To use this library, you must have a distance matrix showing  distance among all 
First thing to do is create an instance of the RouteFinder class, which reads in a corpus of text and does some indexing on it

Note that this package doesn't do calculate distance matrix in this version. 

The data:

```
nodes = ['A', 'B', 'C', 'D']
dist_mat = [[0, 2, 5, 3], [2, 0, 7, 2], [5, 7, 0, 1], [3, 9, 1, 0 ]]

```

The format of the output should be (note that this is not an optimal route):

```
Vancouver
Calgary
Edmonton
Seattle
Portland
Los Angeles
San Francisco
Denver
5523 km
```

And that's pretty much it!

