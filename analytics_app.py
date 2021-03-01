import pandas as pd
import streamlit as st
import pickle
from PIL import Image

from plotly import tools
from plotly.subplots import make_subplots
import plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot
import plotly.express as px

df = pd.read_pickle('df_br.pkl')

# Removendo NAs da tabela etapa_ensino pelo seu valor mais frequente
most_freq = df['etapa_ensino'].value_counts().index[0]
df['etapa_ensino'].fillna(most_freq, inplace=True)

st.beta_set_page_config(
    page_title="EM | Ebooks",
    page_icon="📚",      # polimento e chiquezas
    layout="centered",
    initial_sidebar_state="expanded",
)

icon = Image.open('logoEM.png')
st.image(icon, width=500)

def main():
    st.title("Análise: Gêneros dos Ebooks") 
    st.markdown("App para analisar a distribuição dos gêneros literários após a classificação automática de 7.000 ebooks.")
    # organizando valores do dataframe em um dicionário -
    df_dict = dict(df['regiao'].value_counts())
    # chaves
    dictk = list(df_dict.keys())
    # valores
    dictv = list(df_dict.values())
    
    # criando dataframe para estados com mais de 400 ebooks
    df2 = df.groupby('estado_escola').filter(lambda x: len(x)>200)
    # organizando valores do dataframe em um dicionário -
    df2_dict = dict(df2['estado_escola'].value_counts())
    # chaves
    dic2tk = list(df2_dict.keys())
    # valores
    dic2tv = list(df2_dict.values())
    
    colors = ["#ff9999", "#b3d9ff", " #e6ffb3"]
    
    fig = make_subplots(rows=1, cols=2,
                       specs=[[{"type": "domain"}, {"type": "domain"}]],
                       subplot_titles=['Por região', 'Por estado (com + de 300 ebooks)'])

    fig.add_trace(
        go.Pie(labels=dictk, values=dictv,
               hoverinfo='percent', textinfo='label+value',
               textfont=dict(size=15),
               marker=dict(colors=colors,
                   line=dict(color='#000000', width=2)
                          )
              ),
        row=1, col=1
    )

    fig.add_trace(
        go.Pie(labels=dic2tk, values=dic2tv,
               hoverinfo='percent', textinfo='label+value',
               textfont=dict(size=15),
               marker=dict(colors=colors,
                   line=dict(color='#000000', width=2)
                          )
              ),
        row=1, col=2
    )

    fig.update_layout(title_text='Qtde. de Ebooks por Localidade', showlegend=False)
    st.plotly_chart(fig)
    
    def graph_plot(var, histnorm, barnorm, barmode):
        fig2 = px.histogram(df, x='categoria_prevista', 
                       color=var,
                       histnorm=histnorm,
                       barnorm=barnorm,
                       title='Distribuição dos gêneros',
                       barmode=barmode
                      )
        
        if (histnorm=='percent') | (barnorm=='percent'):
            fig2.update_layout(yaxis={'ticksuffix':'%', 'title':'Porcentagem'})
        fig2.update_layout(xaxis={'title':'Gênero'}
             )
        return fig2
    
    var = st.sidebar.selectbox(label='Variável (y):', options=['regiao','tipo_escola', 'estado_escola', 'cidade_escola', 'etapa_ensino'])
    
    histnorm = st.sidebar.radio(label='Normalização (histograma)', options=['percent', None])
    
    barnorm = st.sidebar.radio(label='Normalização (barra)', options=[None, 'percent'])
    
    barmode = st.sidebar.radio(label='Exibição', options=['overlay', 'group', 'relative'])
    
    st.plotly_chart(graph_plot(var, histnorm, barnorm, barmode))
    
if __name__=='__main__':
    main()
