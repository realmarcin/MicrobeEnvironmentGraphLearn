
import sys
import os
import numpy as np
import argparse
import networkx as nx
import random
import matplotlib.pyplot as plt
import pandas as pd
assert nx.__version__ >= '2.4'
import time

import array as arr 


def read_graph(node_input_file, edge_input_file):
    """
    Reads the input network in networkx.
    """
    print("starting")

    print("read nodes")
    ddf = open(node_input_file, 'r')
 
    nodes = pd.read_csv(node_input_file, delim_whitespace=True)
    data = nodes.set_index('nodes').to_dict('index').items()
 
    G=nx.Graph()

    edges_raw = pd.read_csv(edge_input_file, delim_whitespace=True)
    subject_i = edges_raw.columns.get_loc("subject")
    object_i = edges_raw.columns.get_loc("object")
    for row in edges_raw.values:
      G.add_edge(row[subject_i], row[object_i])
    print(G.nodes())
    print(G.edges())

    print(G.number_of_nodes())

    print("read edges")
    f = open(edge_input_file, 'r')
   
    c = 0 
    for line in f:
       if(c>0):
         print(line)
         line = line.replace('\n', '')
         split = line.split("\t")
         aline = [split[0] + " "+split[1]]
         #aline = [(split[0], split[1])]
         #aline = ["1 2", "3 4"]
         print(aline)
         Gnow = nx.parse_edgelist(aline, nodetype = str)
         print("Gnow "+str(Gnow))
         print(Gnow.nodes())
         print(Gnow.edges())
         G.add_edges_from(Gnow)
         print(G)
         print(G.number_of_nodes())
         print(G.number_of_edges())
         c = c + 1
       c = c + 1 
	

    f.close()

    return G


def remove_edges_from_graph(graph, n_edges_to_remove):
    """
    Remove edges from the graph.
    The removed edges are then positive examples for test/validation
    """
    max_failures = 50
    n_failures = 0
    removed_edges = []
    while len(removed_edges) <= n_edges_to_remove:
        ran_edge = random.choice(list(graph.edges())) # random candidate for removal
        node1 = ran_edge[0]
        node2 = ran_edge[1]
        #check if the degree of node corresponding to an edge that is going to be removed is greater than 1
        if graph.degree[node1] == 1 or graph.degree[node2] == 1:
            n_failures += 1
            if n_failures == max_failures:
                print("[WARNING] Could not generate sufficient edges. Cannot finish edge extraction")
                break
        else:
            graph.remove_edge(*ran_edge)
            removed_edges.append(ran_edge)
            n_failures = 0
        if len(removed_edges) % 100 == 0:
            print("Extracted %d edges" % len(removed_edges))
    return removed_edges


def generate_negative_edges_from_graph(graph, n_edges_to_generate):
    print("[INFO] Will extract negative edges.")
    negative_edges = []
    i = 0
    max_failures = 100
    n_failures = 0
    start = time.time()
    edges_graphs = graph.edges()
    while i <= n_edges_to_generate:
        rand_node_1 = random.choice(list(graph.nodes()))
        rand_node_2 = random.choice(list(graph.nodes()))
        edge = (rand_node_1, rand_node_2)
        #print(edge)
        if edge not in edges_graphs and edge not in negative_edges:
            #print(edge)
            negative_edges.append(edge)
            n_failures = 0
            i += 1
            if i % 1000 == 0:
                print("Extracted %d negative edges" % i)
                end = time.time()
                print(str(end - start))
                start = time.time()

        elif n_failures == max_failures:
                print("[WARNING] Could not generate sufficient edges. Cannot finish edge extraction")
                break
        else:
            n_failures += 1
            continue
    return negative_edges


def extract_test_edges(graph, test_proportion, validation_proportion):
    """
    extract 'proportion' amount of edges from graph without disconnecting the graph.
    Assumption is that graph is connected (not tested here)
    """
    if not isinstance(graph, nx.Graph):
        raise TypeError("graph parameter must be a networkx Graph object")
    if not isinstance(test_proportion, float):
        raise TypeError("test_proportion must be a float")
    if not isinstance(validation_proportion, float):
        raise TypeError("validation_proportion must be a float")
    if not 0.0 < test_proportion < 1.0:
        raise ValueError("test_proportion must be between zero and one")
    if not 0.0 < validation_proportion < 1.0:
        raise ValueError("test_proportion must be between zero and one")

    n_edges_graph = len(graph.edges())
    n_test_edges = int(test_proportion * len(graph.edges()))
    n_validation_edges = int(validation_proportion * len(graph.edges()))

    # number of edges that are left after removing test edges and validation edges
    n_train_edges = n_edges_graph - n_test_edges - n_validation_edges

    n_negative_train_edges = n_train_edges

    print("[INFO] Generating negative edges")
    total_neg_edges = n_test_edges + n_validation_edges + n_negative_train_edges
    neg_edges = generate_negative_edges_from_graph(graph, total_neg_edges)

    negative_test_edges = neg_edges[:n_test_edges]
    negative_validation_edges = neg_edges[n_test_edges:(n_test_edges + n_validation_edges)]
    negative_train_edges = neg_edges[(n_test_edges + n_validation_edges):]

    print("[INFO] Will extract testing edges with proportion ", test_proportion)
    print("[INFO] n_test edges=%d and original number of edges = %d" % (n_test_edges, len(graph.edges())))

    print("[INFO] Will extract validation edges with proportion ", validation_proportion)
    print("[INFO] n_validation edges=%d and original number of edges = %d" % (n_validation_edges, len(graph.edges())))
    test_edges = remove_edges_from_graph(graph, n_test_edges)
    validation_edges = remove_edges_from_graph(graph, n_validation_edges)

    return list(test_edges), list(negative_test_edges), list(validation_edges), list(negative_validation_edges), list(
        graph.edges()), list(negative_train_edges)


