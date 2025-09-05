# gerador_pdf.py

from fpdf import FPDF
from datetime import datetime

# Definindo constantes para o layout
LARGURA_PAGINA = 210  # A4 width in mm
ALTURA_PAGINA = 297   # A4 height in mm
MARGEM = 15

class PDF(FPDF):
    def header(self):
        # Adiciona as fontes com os nomes corretos (com tamanho óptico)
        # --- LINHAS ATUALIZADAS ---
        self.add_font('Merriweather', 'B', 'fonts/Merriweather_24pt-Bold.ttf')
        self.add_font('Merriweather', '', 'fonts/Merriweather_24pt-Regular.ttf')
        
        # Título do Jornal (Masthead)
        self.set_font('Merriweather', 'B', 24)
        self.cell(0, 10, 'Oficina de Notícias Digital', border=0, ln=1, align='C')
        
        # Data e Edição
        data_hoje = datetime.now().strftime('%d de %B de %Y')
        self.set_font('Merriweather', '', 10)
        self.cell(0, 10, f'Edição de {data_hoje}', border=0, ln=1, align='C')
        
        # Linha horizontal separadora
        self.line(MARGEM, self.get_y() + 5, LARGURA_PAGINA - MARGEM, self.get_y() + 5)
        
        # Pula um espaço para o conteúdo
        self.ln(15)

    def footer(self):
        # Rodapé com o número da página
        self.set_y(-15)
        self.set_font('Lora', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def criar_pdf_noticia(titulo, texto, autor):
    """
    Gera um PDF formatado como uma página de jornal.
    Retorna o PDF como bytes.
    """
    pdf = PDF()
    pdf.add_page()
    
    # Adiciona as fontes de corpo estáticas (Lora não tem tamanho óptico)
    pdf.add_font('Lora', '', 'fonts/Lora-Regular.ttf')
    pdf.add_font('Lora', 'I', 'fonts/Lora-Italic.ttf')

    # --- Título da Notícia (Headline) ---
    pdf.set_font('Merriweather', 'B', 20)
    pdf.multi_cell(0, 10, titulo, 0, 'L')
    pdf.ln(2)

    # --- Autor da Notícia (Byline) ---
    pdf.set_font('Lora', 'I', 11)
    pdf.cell(0, 8, f'Por {autor}', 0, 1, 'L')
    pdf.ln(8)

    # --- Corpo do Texto da Notícia ---
    pdf.set_font('Lora', '', 12)
    pdf.multi_cell(0, 7, texto, 0, 'J')
    
    # Gera o PDF em memória e retorna como bytes
    return pdf.output(dest='S').encode('latin-1')
