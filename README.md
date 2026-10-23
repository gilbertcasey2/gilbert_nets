# Gilbert Network Science

This is an awesome package of my Network Science functions!

It is not maintained. Be careful. 

The following super-useful functions are included. 

## Functions:

#### Public Functions

1. `test_fx`: This is a simple test of the package to ensure it is working.

2. `test_all`: This is a more robust test of the package that runs all of the functions.

3. `compute_betweeness`: This is a function to calculate the betweeness for each node. It does this by calculating inbetweeness of each node as the percentage of shortest paths it falls on between any other two nodes divided by the total number of shortest paths between those nodes, summed for all nodes.
    - @param: the network (object), whether you want print statements (boolean)
    - @return: dictionary of the betweeness scores for every single node

4. `test_betweenness_func`: This function tests a betweenness function for a variety of different usecases against networkX's betweenness function.  
    - @param: the betweenness function you are testing
    - @return: success (bool), and any errors (list of strings)

5. `grow_barabasi_albert_net`: This function creates a scale-free network using barabasi-albert model. It does so by looping through and adding the proper amount of nodes (specified as param). For each node, it connects via m links to existing nodes.
    - @param: number of nodes (int), number of edges for each node (m), seed to get the same result (int?), whether you want print statements (bool)
    - @return: the scale-free network, an array of degree sequences at N^x

6. `estimate_gamma`: This function estimates the gamma of a network's degree distribution using three different functions: powerlaw estimate, hill estimate, moments estimate, Kernal-type estimate
    - @param: the network to estimate (object)
    - @return: the estimates (dict)

7. `get_power_law_seq`: This function creates a a sequence in a power-law distribution.
    - @param: number of elements in the sequence (int), gamma of the powerlaw (float), average degree (int)
    - @return: sequence of ints of a power-law distribution (list)

#### Private (internal use only) Functions

1. `_pred_recurse`: This function supports the `compute_betweenness function`, which relies on obtaining all shortest paths in a network. This function is the recursion portion, which builds out all possibe shortest paths based on predecessor nodes (working backwards until it hits the source, and appending the new path.)
    - @params: the most recent predecessor node, the current path being built, the source node we are searching for, a list of all paths accumulated for that source, and a list of all predecessors. 
    - @return None, modifies the list in place 

2. `_run_pred_recurse_for_source`: This function also supports the `compute_betweenness function`, which relies on obtaining all shortest paths in a network. It basically runs the recursive portion for each predecessor for a given source node. 
    - @param: the graph, the source node
    - @return: the list of shortest paths

3. `_get_rand_num`: This is a helper function to get a random float between 0 and 1 that doesn't include 0.
