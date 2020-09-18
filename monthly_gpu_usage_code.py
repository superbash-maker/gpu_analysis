import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from datetime import date
import subprocess

# Get the date range that you want to process
form=np.array([])
start_date = date(2020, 3, 1)
end_date = date(2020, 8, 31)
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
options2 = ['2020-1', '2020-3', '2020-5', '2020-7', '2020-8', '2020-10', '2020-12']
options3 = ['2020-2']
# Compute the GPU percentage usage per month by summing up all percentages per day
# And divide by total number of GPU nodes on the cluster (9 nodes) and the number of days in a month
# Keep in mind Feb was a leap year in 2020, so use 29 days instead of 28
monthly_percent1 = appended_data[appended_data['yearmonth'].isin(options1)]
monthly_percent1 = (monthly_percent1.groupby(['yearmonth','code']).sum()/(9*30)).round(1).reset_index()
monthly_percent2 = appended_data[appended_data['yearmonth'].isin(options2)]
monthly_percent2 = (monthly_percent2.groupby(['yearmonth','code']).sum()/(9*31)).round(1).reset_index()
monthly_percent3 = appended_data[appended_data['yearmonth'].isin(options3)]
monthly_percent3 = (monthly_percent3.groupby(['yearmonth','code']).sum()/(9*29)).round(1).reset_index()
# Put all dataframes for each month together
combine_percent = [monthly_percent1, monthly_percent2, monthly_percent3]
merge_percent = pd.concat(combine_percent)
# Sort the list in order of months and reindex
merge_percent = merge_percent.sort_values(by=['yearmonth','percent'])
merge_percent = merge_percent.reset_index(drop=True)
# This gives 2D plot of month and percent usage for each code
fig = px.bar(merge_percent, x = 'yearmonth', y = 'percent', color='code')
fig.update_layout(
title='GPU_USAGE',
xaxis_title='Month',
yaxis_title='Percent Usage',
xaxis_ticktext=["Mar 2020", "Apr 2020", "May 2020", "Jun 2020", "Jul 2020", "Aug 2020"],
xaxis_tickvals=["2020-3", "2020-4", "2020-5", "2020-6", "2020-7", "2020-8"],
font=dict(family='Times New Roman', size=14, color='black'))
fig.write_html('overall_percent_gpu_usage_code.html')
#fig.show()
