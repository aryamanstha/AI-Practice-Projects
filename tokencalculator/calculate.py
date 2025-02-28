import streamlit as st
from transformers import AutoTokenizer

st.title("Token Calculator")
models=[{"name":"Bert (Uncased)","model":"bert-base-uncased"},
        {"name":"Bert (Cased)","model":"bert-base-cased"},
        {"name":"GPT-2","model":"gpt2"},
        {"name":"Flan-T5","model":"google/flan-t5-small"},
        {"name":"GPT-4","model":"Xenova/gpt-4"},
        {"name":"StarCoder2","model":"bigcode/starcoder2-15b"},
        {"name":"Phi-3","model":"microsoft/Phi-3-mini-4k-instruct"},
        ]

def show_tokens(text, tokenizer_name):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    token_ids = tokenizer(text).input_ids
    token_count = len(token_ids)
    char_count = len(text)
    tokens=[]
    for idx, t in enumerate(token_ids):
        token = tokenizer.decode([t]) 
        tokens.append(token)
    return token_count, char_count, tokens
   
model_name = st.selectbox("Select Model", [model["name"] for model in models])

input_prompt=st.text_area("Enter Text")

if st.button("Tokenize"):
    if input_prompt:
        model = [model["model"] for model in models if model["name"]==model_name][0]
        token_count, char_count, tokens = show_tokens(input_prompt, model)
        st.write(f"Tokens: {token_count}, Characters: {char_count}")
        st.markdown(tokens)
    else:
        st.write("Please enter some text to tokenize.")



