# AI Text Generator with Sentiment Analysis

An intelligent text generation application that analyzes sentiment from user prompts and generates sentiment-aligned paragraphs/essays using advanced NLP models. Built with Streamlit frontend and Hugging Face Transformers.

## Features

- **Sentiment Analysis**: Detects sentiment (Positive, Negative, Neutral) using transformer models
- **Text Generation**: Generates coherent paragraphs matching detected sentiment
- **Interactive UI**: User-friendly Streamlit interface with real-time sentiment feedback
- **Customizable Output**: Adjustable text length (Short, Medium, Long)
- **Model Caching**: Optimized model loading for faster inference
- **Error Handling**: Robust error management and user feedback

## Tech Stack

- **Frontend**: Streamlit 1.28.1
- **ML Framework**: Hugging Face Transformers 4.34.0
- **Deep Learning**: PyTorch 2.0.1
- **Python**: 3.8+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Manipal24/ai-text-generator.git
cd ai-text-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## How It Works

1. User enters a prompt in the input field
2. System analyzes sentiment automatically
3. User selects desired sentiment (can override detected)
4. Adjust output length and creativity (temperature)
5. Click "Generate Text" button
6. App generates sentiment-aligned text output

## Project Structure

```
ai-text-generator/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── README.md             # Documentation
└── .gitignore           # Git ignore file
```

## Models Used

- **Sentiment Analysis**: distilbert-base-uncased-finetuned-sst-2-english
- **Text Generation**: GPT-2 (124M parameters)

## Challenges & Solutions

1. **Model Size**: Downloaded models are large; used caching to optimize
2. **Inference Speed**: Implemented Streamlit caching for faster subsequent runs
3. **Memory Management**: Used model optimization techniques for efficient resource usage

## Deployment

The application is ready for deployment on Streamlit Cloud:

```bash
streamlit run app.py
```

## Future Enhancements

- Fine-tuned models for better sentiment alignment
- Support for multiple languages
- Custom training on domain-specific datasets
- Advanced visualization of sentiment distribution
- API endpoint for programmatic access

## Author

Anam Manipal Reddy
- Email: anammanipалreddy@gmail.com
- GitHub: https://github.com/Manipal24
- LinkedIn: https://www.linkedin.com/in/manipalreddy-anam/

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Hugging Face for Transformers library
- Streamlit for the amazing framework
- PyTorch team for deep learning framework
