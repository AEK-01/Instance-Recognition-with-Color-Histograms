This is a Computer Vision Course's homework.
You can find results in report.pdf

To run the code

write to cmd python SimilarityCheck.py 

and give below arguments 

first one is -> grid num : int and 2 for 2x2 grid  3 for 3x3 grid etc  (1 for no grid)

second one is -> query number :int  and (1,2,3) for specific query and 0 for all of them

third one is -> 3D or per-channel: int  and 0 for 3D and 1 for per-channel

fourth one is -> rgb or hsv and if no argument is given than rgb color space/ if --hsvOn is written hsv color space

the other ones are -> bind numbers: int and  if write 4 8   code will do for both 4 bind number and 8 bind number


--example usage-- <br />
2x2 grid <br />
query all <br />
3D histogram <br />
hsv <br />
8 and 64 binds <br />

python /.SimilarityCheck.py 2 0 0 --hsvOn 8 64 


--example usage 2-- <br />
no grid which means 1x1 grid <br />
query 1 <br />
per channel <br />
rgb <br />
32 and 2 binds <br />

python /.SimilarityCheck.py 1 1 1 32 2  <br />


--example usage 3-- <br />
6x6 grid <br />
all queris <br />
per channel <br />
hsv <br />
64 bind <br />

python /.SimilarityCheck.py 6 0 1 --hsvOn 64



