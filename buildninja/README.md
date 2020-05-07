## Step 3

The source code is attached here.
The functions are implemented under the hydrogen_framework::Graph class in Graph.cpp file.
The main workhorse is dfs() function. The path_added() and path_removed() will invoke the dfs() function and print out the paths in console. The printGraph() function has been implemented to color the paths added and paths removed.

Since the program specifications are not provided, the two functions are implemented to be compatible with the original program. Path class keeps track of the instructions and retain all pointers to lines/functions/edges, etc..

## 