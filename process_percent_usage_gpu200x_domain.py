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
# In addition assign a research programme to each and every user corresponding to what appears in user database
subprocess.call("./combine_gpu200x.sh")

# Go to each GPU node and scan through the information provided in the file
# which contains information for the dates provided above
# The file all should have everything for each node
for i in range(1,7):
    j = str(i)
    cols=['date', 'gpunum', 'gpuid', 'hwarenum', 'proc1', 'proc2', 'proc3', 'user', 'code', 'pid', 'prog']
    df1 = pd.read_csv("logs/gpu/gpu200"+j+"/all", names=cols, header=None, low_memory=False)
    df1['date'] = pd.to_datetime(df1["date"], format="%Y%m%d %H:%M")
    # Count the number of times a specific user appears per day
    df1['day'] = df1['date'].apply(lambda x: "%d-%d-%d" % (x.year,x.month,x.day))
    # Group all codes that are considered MD codes
    df1['code'] = df1.code.str.replace(r'(^.*pmemd.cuda.*$)|(^.*gmx.*$)|(^.*namd2.*$)|(^.*desmond.*$)|(^.*charmm.*$)', 'MD')
    # Group all codes that are considered ML codes
    df1['code'] = df1.code.str.replace(r'(^.*python.*$)|(^.*net3.*$)|(^.*imaging.*$)|(^.*dnls.*$)', 'ML')
    # Group all codes that are considered DEM codes
    df1['code'] = df1.code.str.replace(r'(^.*Rocky.*$)', 'DEM')
    # Group all codes that are considered Cryo-EM codes
    df1['code'] = df1.code.str.replace(r'(^.*relion.*$)', 'RELION')
    # Group everything that is not using the GPU
    df1['code'] = df1.code.str.replace(r'(^.*null.*$)', 'NULL')
    # Everything else
    df1['code'] = df1.code.str.replace(r'(^.*a.out.*$)|(^.*lmp.*$)|(^.*nvidia.*$)|(^.* .*$)', 'OTHER')
    # Replace NaN entries with null
#    df1=df1.replace(np.nan, 'NULL', regex=True)
    # Count the number of times a research programme appears per day and calculate percentage
#    df2 = (df1.groupby(['day', 'prog']).size()*100/864).round(1).reset_index(name='percent')
    # Count the number of times a specific code appears per day
    df3 = (df1.groupby(['day', 'code']).size()*100/864).round(1).reset_index(name='percent')
    # This gives 2D plot of date and user/code
#    fig = px.bar(df2, x = 'day', y = 'percent', color = 'prog')
#    fig.update_layout(
#    title='GPU200'+j,
#    xaxis_title='Date',
#    yaxis_title='Percent Usage',
#    font=dict(family='Times New Roman', size=12, color='black'))
#    fig.write_html('gpu200'+j+'_percent_prog.html')
    fig = px.bar(df3, x = 'day', y = 'percent', color='code')
    fig.update_layout(
    title='GPU200'+j,
    xaxis_title='Date',
    yaxis_title='Percent Usage',
    font=dict(family='Times New Roman', size=12, color='black'))
    fig.write_html('gpu200'+j+'_percent_code.html')
#    fig.show()
