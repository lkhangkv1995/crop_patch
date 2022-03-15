#source ~/patch_crop/venv/bin/activate

declare me="Khang"
declare micron=250
declare root="Test"
declare x_pixel=512
declare y_pixel=512
declare images_per_case=500

execution_pip(){
	python execution_function.py --root ${root} --micron ${micron} --x_pixel ${x_pixel} --y_pixel ${y_pixel} --images_per_case ${images_per_case}
}

execution_pip ${root} ${micron} ${x_pixel} ${y_pixel} ${images_per_case}