def write_edges_with_weights(name, graph):
    """
    This function is used for the positive edges, which have weights
    """
    print("Writing file %s" % name)
    i = 0
    with open(name, 'w') as f:
        for edge in graph.edges().data("weight"):
            f.write("{}\t{}\t{}\n".format(edge[0], edge[1], edge[2]))
            i += 1
    f.close()
    print("Wrote %d edges to file %s" % (i, name))


def write_edges_no_weights(name, edge_list):
    """
    This function is used for the negative edges, which do not have weights.
    """
    print("Writing file %s" % name)
    i = 0
    with open(name, 'w') as f:
        for edge in edge_list:
            f.write("{}\t{}\n".format(edge[0], edge[1]))
            i += 1
    f.close()
    print("Wrote %d edges to file %s" % (i, name))


def write_edge_files(g, test_proportion=0.001, validation_proportion=0.001):
    """
    Creates positive train/validation/test and negative train/validation/set sets, writing them to fine
    Args:
        g: a networkx graph object, assumed to be a single connected component
       test_proportion: The proportion of edges to remove to create a testing set
       validation_proportion: The proportion of edges to remove to create a validation set
    """
    g_copy = g.copy()
    positive_test_edges, negative_test_edges, positive_validation_edges, negative_validation_edges, positive_train_edges, negative_train_edges = extract_test_edges(
        g_copy, test_proportion, validation_proportion)
    print("[INFO] Number of positive test edges: %d" % len(positive_test_edges))
    print("[INFO] Number of positive validation edges: %d" % len(positive_validation_edges))
    print("[INFO] Number of positive train edges: %d" % len(positive_train_edges))
    print("[INFO] Number of negative test edges: %d" % len(negative_test_edges))
    print("[INFO] Number of negative validation edges: %d" % len(negative_validation_edges))
    print("[INFO] Number of negative train edges: %d" % len(negative_train_edges))
    # Graphs based on extracted edges
    # We need them to extract weights
    pos_train_graph = g.edge_subgraph(positive_train_edges)
    pos_test_graph = g.edge_subgraph(positive_test_edges)
    pos_validation_graph = g.edge_subgraph(positive_validation_edges)
    print("The pos train graph has %d edges" % len(pos_train_graph.nodes()))
    print("The pos test graph has %d edges" % len(pos_test_graph.nodes()))
    print("The pos vlidation graph has %d edges" % len(pos_validation_graph.nodes()))

    write_edges_with_weights("pos_train_edges_entire_graph", pos_train_graph)
    write_edges_with_weights("pos_test_edges_entire_graph", pos_test_graph)
    write_edges_with_weights("pos_validation_edges_entire_graph", pos_validation_graph)

    write_edges_no_weights("neg_test_edges_entire_graph", negative_test_edges)
    write_edges_no_weights("neg_train_edges_entire_graph", negative_train_edges)
    write_edges_no_weights("neg_validation_edges_entire_graph", negative_validation_edges)

    print("Finished writing four edge sets to file")
    print("number of positive train edges =", len(positive_train_edges))
    print("number of positive test edges =", len(positive_test_edges))
    print("number of positive validation edges =", len(positive_validation_edges))

    print("number of negative train edges =", len(negative_train_edges))
    print("number of negative test  edges =", len(negative_test_edges))
    print("number of negative validation  edges =", len(negative_validation_edges))



print("begin")
g = read_graph("./ENIGMA_data/masterG_nodes_1000.tsv", "./ENIGMA_data/masterG_edges_1000.tsv")
print("[INFO] Will create training/validation/test files from entire graph ")
print("[INFO] Number of nodes:{} and number of edges: {}.".format(len(g.nodes()), len(g.edges())))


test_proportion = 0.15
validation_proportion = 0.15
write_edge_files(g, test_proportion, validation_proportion)

