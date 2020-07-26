import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
df = pd.read_csv('user_usage_gpu2001_0.csv')
fig = px.scatter(df, x = 'Date', y = 'Percent_Usage', title='GPU2001_ID_0', text='Username')
fig.update_traces(textposition='top center')
fig.show()
