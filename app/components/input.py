import streamlit as st


class CustomInput:
    """
    Classe para criar um campo de entrada customizado no Streamlit com label estilizado em gradiente.

    Parâmetros:
        label (str): Texto do label a ser exibido.
        key (str, opcional): Chave única para o campo de entrada.
        placeholder (str, opcional): Texto de placeholder do campo.
        help_text (str, opcional): Texto de ajuda exibido ao passar o mouse.

    Métodos:
        render(): Renderiza o campo de texto no Streamlit.
    """

    def __init__(self, label, key=None, placeholder="", help_text=""):
        """
        Inicializa o campo de entrada customizado.

        Args:
            label (str): Texto do label a ser exibido.
            key (str, opcional): Chave única para o campo de entrada.
            placeholder (str, opcional): Texto de placeholder do campo.
            help_text (str, opcional): Texto de ajuda exibido ao passar o mouse.
        """
        self.label = label
        self.key = key
        self.placeholder = placeholder
        self.help_text = help_text
        self.inside_label = None
        self.__label(label)

    def __label(self, label: str):
        """
        Exibe o label estilizado com gradiente.

        Args:
            label (str): Texto do label.
        """
        self.inside_label = st.markdown(
            f"""
            <h4 style='
                background: linear-gradient(90deg, #4F8BF9 0%, #8F6FE6 50%, #4FD1C5 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                color: transparent;
                font-size: 1.5rem;
                font-weight: bold;
                margin-bottom: 0.2rem;
            '>
                {label}
            </h4>
            """,
            unsafe_allow_html=True,
        )

    def render(self):
        """
        Renderiza o campo de texto no Streamlit com o label oculto (apenas estilizado acima).

        Returns:
            str: Valor digitado no campo de texto.
        """
        return st.text_input(
            label=self.label,
            key=self.key,
            placeholder=self.placeholder,
            help=self.help_text,
            label_visibility="hidden",
        )


# Exemplo de uso para campo de temas
def TopicInput():
    """
    Campo de entrada para adicionar temas à análise de sentimento.
    Adiciona o tema à lista em st.session_state.topics se não for duplicado ou vazio.
    """
    if "topics" not in st.session_state:
        st.session_state.topics = []

    input_field = CustomInput(
        label="Adicionar Tema:",
        key="new_topic",
        placeholder="Ex: Bitcoin, eleições, esportes...",
        help_text="Digite o tema que deseja adicionar. Ex: Bitcoin, eleições, esportes, empresas, tendências etc.",
    )
    value = input_field.render()

    if st.button(label="Adicionar", key="add_topic_button"):
        if not value or value.strip() == "":
            st.warning("Digite um tema para adicionar.")
            return
        if value in st.session_state.topics:
            st.info("Tema já adicionado!")
            return
        st.session_state.topics.append(value)
        st.success(f"Tema '{value}' adicionado!")
        st.rerun()
