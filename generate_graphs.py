import os
import scipy.io
import numpy as np
import networkx as nx
from sklearn.preprocessing import MinMaxScaler
import json

# load the points json file indicating the points of the graph
def load_points(points_path=os.path.join(os.getcwd(), 'landmarks\horse\landmarks.m')):
    points = []
    # points_path = os.path.join(os.getcwd(), 'landmarks\horse\landmarks.m')
    with open(points_path, 'r') as f:
        for i in f:
            split_result = i.split(' = ')
            if len(split_result) >= 2:
                # print(split_result[1].split(';')[0])
                points.append(split_result[1].split(';')[0].split("'")[1])
    return points


# load the graphs json file
def load_graphs(graphs_path=os.path.join(os.getcwd(), 'behavoiur-discovery\graph.json')):
    # graphs_path = os.path.join(os.getcwd(), 'behaviour-discovery', 'graphs.json')
    with open(graphs_path, 'r') as f:
        graph = json.load(f) # the generic graph
    return graph

points = load_points()
graph = load_graphs()


# landmarks directory
def landmarks_path(directory):
    landmarks_folder = os.path.join(os.getcwd(), directory)
    # get the landmarks folder to a list
    landmarks = os.listdir(landmarks_folder)
    # return the path to each file
    return [os.path.join(landmarks_folder, landmark) for landmark in landmarks if landmark.endswith('.mat')]

# load a file
def load_file(filename):
    # only load .mat files
    if filename.endswith('.mat'):
        mat = scipy.io.loadmat(filename)
        return mat['landmarks']

# a function to take in the loaded file and return a sequence of graphs
def graph_sequence(directory='landmarks\horse'):
    # load the files
    files = landmarks_path(directory)
    print(files)
    graphs_dict = dict() # A dictionary of all the files and the graphs
    # load each file
    for file in files:
        graph_list = [] # a list of graphs for each file
        # load the file
        loaded_file = load_file(file)
        print(f'Loaded file: {file}, shape: {loaded_file.shape}')
        # loop through each frame
        for frame in loaded_file[0][0]: # the first frame of the first landmark
            # get the positions and if present
            positions = frame['positions'][0]
            present = frame['present'][0]
            print(f'Positions shape: {positions.shape}') # the x,y coordinates for the first frame
            print(f'Present shape: {present.shape}')
            # normalize the positions to be between 0 and 1
            scaler = MinMaxScaler()
            positions = scaler.fit_transform(positions)
            positions = [np.linalg.norm([x, y]) for x, y in positions]

            # absent_nodes
            absent_nodes = [key for key, val  in dict(zip(points, present)).items() if val == 0]

            # initialize graph
            G = nx.Graph()

            # add nodes and weighted edges
            for node, neighbors in graph.items():
                for neighbor in neighbors:
                    if neighbor not in absent_nodes and node not in absent_nodes:
                        # get the weights
                        weights = dict(zip(points, positions))[neighbor] 
                        # add the weighted edges
                        G.add_edge(node, neighbor, weight=weights)
            # append the graph to the list
            graph_list.append(G)
        # add the file and the list of graphs to the dictionary
        # split the filename
        file2split = file.split('\\')[-1]
        graphs_dict[file2split] = graph_list
    # return the dictionary
    return graphs_dict

if __name__ == '__main__':
    # generate the graph sequence
    graph_seq = graph_sequence()
    # save the graph sequence to a json file for later use
    with open('graph_sequence.json', 'w') as f:
        json.dump(graph_seq, f, indent=4)

