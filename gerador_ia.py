# gerador_ia.py

import streamlit as st
import google.generativeai as genai
from templates import criar_prompt

def configurar_ia():
    """Configura a API do Google com a chave fornecida pelos segredos do Streamlit."""
    try:
        api_key = st.secrets["API_KEY"]
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"Erro ao configurar a API: {e}")
        return False

def gerar_noticia_com_ia(respostas):
    """Envia as respostas para a IA e retorna o texto gerado."""
    if "API_KEY" not in st.secrets or not st.secrets["API_KEY"]:
        return {
            "erro": "API Key não configurada. Por favor, adicione-a nos segredos (Secrets) do seu app no Streamlit Cloud."
        }

    if not configurar_ia():
        return {
            "erro": "Falha ao configurar a API do Google. Verifique sua chave e conexão."
        }
        
    try:
        # --- AQUI ESTÁ A CORREÇÃO ---
        # Trocamos 'gemini-pro' por 'gemini-1.5-flash-latest'
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = criar_prompt(respostas)
        
        response = model.generate_content(prompt)
        
        # Processa a resposta para separar as partes
        texto_completo = response.text
        partes = texto_completo.split('---')
        
        titulo = partes[0].replace('TITULO:', '').strip()
        noticia = partes[1].replace('NOTICIA', '').strip()
        entendendo = partes[2].replace('ENTENDENDO', '').strip()
        glossario = partes[3].replace('GLOSSARIO', '').strip()
        
        return {
            "titulo": titulo,
            "noticia": noticia,
            "entendendo": entendendo,
            "glossario": glossario
        }
    except Exception as e:
        print(f"Ocorreu um erro durante a geração do texto: {e}")
        return {
            "erro": f"Não foi possível gerar a notícia. Tente novamente.\nDetalhe: {e}"
        }
