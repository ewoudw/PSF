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

# define a counter 
counter = 0
# how many modulus of counters do we want.
countmod = 10

# construct a figure
fig, ax = plt.subplots(1,1)
plt.show(False)
plt.draw()
background = fig.canvas.copy_from_bbox(ax.bbox)

# define the x points and construct a plot
xpoints = range(len(np.log10(data)[256:]))
points = ax.plot(xpoints,np.log10(data)[256:])[0]


timevoltage = 1/(70e6) # (s), the time of each voltage measurement
timefft = 512*timevoltage # (s), the time of each fft block: of each 512 voltage measurements an fft is taken
dt = timefft * 64 # (s), to reduce the data rate, the sum of 64 ffts is taken
freqstep = (1/timefft)/1e6 # (MHz), the bandwidth of each frequency bin

maxfreq = (self.mix_freq+21.4) # (MHz)
minfreq = maxfreq-35 # (MHz)

freqs_edges = np.linspace(minfreq, maxfreq, 257) # Frequency bin edges
freqs = (freqs_edges[1:]+freqs_edges[:-1])/2
print(freqs)

timevoltage = 1/(70e6) # (s), the time of each voltage measurement
timefft = 512*timevoltage # (s), the time of each fft block: of each 512 voltage measurements an fft is taken
dt = timefft * 64 # (s), to reduce the data rate, the sum of 64 ffts is taken
freqstep = (1/timefft)/1e6 # (MHz), the bandwidth of each frequency bin

midfreq = 405
maxfreq = (midfreq+21.4) # (MHz)
minfreq = maxfreq-35 # (MHz)

freqs_edges = np.linspace(minfreq, maxfreq, 257) # Frequency bin edges
freqs = (freqs_edges[1:]+freqs_edges[:-1])/2


shift = 4.15e3*DM*(1/freqs[0]**2 - 1/freqs**2)
#binshifts = np.zeros(len(shift),dtype=int)
binshifts = np.rint(shift/dt).astype(int)

sizet = binshifts[-1]
dmdata = np.zeros((sizet,len(shift)))
maxshift = binshifts[-1]

plotarray = np.ones(1000)
xpoints = np.arange(len(plotarray))

# construct the most ugly while loop construction
while True:
    # get the package of the current time
    a = s.recv(2048)
    
    # save the data in the array
    for i in range(1,512):
        data[i-1] = int.from_bytes(a[4*(i-1):4*i],byteorder='big')

    localdata = data[256:]

    for i in range(0,len(shift)):
        dmdata[(counter+binshifts[i])%maxshift,i] = localdata[i]

    newdatapoint += np.sum(dmdata[counter,:])

    
    # if the current time is a plot time, plot
    if counter%countmod==0:
        plotarray = np.roll(plotarray,1)
        plotarray[0] = newdatapoint/countmod
        # plot the current time normalized
        points.set_data(xpoints,plotarray)
        fig.canvas.restore_region(background)
        ax.draw_artist(points)
        fig.canvas.blit(ax.bbox)
        print(counter)
        
        newdatapoint = 0
        
    counter += 1

plt.close(fig)






