import sys
import parser_arguments
import tightup_function
import os
#Execute function, given the root folder

#Import arguments for parser
args = parser_arguments.getArgs(sys.argv[1:])
print("Cropping parameters:")
print(args)

print("")
print("Items in Test folder:")
for items in os.listdir(args.root):
	print(items)

print("")
print("Start cropping ...")
#Here we go
for folder in os.listdir(args.root):
	folder_path = os.path.join(args.root, folder)
	tightup_function.tightup_function(folder_path, folder, args.micron, args.x_pixel, args.y_pixel, args.images_per_case)
print("ALL DONE!")
	#This would help to bypass the folder without .xml file
