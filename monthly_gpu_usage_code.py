import pandas as pd
import plotly.express as px
import numpy as np
from datetime import date
import subprocess

# Get the date range that you want to process
form=np.array([])
start_date = date(2020, 12, 1)
end_date = date(2021, 5, 31)
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
    df1['day'] = df1['date'].apply(lambda x: "%d-%02d-%d" % (x.year,x.month,x.day))
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
    df1['day'] = df1['date'].apply(lambda x: "%d-%02d-%d" % (x.year,x.month,x.day))
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
appended_data['yearmonth'] = appended_data['day'].astype(str).str[:7]
# Store the months that have 30, 31 and 28 days, respectively
options1 = ['2021-04', '2021-06', '2021-09', '2021-11']
options2 = ['2021-01', '2021-03', '2021-05', '2021-07', '2021-08', '2021-10', '2020-12']
options3 = ['2021-02']
# Compute the GPU percentage usage per month by summing up all percentages per day
# And divide by total number of GPU nodes on the cluster (9 nodes) and the number of days in a month
monthly_percent1 = appended_data[appended_data['yearmonth'].isin(options1)]
monthly_percent1 = (monthly_percent1.groupby(['yearmonth','code']).sum()/(9*30)).round(1).reset_index()
monthly_percent2 = appended_data[appended_data['yearmonth'].isin(options2)]
monthly_percent2 = (monthly_percent2.groupby(['yearmonth','code']).sum()/(9*31)).round(1).reset_index()
monthly_percent3 = appended_data[appended_data['yearmonth'].isin(options3)]
monthly_percent3 = (monthly_percent3.groupby(['yearmonth','code']).sum()/(9*28)).round(1).reset_index()
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
xaxis_ticktext=["Dec 2020", "Jan 2021", "Feb 2021", "Mar 2021", "Apr 2021", "May 2021"],
xaxis_tickvals=["2020-12", "2021-01", "2021-02", "2021-03", "2021-04", "2021-05"],
font=dict(family='Times New Roman', size=14, color='black'))
#fig.write_html('overall_percent_gpu_usage_code.html')
fig.show()
