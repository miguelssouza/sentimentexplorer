import time
import streamlit as st


class DisplayThemes:
    """
    DisplayThemes is a class responsible for displaying and managing a list of topics (themes) in a Streamlit application.
    It provides a stylized label for the section and displays each topic with an option to remove it individually or clear all topics at once.
    The class also uses Streamlit's status component to indicate the loading and completion of theme management actions.
    Attributes:
        topics (list): The list of topics stored in Streamlit's session state.
    Methods:
        __init__():
            Initializes the DisplayThemes class, retrieves topics from session state, and triggers the display of the label and themes.
        __label(label: str):
            Displays a stylized section title using HTML and CSS within Streamlit's markdown component.
        __themes_display():
            Displays the list of topics with options to remove each individually or all at once.
            Utilizes Streamlit's status component to provide feedback on the loading and completion of actions.
    """
    def __init__(self):
        # Inicializa a classe e exibe o label e os temas
        self.topics = st.session_state.topics

        self.__label("Temas:")
        self.__themes_display()

    def __label(self, label: str):
        # Exibe um título estilizado para a seção de temas
        return st.markdown(
            f"""
            <h4 style='
                background: linear-gradient(90deg, #4F8BF9 0%, #8F6FE6 50%, #4FD1C5 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                color: transparent;
                font-size: 1.5rem;
                font-weight: bold;
                margin-bottom: 0.8rem;
            '>
                {label}
            </h4>
            """,
            unsafe_allow_html=True,
        )
        
    def __themes_display(self):
        # Exibe os temas adicionados e permite removê-los individualmente ou todos de uma vez
        with st.status("Adicionando temas...") as status:
            for topic in self.topics:
                col_topic, col_btn = st.columns([5, 1])
                with col_topic:
                    st.markdown(
                        f"<span style='font-size:1.3rem; color:#5A67D8; font-weight:bold;'>{topic} ✅</span>",
                        unsafe_allow_html=True,
                    )
                with col_btn:
                    if st.button("❌", key=f"remove_{topic}"):
                        self.topics.remove(topic)
                        st.rerun()
            
            if st.button("Remover todos", key="remove_all_topics"):
                self.topics = []
                st.rerun()
            
            status.update(label="Carregando temas...", state="running")
            time.sleep(1)
            status.update(label="Temas carregados! ✅", state="complete")
            time.sleep(1)
            status.update(label="Ver os temas adicionados. (Clique aqui)", state="complete")

class DisplayPredictions:
    def __init__(self):
        # Inicializa a classe e exibe os resultados da análise de sentimento
        self.__display()

    def __sentiment_label(self, score):
        # Retorna o rótulo e a cor correspondente ao score de sentimento
        if score <= -1.5:
            return "Muito Negativo", "#3182CE"
        elif score <= -0.5:
            return "Negativo", "#4299E1"
        elif score < 0.5:
            return "Neutro", "#F6AD55"
        elif score < 1.5:
            return "Positivo", "#48BB78"
        else:
            return "Muito Positivo", "#38A169"

    def __display(self):
        # Exibe os temas, labels e scores lado a lado em uma linha
        st.markdown(
            "<h4 style='"
            "background: linear-gradient(90deg, #4F8BF9 0%, #8F6FE6 50%, #4FD1C5 100%);"
            "-webkit-background-clip: text;"
            "-webkit-text-fill-color: transparent;"
            "background-clip: text;"
            "color: transparent;"
            "font-size: 1.6rem;"
            "font-weight: bold;"
            "margin-bottom: 1.2rem;'>"
            "Resultados"
            "</h4>",
            unsafe_allow_html=True,
        )
        cols = st.columns([2, 2, 1])
        cols[0].markdown("**Tema**")
        sorted_df = st.session_state.output_sentiment_df.sort_values(
            by="sentiment_weight", ascending=False
        )

        for idx, row in sorted_df.iterrows():
            label, color = self.__sentiment_label(row["sentiment_weight"])
            cols = st.columns([2, 2, 1])
            cols[0].markdown(
                f"<span style='font-size:1.2rem; font-weight:600; color:#4F8BF9'>{row['query']}</span>",
                unsafe_allow_html=True,
            )
            cols[1].markdown(
                f"<span style='background: {color}; color: #fff; border-radius: 1rem; padding: 0.3rem 1.1rem; font-size: 1.05rem; font-weight: 600;'>{label}</span>",
                unsafe_allow_html=True,
            )
            # Badge para o score
            cols[2].markdown(
                f"<span style='background: #2D3748; color: #fff; border-radius: 1rem; padding: 0.3rem 1.1rem; font-size: 1.05rem; font-weight: 600;'>{row['sentiment_weight']:.2f}</span>",
                unsafe_allow_html=True,
            )

class PageHeader:
    """
    PageHeader class responsible for rendering the main header section of the Streamlit app.

    Methods
    -------
    __init__():
        Initializes the PageHeader instance and renders the header upon instantiation.
    __header():
        Private method that displays a styled HTML header and subheader using Streamlit's markdown component.
        The header includes a gradient-styled title and a descriptive subtitle, both centered on the page.
    """
    def __init__(self):
        self.__header()
    
    def __header(self):
        return st.markdown(
            """
            <h1 style='
                text-align: center;
                background: linear-gradient(90deg, #4F8BF9 0%, #8F6FE6 50%, #4FD1C5 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                color: transparent;
                font-size: 2.8rem;
                font-weight: bold;
                margin-bottom: 1.5rem;
            '>
                AI-Powered Sentiment Explorer
            </h1>
            <h3 style='
                text-align: center;
                color: gray;
                font-size: 1.2rem;
                font-weight: 500;
                margin-top: -1rem;
                margin-bottom: 2rem;
            '>
                Descubra a tendência de sentimento do mercado sobre qualquer tema, analisando notícias dos últimos 7 dias.
            </h3>
            """,
            unsafe_allow_html=True,
        )
