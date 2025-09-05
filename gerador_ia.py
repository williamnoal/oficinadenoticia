# gerador_ia.py
import google.generativeai as genai
from config import API_KEY
from templates import criar_prompt

def configurar_ia():
    """Configura a API do Google com a chave fornecida."""
    try:
        genai.configure(api_key=API_KEY)
        return True
    except Exception as e:
        print(f"Erro ao configurar a API: {e}")
        return False

def gerar_noticia_com_ia(respostas):
    """Envia as respostas para a IA e retorna o texto gerado."""
    if API_KEY == "SUA_CHAVE_DE_API_AQUI" or not API_KEY:
        return {
            "erro": "API Key não configurada. Por favor, edite o arquivo config.py."
        }

    if not configurar_ia():
        return {
            "erro": "Falha ao configurar a API do Google. Verifique sua chave e conexão."
        }
        
    try:
        model = genai.GenerativeModel('gemini-1.0-pro-latest')
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