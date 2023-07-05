import numpy as np
import pandas as pd
import os
from IPython.display import display
import glob
import matplotlib.pyplot as plt
import seaborn as sns


#%% write the folder path from your computer

folder_path = "C:/Users/gabv1/bobinas"
listatfr = list()
lista= list()
file_paths = glob.glob(folder_path + "/*")



#%% load data from coils and save it in a list

for elements in file_paths:
    dummy = pd.read_excel (elements)
    lista.append (dummy)

#%%  transform the list into a numpy array 
array_bobinas = np.array (lista)
#%% Apply transformation to all datapoints in numpy array

Milivolts=(array_bobinas*3300)/1023 #calculo de mV
offset=(508*3300)/1023
Magnetic_field_mT=(Milivolts-offset)/7.5
Magnetic_field_gauss=Magnetic_field_mT*(10)

#%% Take the top 1000 highest values of each of the measurement points. Use this first, if not, average will be near to zero
iterate = np.arange(5)
top = list()
for coil in iterate:
    top_indices = np.argpartition(Magnetic_field_gauss[coil], -1000, axis=0)[-1000:]
    top_values = np.take_along_axis(Magnetic_field_gauss[coil], top_indices, axis=0)
    top.append (top_values)
#%% create new array with only the top values, transform it into a numpy and then take the average of the values. 

array_top = np.array(top)
array_final = np.mean (array_top, axis=1)
#%% Reshape
reshaped_data = np.reshape(array_final, (5, 12, 12))
#%% Plot




sns.heatmap(reshaped_data[0], cmap='inferno', vmin=-5, vmax=350, annot=True, fmt='.2f', cbar=True, annot_kws={"size": 9})
sns.heatmap(reshaped_data[1], cmap='inferno', vmin=-5, vmax=350, annot=True, fmt='.2f', cbar=True, annot_kws={"size": 9})
sns.heatmap(reshaped_data[2], cmap='inferno', vmin=-5, vmax=350, annot=True, fmt='.2f', cbar=True, annot_kws={"size": 9})
sns.heatmap(reshaped_data[3], cmap='inferno', vmin=-5, vmax=350, annot=True, fmt='.2f', cbar=True, annot_kws={"size": 9})
sns.heatmap(reshaped_data[4], cmap='inferno', vmin=-5, vmax=350, annot=True, fmt='.2f', cbar=True, annot_kws={"size": 9})



