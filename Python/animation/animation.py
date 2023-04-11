import matplotlib.pyplot as plt
from matplotlib import animation
import random
import numpy as np


def barlist(n):
    return [int(0.028*n*k)+random.randrange(0,10) for k in [23000,2602,1420,1952,711,10]]


def month(n):
    month_ref = ['Oct 2017', 'Nov 2017', 'Dec 2017', 'Jan 2018', 'Feb 2018', 'Mar 2018', 'Apr 2018', 'May 2018',
                 'Jun 2018', 'Jul 2018', 'Aug 2018', 'Sep 2018']
    return month_ref[n]


fig, ax = plt.subplots()
ax.set_xlim(0, 7)
ax.set_ylim(0, 300000)

n=365 #Number of frames
x=range(1,7)

barcollection = plt.bar(x,barlist(1),color="#87CEFA")
textcollection= [plt.text(x,y,'%.1f'%y,ha='center') for x,y in zip(x,barlist(10))]
annotate1=plt.text(5,280000,'How many data we have?',ha='center',fontsize=15)
annotate2=plt.text(5,263000,sum(barlist(10)),ha='center',fontsize=15)

plt.xticks(x, ('Warranty', 'CAC', 'Online', 'TIPS', 'CRM', 'AQSIQ'),fontsize=12)
plt.ylabel('Cases',fontsize=5)


def animate(i):
    y=barlist(i+1)
    for i, b in enumerate(barcollection):
        #print(i,b)
        b.set_height(y[i])
    for i,c in enumerate(textcollection):
        c.set_y(y[i] + 15)
        c.set_text(y[i])
    annotate2.set_text(np.sum(y))

anim=animation.FuncAnimation(fig,animate,repeat=False,blit=False,frames=n,interval=200)
anim.save('mymovie.mp4',writer=animation.FFMpegWriter(fps=20))
plt.show()

