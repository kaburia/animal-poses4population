import mediapipe as mp
import cv2
import pandas as pd
import datetime
import os
import json
import matplotlib.pyplot as plt
import json
import networkx as nx
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from umap import UMAP

def mediapipe_pose_graph(landmarks: dict, pose_graph: dict, draw: bool = False):
    """
    Create a graph from the landmarks and the pose graph
    """
    # if null landmarks, return None
    if landmarks is None:
        return 
    # Initialize a new graph
    G = nx.Graph()

    node_positions = {k: (0, 0) if v['visibility'] == 0 else (v['x'], -v['y']) for k, v in landmarks.items()}

    # Add nodes with positions and existence probability
    for node, coord_prob in landmarks.items():
        # x,y is zero if the visibility is zero
        if coord_prob['visibility'] == 0:
            x, y = 0, 0
        else:
            x, y = coord_prob['x'], coord_prob['y']
        G.add_node(node, pos=(x, y), probability=coord_prob['visibility'])

    # Add edges with weights
    for node, neighbors in pose_graph.items():
        for neighbor in neighbors:
            # check if the nodes are present
            if landmarks[neighbor]['visibility'] == 0 or landmarks[node]['visibility'] == 0:
                    continue
            x1, y1 = landmarks[node]['x'], landmarks[node]['y']
            x2, y2 = landmarks[neighbor]['x'], landmarks[neighbor]['y']
            weight = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            
            G.add_edge(node, neighbor, weight=weight)

    # Draw the graph
    if draw:
        nx.draw(G, pos=node_positions, with_labels=True, node_size=100, node_color='lightblue', font_size=8)
        # plt.show()

    return G

def dimensionality_reduction(landmarks_frames: list):
    """
    Perform dimensionality reduction on the landmarks
    """
    # Convert the list of landmark frames to a numpy array
    landmark_frames_array = np.array(landmarks_frames)

    # Reshape the array to 2D
    landmark_frames_2d = landmark_frames_array.reshape(landmark_frames_array.shape[0], -1)

    # Apply PCA
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(landmark_frames_2d)

    # Apply t-SNE
    tsne = TSNE(n_components=2)
    tsne_result = tsne.fit_transform(landmark_frames_2d)

    # Apply UMAP
    umap = UMAP(n_components=2)
    umap_result = umap.fit_transform(landmark_frames_2d)

    return pca_result, tsne_result, umap_result

def plot_dimensionality_reduction(pca_result, tsne_result, umap_result):
    """
    Plot the dimensionality reduction results
    """
    # Plot the PCA result
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 3, 1)
    plt.scatter(pca_result[:, 0], pca_result[:, 1])
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('PCA of Landmark Frames')

    # Plot the t-SNE result
    plt.subplot(1, 3, 2)
    plt.scatter(tsne_result[:, 0], tsne_result[:, 1])
    plt.xlabel('t-SNE Dimension 1')
    plt.ylabel('t-SNE Dimension 2')
    plt.title('t-SNE of Landmark Frames')

    # Plot the UMAP result
    plt.subplot(1, 3, 3)
    plt.scatter(umap_result[:, 0], umap_result[:, 1])
    plt.xlabel('UMAP Dimension 1')
    plt.ylabel('UMAP Dimension 2')
    plt.title('UMAP of Landmark Frames')

    plt.tight_layout()
    plt.show()


def display_frame_at_frame_count(frame_count, file_no):
    # Load the video
    video_file = os.path.join(os.getcwd(), 'video', f'video_{file_no}.avi')

    # Define the framerate
    # framerate = 60

    cap = cv2.VideoCapture(video_file)

    # Set the frame position to the desired point
    # frame_position = int(frame_count / framerate * cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)

    # Read the frame at the desired point
    success, frame = cap.read()
    if not success:
        print('Error reading the video file')
        return

    # Display the frame with matplotlib
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.show()

    # Release the video
    cap.release()