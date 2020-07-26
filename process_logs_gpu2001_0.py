import numpy as np
import pandas as pd
import collections
from datetime import date, timedelta
import os

# Remove any existing file:
os.remove("user_usage_gpu2001_0.csv")
os.remove("code_usage_gpu2001_0.csv")

# Create file to write to:
fu = open("user_usage_gpu2001_0.csv","a")
fu.write("Date"+","+"GPUID"+","+"Username"+","+"Percent_Usage"+"\n")
# Create file to write to:
fc = open("code_usage_gpu2001_0.csv","a")
fc.write("Date"+","+"GPUID"+","+"Code"+","+"Percent_Usage"+"\n")

#This will cycle through dates from 27 July 2019 - Present
form=np.array([])
form2=np.array([])
start_date = date(2020, 7, 1)
end_date = date(2020, 7, 21)
daterange = pd.date_range(start_date, end_date)
for single_day in daterange:
    form=np.append(form, single_day.strftime("%Y%m%d"))
    form2=np.append(form2, single_day.strftime("%Y-%m-%d"))

for day in range(len(form)):
    # Extract the raw data and store them in arrays
    alldata=np.char.strip(np.loadtxt("logs/gpu/gpu2001/"+form[day], dtype='str', delimiter=","))
    datetime=alldata[0:,0]
    gpunode=alldata[0:,1]
    app=alldata[0:,8]
    gpunum=alldata[0:,2]
    username=alldata[0:,7]

    # Create empty arrays that will store the important information needed
    codegpu=np.array([])
    usergpu=np.array([])
    date=np.array([])

    for i in range(len(gpunode)):
    # Ignore all null enteries as this means no GPU usage
        if ((gpunum[i] == "0")):
            codegpu=np.append(codegpu,app[i])
            usergpu=np.append(usergpu,username[i])
            date=np.append(date,form2[day])
    userid=pd.Series(usergpu).value_counts().keys().tolist()
    countu=pd.Series(usergpu).value_counts().tolist()
    codeid=pd.Series(codegpu).value_counts().keys().tolist()
    countc=pd.Series(codegpu).value_counts().tolist()
 
    # Create empty arrays to store user usage
    useruse=np.array([])
    userper=np.array([])
    for j in range(len(userid)):
        # Work out number of hours used by user
        # Keep in mind each instance of a user being found corresponds to 5 minutes
        # Convert the number of minutes that user was on GPU to hours
        if (userid[j] == "null"):
            calcu=round((countu[j]*5)/60,1)
            calcup=calcu*0
        else:
            calcu=round((countu[j]*5)/60,1)
            calcup=round((calcu/24)*100,1)
        useruse=np.append(useruse,calcu)
        userper=np.append(userper,calcup)
        fu.write(str(date[j])+","+"0"+","+str(userid[j])+","+str(userper[j])+"\n")

    # Create empty arrays to store code usage
    codeuse=np.array([])
    codeper=np.array([])
    for k in range(len(codeid)):
        # Work out number of hours used per code
        # Keep in mind each instance of a code being found corresponds to 5 minutes
        # Convert the number of minutes that code was on GPU to hours
        if (codeid[k] == "null"):
            calcc=round((countc[k]*5)/60,1)
            calccp=calcc*0
        else:
            calcc=round((countc[k]*5)/60,1)
            calccp=round((calcc/24)*100,1)
        codeuse=np.append(codeuse,calcc)
        codeper=np.append(codeper,calccp)
        fc.write(str(date[k])+","+"0"+","+str(codeid[k])+","+str(codeper[k])+"\n")
fc.close()
fu.close()
