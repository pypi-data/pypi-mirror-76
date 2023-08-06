from spatialmath.base import *
import spatialmath as sm

R = sm.SO3.Rx( 0.3)
R.plot(block=True)

#a = trplot2(transl2(0,0), block=False)
##tranimate(transl(4, 3, 4)@trotx(2)@troty(-2), frame='A', arrow=False, dims=[0, 5], nframes=200, repeat=False)
#tranimate2(transl2(4, 3)@trot2(2), frame='A', arrow=False, dims=[0, 5], nframes=200, repeat=False)