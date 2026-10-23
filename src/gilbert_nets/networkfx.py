# imports
from tailestim import HillEstimator, KernelTypeEstimator, MomentsEstimator
import random, math
import powerlaw
import networkx as nx


def test_fx():
    return "Hello there! You've found my network functions."


# Assignment 1 functions
def pred_recurse(pred, curr_path, r_source, all_paths, all_predecessors):
    """
    The recursion portion. This builds out all possibly shortest paths recursively
    based on predecessor nodes.

    @param pred (int): The predecessor node we are building off of
    @param curr_path (list): the current path as it is built
    @param source (int): the source node we are getting all shortest paths to
    @param all_paths (list of lists): A list of all paths we have accumulated for that source

    @return None because we are just adding to the list as we go
            That might be bad practice. Not sure.
    """
    new_path = [pred] + curr_path
    if new_path[0] == r_source:
        all_paths.append(new_path)
        return
    new_preds = all_predecessors[pred]
    for new_pred in new_preds:
        pred_recurse(new_pred, new_path, r_source, all_paths, all_predecessors)


def run_pred_recurse_for_source(graph, source_node):
    """
    This runs the recursion portion for each

    @param graph (object): The graph we are working with
    @param source_node (int): the source node we want all shortest paths from

    @return all_paths (list of lists): a list of all the shortest paths from the source to every other node
                                        Some node pairs have multiple shortest paths
    """
    predecessors = nx.predecessor(
        graph, source_node
    )  # a dictionary of predecessors for the path from source to all nodes in the graph.
    all_paths = []
    for init_pred in predecessors:
        pred_recurse(init_pred, [], source_node, all_paths, predecessors)
    return all_paths


def test_my_shortest_paths(graph, test_source):
    """
    This just tests my shortest graph algorithm against Network X's.

    @param graph (object): The graph we are working with
    @param source_node (int): the source node we want to test shortest paths from

    @return success (bool), string of results
    """
    my_paths = run_pred_recurse_for_source(graph, test_source)
    incorrect_nodes = []
    for node in graph.nodes:
        my_path_list = [my_p for my_p in my_paths if my_p[-1] == node]
        their_path_list = [p for p in nx.all_shortest_paths(graph, test_source, node)]
        if not my_path_list == their_path_list:
            incorrect_nodes.append(node)

    if len(incorrect_nodes) > 0:
        return (
            False,
            f"Found the following target nodes for source {test_source} with mismatched paths: {incorrect_nodes}",
        )
    else:
        return (
            True,
            f"All paths are equal to Network X's paths for source {test_source}!",
        )


def compute_betweeness(network, print_statements=False):
    """
    This function calculates the inbetweeness for each node.

    It calculates inbetweeness of each node as the percentage of
    shortest paths it falls on between any other two nodes divided
    by the total number of shortest paths between those nodes, summed for
    all nodes.

    Basically, it loops through all the nodes and gets all the shortest paths
    from that node to every other node (using my speedier function!). Then it loops through
    all the nodes again starting at itself (so that we don't calculate all the short paths
    twice, i.e. between Node A and Node C and Node C and Node A) and gets the subset
    of shortest paths. For every node in those paths, we add 1/(# of paths) to that node's
    betweeness score, which is stored in a dictionary.


    @param network (object): The network we are looking at
    @param print_statements (boolean): whether it prints obnoxious quantities of print statements

    @return dictionary of the betweeness scores for every single node
    """

    # make sure it is a networkX object
    if type(network) != nx.Graph and type(network) != nx.DiGraph:
        raise Exception("Network must be NetworkX graph.")

    # Check to make sure graph has nodes
    if len(list(network.nodes)) < 1:
        raise Exception("Network must have nodes.")

    # First, get all the shortest paths and store in a dict
    running_betweenness = dict()
    for node_x in network.nodes:
        if print_statements:
            print(f"\n\nStarting node x {node_x}...")
        # get all shortest paths
        all_node_paths = run_pred_recurse_for_source(network, node_x)
        if running_betweenness.get(node_x) == None:
            running_betweenness[node_x] = 0
        for i in range(int(node_x), len(network.nodes)):
            node_y = list(network.nodes)[i]
            if print_statements:
                print(f"node y : {node_y}")
            shortest_paths = [my_p for my_p in all_node_paths if my_p[-1] == node_y]
            if print_statements:
                print(f"shortest_paths: {shortest_paths}")
            for shorty in shortest_paths:
                shorty_innards = shorty[1:-1]  # doesn't count if its an endpoint
                for el in shorty_innards:
                    current_val = running_betweenness.get(el, 0)
                    running_betweenness[el] = current_val + (1 / len(shortest_paths))
                    if print_statements:
                        print(f"Old val for {el}: {current_val}")
                        print(f"New val: {running_betweenness[el]}")
    if print_statements:
        print(f"Running betweeness: {running_betweenness}")
    return dict(sorted(running_betweenness.items()))


# Assignment 2 Functions


