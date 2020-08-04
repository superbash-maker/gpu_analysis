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
start_date = date(2020, 5, 1)
end_date = date(2020, 7, 31)
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
subprocess.call("./combine_gpu400x.sh")

# Go to each GPU node and scan through the information provided in the file
# which contains information for the dates provided above
# The file all should have everything for each node
appended_data = pd.DataFrame()
# Get all GPU200x data and append to single dataframe
for i in range(1,7):
    j = str(i)
    cols=['date', 'gpunum', 'gpuid', 'hwarenum', 'proc1', 'proc2', 'proc3', 'user', 'code', 'pid']
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
    # Count the number of times a specific code appears per day and get percentage
    # Remember that GPU200x nodes have 864 entries per day
    df2 = (df1.groupby(['day', 'code']).size()*100/864).round(1).reset_index(name='percent')
    # Count the number of times a specific code appears per day
    appended_data=appended_data.append(df2,ignore_index=True)

# Get all GPU400x data and append to same dataframe as above
for i in range(1,4):
    j = str(i)
    cols=['date', 'gpunum', 'gpuid', 'hwarenum', 'proc1', 'proc2', 'proc3', 'user', 'code', 'pid']
    df1 = pd.read_csv("logs/gpu/gpu400"+j+"/all", names=cols, header=None, low_memory=False)
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
    # Count the number of times a specific code appears per day and get percentage
    # Remember that GPU400x nodes have 1152 entries per day
    df2 = (df1.groupby(['day', 'code']).size()*100/1152).round(1).reset_index(name='percent')
    appended_data=appended_data.append(df2,ignore_index=True)

# Get the year and month and store in new column on appended_data dataframe
appended_data['yearmonth'] = appended_data['day'].astype(str).str[:6]
# Store the months that have 30, 31 and 28 days, respectively
options1 = ['2020-4', '2020-6', '2020-9', '2020-11']
options2 = ['2020-1', '2020-3', '2020-5', '2020-7', '2020-8', '2020-10', '2020-11']
options3 = ['2020-2']
# Compute the GPU percentage usage per month by summing up all percentages per day
# And divide by total number of GPU nodes on the cluster (9 nodes)
# Also divide by the number of days of a month
monthly_percent1 = appended_data[appended_data['yearmonth'].isin(options1)]
monthly_percent1 = (monthly_percent1.groupby(['yearmonth','code']).sum()/(9*30)).round(1).reset_index()
monthly_percent2 = appended_data[appended_data['yearmonth'].isin(options2)]
monthly_percent2 = (monthly_percent2.groupby(['yearmonth','code']).sum()/(9*31)).round(1).reset_index()
monthly_percent3 = appended_data[appended_data['yearmonth'].isin(options3)]
monthly_percent3 = (monthly_percent3.groupby(['yearmonth','code']).sum()/(9*28)).round(1).reset_index()
frames = [monthly_percent1, monthly_percent2, monthly_percent3]
merge_percent = pd.concat(frames)
print(merge_percent)
# This gives 2D plot of date and code
#fig = px.bar(monthly_percent, x = 'month', y = 'percent', color='code')
#fig.update_layout(
#title='GPU_USAGE',
#xaxis_title='Month',
#yaxis_title='Percent Usage',
#font=dict(family='Times New Roman', size=12, color='black'))
##fig.write_html('gpu200'+j+'_percent_code.html')
#fig.show()
