# load the frame
import cv2
import matplotlib.pyplot as plt
from networkx import NetworkXError
import networkx as nx
import numpy as np

# load the frame
def evaluate_frame(video_file, frame_no):
    # capture the video
    vid = cv2.VideoCapture(video_file)
    try:
        # read the  frame
        vid.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ret, frame = vid.read()

        # show the frame
        plt.imshow(frame)
        plt.show()
        return frame
    except TypeError as e:
        print(f'{e}')
        plt.close()
        return None

# Generate adjacency matrix from the graph and pad it with zeros
def adjacency_matrix(graph_list, pad=True, nodes_number=(19,19)):
    adj = []
    if isinstance(graph_list, list):
        for no, i in enumerate(graph_list):
            if no == 300:
                break
            try:
                xc = nx.adjacency_matrix(i).todense()
                adj.append(xc)
            except NetworkXError:
                # print(no)
                print(f'Frame {no} has no nodes')
        
        if pad:
            # Get the maximum number of nodes by shape
            max_shape = nodes_number
            
            # print(max_shape)
        # Pad the adjacency matrix with zeros
            padded_adj = np.array([np.pad(matrix, ((0, max_shape[0] - matrix.shape[0]), 
                                          (0, max_shape[1] - matrix.shape[1])), 
                                          mode='constant') for matrix in adj])

            return padded_adj
        else:
            return adj
        
    else:
        raise TypeError('graph_list must be a list of graphs')
