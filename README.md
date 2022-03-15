This repository used to make a utility pipeline for patch-cropping given a case with contained files:

	-One .svs file for whole slide image (WSI)
	
	-One .xml file for "Polygon" annotation

Annotation of .svs file to create .xml can be conducted by ASAP software. The software can be found and downloaded from [here](https://computationalpathologygroup.github.io/ASAP/).


First, we need to determine the following parameters (can be found adjustable in execution.sh):

	-micron: the actual size of the patch
	
	-x_pixel: the resolution size of x-axis
	
	-y_pixel: the resolution size of y-axis
	
	-images_per_case: determine number of patches per case

Then: move the "TCGA" folders (containing 1 .svs files and 1 corresonponding .xml file) into "Test" folder
(not the "Done" folder into the "Test" folder)

Next: change these parameters in execution.sh file (do not change the "root" parameter)

Finally, on Ubuntu, execute the commands:

```
git clone https://github.com/lkhangkv1995/crop_patch
cd patch_crop
python3 -m venv venv
source venv/bin/activate
pip install -r pip_requirements.txt
chmod +x execution.sh
./execution.sh
```
Then Ubuntu should be running...

