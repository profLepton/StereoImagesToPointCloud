# -*- coding: utf-8 -*-
"""DepthMaptoPointCloud

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1egsc7o9zF3AENvW2BfZJrTEI5H81au6_
"""

import argparse
import sys
import os
from PIL import Image
import open3d as o3d
import numpy as np

focalLength = 433.0
centerX = 319.5
centerY = 239.5
scalingFactor = 1000

def generate_pointcloud(rgb_file,depth_file,ply_file):
    """
    Generate a colored point cloud in PLY format from a color and a depth image.
    
    Input:
    rgb_file -- filename of color image
    depth_file -- filename of depth image
    ply_file -- filename of ply file
    
    """
    rgb = Image.open(rgb_file)
    depth = Image.open(depth_file)
    width, height =  rgb.size
    print(width)
    centerX = width/2 
    centerY = height/2

    
    if rgb.size != depth.size:
        raise Exception("Color and depth image do not have the same resolution.")
    if rgb.mode != "RGB":
        raise Exception("Color image is not in RGB format")
    

    points = []
    pointColors = []    
    for v in range(rgb.size[1]):
        for u in range(rgb.size[0]):
            color = rgb.getpixel((u,v))
           
            Z = depth.getpixel((u,v)) / scalingFactor
            if Z==0: continue
            X = (u - centerX) * Z / focalLength
            Y = (v - centerY) * Z / focalLength
            points.append([X, Y, Z])
            pointColors.append([color[0], color[1], color[2]])
            # points.append("%f %f %f"%(X,Y,Z))
            # pointColors.append("%d %d %d"%(color[0], color[1], color[2]))
    print(points[0])
    file = open(ply_file,"w")
    file.write(f"{points}")
    return points, pointColors

vector, color = generate_pointcloud('/content/Yeuna9x.png', '/content/disparity.png', './final1.ply')

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(vector)
color = np.array(color, dtype=np.float32)
pcd.colors = o3d.utility.Vector3dVector(color.astype(np.float) / 255.0)
o3d.io.write_point_cloud("./final5.ply", pcd)

