import streamlit as st
from openai import OpenAI
import json

st.set_page_config(layout="wide")

st.markdown('''
            <style>
                .e1f1d6gn3{
                    box-shadow: rgba(207,1,59, 0.1) 0px 4px 12px;
                    padding: 10px;
                    border-radius: 10px;
                }
                
                .stSlider{
                    border: solid rgba(207,1,59, 0.6);
                    padding: 0 10px;
                    margin-top: 10px;
                    border-radius: 10px;
                }
                
                stMainBlockContainer{
                    background-color: #CFD8E3;
                }
                
                .cor{
                    background-color: #2B3B4B;
                    color: #CFD8E3;
                    text-align: center;
                    border-radius: 10px;
                    margin: 1px;   
                }
                
                .conteudo{
                    font-size: 15px;
                    font-weight: bold;
                }
                
                .pergunta{
                    padding: 10px;
                    background-color: #CFD8E3;
                    border-radius: 10px;
                    font-weight: bold;
                    text-align: justify;
                    font-size: 17px;
                    margin: 5px 0 ;
                }
                
                .pergunta2{
                    padding: 10px;
                    background-color: #CFD8E3;
                    border-radius: 10px;
                    font-weight: bold;
                    text-align: center;
                    font-size: 17px;
                    margin: 5px 0 ;
                }
                
                .ef3psqc11{
                    background-color: rgba(207,1,59);
                    color: white;
                    font-weight: bold;
                    font-size: 15px;
                }
                
                .ef3psqc11:hover{
                    color: white;
                    background-color: #2B3B4B;
                }
                
                .e1f1d6gn4{
                    padding: 5px;
                }
                
                
            </style>
            ''', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2,3,2])

if "question" not in st.session_state:
    st.session_state.question = ""

if "tamanho" not in st.session_state:
    st.session_state.tamanho = ""

if "questionario" not in st.session_state:
    st.session_state.questionario = ""

if "numero" not in st.session_state:
    st.session_state.numero = 1

if "imagem" not in st.session_state:
    st.session_state.imagem = ""

if "descricao" not in st.session_state:
    st.session_state.descricao = ""

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "conteudo" not in st.session_state:
    st.session_state.conteudo = "#### Carregue o conteúdo no campo de gerar perguntas"

if "gabarito" not in st.session_state:
    st.session_state.gabarito = ""

if "pergunta" not in st.session_state:
    st.session_state.pergunta = "Insira um assunto no sobre o CTFL para que a questão seja gerada..."

if "opcao1" not in st.session_state:
    st.session_state.opcao1 = "Opção 1"
if "opcao2" not in st.session_state:
    st.session_state.opcao2 = "Opção 2"
if "opcao3" not in st.session_state:
    st.session_state.opcao3 = "Opção 3"
if "opcao4" not in st.session_state:
    st.session_state.opcao4 = "Opção 4"
if "opcao5" not in st.session_state:
    st.session_state.opcao5 = "Opção 5"

if "explicacao" not in st.session_state:
    st.session_state.explicacao = ""
    

assunto = ""

client = OpenAI()

