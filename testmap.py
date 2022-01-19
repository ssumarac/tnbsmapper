import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import (AutoMinorLocator, FixedLocator)
import os
import math
from matplotlib import transforms




AC_Y = 111
AC_Z = 97


PC_Y = 85
PC_Z = 102

AC_PC_length = math.dist([AC_Y,AC_Z],[PC_Y,PC_Z])

Y = 97
Z = 105
Ring = 60
Arc = 100

zoom_level = 100

zoom_level = zoom_level*2


df = pd.read_csv(os.getcwd()+"/Coronal_map.csv")

shape_id = df['shape_id']
shapes = df['shapes'].dropna()

fig, ax = plt.subplots()
ax.set_facecolor('black')
ax.set_xlim([0, 290])
ax.set_ylim([0, 460])

midline_X_raw = 0
midline_Z_raw = 460/2


step_size = 5*235/AC_PC_length
step_size_raw = 5*235/AC_PC_length

# #raw for axis
Z_ticks_up = np.arange(midline_Z_raw, 460, step=step_size)
Z_ticks_down = np.sort(np.abs(np.arange(-midline_Z_raw, 0, step=step_size)))
X_ticks = np.sort(np.abs(np.arange(midline_X_raw, 290, step=step_size)))
Z_ticks = np.unique(np.concatenate((Z_ticks_down, Z_ticks_up), axis=0))

# #mapping for axis
Z_ticks_up_axis = np.arange(100-5*(len(Z_ticks_up)-1),105,5)[::-1]
Z_ticks_down_axis = np.arange(100,100+5*len(Z_ticks_down),5)[::-1]
X_ticks_axis = np.arange(0,5*len(X_ticks),5)
Z_ticks_axis = np.unique(np.concatenate((Z_ticks_down_axis, Z_ticks_up_axis), axis=0))[::-1]

# #set axis
ax.xaxis.set_major_locator(FixedLocator(X_ticks))
ax.yaxis.set_major_locator(FixedLocator(Z_ticks))
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.yaxis.set_minor_locator(AutoMinorLocator(5))

ax.grid(which='major', color='darkblue', linestyle='--')
ax.grid(which='minor', color='darkblue', linestyle=':')

plt.xlabel("Y")
plt.ylabel("Z",rotation=0)

ax.set_xticklabels(X_ticks_axis)
ax.set_yticklabels(Z_ticks_axis)

# step_size_raw = 0.5*192/AC_PC_length

# #raw for convert
# Y_ticks_left_convert_raw = np.sort(np.abs(np.arange(-midline_Y_raw, 0, step=step_size_raw)))
# Y_ticks_right_convert_raw = np.arange(midline_Y_raw, 290, step=step_size_raw)
# Z_ticks_up_convert_raw = np.arange(midline_Z_raw, 460, step=step_size_raw)
# Z_ticks_down_convert_raw = np.sort(np.abs(np.arange(-midline_Z_raw, 0, step=step_size_raw)))
# Y_ticks_convert_raw = np.unique(np.concatenate((Y_ticks_left_convert_raw, Y_ticks_right_convert_raw), axis=0))
# Z_ticks_convert_raw = np.unique(np.concatenate((Z_ticks_down_convert_raw, Z_ticks_up_convert_raw), axis=0))

# #mapping for convert
# Y_ticks_left_convert = np.arange(100-0.5*(len(Y_ticks_left_convert_raw)-1),100.5,0.5)
# Y_ticks_right_convert = np.arange(100,100+0.5*len(Y_ticks_right_convert_raw),0.5)
# Z_ticks_up_convert = np.arange(100-0.5*(len(Z_ticks_up_convert_raw)-1),100.5,0.5)[::-1]
# Z_ticks_down_convert = np.arange(100,100+0.5*len(Z_ticks_down_convert_raw),0.5)[::-1]
# Y_ticks_convert = np.unique(np.concatenate((Y_ticks_left_convert, Y_ticks_right_convert), axis=0))
# Z_ticks_convert = np.unique(np.concatenate((Z_ticks_down_convert, Z_ticks_up_convert), axis=0))[::-1]

# Y_coord = Y_ticks_convert_raw[np.where(Y_ticks_convert == Y)[0][0]]
# Z_coord = Z_ticks_convert_raw[np.where(Z_ticks_convert == Z)[0][0]]


# AC_Y_coord = Y_ticks_convert_raw[np.where(Y_ticks_convert == AC_Y)[0][0]]
# AC_Z_coord = Z_ticks_convert_raw[np.where(Z_ticks_convert == AC_Z)[0][0]]

# PC_Y_coord = Y_ticks_convert_raw[np.where(Y_ticks_convert == PC_Y)[0][0]]
# PC_Z_coord = Z_ticks_convert_raw[np.where(Z_ticks_convert == PC_Z)[0][0]]


# # ax.axes.xaxis.set_ticklabels([])
# # ax.axes.yaxis.set_ticklabels([])

ax.plot([0,290], [midline_Z_raw, midline_Z_raw], 'red', linewidth=0.5)
ax.plot([midline_X_raw,midline_X_raw], [0,290], 'red', linewidth=0.5)
# ax.plot([AC_Y_coord,PC_Y_coord], [AC_Z_coord,PC_Z_coord], 'white', linewidth=0.5)

ax.plot(midline_X_raw, midline_Z_raw, 'yellow', marker="x")
# ax.plot(PC_Y_coord, PC_Z_coord, 'green', marker="s", mfc='none')
# ax.plot(AC_Y_coord, AC_Z_coord, 'blue', marker="s", mfc='none')

# ax.plot(MCP_Y_raw, MCP_Z_raw, 'purple', marker="s", mfc='none')
# ax.axline((Y_coord, Z_coord), slope=np.tan(np.radians(Ring)), color='white',linewidth=0.5)
# ax.plot(Y_coord, Z_coord, 'yellow', marker=".")

for i in range(0,len(shapes)):
    
    x = df[df['shape_id'] == shapes[i]]['X']*290/100
    y = df[df['shape_id'] == shapes[i]]['Y']*460/100
    
    ax.plot(x, y, 'white', linewidth=0.5) 


# plt.show()



