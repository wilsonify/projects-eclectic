import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap

#load the data
pwd=os.getcwd()
traveldata=pd.read_csv(pwd+'/OhThePlacesIveBeen.csv')

# initialize figure and axes
fig = plt.figure(figsize=(10,10))
ax = fig.add_axes([0.1,0.1,0.8,0.8])

# setup the map
my_map = Basemap(projection='robin', lat_0=0, lon_0=-100, resolution='h', area_thresh=1000.0)
my_map.bluemarble()

# add the data
for lon,lat in zip(traveldata['Longitude'],traveldata['Latitude']):
    x,y = my_map(lon, lat)
    my_map.plot(x, y, 'ro', markersize=10)

# disply the data
plt.title("Oh, the Places I've Been!")    

#fig.savefig(pwd+'/PlacesIveBeen.png', transparent=True)
plt.show()
