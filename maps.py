import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import (AutoMinorLocator, FixedLocator)
import streamlit as st
import os

os.getcwd()

st.title("MER Mapping Software")
st.subheader('By Srdjan Sumarac')

target = st.sidebar.selectbox('Select Target', ['STN', 'GPi', 'VIM'])

st.sidebar.subheader("AC Coordinates")

AC_X = st.sidebar.number_input('AC X', 0, 200,100)
AC_Y = st.sidebar.number_input('AC Y', 0, 200,100)
AC_Z = st.sidebar.number_input('AC Z', 0, 200,100)

st.sidebar.subheader("PC Coordinates")

PC_X = st.sidebar.number_input('PC X', 0, 200,100)
PC_Y = st.sidebar.number_input('PC Y', 0, 200,100)
PC_Z = st.sidebar.number_input('PC Z', 0, 200,100)

AC_PC_length = 23

st.sidebar.write("AC/PC Length:", AC_PC_length)

st.sidebar.subheader("Final Targeting")
st.sidebar.write("Enter either left of right coordinates")
X = st.sidebar.number_input('X', 0, 200,100)
Y = st.sidebar.number_input('Y', 0, 200,100)
Z = st.sidebar.number_input('Z', 0, 200,100)
Ring = st.sidebar.number_input('Ring Angle', 0, 200,60)
Arc = st.sidebar.number_input('Arc Angle', 0, 200,100)




zoom_level = st.slider('Zoom', 0, 200)

df = pd.read_excel (os.getcwd()+"/map.xlsx", sheet_name = target)

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

ax.set_xticklabels(np.arange(65,140,5))
ax.set_yticklabels(np.arange(75,130,5))

# ax.axes.xaxis.set_ticklabels([])
# ax.axes.yaxis.set_ticklabels([])

ax.plot([0,640], [np.mean(y_ACPC),np.mean(y_ACPC)], 'red', linewidth=0.5)
ax.plot([np.mean(x_ACPC),np.mean(x_ACPC)], [0,460], 'red', linewidth=0.5)
ax.plot(x_ACPC, y_ACPC, 'white', linewidth=0.5)

ax.plot(np.mean(x_ACPC), np.mean(y_ACPC), 'yellow', marker="x")
ax.plot(x_ACPC[0], y_ACPC[0], 'green', marker="s", mfc='none')
ax.plot(x_ACPC[1], y_ACPC[1], 'blue', marker="s", mfc='none')

ax.plot(Y, Z, 'white', marker="s", mfc='none')
ax.axline((Y, Z), slope=np.tan(np.radians(Ring)), color='white',linewidth=0.5)

for i in range(1,len(shapes)):
    x = df[df['shape_id'] == shapes[i]]['X']
    y = df[df['shape_id'] == shapes[i]]['Y']

    
    ax.plot(x, y, 'white', linewidth=0.5)

st.write(fig)
