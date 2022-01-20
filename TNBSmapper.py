import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import (AutoMinorLocator, FixedLocator)
import streamlit as st
import os
#import math
from matplotlib import transforms
from PIL import Image
import matplotlib as mpl
from matplotlib.offsetbox import AnchoredText
from datetime import datetime

st.title("TNBS: MER Mapping Software")
st.info('By Srdjan Sumarac')
st.image(Image.open('tnbs_logo.png'),width=150)

st.sidebar.subheader("Patient Information")
patient_name = st.sidebar.text_input("Patient Name")
patient_id = st.sidebar.number_input("Patient ID (MER)",step=1)
mrn = st.sidebar.number_input("MRN",step=1)
sex = st.sidebar.selectbox("Sex",["","Male","Female"])
dob = st.sidebar.date_input("DOB",value=(datetime(1900, 1, 1)),min_value=(datetime(1900, 1, 1)), max_value=(datetime(2030, 1, 1)))

st.sidebar.subheader("Surgery Information")
op_date = st.sidebar.date_input("Operation Date")
surgeon = st.sidebar.selectbox("Surgeon",["","SK","AL","MH"])
target = st.sidebar.selectbox('Target', ['STN', 'GPi', 'VIM'])
disease = st.sidebar.selectbox('Disease', ["",'PD', 'CD', 'ET'])
s_track = st.sidebar.selectbox("Track:",["s1","s2","s3","s4","s5","s6","s7","s8","s9","s10"])
hemi = st.sidebar.selectbox("Hemisphere:",["Right", "Left"])
start_mm = st.sidebar.selectbox("Starting Depth",["10mm","15mm"])

st.sidebar.subheader("View")
invert = st.sidebar.selectbox("Select normal/inverted view", ["Normal","Inverted"],index=0)
ticks = st.sidebar.selectbox("Show Ticks", ["Yes","No"],index=0)
background = st.sidebar.selectbox("Select black/white background", ["Black","White"],index=0)
which_trajectroy = st.sidebar.selectbox("Select trajectory line type", ["Not Angled","Angled"],index=0)

if background == "Black":
    mpl.rcParams['text.color'] = "white"
else:
    mpl.rcParams['text.color'] = "black"

col_AC, col_PC = st.columns(2)

col_AC.subheader("AC Coordinates")

AC_X = col_AC.number_input('AC X', 0.0, 200.0,100.0,0.5)
AC_Y = col_AC.number_input('AC Y', 0.0, 200.0,111.5, 0.5)
AC_Z = col_AC.number_input('AC Z', 0.0, 200.0,100.0, 0.5)

col_PC.subheader("PC Coordinates")

PC_X = col_PC.number_input('PC X', 0.0, 200.0,100.0,0.5)
PC_Y = col_PC.number_input('PC Y', 0.0, 200.0,88.5,0.5)
PC_Z = col_PC.number_input('PC Z', 0.0, 200.0,100.0,0.5)

#AC_PC_length = math.dist([AC_Y,AC_Z],[PC_Y,PC_Z])

AC_PC_length = np.sqrt((PC_Y-AC_Y)**2 + (PC_Z-AC_Z)**2)

st.write("AC/PC Length:", round(AC_PC_length,2))

st.subheader("Final Targeting")
#st.write("Enter either left or right coordinates")

X = st.number_input('X', 0.0, 200.0,100.0,0.5)
Y = st.number_input('Y', 0.0, 200.0,100.0,0.5)
Z = st.number_input('Z', 0.0, 200.0,100.0,0.5)
Ring = st.number_input('Ring Angle', 0.0, 90.0,60.0)
Arc = st.number_input('Arc Angle', 0.0, 180.0,100.0)

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

if invert == "Normal":
    plt.xlabel("Anterior ← Y → Posterior")
else: 
    plt.xlabel("Posterior ← Y → Anterior")

plt.ylabel("Inferior ← Z → Superior")

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

st.sidebar.subheader("Annotations")

