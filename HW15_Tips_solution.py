import seaborn as sns
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = sns.load_dataset('tips')

df.sex = df.sex.astype(str)
df.smoker = df.smoker.astype(str)
df.day = df.day.astype(str)
df.time = df.time.astype(str)

st.title('小費統計分析')

# https://docs.streamlit.io/en/stable/api.html#display-charts
fig, ax = plt.subplots()
ax.hist(df['tip'], bins=20)
st.pyplot(fig)

# https://docs.streamlit.io/en/stable/api.html#display-interactive-widgets
sex = st.multiselect(
    '性別',
     df['sex'].unique())

wday = st.multiselect(
    '星期?',
     df['day'].unique())

meal = st.multiselect(
    '時間',
     df['time'].unique())

total_bill = st.slider('計程車費', df['total_bill'].min(), df['total_bill'].max(), float(df['total_bill'].mean())) 
  
data = df.loc[(df['sex'].isin(sex)) & (df['day'].isin(wday)) & (df['time'].isin(meal)) & (df['total_bill']>=total_bill)]
st.write("Total tips ", data.sort_index())  

st.write("小計 ", data[['sex', 'day', 'time', 'tip']].groupby(by=['sex', 'day', 'time']).mean())  
