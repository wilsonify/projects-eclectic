import numpy as np
import pandas as pd
from scipy.stats import norm
from matplotlib import pyplot as plt
from matplotlib import dates
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

# read in data
annual_highs=pd.read_csv('/home/thom/projects/flood/BraysBayouPeakHeight.csv')

# make dates plotable
annual_highs['Date']=pd.to_datetime(annual_highs['Date']).map(lambda x: dates.date2num(x))

# fit to normal
mu, std = norm.fit(annual_highs['HT'])

# calculate cumulative probability
annual_highs['rank']=annual_highs['HT'].rank()
annual_highs['cumprob']=annual_highs['rank']/len(annual_highs)

# calculate probability density function and cumulative probability function
xmin = annual_highs['HT'].min()-std
xmax = annual_highs['HT'].max()+std
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
cp = norm.cdf(x, mu, std)

# solve for 100-year flood level
one_hundred_year_flood=norm.ppf(0.99,mu,std)

# initialize the figure and subplot/axes
fig=plt.figure(figsize=(12,12))
ax1=fig.add_subplot(221) #2rows, 2cols, 1st subplot
ax2=fig.add_subplot(222, sharey=ax1) #2rows, 2cols, 2nd subplot
ax3=fig.add_subplot(223) #2rows, 2cols, 3rd subplot
ax4=fig.add_subplot(224) #2rows, 2cols, 4th subplot

# timeline
ax1.scatter(annual_highs['Date'],annual_highs['HT'])
ax1.xaxis.set_major_locator(dates.AutoDateLocator())
ax1.xaxis.set_major_formatter(dates.AutoDateFormatter(locator=dates.AutoDateLocator()))
ax1.set_ybound(xmin-1,xmax+1)
ax1.set(xlabel='year',ylabel='feet')

# histogram with normal overlayed
ax2.hist(annual_highs['HT'], orientation='horizontal', bins=10, normed=True, alpha=0.7)
ax2.plot(p, x, 'k', linewidth=2)
ax2.set(xlabel='fraction of observations',ylabel='feet')


# cumulative 
ax3.scatter(annual_highs['HT'],annual_highs['cumprob'])
ax3.plot(x, cp, 'k', linewidth=2)
ax3.set(xlabel='feet',ylabel='cumulative probability')

# zoom in for 2nd subplot
ax4.scatter(annual_highs['HT'],annual_highs['cumprob'])
ax4.plot(x,cp,'k')
ax4.set(xlim=(50,60),ylim=(0.9,1.0),xlabel='feet',ylabel='cumulative probability')
ax4.axhline(0.99,linestyle='dashed')
ax4.axvline(one_hundred_year_flood, linestyle='dashed')
ax4.annotate(xy=(one_hundred_year_flood+0.1,0.98),s='100-year = '+"%0.1f ft" % one_hundred_year_flood)
mark_inset(ax3, ax4, loc1=1, loc2=3, fc="none", ec="0.5")

# set title
plt.suptitle('Annual High Water Mark - Brays Bayou',x=0.5, y=0.925, fontsize=15)
plt.show()