if start_mm == "15mm": 
    d15 = st.sidebar.text_input("15.0mm:")
    d14 = st.sidebar.text_input("14.0mm:")
    d13 = st.sidebar.text_input("13.0mm:")
    d12 = st.sidebar.text_input("12.0mm:")
    d11 = st.sidebar.text_input("11.0mm:")

d10 = st.sidebar.text_input("10.0mm:")
d9 = st.sidebar.text_input("9.0mm:")
d8 = st.sidebar.text_input("8.0mm:")
d7 = st.sidebar.text_input("7.0mm:")
d6 = st.sidebar.text_input("6.0mm:")
d5 = st.sidebar.text_input("5.0mm:")
d4 = st.sidebar.text_input("4.0mm:")
d3 = st.sidebar.text_input("3.0mm:")
d2 = st.sidebar.text_input("2.0mm:")
d1 = st.sidebar.text_input("1.0mm:")
d0 = st.sidebar.text_input("0.0mm:")
dm1 = st.sidebar.text_input("-1.0mm:")
dm2 = st.sidebar.text_input("-2.0mm:")
dm3 = st.sidebar.text_input("-3.0mm:")
dm4 = st.sidebar.text_input("-4.0mm:")
dm5 = st.sidebar.text_input("-5.0mm:")
dm6 = st.sidebar.text_input("-6.0mm:")
dm7 = st.sidebar.text_input("-7.0mm:")
dm8 = st.sidebar.text_input("-8.0mm:")
dm9 = st.sidebar.text_input("-9.0mm:")

for i in range(51):
    
    if invert == "Inverted":
        ax.plot(trajectory_end_Y+i*trajetory_tick_Y, trajectory_end_Z+i*trajetory_tick_Z, 'red', marker=(2, 0, Ring), markersize=5)
        
        if start_mm == "15mm":    
            if i == 40:
                ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(15)+str("   ")+str(d15), fontsize=6)
            if i == 39:
                ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(14)+str("   ")+str(d14), fontsize=6)
            if i == 38:
                ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(13)+str("   ")+str(d13), fontsize=6)
            if i == 37:
                ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(12)+str("   ")+str(d12), fontsize=6)
            if i == 36:
                ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(11)+str("   ")+str(d11), fontsize=6)

        if i == 35:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(10)+str("   ")+str(d10), fontsize=6)
        elif i == 34:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(9)+str("   ")+str(d9), fontsize=6)
        elif i == 33:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(8)+str("   ")+str(d8), fontsize=6)
        elif i == 32:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(7)+str("   ")+str(d7), fontsize=6)
        elif i == 31:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(6)+str("   ")+str(d6), fontsize=6)
        elif i == 30:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(5)+str("   ")+str(d5), fontsize=6)
        elif i == 29:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(4)+str("   ")+str(d4), fontsize=6)
        elif i == 28:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(3)+str("   ")+str(d3), fontsize=6)
        elif i == 27:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(2)+str("   ")+str(d2), fontsize=6)
        elif i == 26:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(1)+str("   ")+str(d1), fontsize=6)
        elif i == 25:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(0)+str("   ")+str(d0), fontsize=6)
        elif i == 24:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(-1)+str("   ")+str(dm1), fontsize=6)
        elif i == 23:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(-2)+str("   ")+str(dm2), fontsize=6)
        elif i == 22:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(-3)+str("   ")+str(dm3), fontsize=6)
        elif i == 21:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(-4)+str("   ")+str(dm4), fontsize=6)
        elif i == 20:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(-5)+str("   ")+str(dm5), fontsize=6)
        elif i == 19:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(-6)+str("   ")+str(dm6), fontsize=6)
        elif i == 18:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(-7)+str("   ")+str(dm7), fontsize=6)
        elif i == 17:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(-8)+str("   ")+str(dm8), fontsize=6)
        elif i == 16:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y+4,trajectory_end_Z+i*trajetory_tick_Z-3,str(-9)+str("   ")+str(dm9), fontsize=6)
            
    else:
        ax.plot(trajectory_end_Y+i*trajetory_tick_Y, trajectory_end_Z+i*trajetory_tick_Z, 'red', marker=(2, 0, 180-Ring), markersize=5)
        
        if start_mm == "15mm":    
            if i == 40:
                ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(15)+str("   ")+str(d15), fontsize=6)
            if i == 39:
                ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(14)+str("   ")+str(d14), fontsize=6)
            if i == 38:
                ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(13)+str("   ")+str(d13), fontsize=6)
            if i == 37:
                ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(12)+str("   ")+str(d12), fontsize=6)
            if i == 36:
                ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(11)+str("   ")+str(d11), fontsize=6)

        if i == 35:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(10)+str("   ")+str(d10), fontsize=6)
        elif i == 34:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(9)+str("   ")+str(d9), fontsize=6)
        elif i == 33:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(8)+str("   ")+str(d8), fontsize=6)
        elif i == 32:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(7)+str("   ")+str(d7), fontsize=6)
        elif i == 31:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(6)+str("   ")+str(d6), fontsize=6)
        elif i == 30:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(5)+str("   ")+str(d5), fontsize=6)
        elif i == 29:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(4)+str("   ")+str(d4), fontsize=6)
        elif i == 28:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(3)+str("   ")+str(d3), fontsize=6)
        elif i == 27:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(2)+str("   ")+str(d2), fontsize=6)
        elif i == 26:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(1)+str("   ")+str(d1), fontsize=6)
        elif i == 25:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(0)+str("   ")+str(d0), fontsize=6)
        elif i == 24:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(-1)+str("   ")+str(dm1), fontsize=6)
        elif i == 23:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(-2)+str("   ")+str(dm2), fontsize=6)
        elif i == 22:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(-3)+str("   ")+str(dm3), fontsize=6)
        elif i == 21:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(-4)+str("   ")+str(dm4), fontsize=6)
        elif i == 20:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(-5)+str("   ")+str(dm5), fontsize=6)
        elif i == 19:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(-6)+str("   ")+str(dm6), fontsize=6)
        elif i == 18:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(-7)+str("   ")+str(dm7), fontsize=6)
        elif i == 17:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(-8)+str("   ")+str(dm8), fontsize=6)
        elif i == 16:
            ax.text(trajectory_end_Y+i*trajetory_tick_Y-5,trajectory_end_Z+i*trajetory_tick_Z+1,str(-9)+str("   ")+str(dm9), fontsize=6)

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
                                                          
    ax.plot(x_rot+x_shift, y_rot+y_shift, 'gray', linewidth=0.5) 

