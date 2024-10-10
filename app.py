import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')


#importando csv
# -------------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'css/style.css')
with open(file_path) as f:
    css = f.read()


#funções
# -------------------------------------------------------------
def carrega_dados_recentes(pasta_dados):
    '''
        Carrega arquivos CSV mais recentes
    '''
    pastas = False
    try:
        pastas = [f for f in os.listdir(pasta_dados) if os.path.isdir(os.path.join(pasta_dados, f))]
    except:
        pass
    if pastas:
        pasta_mais_recente = max(pastas, key=lambda x: os.path.getmtime(os.path.join(pasta_dados, x)))
        caminho_pasta = os.path.join(pasta_dados, pasta_mais_recente)
        arquivos = [f for f in os.listdir(caminho_pasta) if f.endswith('.csv')]
        if len(arquivos) >= 2:
            path_1 = os.path.join(caminho_pasta, arquivos[0])
            df_1 = pd.read_csv(path_1)
            path_2 = os.path.join(caminho_pasta, arquivos[2])
            df_2 = pd.read_csv(path_2)
            return df_1, df_2
        else:
            return None, None
    else:
        return None, None


#app
# -------------------------------------------------------------

#nomeando página
st.set_page_config(
    page_title='ClimateFlow', 
    page_icon='img/ico.ico'
)
#título
col1, col2 = st.columns([.2, .8])
with col1:
    st.image('img/logo.png')
with col2:
    st.title('ClimateFlow')
#carregando dados
pasta_dados = 'data'
clima_descricao, clima_temperaturas = carrega_dados_recentes(pasta_dados)
if clima_descricao is not None and clima_temperaturas is not None:
    clima_descricao['datetime'] = pd.to_datetime(clima_descricao['datetime'])
    clima_temperaturas['datetime'] = pd.to_datetime(clima_temperaturas['datetime'])
    clima = pd.merge(clima_descricao, clima_temperaturas, on='datetime', how='left')
    #calculando temperatura mínima, máxima e média
    st.dataframe(clima)
    temp_min = clima['temp'].min()
    temp_max = clima['temp'].max()
    temp_media = clima['temp'].mean()
    #cards
    st.subheader('Informações de Temperatura')
    st.write(f'Temperatura Mínima: {temp_min:.1f} °C')
    st.write(f'Temperatura Máxima: {temp_max:.1f} °C')
    st.write(f'Temperatura Mediana: {temp_media:.1f} °C')
    #figuras
    st.subheader('Temperatura Diária')
    fig_temp = go.Figure(data=[go.Scatter(x=clima['datetime'], y=clima['temp'], mode='lines', name='Temperatura')])
    fig_temp.update_layout(
        xaxis_title='Data',
        yaxis_title='Temperatura (°C)',
        template='plotly_white'
    )
    st.plotly_chart(fig_temp)
    st.subheader('Temperaturas Diárias (Mínima, Média, Máxima)')
    fig_temp_minmax = go.Figure()
    fig_temp_minmax.add_trace(go.Scatter(x=clima['datetime'], y=clima['tempmin'], mode='lines', name='Temperatura Mínima'))
    fig_temp_minmax.add_trace(go.Scatter(x=clima['datetime'], y=clima['temp'], mode='lines', name='Temperatura Média'))
    fig_temp_minmax.add_trace(go.Scatter(x=clima['datetime'], y=clima['tempmax'], mode='lines', name='Temperatura Máxima'))
    fig_temp_minmax.update_layout(
        xaxis_title='Data',
        yaxis_title='Temperatura (°C)',
        template='plotly_white'
    )
    st.plotly_chart(fig_temp_minmax)
    st.subheader('Condições Climáticas')
    fig_condicoes = go.Figure()
    fig_condicoes.add_trace(go.Bar(x=clima['datetime'], y=clima['icon'].apply(lambda x: 1 if x == 'rain' else 0), name='Chuva'))
    fig_condicoes.add_trace(go.Bar(x=clima['datetime'], y=clima['icon'].apply(lambda x: 1 if x == 'partly-cloudy-day' else 0), name='Parcialmente Nublado'))
    fig_condicoes.add_trace(go.Bar(x=clima['datetime'], y=clima['icon'].apply(lambda x: 1 if x == 'clear-day' else 0), name='Ensolarado'))
    fig_condicoes.update_layout(
        xaxis_title='Data',
        yaxis_title='Frequência',
        barmode='stack',
        template='plotly_white'
    )
    st.plotly_chart(fig_condicoes)
else:
    st.error('Não há dados disponíveis na pasta')

#aplicando css
st.write(f'<style>{css}</style>', unsafe_allow_html=True)