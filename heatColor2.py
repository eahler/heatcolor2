#Ethan Ahler

#This is a pyMOL script that is colors atoms in a pdb structure using an input file

from pymol import cmd, stored
import os, math
import matplotlib.pyplot as plt
import numpy as np
import sys
from matplotlib import pyplot
 
def heatColor2(directory, mode, offset, batch, png, colorChoice):
	'''
	directory = directory with a list of intensity value files
	mode = mode in which to run, valid options are raw, normalized and log2normalized
	offset = integer describing how many residues into the chain to begin coloring
	batch = if TRUE, heatColor will iterate over all items in a directory, otherwise batch = filename within directory to produce
	png = if TRUE, heatColor will produce a png output file.  if FALSE, it will not

	The argument colorChoice is new to heatColor2.py:
	colorChoice = String designating color pallet of heatmap, from matplotlib. Diverging colormap options (which are recommended) are listed below,
				  but in principle any matplotlib color map will work.  
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
			Reverse the color order of these by appending '_r' (e.g. 'RdBu' goes Red -> Blue, 'RdBu_r' goes Blue -> Red)
			For a list of other colormap options, go to http://matplotlib.org/examples/color/colormaps_reference.html	
			'''
	
	dirlist = os.listdir(directory)
	print mode
	print batch
	print offset
	print colorChoice

	if batch != 'TRUE':
		dirlist = [batch]
		
	for item in dirlist:
		print item
		if item[0] != '.' and '.png' not in item:
			f_infile = open((directory + item), 'U')
	
			tmpresi = str()
	
			rawvals = f_infile.readlines()
			rawvals = [float(val.rstrip()) for val in rawvals]
			vals = []
			
			if mode == 'raw':
				vals = rawvals
				
			elif mode == 'normalized':				
				for val in rawvals:
					if val < 0:
						vals.append(-1*val/min(rawvals))
					
					if val > 0:
						vals.append(val/max(rawvals))
						
					if val == 0:
						vals.append(0) 

				print vals
			elif mode == 'log2normalized':
				log2vals = []
				log2vals = [math.log(val, 2) for val in rawvals]
				print log2vals
				for val in log2vals:
					if val < 0:
						vals.append(-1*val/min(log2vals))
					
					if val > 0:
						vals.append(val/max(log2vals))
						
					if val == 0:
						vals.append(0) 
				
			else:
				sys.exit('Error: choose a valid mode')
			print vals
			#Calculates appropriate score intervals for coloring & puts each score into a color bin based on the score interval
			valsArray = np.array(vals)
			negativeArray = valsArray[valsArray < 0] #Only negative scores
			positiveArray = valsArray[valsArray > 0] #Only positive scores
			dmsMin = abs(np.amin(negativeArray)) / 128 #Matplotlib color maps span 256 colors, find the minimum score and di 
			dmsMax = abs(np.amax(positiveArray)) / 128 #Matplotlib color maps span 256 colors
			increment = (dmsMin + dmsMax) / 2 #average the two increments to find 
			negativeArrayIncrement = np.arange(np.amin(negativeArray), 0, dmsMin) #This is the bin array for neg histogram (from the min value to 0)
			positiveArrayIncrement = np.arange(0, np.amax(positiveArray), dmsMax) #This is the bin array for pos histogram (from 0 to the max value)
			negHis = np.digitize(negativeArray, negativeArrayIncrement) #bins all negative scores into the bins determined 
			posHis = np.digitize(positiveArray, positiveArrayIncrement) #bins all positive scores into the binds 

		


			for i in range(0, len(vals)):
				colname = 'res' + str(i)
				cmap = plt.cm.get_cmap(colorChoice)

				if vals[i] < 0:
			 		cmd.set_color(colname, str([cmap(negHis[negativeArray.tolist().index(vals[i])])[0], cmap(negHis[negativeArray.tolist().index(vals[i])])[1], cmap(negHis[negativeArray.tolist().index(vals[i])])[2]])) #cm function grabs the RGB values for that color


				if vals[i] > 0:
				 	cmd.set_color(colname, str([cmap(128 + posHis[positiveArray.tolist().index(vals[i])])[0], cmap(128 + posHis[positiveArray.tolist().index(vals[i])])[1], cmap(128 + posHis[positiveArray.tolist().index(vals[i])])[2]])) #The + 128 is to get it to the second half of colors
				

				if vals[i] == 0:
					cmd.set_color(colname, str([1, 1, 1]))
					

			
				cmd.color(colname, 'resi ' + str(int(i) + int(offset)))
				print str(int(i) + int(offset))
			
			if png == 'TRUE':
	 			cmd.png((directory + item + '_image'), dpi = 300, ray = 1)



cmd.extend( "heatColor2", heatColor2 );

#Plan to implement ColorBrewer diverging maps

# The below function is not implemented yet, but will allow for the generation of a custom diverging color map.
#
# def custom_div_cmap(numcolors=11, name='custom_div_cmap',
#                     mincol='blue', midcol='white', maxcol='red'):
#     """ Create a custom diverging colormap with three colors
    
#     Default is blue to white to red with 11 colors.  Colors can be specified
#     in any way understandable by matplotlib.colors.ColorConverter.to_rgb()
#     """

#     from matplotlib.colors import LinearSegmentedColormap 
    
#     cmap = LinearSegmentedColormap.from_list(name=name, 
#                                              colors =[mincol, midcol, maxcol],
#                                              N=numcolors)
#     return cmap

# load into pymol shell -> 'run /path/to/heatColor.py'
# 
#Example of command to run:
#heatColor2('/Users/ethanahler/Desktop/Scripting/Pymol/2016.08.22 PyMol Lecture/', 'raw', 100, 'zero_heat_input.txt', 'FALSE', 'BrBG')
