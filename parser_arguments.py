
import argparse

def getArgs(argv=None):
	parser = argparse.ArgumentParser(description='Parameters for preprocessing',
                                     	formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--root', type=str, help="The root directory of the all slides")
	parser.add_argument('--micron', type=int, default=250, help="Actual size of the patch")
	parser.add_argument('--x_pixel', type=int, default=512, help="The number of pixels in x-axis")
	parser.add_argument('--y_pixel', type=int, default=512, help="The number of pixels in y-axis")
	parser.add_argument('--images_per_case', type=int, default=1000, help="The number of images for 1 case")
	
	return parser.parse_args(argv)

