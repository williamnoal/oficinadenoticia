# interface.py
import customtkinter as ctk
from questionario import PERGUNTAS
from gerador_ia import gerar_noticia_com_ia
import threading

# --- Configurações de Aparência ---
ctk.set_appearance_mode("System")  # Pode ser "Light", "Dark"
ctk.set_default_color_theme("blue")  # Tema de cores

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Oficina de Notícias - Ferramenta de Produção Textual")
        self.geometry("800x600")
        
        self.perguntas = PERGUNTAS
        self.respostas = {}
        self.pergunta_atual = 0

        self.criar_tela_inicial()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def criar_tela_inicial(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        label = ctk.CTkLabel(frame, text="Oficina de Notícias", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=40)

        texto_intro = "Vamos criar uma notícia incrível juntos! Responda às perguntas a seguir para construir sua história passo a passo."
        label_intro = ctk.CTkLabel(frame, text=texto_intro, font=ctk.CTkFont(size=14), wraplength=400)
        label_intro.pack(pady=20, padx=20)

        botao_iniciar = ctk.CTkButton(frame, text="Começar Entrevista", command=self.mostrar_pergunta)
        botao_iniciar.pack(pady=40, ipady=10)

    def mostrar_pergunta(self):
        self.limpar_tela()

        if self.pergunta_atual < len(self.perguntas):
            pergunta = self.perguntas[self.pergunta_atual]

            frame = ctk.CTkFrame(self)
            frame.pack(pady=20, padx=60, fill="both", expand=True)
            
            # Barra de Progresso
            progresso = self.pergunta_atual / len(self.perguntas)
            progress_bar = ctk.CTkProgressBar(frame)
            progress_bar.set(progresso)
            progress_bar.pack(pady=10, padx=20, fill="x")

            label_pergunta = ctk.CTkLabel(frame, text=pergunta["texto"], font=ctk.CTkFont(size=18, weight="bold"), wraplength=600)
            label_pergunta.pack(pady=(40, 10))

            label_exemplo = ctk.CTkLabel(frame, text=pergunta["exemplo"], font=ctk.CTkFont(size=12, slant="italic"), text_color="gray")
            label_exemplo.pack(pady=(0, 20))

            entry = ctk.CTkTextbox(frame, height=100, font=ctk.CTkFont(size=14))
            entry.pack(pady=10, padx=40, fill="x")

            botao_proximo = ctk.CTkButton(frame, text="Próxima Pergunta", command=lambda: self.salvar_e_proximo(entry, pergunta["chave"]))
            botao_proximo.pack(pady=20, ipady=5)
        else:
            self.mostrar_tela_carregando()
            # Usar threading para não travar a interface durante a chamada da API
            threading.Thread(target=self.finalizar_e_gerar).start()

    def salvar_e_proximo(self, entry, chave):
        resposta = entry.get("1.0", "end-1c").strip()
        if resposta: # Só avança se o aluno escreveu algo
            self.respostas[chave] = resposta
            self.pergunta_atual += 1
            self.mostrar_pergunta()

    def mostrar_tela_carregando(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self)
        frame.pack(pady=20, padx=60, fill="both", expand=True)
        label = ctk.CTkLabel(frame, text="Gerando sua notícia com a ajuda da IA...\nAguarde um momento!", font=ctk.CTkFont(size=18))
        label.pack(pady=100, padx=20)
        progress_bar = ctk.CTkProgressBar(frame, mode="indeterminate")
        progress_bar.pack(pady=10, padx=50, fill="x")
        progress_bar.start()

    def finalizar_e_gerar(self):
        resultado = gerar_noticia_com_ia(self.respostas)
        # Garante que a atualização da UI seja feita na thread principal
        self.after(0, self.mostrar_resultado, resultado)

    def mostrar_resultado(self, resultado):
        self.limpar_tela()

        if "erro" in resultado:
            frame = ctk.CTkFrame(self)
            frame.pack(pady=20, padx=60, fill="both", expand=True)
            label_erro = ctk.CTkLabel(frame, text=f"Ocorreu um erro:\n{resultado['erro']}", font=ctk.CTkFont(size=16), text_color="red")
            label_erro.pack(pady=50, padx=20)
            botao_voltar = ctk.CTkButton(frame, text="Tentar Novamente", command=self.criar_tela_inicial)
            botao_voltar.pack(pady=20)
            return

        # Abas para organizar o conteúdo
        tab_view = ctk.CTkTabview(self, width=700)
        tab_view.pack(pady=20, padx=20, fill="both", expand=True)

        tab_view.add("Sua Notícia")
        tab_view.add("Entendendo a Notícia")
        tab_view.add("Glossário")

        # Aba 1: Notícia
        frame_noticia = tab_view.tab("Sua Notícia")
        label_titulo = ctk.CTkLabel(frame_noticia, text=resultado["titulo"], font=ctk.CTkFont(size=22, weight="bold"), wraplength=650)
        label_titulo.pack(pady=20, padx=20)
        
        texto_noticia = ctk.CTkTextbox(frame_noticia, font=ctk.CTkFont(size=14))
        texto_noticia.insert("1.0", resultado["noticia"])
        texto_noticia.configure(state="disabled") # Bloqueia edição
        texto_noticia.pack(pady=10, padx=20, fill="both", expand=True)

        # Aba 2: Entendendo
        frame_entendendo = tab_view.tab("Entendendo a Notícia")
        texto_entendendo = ctk.CTkTextbox(frame_entendendo, font=ctk.CTkFont(size=14))
        texto_entendendo.insert("1.0", resultado["entendendo"])
        texto_entendendo.configure(state="disabled")
        texto_entendendo.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Aba 3: Glossário
        frame_glossario = tab_view.tab("Glossário")
        texto_glossario = ctk.CTkTextbox(frame_glossario, font=ctk.CTkFont(size=14))
        texto_glossario.insert("1.0", resultado["glossario"])
        texto_glossario.configure(state="disabled")
        texto_glossario.pack(pady=20, padx=20, fill="both", expand=True)

        botao_recomecar = ctk.CTkButton(self, text="Criar Outra Notícia", command=self.reiniciar)
        botao_recomecar.pack(pady=10)

    def reiniciar(self):
        self.respostas = {}
        self.pergunta_atual = 0
        self.criar_tela_inicial()