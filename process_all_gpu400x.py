import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from datetime import date
import os
import subprocess

# Get the date range that you want to process
form=np.array([])
start_date = date(2020, 2, 21)
end_date = date(2020, 7, 26)
daterange = pd.date_range(start_date, end_date)
for single_day in daterange:
    form=np.append(form, single_day.strftime("%Y%m%d"))

# Write out the dates to a file called dates
fdate = open("dates","w")
for day in form:
    fdate.write(str(day)+"\n")
fdate.close()

# Got to each directory that contains the raw data and combine the files
# over the date range present in the file dates
subprocess.call("./combine_gpu400x.sh")

# Go to each GPU node and scan through the information provided in the file
# which contains information for the dates provided above
# The file all should have everything for each node
for i in range(1,4):
    j = str(i)
    cols=['date', 'gpunum', 'gpuid', 'hwarenum', 'proc1', 'proc2', 'proc3', 'user', 'code', 'pid']
    df = pd.read_csv("logs/gpu/gpu400"+j+"/all", names=cols, header=None, low_memory=False)
    df['date'] = pd.to_datetime(df["date"], format="%Y%m%d %H:%M")
    # This gives 2D plot of date and user/code
#    fig = px.scatter(df, x = 'date', y = 'user', color='user')
    fig = px.scatter(df, x = 'date', y = 'code', color='code')
    # This is to get 3D plot per GPUID
#    fig = px.scatter_3d(df, x = 'date', y = 'user', z = 'code', color='code')
    fig.update_layout(
    title='GPU400'+j,
    xaxis_title='Date',
    yaxis_title='Code',
    font=dict(family='Times New Roman', size=20, color='black'))
#    fig.write_image("gpu400"+j+"_user.png", width=2560, height=1440)
    fig.write_image("gpu400"+j+"_code.png", width=2560, height=1440)
#    fig.show()
