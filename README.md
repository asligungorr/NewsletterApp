# BeamSec AI Tool - Customizable Weekly Bulletin

## Overview

The **BeamSec AI Tool** is a Streamlit application designed to streamline the creation, customization, and translation of newsletter summaries. With this tool, users can:

- Extract content from text inputs, PDFs, or DOCX files.
- Generate emotion-driven summaries (Excitement, Interesting, Confusion).
- Customize summaries and titles.
- Translate content into multiple languages while preserving formatting.

The tool is ideal for generating weekly bulletins, multilingual content, and summaries tailored to different emotional tones.

---

## Features

### Input Options
- **Text Input**: Paste text directly into the application.
- **File Upload**: Upload files in PDF, DOCX, or TXT format to extract and process content.

### Summary Generation
- **Emotion-Driven Summaries**: Generate summaries based on specific emotions like Excitement 😊, Interesting 🤔, and Confusion 😕.
- **Configurable Summary Length**: Choose from summary lengths of 30, 50, or 100 words.
- **Customizable Title Length**: Specify the number of words in the generated title (from 1 to 10).

### Customization
- **Edit Summaries**: Edit generated summaries and titles directly in the app.
- **Copy to Clipboard**: Easily copy summaries and translations to the clipboard for external use.

### Multilingual Support
- **Translation Options**: Translate summaries into multiple languages while preserving markdown and URL formatting.
- **Supported Languages**: English, Spanish, French, German, Turkish, Azerbaijani, Arabic, Russian, Portuguese.

---
## Project Structure

```plaintext
BeamSec-AI-Tool/
├── app.py                    # Main Streamlit application
├── copy_clipboard.py         # Script for "Copy to Clipboard" functionality
├── openai_api.py             # Helper functions for summarization, translation, and title generation
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker configuration
├── README.md                 # Project documentation
├── .env                      # Environment variables (API keys)
└── src/                      # Additional source modules for organizing code

## Installation

### Prerequisites
- **Python 3.8 or higher**
- **[Streamlit](https://streamlit.io/)** - for running the web application
- **OpenAI API Key** - required for generating summaries and translations (GPT-4 Turbo)

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/beamsec-ai-tool.git
   cd beamsec-ai-tool
