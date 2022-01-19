import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import (AutoMinorLocator, FixedLocator)
import streamlit as st
import os
#import math
from matplotlib import transforms
from PIL import Image

st.title("TNBS: MER Mapping Software")
st.info('By Srdjan Sumarac')
st.image(Image.open('tnbs_logo.png'),width=150)

target = st.sidebar.selectbox('Select Target', ['STN', 'GPi', 'VIM'])

invert = st.sidebar.selectbox("Select normal/inverted view", ["Normal","Inverted"])
ticks = st.sidebar.selectbox("Show Ticks", ["Yes","No"])
background = st.sidebar.selectbox("Select black/white background", ["Black","White"])
which_trajectroy = st.sidebar.selectbox("Select trajectory line type", ["Angled","Not Angled"])

col1, col2 = st.columns(2)

col1.subheader("AC Coordinates")

AC_X = col1.number_input('AC X', 0.0, 200.0,100.0,0.5)
AC_Y = col1.number_input('AC Y', 0.0, 200.0,111.5, 0.5)
AC_Z = col1.number_input('AC Z', 0.0, 200.0,100.0, 0.5)

col2.subheader("PC Coordinates")

PC_X = col2.number_input('PC X', 0.0, 200.0,100.0,0.5)
PC_Y = col2.number_input('PC Y', 0.0, 200.0,88.5,0.5)
PC_Z = col2.number_input('PC Z', 0.0, 200.0,100.0,0.5)

#AC_PC_length = math.dist([AC_Y,AC_Z],[PC_Y,PC_Z])

AC_PC_length = np.sqrt((PC_Y-AC_Y)**2 + (PC_Z-AC_Z)**2)

st.write("AC/PC Length:", round(AC_PC_length,2))

st.subheader("Final Targeting")
st.write("Enter either left or right coordinates")

X = st.number_input('X', 0.0, 200.0,100.0,0.5)
Y = st.number_input('Y', 0.0, 200.0,100.0,0.5)
Z = st.number_input('Z', 0.0, 200.0,100.0,0.5)
Ring = st.number_input('Ring Angle', 0, 90,60)
Arc = st.number_input('Arc Angle', 0, 180,100)

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

if background == "White":
    ax.set_facecolor('white')
else: 
    ax.set_facecolor('black')
    
ax.set_xlim([0+zoom_level, 640-zoom_level])
ax.set_ylim([0+zoom_level*460/640, 460-zoom_level*460/640])

ACPC_default_Y = df[df['shape_id'] == shapes[0]]['X']
ACPC_default_Z = df[df['shape_id'] == shapes[0]]['Y']


MCP_Y_map = (AC_Y+PC_Y)/2
MCP_Z_map = (AC_Z+PC_Z)/2

MCP_Y_raw = np.mean(ACPC_default_Y)
MCP_Z_raw = np.mean(ACPC_default_Z)


Y_to_midline = 100 - MCP_Y_map
Z_to_midline = 100 - MCP_Z_map
midline_Y_raw = MCP_Y_raw + Y_to_midline*192/AC_PC_length
midline_Z_raw = MCP_Z_raw - Z_to_midline*192/AC_PC_length

MCP = [np.mean(ACPC_default_Y), np.mean(ACPC_default_Z)]

step_size = 5*192/AC_PC_length
step_size_raw = 5*192/AC_PC_length

#raw for axis
Y_ticks_left = np.sort(np.abs(np.arange(-midline_Y_raw, 0, step=step_size)))
Y_ticks_right = np.arange(midline_Y_raw, 640, step=step_size)
Z_ticks_up = np.arange(midline_Z_raw, 460, step=step_size)
Z_ticks_down = np.sort(np.abs(np.arange(-midline_Z_raw, 0, step=step_size)))
Y_ticks = np.unique(np.concatenate((Y_ticks_left, Y_ticks_right), axis=0))
Z_ticks = np.unique(np.concatenate((Z_ticks_down, Z_ticks_up), axis=0))

#mapping for axis
Y_ticks_left_axis = np.arange(100-5*(len(Y_ticks_left)-1),105,5)
Y_ticks_right_axis = np.arange(100,100+5*len(Y_ticks_right),5)
Z_ticks_up_axis = np.arange(100-5*(len(Z_ticks_up)-1),105,5)[::-1]
Z_ticks_down_axis = np.arange(100,100+5*len(Z_ticks_down),5)[::-1]
Y_ticks_axis = np.unique(np.concatenate((Y_ticks_left_axis, Y_ticks_right_axis), axis=0))
Z_ticks_axis = np.unique(np.concatenate((Z_ticks_down_axis, Z_ticks_up_axis), axis=0))[::-1]

#set axis
ax.xaxis.set_major_locator(FixedLocator(Y_ticks))
ax.yaxis.set_major_locator(FixedLocator(Z_ticks))
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.yaxis.set_minor_locator(AutoMinorLocator(5))

