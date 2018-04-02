#!/usr/bin/env python
import socket
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('GTKAgg')


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

# make a plot of the spectrum for the first package
for i in range(1,512):
    data[i-1] = int.from_bytes(a[4*(i-1):4*i],byteorder='big')
plt.plot(np.log10(data)[256:])
plt.show()

# define a counter 
counter = 0
# how many modulus of counters do we want.
countmod = 100

# construct a figure
fig, ax = plt.subplots(1,1)
plt.show(False)
plt.draw()
background = fig.canvas.copy_from_bbox(ax.bbox)

# define the x points and construct a plot
xpoints = range(len(np.log10(data)[256:]))
points = ax.plot(xpoints,np.log10(data)[256:])[0]


# construct the most ugly while loop construction
while True:
    # get the package of the current time
    a = s.recv(2048)
    
    # save the data in the array
    for i in range(1,512):
        data[i-1] += int.from_bytes(a[4*(i-1):4*i],byteorder='big')

    
    # if the current time is a plot time, plot
    if counter%countmod==0:
        # plot the current time normalized
        points.set_data(xpoints,np.log10(data/countmod)[256:])
        fig.canvas.restore_region(background)
        ax.draw_artist(points)
        fig.canvas.blit(ax.bbox)
        print(counter)
        
        data = np.zeros(2048,dtype=int)
        
    counter += 1

plt.close(fig)







