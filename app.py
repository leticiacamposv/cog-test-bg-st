import streamlit as st
import re
import openai
import os
import requests

# Page config
st.set_page_config(page_title='Cognitive test', page_icon=':eyeglasses:', layout='wide')

# Primary title on page
st.title('Cognitive test (GPT-4)')

# Sidebar
# st.sidebar.markdown("Selecione os parâmetros")
# max_length = st.sidebar.number_input('Max length', min_value=1, max_value=2048, value=500, step=1, help='Quantidade máxima de tokens ou "limite de palavras" da resposta. Quanto maior o número de tokens, mais demorada a resposta')
# temperature = st.sidebar.slider('Temperature', min_value=0.00, max_value=1.00, step=0.01, help='Controla a aleatoriedade do texto gerado. Quanto maior a temperatura, mais "criativo" e arriscad será o modelo. ')
# top_p = st.sidebar.slider('Top P', min_value=0.00, max_value=1.00, step=0.01, help='Grau de consideração de inclusão de palavras com probabilidades menores aparecerem no texto. Também controla a criatividade')
# freq_penalty = st.sidebar.slider('Frequency penalty', min_value=0.00, max_value=2.00, step=0.01, help='Grau de penalidade para repetição da mesma palavra em texto')
# best_of = st.sidebar.slider('Best of', min_value=1, max_value=20, step=1, help='Quantidade de respostas diferentes geradas. Use para efeito de variedade na resposta')
#end = st.sidebar.text_input('Stop sequence')
#Inject start text
#prob = st.sidebar.checkbox('Quantidade de tokens mais provaveis a ser :')

#Playground
prompt = st.text_area('Digite aqui o texto do(a) candidato(a)', height=200)
btn_submit = st.button('Enviar')

#Tratamento do prompt
# nlp = spacy.load("pt_core_news_lg")
# def lemmatizer(x):
#   lemma = ""
#   for token in nlp(x):
#       lemma += token.lemma_ + " "
#   return re.sub(r'\s([?.!"](?:\s|$))', r'\1', lemma)

# prompt = lemmatizer(prompt)
def remove_accent(x):
    accent_mapping = {
        'á': 'a',
        'ã': 'a',
        'à': 'a',
        'â': 'a',
        'é': 'e',
        'è': 'e',
        'ê': 'e',
        'í': 'i',
        'ì': 'i',
        'ó': 'o',
        'ò': 'o',
        'ô': 'o',
        'ú': 'u',
        'ù': 'u',
        'ç': 'c'
    }
    textclean = ''
    for word in x:
      for char in word:
          textclean += accent_mapping.get(char, char)
    return textclean

prompt = remove_accent(prompt)
#Modelo
os.environ["OPENAI_API_KEY"] = st.secrets["open_api_key"]
openai.api_key = os.getenv("OPENAI_API_KEY")
#model_id='davinci:ft-personal:sup-v2p1-lr0-1-epcs100-dv-2023-03-02-18-39-57'
#model_id = 'davinci:ft-be-growth:gc-model-v6-lr0-05-epcs30-nb-ft2-2023-03-31-13-59-13'
#default_model = "text-davinci-003"
#Predict


if btn_submit:
    headers = {
    #'Authorization': 'bearer ' + command1,
    'Content-Type': 'application/json',
    }

    json_data = {
        'prompts': [
            {
                'role': 'user',
                'content': prompt,
            },
        ],
    }
    with st.spinner('Aguarde...'):
        response = requests.post(
        'https://us-central1-data-test-01-301021.cloudfunctions.net/cog-gpt4',
        headers=headers,
        json=json_data)
    
    answer = ':computer: ' + str(response.content, 'utf-8')
  

    st.write(answer)
