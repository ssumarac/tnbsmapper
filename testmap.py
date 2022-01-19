import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import (AutoMinorLocator, FixedLocator)
import os
import math
from matplotlib import transforms

AC_Y = 111.5
AC_Z = 100


PC_Y = 88.5
PC_Z = 100

AC_PC_length = math.dist([AC_Y,AC_Z],[PC_Y,PC_Z])

X = 110
Y = 95
Z = 104
Ring = 60
Arc = 100

zoom_level = 100

zoom_level = zoom_level*2


df = pd.read_csv("/Users/srdjansumarac/Documents/GitHub/tnbsmapper/Coronal_map.csv")

shape_id = df['shape_id']
shapes = df['shapes'].dropna()

fig, ax = plt.subplots()
ax.set_facecolor('black')
ax.set_xlim([0, 100])
ax.set_ylim([0, 100])

plt.xlabel("X")
plt.ylabel("Z",rotation=0)


midline_X_raw = 0
midline_Z_raw = 48

step_size_X = 15*23/AC_PC_length
step_size_Z = 8*23/AC_PC_length

X_ticks = np.arange(midline_X_raw, 100, step=step_size_X)
Z_ticks_up = np.arange(midline_Z_raw, 100, step=step_size_Z)
Z_ticks_down = np.sort(np.abs(np.arange(-midline_Z_raw, 0, step=step_size_Z)))
Z_ticks = np.unique(np.concatenate((Z_ticks_down, Z_ticks_up), axis=0))

#mapping for axis
X_ticks_axis = np.arange(midline_X_raw,5*len(X_ticks),5)
Z_ticks_up_axis = np.arange(100-5*(len(Z_ticks_up)-1),105,5)[::-1]
Z_ticks_down_axis = np.arange(100,100+5*len(Z_ticks_down),5)[::-1]
Z_ticks_axis = np.unique(np.concatenate((Z_ticks_down_axis, Z_ticks_up_axis), axis=0))[::-1]

#set axis
ax.xaxis.set_major_locator(FixedLocator(X_ticks))
ax.yaxis.set_major_locator(FixedLocator(Z_ticks))
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.yaxis.set_minor_locator(AutoMinorLocator(5))


ax.grid(which='major', color='darkblue', linestyle='--')
ax.grid(which='minor', color='darkblue', linestyle=':')

plt.xlabel("X")
plt.ylabel("Z",rotation=0)

ax.set_xticklabels(X_ticks_axis)
ax.set_yticklabels(Z_ticks_axis)





step_size_X_raw = 15/10*23/AC_PC_length
step_size_Z_raw = 8/10*23/AC_PC_length

#raw for convert
X_ticks_convert_raw = np.arange(midline_X_raw, 100, step=step_size_X_raw)
Z_ticks_up_convert_raw = np.arange(midline_Z_raw, 100, step=step_size_Z_raw)
Z_ticks_down_convert_raw = np.sort(np.abs(np.arange(-midline_Z_raw, 0, step=step_size_Z_raw)))
Z_ticks_convert_raw = np.unique(np.concatenate((Z_ticks_down_convert_raw, Z_ticks_up_convert_raw), axis=0))

#mapping for convert
X_ticks_convert = np.arange(midline_X_raw,0.5*len(X_ticks_convert_raw),0.5)
Z_ticks_up_convert = np.arange(100-0.5*(len(Z_ticks_up_convert_raw)-1),100.5,0.5)[::-1]
Z_ticks_down_convert = np.arange(100,100+0.5*len(Z_ticks_down_convert_raw),0.5)[::-1]
Z_ticks_convert = np.unique(np.concatenate((Z_ticks_down_convert, Z_ticks_up_convert), axis=0))[::-1]

X_coord = X_ticks_convert_raw[np.where(X_ticks_convert == np.abs(100-X))[0][0]]
Z_coord = Z_ticks_convert_raw[np.where(Z_ticks_convert == Z)[0][0]]




ax.axline((X_coord, Z_coord), slope=np.tan(np.radians(90-Arc/2)), color='red',linewidth=1)
ax.plot(X_coord, Z_coord, 'yellow', marker=".")

for i in range(0,len(shapes)):
    
    x = df[df['shape_id'] == shapes[i]]['X']
    y = df[df['shape_id'] == shapes[i]]['Y']
    
    ax.plot(x, y, 'white', linewidth=0.5) 


plt.show()