def grow_barabasi_albert_net(N, m, seed=None, debug=False):
    """
    This function creates a scale-free network using barabasi-albert model.

    It loops through and adds the proper amount of nodes (specified as param).
    For each node, it connects via m links to existing nodes.

    NOTES:
    Adds links with preferential attachment, the preferential attachment comes from choosing a random edge.
    So a node with twice as many edges is twice as likely to have an edge chosen.
    Because degree = edge count * 2, th probability for each node is then halved
    This is taken care of when we randomly select one of the edge's nodes.

    This doesn't allow self loops, and isn't exactly LCD, but it is computationally cleaner,
    and I think should create scale-free networks.

    @param N (int): The number of nodes
    @param m (int): Number of edges formed for each new node
    @param seed (int?): The seed for the network (optional)
    @param debug (bool): Whether or not you want print statements

    @return the scale-free network
    @return an array of degree sequences at N^x
    """

    # Create the graph
    degree_sequences = []
    simple_graph = nx.complete_graph(4)
    start_graph = nx.MultiGraph(simple_graph)

    # Set our seed
    random.seed(seed)

    # Our time counter
    # Start with 5 because the network always starts with 4 nodes
    t = 5

    # get our order of magnitude so we know what to print
    o_of_m = int(math.log10(N))

    degree_sequences_vals = []
    if o_of_m > 1:
        for i in range(2, o_of_m + 1):
            degree_sequences_vals.append(10**i)
    if debug:
        print(degree_sequences_vals)
    while t < N:
        t = t + 1

        # add node
        start_graph.add_node(t)

        # we don't want to accidentally select the new node's edge,
        # so we get the edge list ahead of time
        edge_list = list(start_graph.edges)

        # Now add the m edges
        for i in range(0, m):
            # get random edge
            chosen_edge = edge_list[random.randint(0, len(edge_list) - 1)]
            # print(f"chosen_edge: {chosen_edge}")

            # randomly choose one edge of that link
            chosen_node = chosen_edge[random.randint(0, 1)]
            # print(f"Chosen node: {chosen_node}")

            # attach the new edge
            start_graph.add_edge(t, chosen_node)

        if t in degree_sequences_vals:
            degree_seq = np.array(list(dict(start_graph.degree()).values()))
            degree_sequences.append(degree_seq)

    return start_graph, degree_sequences


def estimate_gamma(G):
    """
    This function estimates the gamma of a network's degree distribution using three different functions:
    - powerlaw estimate
    - hill estimate
    - moments estimate
    - Kernal-type estimate

    @param G (NetworkX network): The network you want to estimate

    @return a dict of the estimates, labeled "power", "hill", "moments", and "kernel"
    """

    gamma_estimates = dict()

    # Get the distribution
    degree_seq = np.array(list(dict(G.degree()).values()))

    # powerlaw estimate
    fit = powerlaw.Fit(degree_seq)
    pwr_gamma = fit.power_law.alpha
    gamma_estimates["power"] = pwr_gamma

    # HillEstimator
    hill_estimator = HillEstimator()
    hill_estimator.fit(degree_seq)
    hill_result = hill_estimator.get_result()
    hill_gamma = hill_result.gamma_
    gamma_estimates["hill"] = hill_gamma

    # Moments Estimator
    moments_estimator = MomentsEstimator()
    moments_estimator.fit(degree_seq)
    moments_result = moments_estimator.get_result()
    moments_gamma = moments_result.gamma_
    gamma_estimates["moments"] = moments_gamma

    # Moments Estimator
    kernel_estimator = KernelTypeEstimator()
    kernel_estimator.fit(degree_seq)
    kernel_result = kernel_estimator.get_result()
    kernel_gamma = kernel_result.gamma_
    gamma_estimates["kernel"] = kernel_gamma

    return gamma_estimates


def get_rand_num():
    """
    Helper function to return a random float that doesn't include 0

    @returns float between (0,1)
    """
    num = random.random()
    while num == 0:
        num = random.random()
    return num


def get_power_law_seq(n, gamma, avg_deg):
    """
    This function creates a a sequence in a power-law distribution.

    @param n (int): The number of elements in the sequence
    @param gamma (int): The exponent of the powerlaw
    @param avg_deg (int): The average degree for the distribution

    @return a sequence of ints that form a power-law distribution
    """
    r_i = []
    # generate random numbers
    for i in range(0, n):
        rand = get_rand_num()
        r_i.append(rand)

    # Get k-min and k-max from average degree
    k_min = math.ceil(avg_deg * ((gamma - 2) / (gamma - 1)))
    k_max = math.ceil((k_min * n ** (1 / (gamma - 1))))

    # Now get our probabilities for each possible degree,
    # based on the power-law distribution
    probs = []
    for k in range(k_min, k_max + 1):
        # Get D(K)
        D_k = (k / k_min) ** (-(gamma - 1))
        probs.append(D_k)
        # print(f"K {k} is {D_k}")

    # Now use those probabilities to calculate degree count for each number
    final_degrees = []
    for r in r_i:
        for j, _ in enumerate(probs):
            # descend down the distribution until we are not smaller
            # than the next number
            if j + 1 >= len(probs) or r > probs[j + 1]:
                final_degrees.append(j + k_min)
                break
    final_degrees.sort()
    return final_degrees
