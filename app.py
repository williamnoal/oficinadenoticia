# app.py

import streamlit as st
from questionario import PERGUNTAS
from gerador_ia import gerar_noticia_com_ia

# --- Configuração da Página ---
st.set_page_config(
    page_title="Oficina de Notícias",
    page_icon="✍️",
    layout="centered"
)

# --- Título e Introdução ---
st.title("✍️ Oficina de Notícias")
st.markdown("Vamos criar uma notícia incrível juntos! Responda às perguntas a seguir para construir sua história passo a passo.")

# --- Inicialização do Estado da Aplicação ---
# O st.session_state guarda informações enquanto o usuário interage com a página
if 'pergunta_atual' not in st.session_state:
    st.session_state.pergunta_atual = 0
    st.session_state.respostas = {}
    st.session_state.noticia_gerada = False
    st.session_state.resultado = {}

# --- Lógica do Questionário ---
if not st.session_state.noticia_gerada:
    total_perguntas = len(PERGUNTAS)
    indice_atual = st.session_state.pergunta_atual

    if indice_atual < total_perguntas:
        pergunta_obj = PERGUNTAS[indice_atual]

        st.subheader(f"Pergunta {indice_atual + 1} de {total_perguntas}")
        st.progress((indice_atual) / total_perguntas) # Barra de progresso

        st.markdown(f"### {pergunta_obj['texto']}")
        st.caption(pergunta_obj['exemplo'])

        # Usamos uma "key" única para o campo de texto de cada pergunta
        resposta = st.text_area("Sua resposta:", key=f"resposta_{indice_atual}", height=120)

        if st.button("Próxima Pergunta"):
            if resposta:
                st.session_state.respostas[pergunta_obj['chave']] = resposta
                st.session_state.pergunta_atual += 1
                st.rerun() # Recarrega a página para mostrar a próxima pergunta
            else:
                st.warning("Por favor, escreva uma resposta antes de continuar.")
    else:
        # Quando todas as perguntas forem respondidas
        st.success("🎉 Entrevista concluída! Agora vamos gerar sua notícia.")
        if st.button("Criar minha Notícia!"):
            with st.spinner("A Mágica da IA está acontecendo... Aguarde!"):
                resultado = gerar_noticia_com_ia(st.session_state.respostas)
                st.session_state.resultado = resultado
                st.session_state.noticia_gerada = True
                st.rerun()

# --- Exibição do Resultado Final ---
if st.session_state.noticia_gerada:
    resultado = st.session_state.resultado

    if "erro" in resultado:
        st.error(f"Ocorreu um erro: {resultado['erro']}")
    else:
        # Abas para organizar o conteúdo
        tab1, tab2, tab3 = st.tabs(["📰 Sua Notícia", "🧠 Entendendo a Notícia", "📚 Glossário"])

        with tab1:
            st.header(resultado["titulo"])
            st.write(resultado["noticia"])

        with tab2:
            st.header("🧠 Entendendo a Notícia")
            st.write(resultado["entendendo"])

        with tab3:
            st.header("📚 Glossário")
            st.write(resultado["glossario"])

    if st.button("Criar Outra Notícia"):
        # Limpa o estado para recomeçar
        st.session_state.pergunta_atual = 0
        st.session_state.respostas = {}
        st.session_state.noticia_gerada = False
        st.session_state.resultado = {}
        st.rerun()