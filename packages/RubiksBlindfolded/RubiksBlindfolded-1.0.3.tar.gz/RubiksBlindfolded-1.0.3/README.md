# RubiksBlindfolded
This python package is about the solving algorithm of Rubik’s cube in blindfolded technique

It provides the solving sequence for edges and corners separately, the indexes of swapping cubies in the initial scrambled cube, also the parity check and specify if the number of swapping is odd or even. You can display the current cube state manually after each step to track the changes

Memorizing the cubies is the hardest part for any beginner, making a visual tool may help you to reduce the load from your brain and you don’t need imagination!
You can use the pacakge to build any blindfolded tool for beginners.


The solving algorithm is based on a previous project developed by javascript, you can see the project https://github.com/mn-banjar/RubiksCubeBlindfolded

## Installation
This package is published on PyPI org and can be installed by this instruction 
```$ pip install RubiksBlindfolded```

## Usage
First you have to import the package onto your script 

### Inputs
the package requires only 3 inputs dictionaries: cube sides, edge priorities, and corner priorities. Here are some example of how to write these dictionaries:
```
sides = {'U': ['D', 'B', 'U', 'L', 'U', 'U', 'R', 'R', 'B'],
         'F': ['U', 'F', 'R', 'F', 'F', 'R', 'U', 'R', 'R'],
         'R': ['D', 'F', 'B', 'D', 'R', 'D', 'F', 'R', 'D'],
         'D': ['F', 'U', 'U', 'D', 'D', 'B', 'F', 'L', 'L'],
         'B': ['L', 'U', 'R', 'B', 'B', 'L', 'B', 'B', 'D'],
         'L': ['F', 'F', 'B', 'U', 'L', 'D', 'L', 'L', 'L']}
			 
edgePriority = {0:['U',1,'B',1],
                1:['U',3,'L',1],
                2:['U',7,'F',1],
                3:['B',5,'L',3],
                4:['L',5,'F',3],
                5:['F',5,'R',3],
                6:['R',5,'B',3],
                7:['D',1,'F',7],
                8:['D',3,'L',7],
                9:['D',5,'R',7],
               10:['D',7,'B',7]}

cornerPriority = {0:['U',2,'R',2,'B',0],
                  1:['U',6,'L',2,'F',0],
                  2:['U',8,'F',2,'R',0],
                  3:['D',0,'F',6,'L',8],
                  4:['D',2,'R',6,'F',8],
                  5:['D',6,'L',6,'B',8],
                  6:['D',8,'B',6,'R',8]}
```
The priorities of swapping will be explaned in below sections 

### Functions
This package has 16 functions, there are some unique functions and others that repeated for edges and corners.

```setCube(sides)``` takes 1 dictionary input argument which is the cube sides, this function is used to store the cube state and this function must be executed before solving the cube

```displayCube()``` returns the current cube state (as a dictionary output) and it can be used to track the changes
 
```displayEdgePriority()``` & ```displayCornerPriority()``` return the default edge or corner priorities (as a dictionary output)

```updateEdgePriority(edgePriority)``` & ```updateCornerPriority(cornerPriority)``` take 1 dictionary input argument which is the edge or corner priorities, these functions are used to update the priorities and you can only specify the updated items on your dictionary while the rest will be remaining unchanged

```getSolvedEdges()``` & ```getSolvedCorners()``` return a list of already solved cubies and return a None if there are no solved cubies

```solveEdges()``` & ```solveCorners()``` are used to solve the edges or corners, these return the solution sequence as a list output and return a None output if the edges or corners are already solved!

```indexEdgeSequence()``` & ```indexCornerSequence()``` return the solution sequence with its index and returns a None if the edges or corners are already solved. You can use the indexes to point in your cube

```currentEdgeBuffer()``` & ```currentCornerBuffer()``` return a sequence of the current buffer while swapping and return a None if the edges or corners are already solved
```parityCheck()``` this function is used to check if the number of swapping is odd or even. It returns 1 if the number is odd, 0 if the number is even, and None if the cube is already solved

```parityAlgorithm()``` this function is used to apply the parity algorithm if the solution has an odd parity

### Solving the cube
There are some necessary steps you have to follow to get correct results:
*  Don’t miss to set your cube by using this function ```setCube(sides)``` before appling the algorithm and execute any other functions 
*  You can start solving either the edges or corners, but you have to apply the parity algorithm using this function ```parityAlgorithm()``` in between the two solving algorithms


## Cube structure
As it was mentioned the algorithm is used a dictionary input to represent the cube, the keys are used to specify the face letters and the values are lists of 9 items. There are no unique labels for each stickers, the algorithm is based on the cubies structure and it is used a bunch stickers as one unit


Here is the cube structure, notice that the numbers represent the list indexes of each faces
```
	         |                |
	         | U0    U1    U2 |
	         |                |
                 | U3    U4    U5 |
	         |                |
	         | U6    U7    U8 |
	         |________________|
|                |                |                |                |
| L0    L1    L2 | F0    F1    F2 | R0    R1    R2 | B0    B1    B2 |
|                |                |                |                |
| L3    L4    L5 | F3    F4    F5 | R3    R4    R5 | B3    B4    B5 |
|                |                |                |                |
| L6    L7    L8 | F6    F7    F8 | R6    R7    R8 | B6    B7    B8 |
|                |________________|                |                |
	         |                |
	         | D0    D1    D2 |
	         |                |
	         | D3    D4    D5 |
	         |                |
	         | D6    D7    D8 |
	         |                |
```

## Swapping priorities 
You may need to change the buffer while solving the cube, this algorithm has swapping priorities for changing the edge and corner buffer
The default priorities are:
```
edgePriority = {0:['U',1,'B',1],
                1:['U',3,'L',1],
                2:['U',7,'F',1],
                3:['B',5,'L',3],
                4:['L',5,'F',3],
                5:['F',5,'R',3],
                6:['R',5,'B',3],
                7:['D',1,'F',7],
                8:['D',3,'L',7],
                9:['D',5,'R',7],
               10:['D',7,'B',7]}

cornerPriority = {0:['U',2,'R',2,'B',0],
                  1:['U',6,'L',2,'F',0],
                  2:['U',8,'F',2,'R',0],
                  3:['D',0,'F',6,'L',8],
                  4:['D',2,'R',6,'F',8],
		  5:['D',6,'L',6,'B',8],
                  6:['D',8,'B',6,'R',8]}
```
					 
You can update the values by using these two functions ```updateEdgePriority(edgePriority)``` & ```updateCornerPriority(cornerPriority)``` 

## Performance
For faster solution, try not to print any unnecessary results

## Testing
Clone the repository and run the ```test_package.py``` script
