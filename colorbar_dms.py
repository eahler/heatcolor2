'''
Make a colorbar as a separate figure.

'''
from matplotlib.backends.backend_pdf import PdfPages

from matplotlib import pyplot
import matplotlib as mpl
import numpy as np
import sys

scoreFile = sys.argv[1] 
chosenColor = sys.argv[2] 

'''
    scoreFile = '/path/to/dms/scores/'
    chosenColor = 
            'BrBG'
            'bwr'
            'coolwarm'
            'PiYG'
            'PGRGn'
            'PuOr'
            'RdBu'
            'RdGy'
            'RdYIBu'
            'RdYIGn'
            'Spectral'
            'seismic'    
            '''


with open(scoreFile) as f:
    vals = f.read().splitlines()
    
pp = PdfPages('scalebar.pdf')
newVals = [float(i) for i in vals] #converts every item in vals to a float
# Make a figure and axes with dimensions as desired.
fig = pyplot.figure(figsize=(8, 3))
ax1 = fig.add_axes([0.05, 0.80, 0.9, 0.15]) #[left, bottom, width, height]



valsArray = np.array(newVals)
negativeArray = valsArray[valsArray < 0] #Only negative scores
positiveArray = valsArray[valsArray > 0] #Only positive scores
dmsMin = abs(np.amin(negativeArray)) / 128 #Matplotlib color maps span 256 colors, find the minimum score and di 
dmsMax = abs(np.amax(positiveArray)) / 128 #Matplotlib color maps span 256 colors
increment = (dmsMin + dmsMax) / 2 #average the two increments to find 
negativeArrayIncrement = np.arange(np.amin(negativeArray), 0, dmsMin) #This is the bin array for neg histogram (from the min value to 0)
positiveArrayIncrement = np.arange(0, np.amax(positiveArray), dmsMax) #This is the bin array for pos histogram (from 0 to the max value)
negHis = np.digitize(negativeArray, negativeArrayIncrement) #bins all negative scores into the bins determined 
posHis = np.digitize(positiveArray, positiveArrayIncrement) #bins all positive scores into the binds 



# Set the colormap and norm to correspond to the data for which
# the colorbar will be used.
cmap = mpl.cm.get_cmap(chosenColor)

bounds = [np.amin(negativeArray), np.amin(negativeArray) / 2., 0., np.amax(positiveArray) / 2., np.amax(positiveArray)]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)


cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                norm=norm,
                                orientation='horizontal')
cb1.set_label('Enrichment Score')


# pyplot.show()
pp.savefig()

pp.close()


