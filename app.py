import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


#importing csv
# -------------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'css/style.css')
with open(file_path) as f:
    css = f.read()


#functions
# -------------------------------------------------------------
def import_data(data_dir):
    '''
        Carrega arquivos CSV da semana mais recentes, retorna DataFrame e
        datas de início e fim do período
    '''
    try:
        dirs = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
        last_dir = max(dirs, key=lambda x: os.path.getmtime(os.path.join(data_dir, x)))
        dir_path = os.path.join(data_dir, last_dir)
        files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]
        last_file = os.path.join(dir_path, files[1])
        date_start = datetime.fromtimestamp(os.path.getmtime(last_file))
        date_end = date_start + timedelta(days=7)
        df = pd.read_csv(last_file)
        return df, date_start, date_end
    except:
        return None


#app
# -------------------------------------------------------------

#naming the page
st.set_page_config(
    page_title='ClimateFlow', 
    page_icon='img/ico.ico'
)
#title
col1, col2 = st.columns([.2, .8])
with col1:
    st.image('img/logo.png')
with col2:
    st.title('ClimateFlow')
#importing data
data_dir = 'data'
df, date_start, date_end = import_data(data_dir)
if df is not None:
    #cards
    temp_min = df['temp'].min()
    temp_max = df['temp'].max()
    temp_avg = df['temp'].mean()
    st.subheader(f'Temperature for the Period')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Minimum Temperature', f'{temp_min:.1f} °C')
    with col2:
        st.metric('Maximum Temperature', f'{temp_max:.1f} °C')
    with col3:
        st.metric('Average Temperature', f'{temp_avg:.1f} °C')
    st.write(f'Period: {date_start.strftime("%m/%d")} to {date_end.strftime("%m/%d")}, {date_end.strftime("%Y")}')
    #figure
    st.subheader('Temperature Trend')
    fig_temp_minmax = go.Figure()
    fig_temp_minmax.add_trace(go.Scatter(x=df['datetime'], y=df['tempmin'], mode='lines', name='Minimum Temperature'))
    fig_temp_minmax.add_trace(go.Scatter(x=df['datetime'], y=df['temp'], mode='lines', name='Average Temperature'))
    fig_temp_minmax.add_trace(go.Scatter(x=df['datetime'], y=df['tempmax'], mode='lines', name='Maximum Temperature'))
    fig_temp_minmax.update_layout(
        xaxis_title='Date',
        yaxis_title='Temperature (°C)',
        template='plotly_white',
        height=300,
        margin=dict(l=0, r=0, b=0, t=0, pad=0)
    )
    st.plotly_chart(fig_temp_minmax)
    st.subheader('Weather')
    #weather
    col_num = 5
    col_width = 1 / col_num
    with st.container():
        cols = st.columns(col_num) 
        for i, icon in enumerate(df['icon']):
            col = cols[i % col_num]
            with col:
                st.image(f'img/{icon}.png', caption = datetime.strptime(df['datetime'][i], '%Y-%m-%d').strftime('%A'))
else:
    st.error('No data available')

#applying css
st.write(f'<style>{css}</style>', unsafe_allow_html=True)