def ask_openai(assunto, prompt):
    if assunto == "":
        return "Como posso ajudá-lo?"
    try:
        print("Iniciando chat")
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": ('''
                                Você é um analista da qualidade de software senior e está encarregado de formular perguntas para estudantes que irão fazer a prova do CTFL 4.0
                                '''
                                )
                },
                {
                    "role": "user",
                    "content": (f"{prompt}")
                }
            ],

            temperature=1,
            max_tokens=5000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0

            )
        
        answer = completion.choices[0].message.content
        answer = answer.replace("`","").replace("json","") 
        print(f"answer: {answer}")
        return answer
    
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return None

    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

def gerar_imagem(descricao):    
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=f'''{descricao}''',
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        return image_url
    
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return None

    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None
    
    
with col1:
    st.write('''
             <h2 class="cor">Gerador</h2>
             ''',unsafe_allow_html=True)
    with st.form("assunto"):
        assunto = st.text_area("Insira aqui o assunto")
        gerar = st.form_submit_button("Gerar pergunta",use_container_width=True)
        gerar_conteudo = st.form_submit_button("Gerar conteúdo",use_container_width=True)
        
        nivel = st.radio("Selecione o nível",
                         ["Para estudo", "Complexas do simulado CTFL"]
                        )
        
        if assunto == "" and gerar:
            st.warning("Adicione o assunto a ser abordado")
        elif assunto == "" and gerar_conteudo:
            st.warning("Adicione o assunto a ser abordado")
        else:    
            if gerar:
            
                prompt =f'''
                            Elabore 2 perguntas {nivel} de múltipla escolha ou verdadeiro e falso ou de correlação de maneira aleatória e não repetindo o assunto, randomizando as respostas corretas entre as questões, para que possa avaliar minha compreensão do texto
                        ''' + '''exemplo de resposta = {"pergunta1" : {
                                                    "pergunta": "Pergunta elaborada pelo chat de acordo com o assunto enviado", 
                                                    "opcao1": "1° opção gerada",
                                                    "opcao2": "2° opção gerada",
                                                    "opcao3": "3° opção gerada",
                                                    "opcao4": "4° opção gerada",
                                                    "opcao5": "5° opção gerada",
                                                    "gabarito": "Reescreva a opção que está correta aqui",
                                                    "explicacao": "A explicação mais detalhada da sua resposta"
                                                    }
                                                    }
                                                    
                        ''' + f'''assunto = {assunto}
                        '''
                resposta = ask_openai(assunto, prompt)
                
                st.session_state.questionario = json.loads(resposta)
                print(f"resposta_json: {st.session_state.questionario}")
                
            if gerar_conteudo:
                prompt =f'''
                        Quero aprender sobre o texto abaixo: 
                                {assunto}
                        Item 1 - Você é um programa que cria mindmaps utilizando o markmap e escreve somente texto em markdown
                        '''
                
                st.session_state.descricao = ask_openai(assunto, prompt)
                
                prompt =f'''
                        Quero aprender sobre o texto abaixo: 
                                {assunto}  
                        Item 2 - Identifique e compartilhe os 20% mais importantes aprendizados do texto fornecido inicialmente que me ajudarão a entender 80% dele.
                        Item 3 - Converta as principais lições deste tópico em histórias e metáforas envolventes para ajudar na minha memorização.
                        '''
                st.session_state.conteudo = ask_openai(assunto, prompt)
with col2:
    st.write('''<h2 class="cor">Conteúdo</h2>
             ''',unsafe_allow_html=True)
    if st.session_state.conteudo != "":
        st.markdown('''<div class="pergunta2"> O mindmap aparecerá no campo abaixo </div>''',unsafe_allow_html=True)
        html_markdown ='''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8" />
                        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                        <title>Markmap</title>
                        <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@0.16"></script>
                        <style>
                        svg.markmap {
                            width: 100%;
                            height: 100vh;
                            background-color: white;
                        }
                        
                        .node{
                            margin: 10px;
                        }
                        
                        #fullscreen-button {
                            position: absolute;
                            top: 10px;
                            right: 10px;
                            padding: 10px;
                            background-color: rgba(207,1,59);
                            color: white;
                            border: none;
                            cursor: pointer;
                            z-index: 1000;
                        }
                        
                        body, html {
                            margin: 0;
                            height: 100%;
                            overflow: hidden;
                        }

                        #mindmap-container {
                            height: calc(100% - 50px);
                            width: 100%;
                            transition: transform 0.3s ease;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                        }
                        
                        </style>
                    </head>
                    <body>
                        <button id="fullscreen-button">Tela cheia</button>
                        <div id="mindmap-container" class="markmap node">
                            <script type="text/template">
                                ---
                                markmap:
                                maxWidth: 400
                                colorFreezeLevel: 2
                                ---''' + f'''
                                {st.session_state.descricao}
                                ''' + '''
                                
                            </script>
                        </div>
                    <script>
                        const fullscreenButton = document.getElementById('fullscreen-button');
                        const mindmapContainer = document.getElementById('mindmap-container');
                        
                        function updateButtonLabel() {
                            if (document.fullscreenElement) {
                                fullscreenButton.textContent = 'Sair da Tela Cheia';
                            } else {
                                fullscreenButton.textContent = 'Tela Cheia';
                                mindmapContainer.style.transform = 'none';
                            }
                        }

                        fullscreenButton.addEventListener('click', () => {
                            const elem = document.documentElement;
                            if (!document.fullscreenElement) {
                                elem.requestFullscreen().catch(err => {
                                    alert(`Error attempting to enable fullscreen mode: ${err.message} (${err.name})`);
                                });
                            } else {
                                document.exitFullscreen();
                            }
                        });
                        
                        document.addEventListener('fullscreenchange', updateButtonLabel);
                    </script>
                    </body>
                    </html>
                    '''
        st.components.v1.html(html_markdown, height=300)
        #st.markdown(st.session_state.descricao)
        st.markdown(st.session_state.conteudo)
    else:        
        st.markdown('''<div class="pergunta2"> Mindmap </div>''',unsafe_allow_html=True)

with col3:
    
    st.write(f'''<h2 class="cor">Questões</h2>
             ''',unsafe_allow_html=True)
    st.session_state.numero = st.slider("Selecione uma questão",min_value=1, max_value=2, step=1)

    if st.session_state.questionario != "":
        st.session_state.tamanho = len(st.session_state.questionario[f'pergunta{st.session_state.numero}']) - 3
        print(f'Tamanho:{st.session_state.tamanho}')
                    
        st.session_state.pergunta = json.dumps(st.session_state.questionario[f'pergunta{st.session_state.numero}']['pergunta'], ensure_ascii=False)

        i = 0

        for i in range(1,st.session_state.tamanho+1):
            if i <= st.session_state.tamanho:
                st.session_state[f'opcao{i}'] = json.dumps(st.session_state.questionario[f'pergunta{st.session_state.numero}'][f'opcao{i}'], ensure_ascii=False)
            print(i)
        if i >= st.session_state.tamanho:
            print(i)
            for i in range(i+1,6):
                st.session_state[f'opcao{i}'] = "NA"

        st.session_state.gabarito = json.dumps(st.session_state.questionario[f'pergunta{st.session_state.numero}']['gabarito'], ensure_ascii=False)
        st.session_state.explicacao = json.dumps(st.session_state.questionario[f'pergunta{st.session_state.numero}']['explicacao'], ensure_ascii=False)

        print(f'''pergunta: {st.session_state.pergunta}''')
        print(f'''resposta: {st.session_state.opcao1}''')
        print(f'''resposta: {st.session_state.opcao2}''')
        print(f'''resposta: {st.session_state.opcao3}''')
        print(f'''resposta: {st.session_state.opcao4}''')
        print(f'''resposta: {st.session_state.opcao5}''')
        print(f'''gabarito: {st.session_state.gabarito}''')
        print(f'''explicacao: {st.session_state.explicacao}''')

    pergunta = st.session_state.pergunta
    pergunta = pergunta.replace('"','')
    opcao1 = st.session_state.opcao1 
    opcao1 = opcao1.replace('"','')
    opcao2 = st.session_state.opcao2 
    opcao2 = opcao2.replace('"','')
    opcao3 = st.session_state.opcao3 
    opcao3 = opcao3.replace('"','')
    opcao4 = st.session_state.opcao4 
    opcao4 = opcao4.replace('"','')
    opcao5 = st.session_state.opcao5 
    opcao5 = opcao5.replace('"','')
    gabarito = st.session_state.gabarito 
    gabarito = gabarito.replace('"','')
    explicacao = st.session_state.explicacao 
    explicacao = explicacao.replace('"','')
    st.write(f'''<div class="pergunta">{st.session_state.numero}° - {pergunta}</div>''', unsafe_allow_html=True)    

    with st.form("Ask"):

        question = st.radio(
            "Selecione a opção certa para a pergunta acima",
            [opcao1,opcao2, opcao3, opcao4, opcao5]
        )

        print(f'''Você escolheu: {question}''')
        st.session_state.question = question
        responder = st.form_submit_button("Responder", use_container_width=True)
        if responder:
            print(f'Número: {st.session_state.numero}')
            if question == gabarito:
                st.success("Você acertou!")
                st.write("Explicação")
                st.success(explicacao)
                
            else:
                print(f'Número: {st.session_state.numero}')
                st.error("Você errou")
                st.write("Opção certa")
                st.success(gabarito)
                st.write("Explicação")
                st.success(explicacao)
                
            
                