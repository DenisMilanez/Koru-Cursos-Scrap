import requests
import os
import unicodedata
from youtube_transcript_api import YouTubeTranscriptApi
from tkinter import messagebox
import time

# variavel global para armazenar dados dos cursos
dados_cursos = {}

########## FUNÇÃO EXTRAIR VIDEO ##########
def extrair_video_url(data_video):
    '''
    recebe JSON do komposer e captura link do youtube
    '''
    komposer_data = data_video.get('komposer', {}).get('content', {}).get('children', {})

    for _, row in komposer_data.items():
        if row.get('type') == 'ROW':
            for _, column in row.get('children', {}).items():
                if column.get('type') == 'COLUMN':
                    for _, video in column.get('children', {}).items():
                        if video.get('type') == 'VIDEO' and video.get('host') == 'YOUTUBE':
                            return video.get('sourceURL')  # Retorna o primeiro vídeo encontrado

    return None  # Se não encontrar um vídeo válido

########## FUNÇÃO CAPTURAR DADOS CURSO ##########
def extrator_cursos(email, senha, atualizar_terminal):

    global dados_cursos
    dados_cursos.clear()

    atualizar_terminal(f'#' * 10 + ' Iniciando Scrap ' + '#' * 10)

    url_login = 'https://desenvolve-api.kflix.com.br/users/login'

    payload = {
        'email': email,
        'password': senha
    }

    # iniciando sessão
    session = requests.Session()
    response_login = session.post(url_login, json=payload)

    if response_login.status_code == 201:
        data_login = response_login.json() # dados login
        # capturando user_id e token
        user_id = data_login.get('id')
        token = data_login.get('token')

        headers = {
            'Authorization': f'Bearer {token}'
        }

        url_cursos = f'https://desenvolve-api.kflix.com.br/registration/trail/2/user/{user_id}'
        response_cursos = requests.get(url_cursos, headers=headers)

        if response_cursos.status_code == 200:
            data_cursos = response_cursos.json()
            # dic p/ armazenar dados
            # dados_cursos = {}
            # iterando os cursos
            for item in data_cursos:
                curso = item.get('course', {})
                # exclui curso destinado a avaliação
                if curso.get('approval_average') is None: 
                    curso_id = curso['id']
                    curso_nome = curso['name']

                    dados_cursos[curso_id] = {
                        'curso_nome': curso_nome,
                        'modulos': {}
                    }
            # percorre para preencher dados dos módulos
            for curso_id, dados_curso in dados_cursos.items():
                atualizar_terminal(f'Curso: {dados_curso["curso_nome"]} (ID: {curso_id})')

                url_modulos = f'https://desenvolve-api.kflix.com.br/course_module/course/{curso_id}?loadChildren=true&active=true&ignoreStatus=false'
                response_modulos = requests.get(url_modulos, headers=headers)

                if response_modulos.status_code == 200:
                    data_modulos = response_modulos.json()

                    # iterando módulos        
                    for modulo in data_modulos['data']:
                        atualizar_terminal(f"Processando: {modulo['name']} - {modulo['module_description']} (ID: {modulo['id']})") 

                        modulo_id = modulo['id']
                        modulo_nome = modulo['name']
                        modulo_descricao = modulo['module_description']

                        dados_cursos[curso_id]['modulos'][modulo_id] = {
                            'modulo_nome': modulo_nome,
                            'modulo_descricao': modulo_descricao,
                            'aulas': {}
                        }
                        # coletar dados das aulas
                        for aula in modulo.get('children', []):
                            atualizar_terminal(f"    - {aula['name']} (ID: {aula['id']})") 
                            aula_id = aula['id']
                            aula_nome = aula['name']

                            url_aula = f'https://desenvolve-api.kflix.com.br/course_module/{aula_id}/komposer'
                            response_video = requests.get(url_aula, headers=headers)
        
                            if response_video.status_code == 200:
                                data_video = response_video.json()

                                dados_cursos[curso_id]['modulos'][modulo_id]['aulas'][aula_id] = {
                                    'aula_nome': aula_nome,
                                    'video': extrair_video_url(data_video) # executa função pra obter url video youtube
                                }
                        atualizar_terminal('')
                else:
                    messagebox.showerror('ERRO', f'Erro ao acessar módulos do curso {curso_id}: {response_modulos.status_code}')
                    atualizar_terminal(f'Erro ao acessar módulos do curso {curso_id}: {response_modulos.status_code}')
        else:
            messagebox.showerror('ERRO', f'Erro ao acessar cursos: {response_cursos.status_code}')
            atualizar_terminal(f'Erro ao acessar cursos: {response_cursos.status_code}')

        # Pergunta se quer fazer download das legendas do youtube
        pergunta = messagebox.askyesno('Operação Finalizada', 'Fazer o download das legendas dos vídeos dos cursos?')
        if pergunta:
            salvar_arquivos_legendas(dados_cursos, atualizar_terminal)
        else:
            messagebox.showinfo('Finalizado', 'Operação encerrada.')
        
    else:
        messagebox.showerror('ERRO', f'Erro no login: {response_login.status_code}')
        atualizar_terminal(f'Erro no login: {response_login.status_code}')

    atualizar_terminal('#' * 10 + ' FIM ' + '#' * 10)
    session.close()


