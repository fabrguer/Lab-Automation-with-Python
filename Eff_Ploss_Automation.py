# last update: 1/25/2016

import visa
import time
import numpy as np
import pandas as pd


# INPUT PARAMETERS
Loads = np.arange(0,30+1,1)		# (min,max,step size)	

# CONFIGURE GPIB 
chroma = visa.instrument("GPIB::2")		# initialize and create the electronic load object
chroma.write("MODE CCH")				# configure the load mode	
chroma.write("LOAD ON")					# turns on the load

daq = visa.instrument("GPIB::9")		# initialize and create the DAQ object

# MAIN LOOP
df = pd.DataFrame()				# create an empty dataframe

for load in Loads:

	chroma.write("CURR:STAT:L1 %.2f" % load)			# set the load current
	time.sleep(2)										# wait 2 seconds

	temp = {}											# empty dictionary

	daq.write("MEAS:VOLT:DC? AUTO,DEF,(@102)")											
	temp['Iout']=float(daq.read())/0.004				# read Iout

	daq.write("MEAS:VOLT:DC? AUTO,DEF,(@101)")
	temp['Vout']=float(daq.read())						# read Vout

	daq.write("MEAS:VOLT:DC? AUTO,DEF,(@103)")
	temp['Iin']=float(daq.read())/0.004					# read Iin

	daq.write("MEAS:VOLT:DC? AUTO,DEF,(@105)")
	temp['Vin']=float(daq.read())						# read Vin

	temp['Eff']=temp['Vout']*temp['Iout']/temp['Vin']/temp['Iin']		# calculate Efficiency
	temp['Ploss']=temp['Vin']*temp['Iin']-temp['Vout']*temp['Iout']		# calculate Ploss
	
	# prints some text on the terminal
	print "Vout: %.3fV\tIout: %.3fA\tEff: %.1f%%" % (temp['Vout'], temp['Iout'], temp['Eff']*100.0)

	df = df.append(temp, ignore_index=True)			# append loop results

	
df.to_csv('Eff_Ploss_Results.csv')		# save results in .csv file