if invert == "Normal":
    ax.invert_xaxis()



labels1 = "Name: "+str(patient_name)+"\n"+"ID (MER): "+str(int(patient_id))+"\n"+"MRN: "+str(int(mrn))+"\n"+"Sex: "+str(sex)+"\n"+"DOB: "+str(dob)+"\n"+"OP Date: "+str(op_date)+"\n"+"Surgeon: "+str(surgeon)
labels2 = "Target: "+str(target)+"\n"+"Disease: "+str(disease)+"\n"+"Track: "+str(s_track)+"\n"+"Hemisphere: "+str(hemi)+"\n"+"AC(x,y,z): "+"("+str(AC_X)+", "+str(AC_Y)+", "+str(AC_Z)+")""\n"+"PC(x,y,z): "+"("+str(PC_X)+", "+str(PC_Y)+", "+str(PC_Z)+")""\n"+"Coord(x,y,z): "+"("+str(X)+", "+str(Y)+", "+str(Z)+")""\n"+"Ring Angle: "+str(Ring)+"°"+"\n"+"Arc Angle: "+str(Arc)+"°"+"\n"

if invert == "Normal":
    anchored_text1 = AnchoredText(labels1, prop=dict(size=6,color='black'),loc=1)
    anchored_text2 = AnchoredText(labels2, prop=dict(size=6,color='black'),loc=3)
else:
    anchored_text1 = AnchoredText(labels1, prop=dict(size=6,color='black'),loc=2)
    anchored_text2 = AnchoredText(labels2, prop=dict(size=6,color='black'),loc=4)

ax.add_artist(anchored_text1)
ax.add_artist(anchored_text2)

st.write(fig)


