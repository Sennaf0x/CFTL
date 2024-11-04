import streamlit as st
from openai import OpenAI
import json

st.set_page_config(layout="wide")

col1, col2 = st.columns(2)

if "question" not in st.session_state:
    st.session_state.question = ""

if "gabarito" not in st.session_state:
    st.session_state.gabarito = ""

if "pergunta" not in st.session_state:
    st.session_state.pergunta = ""

if "opcao1" not in st.session_state:
    st.session_state.opcao1 = ""
if "opcao2" not in st.session_state:
    st.session_state.opcao2 = ""
if "opcao3" not in st.session_state:
    st.session_state.opcao3 = ""
if "opcao4" not in st.session_state:
    st.session_state.opcao4 = ""
if "opcao5" not in st.session_state:
    st.session_state.opcao5 = ""

if "explicacao" not in st.session_state:
    st.session_state.explicacao = ""
    


assunto = ""

client = OpenAI()
def ask_openai(assunto):
    if assunto == "":
        return "Como posso ajudá-lo?"
    try:
        print("Iniciando chat")
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": ('''
                                Você é um avaliador  que fará a prova de  exame do CTFL 4.0
                                '''
                                )
                },
                {
                    "role": "user",
                    "content": ('''
                                Elabore uma pergunta com 5 opções de resposta somente uma sendo verdadeira, conforme o texto do assunto enviado seguindo o seguinte exemplo:
                                exemplo de resposta = {
                                                       "pergunta": "Pergunta elaborada pelo chat de acordo com o assunto enviado", 
                                                       "opcao1": "1° opção gerada",
                                                       "opcao2": "2° opção gerada",
                                                       "opcao3": "3° opção gerada",
                                                       "opcao4": "4° opção gerada",
                                                       "opcao5": "5° opção gerada",
                                                       "gabarito": "Reescreva a opção que está correta aqui"
                                                       "explicacao": "A explicação mais detalhada da sua resposta"
                                                      }
                                            
                                ''' + f'''assunto = {assunto}
                                ''')
                }
            ],

            temperature=1,
            max_tokens=4000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0

            )
        
        answer = completion.choices[0].message.content
        answer = answer.replace("`","").replace("json","") 
        print(f"answer: {answer}")
        resposta_json = json.loads(answer)
        print(f"resposta_json: {resposta_json}")
        return resposta_json
    
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return None

    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None
    
with col1:
    st.write("Gerador de perguntas")
    with st.form("assunto"):
        assunto = st.text_input("Insira aqui o assunto")
        gerar = st.form_submit_button("Gerar")
    if gerar:
        questionario = ask_openai(assunto)
        st.session_state.pergunta = json.dumps(questionario['pergunta'], ensure_ascii=False)
        st.session_state.opcao1 = json.dumps(questionario['opcao1'], ensure_ascii=False)
        st.session_state.opcao2 = json.dumps(questionario['opcao2'], ensure_ascii=False)
        st.session_state.opcao3 = json.dumps(questionario['opcao3'], ensure_ascii=False)
        st.session_state.opcao4 = json.dumps(questionario['opcao4'], ensure_ascii=False)
        st.session_state.opcao5 = json.dumps(questionario['opcao5'], ensure_ascii=False)
        st.session_state.gabarito = json.dumps(questionario['gabarito'], ensure_ascii=False)
        st.session_state.explicacao = json.dumps(questionario['explicacao'], ensure_ascii=False)
        
        print(f'''pergunta: {st.session_state.pergunta}''')
        print(f'''resposta: {st.session_state.opcao1}''')
        print(f'''resposta: {st.session_state.opcao2}''')
        print(f'''resposta: {st.session_state.opcao3}''')
        print(f'''resposta: {st.session_state.opcao4}''')
        print(f'''resposta: {st.session_state.opcao5}''')
        print(f'''gabarito: {st.session_state.gabarito}''')
        print(f'''explicacao: {st.session_state.explicacao}''')
        
    
with col2:
    st.write(st.session_state.pergunta)    

    with st.form("Ask"):
        
        question = st.radio(
            "Selecione a opção certa para a pergunta acima",
            [st.session_state.opcao1,st.session_state.opcao2,st.session_state.opcao3,st.session_state.opcao4,st.session_state.opcao5]
        )

        print(f'''Você escolheu: {question}''')
        
        st.session_state.question = question
        
        responder = st.form_submit_button("Responder")
        if responder:
            if st.session_state.question == st.session_state.gabarito:
                st.success("Você acertou!")
                st.write("Explicação")
                st.success(f'''{st.session_state.explicacao}''')
            else:
                st.error("Você errou")