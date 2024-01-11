=================================================================================================================================
Behavior discovery dataset 2.0

Luca Del Pero, Susanna Ricco, Rahul Sukthankar, Vittorio Ferrari
=================================================================================================================================

This dataset contains video shots for two different object classes: tigers and dogs. 
We ensure that each shot contains at least one object of the corresponding class.
This release contains 523 tiger shots collected from nature documentaries,
and 102	 dog shots and 99 horse shots from YouTube. 
For each class, the <classname>.tar.gz file contains all frames of all shots. 

We release individual video frames after decompression, in order to eliminate possible confusion when decoding the videos and 
in the frame numbering. The frames are stored in .jpg format. For each class, all frames from all shots are concatenated and 
named sequentially using 8 digits (e.g 00000001.jpg, 00000002.jpg etc).

=================================================================================================================================
1. Ranges
=================================================================================================================================

We provide a ranges.mat file for each class, specifying which frames belong to which shot.
This contains a 3xS array, where S is the number of shots for the class: 
---------------------------------------------------------------------------------------------------------------------------------
col 1: shot_id
col 2: Index of the first frame of the shot
col 3: Index of the last frame of the shot
---------------------------------------------------------------------------------------------------------------------------------

Note that the data at point 2 and onwards is not available for all shot ids.

We also provide the splits used in [1].
For tigers we use three splits:
1) tigersVal, used for training
2) tigersFg, containing video intervals from 100 shots manually selected such that the foreground segmentation produced by [2] is accurate
3) tigersAll, containing all video_intervals from tiger shots.
4) tigersAllAuto, like in tiger_all, but here the intervals were temporally segmented automatically as discussed in [1]. For all other splits,
the video intervals are temporally segmented manually, such that they contain exactly one behavior.
For dogs, we only use one split:
1) dogsAll, containing all dog shots
For horses, we only use one split:
1) horsesAll, containing all horse shots
Each file contains an NX3 matrix (videoIntervals), where N is the number of intervals in the split. 
Each row contains the following:
[shot_id start_frame end_frame]
For example [4 10 20] is the interval between the 10th and the 20th frame (included) from shot_id 4 
(use this in ranges.mat to recover the start and end frame of the shot).
Ground-truth labels (see below) are available for all frames in all video intervals in these splits. 

=================================================================================================================================
2. Ground-truth behavior labels
=================================================================================================================================

We annotated each frame with the behavior performed by the foreground object (e.g. walk, run, turn head).
If more than an object is present, we annotated the behavior of the object closest to the camera.
If an object is performing more than one behavior, we annotated them all starting from the behavior
happening at the largest scale (for example, "walk" before "turn head", "turn head" before "blink").
All behaviors involve object motion (for example lying still is not a behavior, nor is standing still on a skateboard).

For each shot, the ground-truth file behaviors/<class>/<shot_id>.mat contains an cell array of length K (annotations) 
and a vector of length K (numAnnotations), where K is the number of frames in the shot.
Each cell in “annotations” contains the ids of the behaviors in that frame sorted by scale (it is empty if there is no behavior).
Each entry in numAnnotations is the number of behaviors for that frame (numAnnotations(K) = length(annotations{K}).
Note that for evaluation in [1] we only used one label per frame (the one at the largest scale, i.e. the first one
in “annotations” ). 
Files behaviors/<class>/behaviors.m contain the meaning of these ids (e.g. 1="walking”, 2="turning_head", etc.) 

=================================================================================================================================
3. Ground-truth landmarks [2]
=================================================================================================================================

These are available for most horse shots, and for shots in tigerVal.
For each shot, the ground-truth file landmarks/<class>/<shot_id>.mat contains a cell array of length K (landmarks).
landmarks{k} contains two fields:
present -> a 1xNum_landmarks vector of boolean. An entry set to true means the corresponding
           landmark is visible in frame k
position -> a 2xNum_landmarks vector. It contains the (X,Y) position of the landmarks at frame k.

The list of landmark is available in files landmarks/<class>/landmarks.m.
Videos visualizing the landmarks are in landmarksVideos/<class>.

=================================================================================================================================
4. Foreground segmentations by [3]
=================================================================================================================================

Folder <class>Seg contains the foreground segmentations computed using [3] for all shots of the class.
For each shot, we provide a cell array of length N (one cell per frame) in file <class>Seg/<shot_id>.mat.
Each cell is a binary mask of the same size of the frame (1=foreground, 0=background).

=================================================================================================================================
5. Comparison to [1]
=================================================================================================================================
In [1] we cluster the video intervals in a split using several different representation.
We evaluate in terms of clustering purity and Adjusted Rand Index (ARI) computed with respect to the ground-truth behaviors.
For all splits except tiger_all, each video interval contains exactly one behavior.
For tiger_all_auto, we select as ground-truth the most frequent behavior label in the interval as explained
in [1] (we use an extra “dummy” label for intervals where the majority of the frames have no behavior label). 


=================================================================================================================================
References
=================================================================================================================================

[1] Articulated Motion Discovery using Pairs of Trajectories
Luca Del Pero, Susanna Ricco, Rahul Sukthankar, Vittorio Ferrari,
In Computer Vision and Pattern Recognition (CVPR), 2015.

[2] Recovering Spatiotemporal Correspondences between Deformable Objects by Exploiting Consistent Foreground Motion in Video
Luca Del Pero, Susanna Ricco, Rahul Sukthankar, Vittorio Ferrari,
arXiv pre-print, 2015

[3] Fast object segmentation in unconstrained video
Anestis Papazoglou, Vittorio Ferrari,
In International Conference on Computer Vision (ICCV), 2013

=================================================================================================================================
Support
=================================================================================================================================

For any query/suggestion/complaint please send us an email:

ldelper@inf.ed.ac.uk (please contact this address first)
vittoferrari@gmail.com

=================================================================================================================================
Versions history
=================================================================================================================================

2.0
---
- second release
