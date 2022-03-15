This folder used to make patch cropping given a case with contained files:
	+One .svs file for WSI
	+One .xml file for "Polygon" annotation



First, we need to determine the following parameters:
	-micron: the actual size of the patch
	-x_pixel: the resolution size of x-axis
	-y_pixel: the resolution size of y-axis
	-images_per_case: determine number of patches per case

Then: move the "TCGA" folders (containing 1 .svs files and 1 corresonponding .xml file) into "Test" folder
(not the "Done" folder into the "Test" folder)

Next: change these parameters in execution.sh file (do not change the "root" parameter)

Finally, on Ubuntu, execute the commands:

#Change directory to this folder (could be different regarding local PC):
'''
cd ~/patch_crop
'''
#From now on, the same for all local PCs:

'''
python3 -m venv venv
source venv/bin/activate
pip install -r pip_requirements.txt
chmod +x execution.sh
./execution.sh
'''
Then Ubuntu should be running...

