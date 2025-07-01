import sys
import streamlit as st
import time
from notebooks import SentimentAnalyzerNotebook
from components import (
    TopicInput,
    DisplayThemes,
    DisplayPredictions,
    PageHeader,
)

st.set_page_config(
    page_title="Sentiment Explorer",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🦈"
)

# Exibe o cabeçalho da página
PageHeader()


def load_data():
    sentiment_analyzer = SentimentAnalyzerNotebook()
    sentiment_analyzer.main(st.session_state.topics)
    output_sentiment_df = sentiment_analyzer.sentiment_indicator
    st.session_state.output_sentiment_df = output_sentiment_df
    st.session_state.news_df = sentiment_analyzer.news_df
    
# Centraliza os campos usando colunas do Streamlit
col1, col2, col3 = st.columns([1, 2, 1])

# Usar session_state para manter os temas adicionados
if "topics" not in st.session_state:
    st.session_state.topics = ["Bitcoin", "Ethereum"]

with col2:

    TopicInput()
    if st.session_state.topics:
        DisplayThemes()
    else:
        st.info("Nenhum tema adicionado.")

    analysis_run = st.button(
        "Executar Análise",
        key="run_analysis",
        help="Clique para executar a análise de sentimento",
        use_container_width=True,
    )

if analysis_run:
    st.toast("Buscando informações...", icon="🔄")
    load_data()
    time.sleep(1)
    st.toast("Executando análise...", icon="🔍")
    time.sleep(1)
    st.toast("Análise concluida com sucesso!", icon="✅")
    st.balloons()
    st.divider()
    DisplayPredictions()
