# legacySrepTransformer
# author: Zhiyuan Liu
# date: 2018.6.7

This project is one submodule of SlicerSALT, short for Slicer Shape AnaLysis Toolkit.
This is an extension to Slicer, accomplishing transformation as well as visualization of s-rep.

The input of this extension could be either legacy s-rep, namely, one *.m3d file for an s-rep model, or new s-rep.

Pre-requirements:
1. Slicer 4.8+
2. python 2.7+

Usage:
1. cd ~/projects/s-rep
2. git clone https://github.com/ZhiyLiu/newSrepVisualizer.git
3. Open Slicer, Edit->Application Settings->Modules, add path a) newSrepVisualizer/build b) newSrepVisualizer/visualizer into Additional module paths
4. Restart Slicer(required)
5. Search module: visualizer
6. Visualize s-rep
6.1 For legacy s-rep, adjust distance to expand fold curve. Recommendation: 0.02 is good for hippo.m3d in test_dat. 0.5 has better visualization effect for another 2 m3d files in test_data
    Then click Select s-rep file, select the m3d file, Then you should see s-rep on 3-D window after centering and zooming in the viewport
    NOTE: the legacy s-rep will be transformed into new s-rep and saved in newSrepVisualizer/tmp. This new s-rep can be overwritten or removed by later operations.
6.2 For new s-rep, only click Select s-rep file, select the header file(*.xml), Then you should see s-rep on 3-D window after centering and zooming in the viewport
    
Example:
See test_data

Features:
a. Fix the bug caused by precision error. Need to set medial_points data type to double, it is found when try to apply TPS 
b. Move fold points away from their partners along crest spoke direction. The distance is defined by epsilon.
c. Save new srep to one header.xml along with 3 vtp file: up.vtp, down.vtp and crest.vtp
d. Support both legacy s-rep and new s-rep. For legacy s-rep, need to set distance to expand fold curve

Report bugs and comments:
Any report, comments and critics are welcome. Contact me via email: mr.zhiyuan.liu@gmail.com