########## FUNÇÃO PEGAR LEGENDA DO YOUTUBE ##########
def legenda_youtube(youtube_url, atualizar_terminal):
    '''Obtém a legenda de um vídeo do YouTube com tentativa múltipla'''

    atualizar_terminal(f'youtube_url: {youtube_url}')
    # atualizar_terminal('youtube_url: >> print do {youtube_url} <<') # para não aparecer os links na exibição
    id_youtube = youtube_url.split('/')[-1].split('?')[0]  # extrai id video
    tentativas = 0 # tentativa pois ocorrem falhas com a api (pois ñ resolveu com timesleep)

    while tentativas < 5:
        try:
            t = YouTubeTranscriptApi.get_transcript(id_youtube, languages=['pt'])
            # captura 'texto' do dic e retorna como string
            legenda = '\n'.join([item['text'] for item in t])
            return legenda
        except Exception as e:
            tentativas += 1
            atualizar_terminal(f"Tentativa {tentativas}: Erro ao obter legenda - {e}")
            time.sleep(2)  # sleep para tentar novamente
    
    return None

########## FUNÇÃO PARA NORMALIZAR CARACTERES DOS NOMES P/ CRIAR ARQUIVOS OU PASTAS ##########
def normalizar_nome(nome):
    '''remove acentos, pontuações e caracteres para poderz criar nomes de arquivos/pastas'''
    # remove acentos
    nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    # remove pontuações e caracteres
    nome = ''.join(c for c in nome if c.isalnum() or c in (' ', '-'))  # mantem letras, numeros, espaco e '-'
    return nome


########## FUNÇÃO PARA CRIAR PASTAS E SALVAR ARQUIVOS ##########
def salvar_arquivos_legendas(dados_cursos, atualizar_terminal):
    # cria diretorio para base para os dados
    base_path = 'data'
    os.makedirs(base_path, exist_ok=True)

    # itera por todos os cursos
    for curso_id, curso_info in dados_cursos.items():
        curso_nome = normalizar_nome(curso_info['curso_nome']) # normaliza nome do curso
        curso_path = os.path.join(base_path, curso_nome)
        os.makedirs(curso_path, exist_ok=True)  # cria pasta do curso

        # percorre módulos
        for modulo_id, modulo_info in curso_info['modulos'].items():
            modulo_nome = normalizar_nome(modulo_info['modulo_nome']) # normaliza nome do módulo
            modulo_descricao = normalizar_nome(modulo_info.get('modulo_descricao', '')) # normaliza descrição do módulo

            # define nome do módulo (se possuir descricao) e cria diretorio
            modulo_folder_name = f"{modulo_nome} - {modulo_descricao}" if modulo_descricao else modulo_nome
            modulo_path = os.path.join(curso_path, modulo_folder_name)

            # obtem lista todas as aulas do módulo filtrando somente aquelas em que video não é None
            aulas_com_video = [aula for aula in modulo_info['aulas'].values() if aula['video']]

            if aulas_com_video:
                os.makedirs(modulo_path, exist_ok=True)  # true p/ ignorar erro caso a pasta módulo já exista

                # iterando as aulas
                for aula_id, aula_info in modulo_info['aulas'].items():
                    video_url = aula_info['video']
                    aula_nome = normalizar_nome(aula_info['aula_nome']) # normaliza nome da aula

                    if video_url:
                        legenda = legenda_youtube(video_url,atualizar_terminal) # tenta capturar legenda do video
                        if legenda:
                            arquivo_nome = f'{aula_nome}.txt'
                            arquivo_path = os.path.join(modulo_path, arquivo_nome)

                            # salvando legenda
                            with open(arquivo_path, 'w', encoding='utf-8') as file:
                                file.write(legenda)
                            
                            atualizar_terminal(f'Legenda salva: {arquivo_path}')
                    # time.sleep(1)
    messagebox.showinfo('Finalizado', 'arquivos salvos')