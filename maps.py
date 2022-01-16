import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import (AutoMinorLocator, FixedLocator)
import streamlit as st
import os

st.title("MER Mapping Software")
st.subheader('By Srdjan Sumarac')

target = st.sidebar.selectbox('Select Target', ['STN', 'GPi', 'VIM'])

st.sidebar.subheader("AC Coordinates")

AC_X = st.sidebar.info('X coordinate for AC not necessary for saggital view')
AC_Y = st.sidebar.number_input('AC Y', 0.0, 640.0,111.5)
AC_Z = st.sidebar.number_input('AC Z', 0.0, 460.0,100.0)

st.sidebar.subheader("PC Coordinates")

PC_X = st.sidebar.info('X coordinate for PC not necessary for saggital view')
PC_Y = st.sidebar.number_input('PC Y', 0.0, 640.0,88.5)
PC_Z = st.sidebar.number_input('PC Z', 0.0, 460.0,100.0)

AC_PC_length = AC_Y - PC_Y

st.sidebar.write("AC/PC Length:", AC_PC_length)


st.sidebar.subheader("Final Targeting")
st.sidebar.write("Enter either left of right coordinates")


X = st.sidebar.info('X coordinate not necessary for saggital view')
Y = st.sidebar.number_input('Y', 70.0, 130.0,100.0,0.5)
Z = st.sidebar.number_input('Z', 80.0, 120.0,100.0,0.5)
Ring = st.sidebar.number_input('Ring Angle', 0, 90,60)
Arc = st.sidebar.number_input('Arc Angle', 0, 180,100)

zoom_level = st.slider('Zoom (%)', 0, 100)

zoom_level = zoom_level*2

if target == "STN":
    df = pd.read_csv(os.getcwd()+"/STN_map.csv")
elif target == "GPi":
    df = pd.read_csv(os.getcwd()+"/GPi_map.csv")
else:
    df = pd.read_csv(os.getcwd()+"/VIM_map.csv")

shape_id = df['shape_id']
shapes = df['shapes'].dropna()

fig, ax = plt.subplots()
ax.set_facecolor('black')
ax.set_xlim([0+zoom_level, 640-zoom_level])
ax.set_ylim([0+zoom_level*460/640, 460-zoom_level*460/640])

x_ACPC = df[df['shape_id'] == shapes[0]]['X']
y_ACPC = df[df['shape_id'] == shapes[0]]['Y']

xticks_left = np.sort(np.abs(np.arange(-np.mean(x_ACPC), 0, step=5*192/23)))
xticks_right = np.arange(np.mean(x_ACPC), 640, step=5*192/23)

yticks_up = np.arange(np.mean(y_ACPC), 460, step=5*192/23)
yticks_down = np.sort(np.abs(np.arange(-np.mean(y_ACPC), 0, step=5*192/23)))

xticks = np.unique(np.concatenate((xticks_left, xticks_right), axis=0))
yticks = np.unique(np.concatenate((yticks_down, yticks_up), axis=0))

ax.xaxis.set_major_locator(FixedLocator(xticks))
ax.yaxis.set_major_locator(FixedLocator(yticks))
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.yaxis.set_minor_locator(AutoMinorLocator(5))

ax.grid(which='major', color='darkblue', linestyle='--')
ax.grid(which='minor', color='darkblue', linestyle=':')

plt.xlabel("Y")
plt.ylabel("Z",rotation=0)

xticks_mapped = np.arange(65,140,5)
yticks_mapped = np.arange(75,130,5)[::-1]


ax.set_xticklabels(xticks_mapped)
ax.set_yticklabels(yticks_mapped)



xticks_left_convert = np.sort(np.abs(np.arange(-np.mean(x_ACPC), 0, step=0.5*192/23)))
xticks_right_convert = np.arange(np.mean(x_ACPC), 640, step=0.5*192/23)

yticks_up_convert = np.arange(np.mean(y_ACPC), 460, step=0.5*192/23)
yticks_down_convert = np.sort(np.abs(np.arange(-np.mean(y_ACPC), 0, step=0.5*192/23)))

xticks_convert = np.unique(np.concatenate((xticks_left_convert, xticks_right_convert), axis=0))
yticks_convert = np.unique(np.concatenate((yticks_down_convert, yticks_up_convert), axis=0))

xticks_mapped_convert = np.arange(61.5,139,0.5)
yticks_mapped_convert = np.arange(75.5,127.5,0.5)[::-1]

x_coord = xticks_convert[np.where(xticks_mapped_convert == Y)[0][0]]
y_coord = yticks_convert[np.where(yticks_mapped_convert == Z)[0][0]]


# ax.axes.xaxis.set_ticklabels([])
# ax.axes.yaxis.set_ticklabels([])

ax.plot([0,640], [np.mean(y_ACPC),np.mean(y_ACPC)], 'red', linewidth=0.5)
ax.plot([np.mean(x_ACPC),np.mean(x_ACPC)], [0,460], 'red', linewidth=0.5)
ax.plot(x_ACPC, y_ACPC, 'white', linewidth=0.5)

ax.plot(np.mean(x_ACPC), np.mean(y_ACPC), 'yellow', marker="x")
ax.plot(x_ACPC[0], y_ACPC[0], 'green', marker="s", mfc='none')
ax.plot(x_ACPC[1], y_ACPC[1], 'blue', marker="s", mfc='none')

ax.plot(x_coord, y_coord, 'white', marker="s", mfc='none')
ax.axline((x_coord, y_coord), slope=np.tan(np.radians(Ring)), color='white',linewidth=0.5)

for i in range(1,len(shapes)):
    x = df[df['shape_id'] == shapes[i]]['X']
    y = df[df['shape_id'] == shapes[i]]['Y']

    
    ax.plot(x, y, 'white', linewidth=0.5)

st.write(fig)
