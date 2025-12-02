# Install localtunnel to expose the Streamlit app
!npm install -g localtunnel

# Run the Streamlit app in the background and expose it using localtunnel
import subprocess
import threading
import time
import socket

def run_streamlit():
    # Use the path to the current Python script within the Colab environment
    # This assumes the Streamlit app code is saved as a Python file, or we can pipe it.
    # For simplicity, we'll assume the primary app logic is in the current cell's output
    # and save it to a temporary file.
    app_code = '''
import streamlit as st
from transformers import pipeline
import torch

st.set_page_config(
    page_title='AI Text Generator',
    page_icon='✨',
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
'''

    with open('app.py', 'w') as f:
        f.write(app_code)

    # Pick a free port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    port = s.getsockname()[1]
    s.close()

    # Run Streamlit in a separate process
    print(f"Streamlit app running on port: {port}")
    subprocess.run(['streamlit', 'run', 'app.py', '--server.port', str(port), '--server.headless', 'true'])

def run_localtunnel(port):
    print(f"Exposing port {port} with localtunnel...")
    # The localtunnel command needs to run in the background to not block the kernel
    lt_process = subprocess.Popen(['npx', 'localtunnel', '--port', str(port)], stdout=subprocess.PIPE, text=True)
    while True:
        line = lt_process.stdout.readline()
        if 'your url is:' in line:
            url = line.split('your url is: ')[1].strip()
            print(f"Your Streamlit app is live at: {url}")
            break
        time.sleep(1)

# Start Streamlit in a new thread
streamlit_thread = threading.Thread(target=run_streamlit)
streamlit_thread.start()

# Give Streamlit a moment to start and get a port
time.sleep(10) # Adjust as needed based on model loading times

# Assume Streamlit will run on 8501 by default if no port specified or if above logic fails
# Or, ideally, we'd capture the actual port from run_streamlit if it could communicate it back.
# For now, let's hardcode 8501 or use the logic to get a free port if needed.

# To make this robust, we need to know the port Streamlit is *actually* listening on.
# Since `run_streamlit` is in a thread and directly calls `subprocess.run`, it blocks the thread.
# A better way is to find a free port, then pass it to streamlit, and then pass it to localtunnel.

# Let's find a free port to use for both streamlit and localtunnel
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 0))
streamlit_port = s.getsockname()[1]
s.close()

def run_streamlit_with_port(port):
    print(f"Streamlit app starting on port: {port}")
    # Save the current Streamlit app content to a file to run it
    app_content = """
import streamlit as st
from transformers import pipeline
import torch

st.set_page_config(
    page_title='AI Text Generator',
    page_icon='✨',
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

    """
    with open("streamlit_app.py", "w") as f:
        f.write(app_content)
    subprocess.Popen(["streamlit", "run", "streamlit_app.py", "--server.port", str(port), "--server.headless", "true"])

streamlit_thread = threading.Thread(target=run_streamlit_with_port, args=(streamlit_port,))
streamlit_thread.start()

# Wait for Streamlit to start up
time.sleep(5) # Give it a few seconds to initialize

# Start localtunnel in the main thread (or another thread if needed)
localtunnel_thread = threading.Thread(target=run_localtunnel, args=(streamlit_port,))
localtunnel_thread.start()
