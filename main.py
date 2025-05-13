import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from contextlib import redirect_stdout
import io
from extrator import extrator_cursos, salvar_arquivos_legendas, dados_cursos

# janela principal
root = tk.Tk()
root.title('Scrap legendas Youtube | Programa Desenvolve | Grupo Boticario | KORU |')
root.geometry('750x400')

# frame principal
frame_principal = tk.Frame(root)
frame_principal.grid(row=0, column=0, sticky='nsew')

# frames para esquerda (login) e direita (terminal)
frame_esquerdo = tk.Frame(frame_principal)
frame_esquerdo.grid(row=0, column=0, padx=10, pady=10, sticky='n')

frame_direito = tk.Frame(frame_principal)
frame_direito.grid(row=0, column=1, padx=10, pady=5, sticky='nsew')

##################### FUNÇÕES #####################

# inicia a extração, função executada ao clicar no botão "iniciar"
def iniciar_extracao():
    email = email_entry.get()
    senha = password_entry.get()

    if not email or not senha:
        messagebox.showwarning('Aviso', 'Preencha o e-mail e senha!')
        return
    
    # criar thread para executar função sem travar gui
    thread_extracao = threading.Thread(target=executar_extracao, args=(email, senha))
    thread_extracao.start()

# uso na função iniciar_extracao(), recebe email/senha, atualiza terminais com os print() da extrator_curso()
# chama verificar_dados_cursos() no fim para tornar o btn download legendas cliclável ou não
def executar_extracao(email, senha):
    buffer = io.StringIO()
    with redirect_stdout(buffer):  # Redireciona saída do print() para o buffer
        extrator_cursos(email, senha, atualizar_terminal)

    # Atualiza o terminal do Tkinter conforme os prints ocorrem
    terminal_output.insert(tk.END, buffer.getvalue())
    terminal_output.see(tk.END)  # Auto-scroll para última linha

    verificar_dados_cursos()

# substitui o print no extrator.py para capturar mensagem e exibir no widget do terminal
def atualizar_terminal(mensagem):
    terminal_output.insert(tk.END, mensagem + '\n')
    terminal_output.see(tk.END)
    terminal_output.update_idletasks()

# executa em thread função para download de legendas do extrator.py iniciada por btn_download_legendas
def iniciar_download_legendas():
    thread_download = threading.Thread(target=salvar_arquivos_legendas, args=(dados_cursos, atualizar_terminal))
    thread_download.start()

# Função para ativar/desativar o botão com base na variável global `dados_cursos`
def verificar_dados_cursos():
    if len(dados_cursos) > 0:  # Se há cursos na variável global
        btn_download_legendas.config(state='normal')  # Ativa o botão
    else:
        btn_download_legendas.config(state='disabled')  # Mantém desativado

##################### FRAME ESQUERDO #####################

# texto informativo
tk.Label(frame_esquerdo, text='https://desenvolve.kflix.com.br/\nFaça o login com seu email cadastrado para acessar a API do Programa Desenvolve, capturar os cursos, módulos e aulas disponíveis,\
 e fazer o download das legendas das videoaulas do YouTube.', 
         font=('Arial', 10), justify='left', wraplength=300).grid(row=0, column=0, columnspan=2, pady=(0, 5))

# campo email
tk.Label(frame_esquerdo, text='E-mail:', font=('Arial', 10)).grid(
    row=1, column=0, sticky='w', pady=5)
email_entry = tk.Entry(frame_esquerdo, font=('Arial', 10), width=30)
email_entry.grid(
    row=1, column=1, padx=5, pady=5)

# campo senha
tk.Label(frame_esquerdo, text='Senha:', font=('Arial', 10)).grid(
    row=2, column=0, sticky='w', pady=5)
password_entry = tk.Entry(frame_esquerdo, font=('Arial', 10), width=30, show='*')
password_entry.grid(
    row=2, column=1, padx=5, pady=5)

# botão para inicar extração
tk.Button(frame_esquerdo, text='Iniciar', font=('Arial', 10), command=iniciar_extracao).grid(
    row=3, columnspan=2, pady=10)

# botao download legendas (desativado no inicio)
btn_download_legendas = tk.Button(frame_esquerdo, text='Download Legendas', font=('Arial', 10),
                                  command=iniciar_download_legendas, state='disabled')
btn_download_legendas.grid(
    row=4, columnspan=2, pady=10)


##################### FRAME DIREITO #####################
# box terminal saida
tk.Label(frame_direito, text='Terminal', font=('Arial', 10)).grid(
    row=0, column=0, sticky='n')
terminal_output = scrolledtext.ScrolledText(frame_direito, font=('Arial', 10), wrap='word', height=20, width=60)
terminal_output.grid(row=1, column=0, sticky='nsew')



#####################
# atualiza a interface a ajusta largura (pra caber o terminal)
root.update_idletasks()
root.geometry(f'{root.winfo_reqwidth()}x400')

# executando tkinter
root.mainloop()