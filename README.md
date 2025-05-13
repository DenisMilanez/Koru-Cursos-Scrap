# 🎓🐍📃 Extração de Dados de Cursos via API (Programa Desenvolve)

Este projeto/estudo em Python foi desenvolvido durante a Etapa 1 do [**Programa Desenvolve do Grupo Boticário**](https://desenvolve.grupoboticario.com.br/) + parceria com a Koru, uma iniciativa gratuita de formação e inclusão de talentos que possuem interesse na área Tech. Ele extrai automaticamente as informações dos cursos disponíveis para o usuário através de requisições HTTP para acessar os dados na API da plataforma, obtendo os links das videoaulas hospedadas no Youtube e coletando suas transcrições em `.txt`. Todo o processo utiliza uma interface gráfica simples construída com `Tkinter`.

---

## 💡💪 Motivação
Com a chegada da avaliação final da Etapa 1 do Programa Desenvolve (20 de maio de 2025), ter um material para ajudar na revisão dos conteúdos dos cursos é essencial.

Ao revisitar as aulas do curso de Inteligência Artificial do Programa Desenvolve, onde o professor frequentemente apresentava diversas aplicações e usos de diferentes IA's disponíveis no mercado, surgiu a ideia de criar uma ferramenta que automatizasse a obtenção das transcrições das videoaulas para, com o auxílio de IA, transformá-las em material didático estruturado, facilitando o estudo e revisão.

Além disso, este projeto serviu como uma oportunidade para aprimorar as habilidades em Python, explorando integrações úteis para o dia a dia com foco na automação e uso de tecnologia para facilitar processos.

---

## 📌 Objetivo
O objetivo principal do projeto é obter rapidamente as transcrições das videoaulas dos cursos do Programa Desenvolve para usá-las como base em ferramentas de Inteligência Artificial. A ideia é transformar essas aulas em material de estudo, como resumos, mapas mentais e/ou qualquer outro formato que facilite a revisão com ajuda da IA.
Com isso, o projeto:
- Automatiza o acesso aos dados dos cursos, módulos e aulas disponíveis ao usuário usando a API da plataforma;
- Extrai as legendas dos videos do Youtube e salva tudo em pastas organizadas e nomeadas de forma limpa;
- Deixa o conteúdo pronto para ser usado em IA's como ChatGPT, Claude, DeepSeek e etc.;
- Facilitar o estudo com um material mais acessível e personalizável;
- Prática em programação usando bibliotecas como `requests`, `tkinter`, `threading` e `youtube_transcript_api`.

---

## ⚙️ Tecnologias e Bibliotecas Utilizadas
- **Python 3.11.0** - Linguagem principal do projeto;
- [**requests**](https://pypi.org/project/requests/) - Requisições à API;
- [**tkinter** 8.6](https://docs.python.org/3/library/tkinter.html) - Interface gráfica;
- [**youtube-transcript-api** 1.0.3](https://pypi.org/project/youtube-transcript-api/1.0.3/) - Extração de legendas;
- [**unicodedata**](https://docs.python.org/3/library/unicodedata.html) - Normalizar nomes de arquivos e pastas;
- [**threading**](https://docs.python.org/3/library/threading.html) - Processamento assíncrono;
- [**time**](https://docs.python.org/3/library/time.html) - Intervalos de execução (evita erros entre transcrições);
- [**io**](https://docs.python.org/3/library/io.html) e [**contextlib.redirect_stdout**](https://docs.python.org/3/library/contextlib.html#contextlib.redirect_stdout)  - Redirecionar a saída do console e exibir logs dentro do widget terminal.

---

## 🧠 Aprendizados do Projeto
- Autenticação e consumo de endpoints da API utilizando `Session()` e `Requests` para coleta de dados;
- Extração de transcrições de videos do Youtube com a biblioteca `youtube_transcript_api`;
- Desenvolvimento de Interface Gráfica com `Tkinter` para entrada de credenciais e exibição do progresso no widget do Terminal;
- Uso de threads para implementação assíncrona dos processos de extração e download para evitar travamentos na interface;
- Normalização das strings com `unicodedata` para compatibilidade em nomes de arquivos e pastas;
- Criação dinâmica de arquivos `.txt` e pastas 

--- 

## 📁 Estrutura
```
├── data_exemplo/                   # Exemplo do armazenamento dos dados capturados
│   ├── Comece por aqui/            # Nome do Curso
│   │   └── Modulo 1/               # Módulo do Curso
│   |       ├── Abertura do Programa Desenvolve.txt     # Transcrição extraída
│   └── gerado_por_DeepSeek.html    # HTML da transcrição gerado na IA DeepSeek
│
├── extrator.py                     # Script p/ extrair os dados e capturar legendas
├── main.py                         # Interface gráfica (Tkinter)
└── README.md                       # Documentação
```

---

## 🚀 Como executar o Projeto

### 1. Clone o Repositório  
```sh
git clone https://github.com/DenisMilanez/Koru-Cursos-Scrap.git
cd Koru-Cursos-Scrap
```

### 2. Cria e ative o ambiente virtual (opcional)
```sh
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. Instale as dependências
```sh 
pip install tkinter youtube_transcript_api
```

### 4. Executando o código
```sh
python main.py
```

--- 

## 🔍 Como funciona

![demonstrativo](data_exemplo/video_gif.gif) 

#### 🔐 Autenticação
**É necessário ter uma conta válida participante do Programa Desenvolve.**
O login é feito via email e senha (é preciso que cadastro na plataforma tenha sido feito diretamente com essas credenciais).
⚠️Autenticação via Google/Microsoft/Linkedin não são compatíveis com este script.

#### 1. O Usuário informa seu email e senha via interface Tkinter e clica no botão `iniciar`:
- A função é executada em paralelo para não travar a interface;
#### 2. O script inicia uma Session() e faz uma requisição POST para o endpoint:
```
https://desenvolve-api.kflix.com.br/users/login
```
- Isso retorna o `user_id` e o `token` de acesso;
#### 3. Utilizando o `token`, o programa realiza requisições para diversos endpoints da API para obter dados relacionados ao curso e aulas;
- O progresso é printado no terminal do programa
#### 4. O progresso da coleta é mostrado em tempo real no terminal do programa. Os dados são estruturados e armazenando como dicionário em uma variável global;
#### 5. Encerrada a extração dos dados, uma janela do tkinter perguntará se o usuário deseja baixar as transcrições:
- Caso o usuário clique em não, o botão `Download Legendas` fica habilitado para baixar as transcrições;
#### 6. Os nomes dos cursos, módulos e aulas são normalizados com a biblioteca `unicodedata` para serem compatíveis com o sistema de arquivos/pastas;
#### 7. Para cada url do YouTube capturada relacionada as videoaulas, o programa extrai as transcrições em `.txt` utilizando a biblioteca `youtube_transcript_api`;
#### 8. Todos os arquivos são organizados em pastas com a estrutura → `data/<nome_do_curso>/<nome_do_módulo>/<nome_da_aula>.txt`.

---
# 🤖 IA utilizada
A IA escolhida para interpretar as transcrições dos videos foi a [DeepSeek](https://www.deepseek.com/). Ela foi utilizada para gerar um arquivo em `HTML`com um resumo claro e estruturado da aula.
O prompt enviado foi:
```sh
Você é um especialista em transformar transcrições de vídeo aulas em materiais didáticos claros e organizados. 

Objetivo: Quero que você leia um ou mais arquivos ".txt" contendo transcrições de aulas de um mesmo módulo de um curso, e gere o código de um único "arquivo HTML formatado" com:

1. Estrutura de tópicos por aula;
2. Um "índice clicável" no topo da página (com links para cada aula);
3. Emojis e uma apresentação visual leve e didática;
4. Separação clara por "nome do curso, módulo, número e tema da aula", e nome do professor (caso conste);
5. Nenhuma informação deve ser inventada: use "apenas o que está nas transcrições".

Exemplo de formatação:
📘 Curso: Nome do Curso 
🎯 Módulo 2: Titulo do Módulo (se houver) 
👨‍🏫 Professor: Nome do professor

Após isso, aguarde oenvio dos arquivos .txt acompanhados de informações como: nome do curso, nome do módulo, nome do professor (se não houver na transcrição)
```

O arquivo `HTML` criado pode ser visualizado aqui: [Ver HTML gerado](data_exemplo/gerado_por_DeepSeek.html).
