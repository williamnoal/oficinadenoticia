# app.py

import streamlit as st
from questionario import PERGUNTAS
from gerador_ia import gerar_noticia_com_ia
from gerador_pdf import criar_pdf_noticia # IMPORTAÇÃO NOVA

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
if 'pergunta_atual' not in st.session_state:
    st.session_state.pergunta_atual = 0
    st.session_state.respostas = {}
    st.session_state.noticia_gerada = False
    st.session_state.resultado = {}
    st.session_state.autor = "" # NOVO: Guarda o nome do autor

# --- Campo para o nome do autor ---
# Será mostrado apenas no início
if not st.session_state.respostas:
    st.session_state.autor = st.text_input("Qual o nome do(a) jornalista (seu nome)?")

# --- Lógica do Questionário ---
if not st.session_state.noticia_gerada:
    # Só mostra o questionário se o autor preencheu o nome
    if st.session_state.autor:
        total_perguntas = len(PERGUNTAS)
        indice_atual = st.session_state.pergunta_atual

        if indice_atual < total_perguntas:
            pergunta_obj = PERGUNTAS[indice_atual]

            st.subheader(f"Pergunta {indice_atual + 1} de {total_perguntas}")
            st.progress((indice_atual) / total_perguntas)

            st.markdown(f"### {pergunta_obj['texto']}")
            st.caption(pergunta_obj['exemplo'])

            resposta = st.text_area("Sua resposta:", key=f"resposta_{indice_atual}", height=120)

            if st.button("Próxima Pergunta"):
                if resposta:
                    st.session_state.respostas[pergunta_obj['chave']] = resposta
                    st.session_state.pergunta_atual += 1
                    st.rerun()
                else:
                    st.warning("Por favor, escreva uma resposta antes de continuar.")
        else:
            st.success("🎉 Entrevista concluída! Agora vamos gerar sua notícia.")
            if st.button("Criar minha Notícia!"):
                with st.spinner("A Mágica da IA está acontecendo... Aguarde!"):
                    resultado = gerar_noticia_com_ia(st.session_state.respostas)
                    st.session_state.resultado = resultado
                    st.session_state.noticia_gerada = True
                    st.rerun()
    else:
        st.info("Por favor, preencha seu nome para começar.")

# --- Exibição do Resultado Final ---
if st.session_state.noticia_gerada:
    resultado = st.session_state.resultado

    if "erro" in resultado:
        st.error(f"Ocorreu um erro: {resultado['erro']}")
    else:
        tab1, tab2, tab3 = st.tabs(["📰 Sua Notícia", "🧠 Entendendo a Notícia", "📚 Glossário"])

        with tab1:
            st.header(resultado["titulo"])
            st.write(f"_{'Por ' + st.session_state.autor if st.session_state.autor else ''}_")
            st.write(resultado["noticia"])

        with tab2:
            st.header("🧠 Entendendo a Notícia")
            st.write(resultado["entendendo"])

        with tab3:
            st.header("📚 Glossário")
            st.write(resultado["glossario"])
            
        # --- SEÇÃO DE DOWNLOAD DO PDF (NOVA) ---
        st.divider() # Adiciona uma linha divisória
        st.subheader("📰 Baixe sua Página de Jornal")
        
        # Gera o PDF em memória
        pdf_bytes = criar_pdf_noticia(
            titulo=resultado["titulo"],
            texto=resultado["noticia"],
            autor=st.session_state.autor
        )
        
        # Botão de Download
        st.download_button(
            label="Baixar PDF",
            data=pdf_bytes,
            file_name=f"noticia_{st.session_state.autor.replace(' ', '_').lower()}.pdf",
            mime="application/pdf"
        )
        st.caption("Seu arquivo PDF será baixado com a formatação de uma página de jornal.")


    if st.button("Criar Outra Notícia"):
        # Limpa o estado para recomeçar
        st.session_state.pergunta_atual = 0
        st.session_state.respostas = {}
        st.session_state.noticia_gerada = False
        st.session_state.resultado = {}
        st.session_state.autor = "" # Limpa o nome do autor também
        st.rerun()