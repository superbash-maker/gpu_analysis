import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from datetime import date
import os
import subprocess
import datetime

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
    # Count the number of times a specific user appears per day
    df['day'] = df['date'].apply(lambda x: "%d-%d-%d" % (x.year,x.month,x.day))
    df1 = (df.groupby(['day', 'user']).size()*100/1152).round(1).reset_index(name='percent')
#    print(df1)
    # Count the number of times a specific code appears per day
    df2 = (df.groupby(['day', 'code']).size()*100/1152).round(1).reset_index(name='percent')
    # This gives 2D plot of date and user/code
#    fig = px.bar(df1, x = 'day', y = 'percent', color = 'user')
    fig = px.bar(df2, x = 'day', y = 'percent', color='code')
    # This is to get 3D plot per GPUID
    fig.update_layout(
    title='GPU400'+j,
    xaxis_title='Date',
    yaxis_title='Percent',
    font=dict(family='Times New Roman', size=12, color='black'))
#    fig.write_image("gpu400"+j+"percent_user.png", width=2560, height=1440)
#    fig.write_image("gpu400"+j+"percent_code.png", width=2560, height=1440)
    fig.show()
