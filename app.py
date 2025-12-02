import streamlit as st
from transformers import pipeline
import torch

st.set_page_config(
    page_title='AI Text Generator',
    page_icon='\u2728',
    layout='wide'
)

st.title('AI Text Generator with Sentiment Analysis')
st.markdown('An intelligent text generation tool that analyzes sentiment and produces sentiment-aligned content.')

st.sidebar.header('Configuration')
sentiment_choice = st.sidebar.radio(
    'Select Sentiment:',
    options=['Positive', 'Negative', 'Neutral']
)

text_length = st.sidebar.select_slider(
    'Select Output Length:',
    options=['Short', 'Medium', 'Long'],
    value='Medium'
)

@st.cache_resource
def load_sentiment_model():
    return pipeline('sentiment-analysis')

@st.cache_resource
def load_text_gen_model():
    return pipeline('text-generation', model='gpt2')

sentiment_model = load_sentiment_model()
text_gen_model = load_text_gen_model()

col1, col2 = st.columns(2)

with col1:
    st.subheader('Input Prompt')
    user_prompt = st.text_area(
        'Enter your prompt:',
        height=150,
        placeholder='Type your prompt here...'
    )

with col2:
    st.subheader('Sentiment Analysis')
    if user_prompt:
        try:
            sentiment_result = sentiment_model(user_prompt[:512])[0]
            st.metric(
                'Detected Sentiment',
                sentiment_result['label'],
                f"{sentiment_result['score']:.2%} confidence"
            )
        except:
            st.info('Analyzing...')
    else:
        st.info('Enter a prompt to analyze sentiment')

if st.button('Generate Text', type='primary'):
    if not user_prompt:
        st.error('Please enter a prompt')
    else:
        with st.spinner('Generating text...'):
            try:
                sentiment_prefix = {
                    'Positive': 'This is wonderful and amazing. ',
                    'Negative': 'This is unfortunate and sad. ',
                    'Neutral': 'Here is information: '
                }
                
                length_map = {'Short': 50, 'Medium': 100, 'Long': 150}
                
                full_prompt = sentiment_prefix[sentiment_choice] + user_prompt
                
                generated = text_gen_model(
                    full_prompt,
                    max_length=length_map[text_length],
                    num_return_sequences=1
                )
                
                st.subheader('Generated Text')
                st.text_area(
                    'Output:',
                    value=generated[0]['generated_text'],
                    height=200,
                    disabled=True
                )
                
                st.success('Text generated successfully!')
                
            except Exception as e:
                st.error(f'Error: {str(e)}')

with st.expander('How it works'):
    st.markdown('1. Sentiment Analysis using Transformers\n2. Text Generation with GPT-2\n3. Output customization')

st.sidebar.markdown('---')
st.sidebar.info('Tech Stack: Streamlit, Hugging Face Transformers, PyTorch, GPT-2')
