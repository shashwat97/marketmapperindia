import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import requests

st.set_page_config(layout="wide")

st.title('Market Mapper India')

#all_data = 'https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=BSE&opttopic=indexcomp&index=4'

idf = pd.read_csv('nse_links.csv')

#idf = pd.read_excel('nse_links.xlsx')

option = st.selectbox('Select Index: ', idf['Name'], index=0)
all_data = idf[idf['Name'] == option]['Link'].values[0]

r = requests.get(all_data)
df = pd.read_html(r.text)[0].dropna()

new_list = []
for n in df['Industry'].str.split('-').tolist():
    if len(n)==1:
        n.append(n[0])
    new_list.append(n)


df['Company Name'] = df['Company Name'].str[:-34]
df = df.merge(pd.DataFrame(new_list, columns = ['Inds', 'Sector']), right_index = True, left_index = True).dropna()


fig = px.treemap(df, path=['Inds', 'Company Name'], values='Mkt Cap(Rs cr)',
                  color='%Chg', hover_data=['Company Name'],
                  color_continuous_scale='RdYlGn', range_color=[-4,4], 
                  color_continuous_midpoint=np.median(df['%Chg']))


fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
#fig.show()
fig.update_layout(height=800)

# Plot!

st.plotly_chart(fig, use_container_width=True, height=800)
