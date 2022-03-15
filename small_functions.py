#Create small functions from scratch

import openslide
from xml.dom import minidom
import matplotlib.pyplot as plt
import random
import numpy as np
from shapely.geometry import Polygon, Point
import numpy as np
import os


#Define micron, x_pixel, y_pixel

#First build a function to extract ROI id, coordinate order, X, and Y:

def get_values(annotation_path):
	annotated_file = minidom.parse(annotation_path)
	border_coordinates = annotated_file.getElementsByTagName("Coordinate") #Get all elements under the name "Coordinate"
	ordered_coordinates = list() #Call a list to store our desired values
	roi_id = 0
	for i in range(len(border_coordinates)):
		x = border_coordinates[i].attributes["X"].value #Get X attribute
		y = border_coordinates[i].attributes["Y"].value #Get Y attribute
		order = border_coordinates[i].attributes["Order"].value #Get Order attribute
		if order == "0":
			roi_id += 1 #Determine new ROI when order resets to 0, indicating by changes in roi_id
		ordered_coordinates.append((roi_id,order,x,y))
	
	return ordered_coordinates

#Now we have all X, Y coordinates for each specific ROI.


#We then build a function to get an output of 
    #A big list containing small lists (each ROI a small list)
    #The smallist containing (x,y) coordinates of all outer border points

def get_roi(annotation_path):
	annotated_coordinates = get_values(annotation_path)
	geometry_list = []
	roi_id = []
	for each_point in annotated_coordinates:
		roi_id.append(each_point[0])
	n_roi = max(roi_id)
	#First we have to select each ROI:
	ROI_list = [i for i in range(n_roi + 1)]
	for chosen_ROI in ROI_list:
	#We create an outer_border list for the corresponding ROI:
		outer_borders = []
		for point in annotated_coordinates:
			if point[0] == chosen_ROI: #check if the point belongs to the selected ROI
				x, y = float(point[2]), float(point[3])
				outer_borders.append((x,y)) #If true, we add it to the outer_borders list
		geometry_list.append(outer_borders) #After all, we have lists of ROI coordinates regarding different ROIs
	geometry_list = geometry_list[1:len(geometry_list)] #Remove the first none object
	return geometry_list

#Functions to calculate the area of Polygon objects given list of (x,y) outer border points:
#Source: https://www.tutorialspoint.com/program-to-find-area-of-a-polygon-in-python

def getInfo(x1, y1, x2, y2):
	return x1*y2 - y1*x2

def solve(points):
	N = len(points)
	firstx, firsty = points[0]
	prevx, prevy = firstx, firsty
	res = 0

	for i in range(1, N):
		nextx, nexty = points[i]
		res = res + getInfo(prevx,prevy,nextx,nexty)
		prevx = nextx
		prevy = nexty
	res = res + getInfo(prevx,prevy,firstx,firsty)
	return abs(res)/2.0



#Define a function to get a list of ROI areas with the file
def get_ROIarea(annotation_path):
	#Call out the ROIs as list of Polygon objects:
	geometry_list = get_roi(annotation_path)
	geometry_area = list()
	for points in geometry_list:
		area = solve(points)
		geometry_area.append(area)
	return geometry_area

#Functions to get a random point within the ROI

#To do it, we have to define a point as insider of a polygon object:
#Work source: https://stackoverflow.com/questions/58415606/create-random-points-within-a-polygon-within-a-class


def get_randompoints_inROI(annotation_path, slide_path, images_per_case): 
	#We will figure out ways to define folder_path and then assign annotation_path and slide_path later
	#Call out the ROIs as list of Polygon objects:
	geometry_list = get_roi(annotation_path)
	geometry_area = get_ROIarea(annotation_path)
	slide = openslide.OpenSlide(slide_path)
	point_list = list()
	roi_id = 0
	#xmin, ymin, xmax, ymax = 0, 0, slide.dimensions[0], slide.dimensions[1]
	for roi_points in geometry_list:
		#Get the area of the ROI
		area = geometry_area[roi_id]
		roi_id += 1
		#Come back to main task
		one_roi = Polygon(roi_points)
		xmin, ymin, xmax, ymax = np.round(one_roi.bounds) #get the range of x and y to run get random points
		i = 0 #For counting number of points
		n_points = images_per_case*area/np.sum(geometry_area) 
		#The above line make sure the number of random points respect the area of ROI proportionally
		while i <= n_points:
			x = random.randrange(xmin, xmax, 1)#The reason to use randrange is that x, y need to be an integer (each pixel)
			y = random.randrange(ymin, ymax, 1)
			#Check whether the random point belongs to ROI
			if Point(x, y).within(one_roi):
			# if true, add to the random point list
				point_list.append((x,y))
				i += 1
	return point_list

#To get 250 micron, we need to create a function to calculate the appropriate mpp in level 0
def target_size(slide_path, micron):
	#micron, x_pixel, y_pixel = 250, 512, 512. 
	#x_mpp_target = micron/x_pixel
	#y_mpp_target = micron/y_pixel
	slide = openslide.OpenSlide(slide_path)
	#microns per pixel under magnification wsi level
	x_mpp_level0 = np.round(float(slide.properties['openslide.mpp-x']),4)
	y_mpp_level0 = np.round(float(slide.properties['openslide.mpp-y']),4)
	#Now we calculate the target size according to mpp at level 0:
	x_target_size = int(np.round(micron/x_mpp_level0))
	y_target_size = int(np.round(micron/y_mpp_level0))
	return (x_target_size, y_target_size)
