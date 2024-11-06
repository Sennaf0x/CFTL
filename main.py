import streamlit as st
from openai import OpenAI
import json

st.set_page_config(layout="wide")

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
    st.session_state.conteudo = "Carregue o conteúdo "

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
    st.write("Gerador de perguntas")
    with st.form("assunto"):
        assunto = st.text_area("Insira aqui o assunto")
        gerar = st.form_submit_button("Gerar pergunta")
        gerar_conteudo = st.form_submit_button("Gerar conteudo")
        
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
                        Item 1 - Para isso, crie um mapa mental simples e legível, estilo mapa de dialogos e fonte arial, com os principais tópicos e conceitos do texto, utilizando uma cor que destaque o mapa mental criado quando o prompt for visualizado."
                        '''
                
                st.session_state.descricao = ask_openai(assunto, prompt)
                #descricao = st.session_state.descricao
                imagem_url = gerar_imagem(st.session_state.descricao)
                
                st.session_state.imagem = imagem_url
                
                prompt =f'''
                        Quero aprender sobre o texto abaixo: 
                                {assunto}  
                        Item 2 - Identifique e compartilhe os 20% mais importantes aprendizados do texto fornecido inicialmente que me ajudarão a entender 80% dele, utilizando uma analogia simples e cotidiana para um profissional de QA
                        Item 3 - Converta as principais lições deste tópico em histórias e metáforas envolventes para ajudar na minha memorização.
                        '''
                st.session_state.conteudo = ask_openai(assunto, prompt)
with col2:
    
    if st.session_state.imagem != "":
        st.write("Item I - Mapa mental")
        st.image(st.session_state.imagem)
        st.markdown(st.session_state.conteudo)
            
with col3:
    
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
    st.write(pergunta)    

    with st.form("Ask"):

        question = st.radio(
            "Selecione a opção certa para a pergunta acima",
            [opcao1,opcao2, opcao3, opcao4, opcao5]
        )

        print(f'''Você escolheu: {question}''')
        st.session_state.question = question
        responder = st.form_submit_button("Responder")
        if responder:
            print(f'Número: {st.session_state.numero}')
            if question == gabarito:
                st.success("Você acertou!")
                st.write("Explicação")
                st.success(explicacao)
                proximo = st.form_submit_button("Próximo")
                if proximo:
                    st.session_state.numero = st.session_state.numero + 1
                    print(f'Número: {st.session_state.numero}')
            else:
                print(f'Número: {st.session_state.numero}')
                st.error("Você errou")
                st.write("Opção certa")
                st.success(gabarito)
                st.write("Explicação")
                st.success(explicacao)
                proximo = st.form_submit_button("Próximo")
                if proximo:
                    st.session_state.numero = st.session_state.numero + 1
                    print(f'Número: {st.session_state.numero}')
                    st.rerun()
            
                