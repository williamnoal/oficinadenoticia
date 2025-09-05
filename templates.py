# templates.py

def criar_prompt(respostas):
    """Monta o prompt final para a API com base nas respostas do aluno."""
    
    respostas_formatadas = "\n".join([f"- {chave}: {valor}" for chave, valor in respostas.items()])

    prompt = f"""
    Você é um assistente de redação para um jornal escolar. Sua tarefa é transformar as respostas de um aluno do 6º ano em uma notícia.

    **Instruções:**
    1.  Crie uma notícia clara e bem estruturada em exatamente dois parágrafos. A linguagem deve ser envolvente e adequada para leitores de 10 a 12 anos.
    2.  O primeiro parágrafo deve ser o lide, respondendo a O Quê, Quem, Quando, Onde, Como e Por Quê.
    3.  O segundo parágrafo deve ser o corpo, usando as informações adicionais para dar mais detalhes.
    4.  Crie um título curto e chamativo para a notícia.
    5.  Após a notícia, crie uma seção chamada 'Entendendo a Notícia', explicando de forma simples o que é 'Título', 'Lide' e 'Corpo do Texto'.
    6.  Por fim, crie uma seção chamada 'Glossário', identificando 3 palavras no texto que podem ser novas e forneça uma definição simples para cada.
    7.  Formate sua resposta usando marcações simples para separação, como:
        TITULO: [Seu título aqui]
        ---NOTICIA---
        [Parágrafo 1]
        [Parágrafo 2]
        ---ENTENDENDO---
        [Sua explicação aqui]
        ---GLOSSARIO---
        [Seu glossário aqui]

    **Respostas do Aluno:**
    {respostas_formatadas}
    """
    return prompt