if ticks == "Yes":
    ax.grid(which='major', color='darkblue', linestyle='--')
    ax.grid(which='minor', color='darkblue', linestyle=':')

plt.xlabel("Y")
plt.ylabel("Z",rotation=0)

ax.set_xticklabels(Y_ticks_axis)
ax.set_yticklabels(Z_ticks_axis)

step_size_raw = 0.5*192/AC_PC_length

#raw for convert
Y_ticks_left_convert_raw = np.sort(np.abs(np.arange(-midline_Y_raw, 0, step=step_size_raw)))
Y_ticks_right_convert_raw = np.arange(midline_Y_raw, 640, step=step_size_raw)
Z_ticks_up_convert_raw = np.arange(midline_Z_raw, 460, step=step_size_raw)
Z_ticks_down_convert_raw = np.sort(np.abs(np.arange(-midline_Z_raw, 0, step=step_size_raw)))
Y_ticks_convert_raw = np.unique(np.concatenate((Y_ticks_left_convert_raw, Y_ticks_right_convert_raw), axis=0))
Z_ticks_convert_raw = np.unique(np.concatenate((Z_ticks_down_convert_raw, Z_ticks_up_convert_raw), axis=0))

#mapping for convert
Y_ticks_left_convert = np.arange(100-0.5*(len(Y_ticks_left_convert_raw)-1),100.5,0.5)
Y_ticks_right_convert = np.arange(100,100+0.5*len(Y_ticks_right_convert_raw),0.5)
Z_ticks_up_convert = np.arange(100-0.5*(len(Z_ticks_up_convert_raw)-1),100.5,0.5)[::-1]
Z_ticks_down_convert = np.arange(100,100+0.5*len(Z_ticks_down_convert_raw),0.5)[::-1]
Y_ticks_convert = np.unique(np.concatenate((Y_ticks_left_convert, Y_ticks_right_convert), axis=0))
Z_ticks_convert = np.unique(np.concatenate((Z_ticks_down_convert, Z_ticks_up_convert), axis=0))[::-1]

Y_coord = Y_ticks_convert_raw[np.where(Y_ticks_convert == Y)[0][0]]
Z_coord = Z_ticks_convert_raw[np.where(Z_ticks_convert == Z)[0][0]]


AC_Y_coord = Y_ticks_convert_raw[np.where(Y_ticks_convert == AC_Y)[0][0]]
AC_Z_coord = Z_ticks_convert_raw[np.where(Z_ticks_convert == AC_Z)[0][0]]

PC_Y_coord = Y_ticks_convert_raw[np.where(Y_ticks_convert == PC_Y)[0][0]]
PC_Z_coord = Z_ticks_convert_raw[np.where(Z_ticks_convert == PC_Z)[0][0]]

if which_trajectroy == "Angled":
    trajectory_line_length = 25*np.sin(np.deg2rad((180-Arc)/2))*192/AC_PC_length
else:
    trajectory_line_length = 25*192/AC_PC_length

# ax.axes.xaxis.set_ticklabels([])
# ax.axes.yaxis.set_ticklabels([])



trajectory_end_Y = Y_coord-trajectory_line_length*np.cos(np.deg2rad(Ring))
trajectory_start_Z = Z_coord+trajectory_line_length*np.sin(np.deg2rad(Ring))
trajectory_start_Y = Y_coord+trajectory_line_length*np.cos(np.deg2rad(Ring))
trajectory_end_Z = Z_coord-trajectory_line_length*np.sin(np.deg2rad(Ring))

trajetory_tick_Y = trajectory_line_length/25*np.cos(np.deg2rad(Ring))
trajetory_tick_Z = trajectory_line_length/25*np.sin(np.deg2rad(Ring))

for i in range(51):
    
    if invert == "Inverted":
        ax.plot(trajectory_end_Y+i*trajetory_tick_Y, trajectory_end_Z+i*trajetory_tick_Z, 'red', marker=(2, 0, Ring), markersize=5)
    else:
        ax.plot(trajectory_end_Y+i*trajetory_tick_Y, trajectory_end_Z+i*trajetory_tick_Z, 'red', marker=(2, 0, 180-Ring), markersize=5)
    
for i in range(11):
    
    if invert == "Inverted":
        ax.plot(trajectory_end_Y+i*trajetory_tick_Y*5, trajectory_end_Z+i*trajetory_tick_Z*5, 'green', marker=(2, 0, Ring), markersize=10)
    else:
        ax.plot(trajectory_end_Y+i*trajetory_tick_Y*5, trajectory_end_Z+i*trajetory_tick_Z*5, 'green', marker=(2, 0, 180-Ring), markersize=10)

ax.plot(Y_coord, Z_coord, 'yellow', marker=".")
    

ax.plot([0,640], [midline_Z_raw, midline_Z_raw], 'red', linewidth=0.5)
ax.plot([midline_Y_raw,midline_Y_raw], [0,460], 'red', linewidth=0.5)


