import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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
        Carrega arquivos CSV da semana mais recentes
    '''
    try:
        pastas = [f for f in os.listdir(pasta_dados) if os.path.isdir(os.path.join(pasta_dados, f))]
        pasta_mais_recente = max(pastas, key=lambda x: os.path.getmtime(os.path.join(pasta_dados, x)))
        caminho_pasta = os.path.join(pasta_dados, pasta_mais_recente)
        arquivos = [f for f in os.listdir(caminho_pasta) if f.endswith('.csv')]
        df = pd.read_csv(os.path.join(caminho_pasta, arquivos[1]))
        return df
    except (FileNotFoundError, PermissionError) as e:
        st.error(f'Erro ao carregar os dados: {e}')
        return None


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
df_clima = carrega_dados_recentes(pasta_dados)
if df_clima is not None:
    #calculando temperatura mínima, máxima e média
    st.dataframe(df_clima)
    temp_min = df_clima['temp'].min()
    temp_max = df_clima['temp'].max()
    temp_media = df_clima['temp'].mean()
    #cards
    st.subheader('Informações de Temperatura')
    st.write(f'Temperatura Mínima: {temp_min:.1f} °C')
    st.write(f'Temperatura Máxima: {temp_max:.1f} °C')
    st.write(f'Temperatura Mediana: {temp_media:.1f} °C')
    #figuras
    st.subheader('Temperatura Diária')
    fig_temp = go.Figure(data=[go.Scatter(x=df_clima['datetime'], y=df_clima['temp'], mode='lines', name='Temperatura')])
    fig_temp.update_layout(
        xaxis_title='Data',
        yaxis_title='Temperatura (°C)',
        template='plotly_white'
    )
    st.plotly_chart(fig_temp)
    st.subheader('Temperaturas Diárias (Mínima, Média, Máxima)')
    fig_temp_minmax = go.Figure()
    fig_temp_minmax.add_trace(go.Scatter(x=df_clima['datetime'], y=df_clima['tempmin'], mode='lines', name='Temperatura Mínima'))
    fig_temp_minmax.add_trace(go.Scatter(x=df_clima['datetime'], y=df_clima['temp'], mode='lines', name='Temperatura Média'))
    fig_temp_minmax.add_trace(go.Scatter(x=df_clima['datetime'], y=df_clima['tempmax'], mode='lines', name='Temperatura Máxima'))
    fig_temp_minmax.update_layout(
        xaxis_title='Data',
        yaxis_title='Temperatura (°C)',
        template='plotly_white'
    )
    st.plotly_chart(fig_temp_minmax)
    st.subheader('Condições Climáticas')
    fig_condicoes = go.Figure()
    fig_condicoes.add_trace(go.Bar(x=df_clima['datetime'], y=df_clima['icon'].apply(lambda x: 1 if x == 'rain' else 0), name='Chuva'))
    fig_condicoes.add_trace(go.Bar(x=df_clima['datetime'], y=df_clima['icon'].apply(lambda x: 1 if x == 'partly-cloudy-day' else 0), name='Parcialmente Nublado'))
    fig_condicoes.add_trace(go.Bar(x=df_clima['datetime'], y=df_clima['icon'].apply(lambda x: 1 if x == 'clear-day' else 0), name='Ensolarado'))
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