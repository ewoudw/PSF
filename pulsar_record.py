#!/usr/bin/env python
import socket
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('GTKAgg')
import sys

# time in seconds
time = sys.argv[1]
filename = sys.argv[2]

# define data type unsigned int
unsignint = np.dtype(np.uint32)

# construct the socekt
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# get socket info
sinfo = socket.getaddrinfo('0.0.0.0',22102)

# bind with the backend
s.bind(('0.0.0.0',22102))
#s.connect(('10.1.2.3',22102))
data = np.zeros(2048,dtype=int)

# receive one package
a = s.recv(2048)


# define a counter 
counter = 0
# how many modulus of counters do we want.
countmod = 100

alldata = np.zeros( (int(time*2136),256) )


# construct the most ugly while loop construction
for i in range(time*2136):
    # get the package of the current time
    a = s.recv(2048)
    
    # save the data in the array
    for i in range(1,512):
        data[i-1] += int.from_bytes(a[4*(i-1):4*i],byteorder='big')

    alldata[i] = data
    data = np.zeros(2048,dtype=int)
        
    counter += 1


np.save(name+'.npy',alldata)