if background == "White":
    ax.plot([AC_Y_coord,PC_Y_coord], [AC_Z_coord,PC_Z_coord], 'black', linewidth=0.5)
else: 
    ax.plot([AC_Y_coord,PC_Y_coord], [AC_Z_coord,PC_Z_coord], 'white', linewidth=0.5)


ax.plot(midline_Y_raw, midline_Z_raw, 'yellow', marker="x")
ax.plot(PC_Y_coord, PC_Z_coord, 'green', marker="s", mfc='none')
ax.plot(AC_Y_coord, AC_Z_coord, 'blue', marker="s", mfc='none')


ax.plot(MCP_Y_raw, MCP_Z_raw, 'purple', marker="s", mfc='none')

if background == "White":
    ax.plot([trajectory_end_Y,trajectory_start_Y], [trajectory_end_Z,trajectory_start_Z], 'black', linewidth=0.5)
else:
    ax.plot([trajectory_end_Y,trajectory_start_Y], [trajectory_end_Z,trajectory_start_Z], 'white', linewidth=0.5)


ax.plot(Y_coord, Z_coord, 'yellow', marker=".")

rotation_angle = np.degrees(np.arctan(np.abs(AC_Z-PC_Z)/np.abs(AC_Y-PC_Y)))
init_angle = np.degrees(np.arctan(MCP[1]/MCP[0]))

new_angle = init_angle + rotation_angle

#MCP_origin_length = math.dist([0,0],[MCP[1],MCP[0]])

MCP_origin_length = np.sqrt((MCP[1]-0)**2 + (MCP[0]-0)**2)


x_shift_factor = MCP_origin_length*np.cos(np.deg2rad(new_angle))
y_shift_factor = MCP_origin_length*np.sin(np.deg2rad(new_angle))

x_shift = MCP[0] - x_shift_factor
y_shift = MCP[1] - y_shift_factor

for i in range(1,len(shapes)):
    
    x = df[df['shape_id'] == shapes[i]]['X']
    y = df[df['shape_id'] == shapes[i]]['Y']
    
    x_rot = np.cos(np.deg2rad(rotation_angle))*x - np.sin(np.deg2rad(rotation_angle))*y
    y_rot = np.sin(np.deg2rad(rotation_angle))*x + np.cos(np.deg2rad(rotation_angle))*y
              
    if background == "Black":                                                
        ax.plot(x_rot+x_shift, y_rot+y_shift, 'white', linewidth=0.5) 
    else:
        ax.plot(x_rot+x_shift, y_rot+y_shift, 'black', linewidth=0.5) 

if invert == "Normal":
    ax.invert_xaxis()

st.write(fig)

st.subheader("Annotations")

d10 = col1.text_input("10.0mm:")
d9_5 = col1.text_input("9.5mm:")
d9 = col1.text_input("9.0mm:")
d8_5 = col1.text_input("8.5mm:")
d8 = col1.text_input("8.0mm:")
d7_5 = col1.text_input("7.5mm:")
d7 = col1.text_input("7.0mm:")
d6_5 = col1.text_input("6.5mm:")
d6 = col1.text_input("6.0mm:")
d5_5 = col1.text_input("5.5mm:")
d5 = col1.text_input("5.0mm:")
d4_5 = col1.text_input("4.5mm:")
d4 = col1.text_input("4.0mm:")
d3_5 = col1.text_input("3.5mm:")
d3 = col1.text_input("3.0mm:")
d2_5 = col1.text_input("2.5mm:")
d2 = col1.text_input("2.0mm:")
d1_5 = col1.text_input("1.5mm:")
d1 = col1.text_input("1.0mm:")
d0_5 = col1.text_input("0.5mm:")
d0 = col2.text_input("0.0mm:")
dm0_5 = col2.text_input("-0.5mm:")
dm1 = col2.text_input("-1.0mm:")
dm1_5 = col2.text_input("-1.5mm:")
dm2 = col2.text_input("-2.0mm:")
dm2_5 = col2.text_input("-2.5mm:")
dm3 = col2.text_input("-3.0mm:")
dm3_5 = col2.text_input("-3.5mm:")
dm4 = col2.text_input("-4.0mm:")
dm4_5 = col2.text_input("-4.5mm:")
dm5 = col2.text_input("-5.0mm:")
dm5_5 = col2.text_input("-5.5mm:")
dm6 = col2.text_input("-6.0mm:")
dm6_5 = col2.text_input("-6.5mm:")
dm7 = col2.text_input("-7.0mm:")
dm7_5 = col2.text_input("-7.5mm:")
dm8 = col2.text_input("-8.0mm:")
dm8_5 = col2.text_input("-8.5mm:")
dm9 = col2.text_input("-9.0mm:")
dm9_5 = col2.text_input("-9.5mm:")

