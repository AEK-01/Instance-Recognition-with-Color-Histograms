To run the code

write to cmd python SimilarityCheck.py 

and give below arguments 

first one is -> grid num : int and 2 for 2x2 grid  3 for 3x3 grid etc  (1 for no grid)

second one is -> query number :int  and (1,2,3) for specific query and 0 for all of them

third one is -> 3D or per-channel: int  and 0 for 3D and 1 for per-channel

fourth one is -> rgb or hsv and if no argument is given than rgb color space/ if --hsvOn is written hsv color space

the other ones are -> bind numbers: int and  if write 4 8   code will do for both 4 bind number and 8 bind number


--example usage--
2x2 grid
query all
3D histogram
hsv 
8 and 64 binds

python /.SimilarityCheck.py 2 0 0 --hsvOn 8 64


--example usage 2--
no grid which means 1x1 grid
query 1
per channel
rgb
32 and 2 binds

python /.SimilarityCheck.py 1 1 1 32 2


--example usage 3--
6x6 grid
all queris
per channel
hsv
64 bind

python /.SimilarityCheck.py 6 0 1 --hsvOn 64



