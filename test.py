from logging.handlers import RotatingFileHandler
import streamlit as st
from PIL import Image
import os 
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import numpy as np
from matplotlib.offsetbox import AnchoredText

os.chdir("/Users/srdjansumarac/Desktop")

st.title("TNBS: MER Mapping Software")
st.info('By Srdjan Sumarac')

fig, ax = plt.subplots()
ax.set_facecolor('black')
ax.set_xlim([0, 100])
ax.set_ylim([0, 100])



df = pd.read_csv("/Users/srdjansumarac/Documents/GitHub/tnbsmapper/Coronal_map.csv")

shape_id = df['shape_id']
shapes = df['shapes'].dropna()

for i in range(0,len(shapes)):
    
    x = df[df['shape_id'] == shapes[i]]['X']
    y = df[df['shape_id'] == shapes[i]]['Y']
    
    ax.plot(x, y, 'white', linewidth=0.5) 





st.subheader("Annotations")

col1, col2 = st.columns(2)

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

mpl.rcParams['text.color'] = "black"
ax.plot(50, 50, 'yellow', marker=".")
ax.text(90,90,"",bbox=dict(facecolor='white'), fontsize=10)


x = 30*np.random.randn(10000)
mu = x.mean()
median = np.median(x)
sigma = x.std()
textstr = '\n'.join((
    r'$AC X=%.1f, PC X=%.1f$' % (100, 100),
    r'$AC Y=%.1f, PC Y=%.1f$' % (100, 100),
    r'$AC Z=%.1f, PC Z=%.1f$' % (100, 100)))

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

patient_id = 1000
mrn = 1000000
sex = "Male"
dob = "15 Jan 67"

op_date = "20 Jan 22"
surgeon = "AL"
target = "STN"
disease = "PD"
s_track = "s1"
hemi = "Right"

AC_x = 100
AC_y = 100
AC_z = 100

PC_x = 100
PC_y = 100
PC_z = 100


x = 100
y = 100
z = 100
ring = 60
arc = 100

labels = "Patient ID:"+str(patient_id)+"\n"+"MRN:"+str(mrn)+"\n"+"Sex: "+str(sex)+"\n"+"DOB: "+str(dob)+"\n"+"OP Date: "+str(op_date)+"\n"+"Surgeon: "+str(surgeon)+"\n"+"Target: "+str(target)+"\n"+"Track: "+str(s_track)+"\n"+"Hemisphere: "+str(hemi)+"\n"+"AC(x,y,z): "+"("+str(AC_x)+","+str(AC_y)+","+str(AC_z)+")""\n"+"PC(x,y,z): "+"("+str(PC_x)+","+str(PC_y)+","+str(PC_z)+")""\n"+"Coord(x,y,z): "+"("+str(x)+","+str(y)+","+str(z)+")""\n"+"Ring Angle: "+str(ring)+"°"+"\n"+"Arc Angle: "+str(arc)+"°"+"\n"
anchored_text1 = AnchoredText(labels, prop=dict(size=6),loc=1)
ax.add_artist(anchored_text1)







#+"Sex: = "+str(sex)+"\n"
#+"DOB: = "+str(dob)+"\n"







# place a text box in upper left in axes coords
#ax.text(0.6, 0.95, textstr, transform=ax.transAxes, fontsize=7,verticalalignment='top',bbox=dict(facecolor='white', alpha=1))


st.write(fig)