import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import pyttsx3
import SessionState

available_models = {
    "Google Pegasus": "google/pegasus-xsum",
    "Facebook Bart" :  "facebook/bart-large-cnn",    
}

history = []
summary_read = ''
engine = pyttsx3.init()

if 'history' not in st.session_state:
    st.session_state['history'] = []

def summarize_text(text, max_length, model, model_name ):
    global summary_read  

    summarizer = pipeline('summarization', model=model)
    
    summary = summarizer(text, max_length=max_length+10, min_length=max_length, do_sample=False)
    
    st.write(summary[0]['summary_text'])
    print(summary[0]['summary_text'])
    summary_read = summary[0]['summary_text']  

    st.session_state['history'].append({
        'original text' : text,
        'summary': summary[0]['summary_text'],
        'model': model_name,
        'word_limit': max_length-10,
        
    })


st.title('Text Summarizer')
text = st.text_area("Enter Text:", value='', height=None, max_chars=None, key=None)
max_length = st.slider("Max Length:", min_value=10, max_value=100, step=1)
model_name = st.selectbox("Choose a model:", list(available_models.keys()))
model_choice = available_models[model_name] 

col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
with col1:
    st.write(" ")  
with col2:
    st.write(" ")  
with col3:
    like = st.button('👍')
with col4:
    dislike = st.button('👎')
with col5:
    st.write(" ")  

if st.button('Summarize'):
    if text:
        max_length = max_length+10
        print(max_length)
        summarize_text(text, max_length, model_choice, model_name)
    else:
        st.write("Please enter text for summarization.")

for i, item in enumerate(st.session_state['history']):
    st.sidebar.markdown(f'{i+1}.')
    for key, value in item.items():
        st.sidebar.markdown(f'{key}: {value}')