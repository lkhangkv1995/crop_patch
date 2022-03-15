#Create the tight-up function to connect all the work flow:
import openslide
from xml.dom import minidom
import matplotlib.pyplot as plt
import random
import numpy as np
from shapely.geometry import Polygon, Point
import numpy as np
import os
import small_functions

def tightup_function(folder_path, folder, micron, x_pixel, y_pixel, images_per_case):
    	#Get annotation_path and slide_path
	for item in os.listdir(folder_path):
		try:
			file_name, file_type = item.split(".")
		except:
			continue
		if file_type == "xml": #assume that we only have 1 .xml for each folder (1 .xml and 1 .svs file)
			annotation_path = os.path.join(folder_path, item)
		if file_type == "svs":
			slide_path = os.path.join(folder_path, item)
	randompoint_list = small_functions.get_randompoints_inROI(annotation_path, slide_path, images_per_case)
	slide = openslide.OpenSlide(slide_path)
	#Create "Patches" folder inside folder_path
	size = small_functions.target_size(slide_path, micron)
	patch_path = os.path.join(folder_path, "Patches")
	os.makedirs(patch_path, exist_ok=True)
	i = 1
	for randompoint in randompoint_list:
		#If we get each random point as the center of our patches, we use this command:
		patch = slide.read_region(location=randompoint, level=0, size=size).convert("RGB") 
		patch.resize((x_pixel,y_pixel))
		#Basically patch is PIL object.
        	#Start creating the patch number:
		patch_no = str(i)
		number_of_zeros = 5 - len(patch_no) #define number of zeros going before our patch number
		patch_number = str()
		for j in range(number_of_zeros):
			patch_number += "0"
		patch_number += patch_no
		patch_number = str(patch_number)
		#End creating patch number
		name = folder + "_x" + str(x_pixel) + "_y" + str(y_pixel) + "_" + str(micron) + "micron_" + patch_number + ".jpg" #Naming each image
		i += 1
		patch.save(os.path.join(patch_path, name))
	print("Done for " + folder + ", the total number of slides is: " + str(i))
