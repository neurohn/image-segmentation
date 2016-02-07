A python implementation of the algorithm described in the paper [Efficient Graph-Based Image Segmentation](http://www.cs.brown.edu/~pff/segment/).

## Pre-requisites
- Python Imaging Library
- numpy
- scipy
- random

## Correct Usage
Correct usage: ```$ python main.py sigma neighborhood K min_comp_size input_file output_file```


## Implementation Details
- test.sh : shell script provided as an example of sample usage of library
- main.py : core implementation
- graph.py : utilities for building graphs and segmenting forests (Forest here is new class defination for a hierarchical graph)
- smooth_filter.py: utilities for some image filtering operations

## Important Simplification from Original Paper
The internal variation of superpixels is not measured exactly as the maximum edge weight of the minimum spanning tree. Instead, it is approximated as the weight of edge merged last within it. This also happens to be the largest edge weight absorbed by the superpixel.

