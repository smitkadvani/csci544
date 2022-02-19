import math
w=[0.2,0.3,0.9]
bias = 0.5
x = [0.5,0.6,0.1]
z=0
for (wi,xi) in zip(w,x):
	z += wi*xi
z += bias
sigmoid = 1 / (1+pow(math.e,-1*z))
print(sigmoid)