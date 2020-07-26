import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from datetime import date
import os
import subprocess

form=np.array([])
start_date = date(2020, 7, 1)
end_date = date(2020, 7, 2)
daterange = pd.date_range(start_date, end_date)
for single_day in daterange:
    form=np.append(form, single_day.strftime("%Y%m%d"))

fdate = open("dates","w")
for day in form:
    fdate.write(str(day)+"\n")
fdate.close()

subprocess.call("./combine.sh")

for i in range(1,7):
    j = str(i)
    cols=['date', 'gpunum', 'gpuid', 'hwarenum', 'proc1', 'proc2', 'proc3', 'user', 'code', 'proc4']
    df = pd.read_csv("logs/gpu/gpu200"+j+"/all", names=cols, header=None)
    fig = px.scatter(df, x = 'date', y = 'user')
    fig.show()
