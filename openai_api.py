# openai_api.py
import os
from dotenv import load_dotenv
import openai
from typing import Literal
from dataclasses import dataclass
import streamlit as st
from copy_clipboard import add_copy_to_clipboard_button

# Load environment variables
load_dotenv()
openai.api_key = st.secrets["OPENAI_API_KEY"]

@dataclass
class Summary:
    title: str
    content: str
    url: str = ""

def create_chat_completion(messages, temperature=1.0):
    """Helper function to create chat completion with GPT-4 Turbo"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature=temperature,
            top_p=1,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def enforce_word_limit(text: str, limit: int) -> str:
    """Ensure text stays within specified word limit"""
    words = text.split()
    if len(words) > limit:
        return ' '.join(words[:limit])
    return text

def generate_title(
    newsletter_text: str,
    title_length: int,
    emotion: Literal["excitement", "interesting", "confusion"]
) -> str:
    messages = [
        {"role": "system", "content": (
            f"You are a title generator. Create a title that:\n"
            f"1. Must be EXACTLY {title_length} words long\n"
            f"2. Conveys {emotion}\n"
            f"Do not include any other text in your response."
        )},
        {"role": "user", "content": newsletter_text}
    ]
    
    title = create_chat_completion(messages, temperature=0.9)
    return enforce_word_limit(title.strip(), title_length)

def summarize_newsletter(
    newsletter_text: str,
    summary_length: int,
    emotion: Literal["excitement", "interesting", "confusion"]
) -> str:
    messages = [
        {"role": "system", "content": (
            f"You are a newsletter summarizer. Create a summary that:\n"
            f"1. Must be LESS THAN {summary_length} words\n"
            f"2. Conveys {emotion}\n"
            f"3. Is clear and concise\n"
            f"Do not include any other text in your response."
        )},
        {"role": "user", "content": newsletter_text}
    ]
    
    summary = create_chat_completion(messages, temperature=1.2)
    return enforce_word_limit(summary, summary_length)

def format_summary_with_localized_link(summary: Summary, language: str) -> str:
    """Format summary with bold title and localized read more link"""
    # The title is already wrapped in ** for bold formatting
    formatted_text = f"**{summary.title}**\n\n{summary.content}"
    if summary.url:
        read_more_text = get_read_more_translation(language)
        formatted_text += f"\n\n[{read_more_text}]({summary.url})"
    return formatted_text

def translate_text(text: str, target_language: str) -> str:
    """Translate text while preserving markdown formatting"""
    messages = [
        {"role": "system", "content": (
            f"You are a translator. Translate the text to {target_language} while:\n"
            "1. Preserving all markdown formatting (**, [], etc.)\n"
            "2. Maintaining the original text structure\n"
            "3. Keeping any URLs unchanged"
        )},
        {"role": "user", "content": text}
    ]
    return create_chat_completion(messages, temperature=0.7)

def translate_multiple(text: str, target_languages: list[str]) -> dict[str, str]:
    """Translate text to multiple languages simultaneously"""
    translations = {}
    for language in target_languages:
        translations[language] = translate_text(text, language)
    return translations


def display_summary(emotion: str, emoji: str, summary: Summary, language: str):
    """Display a single summary with its controls and make it editable"""
    st.markdown(f"### {emoji} {emotion}")
    
    # Format the summary with localized read more text and ensure title stays bold
    formatted_text = format_summary_with_localized_link(summary, language)
    
    # Create an editable text area with the formatted content
    edited_text = st.text_area(
        f"Edit {emotion} Summary",
        value=formatted_text,
        height=200,
        key=f"editable_{emotion}"
    )
    
    # Add controls
    col1, col2 = st.columns(2)
    with col1:
        add_copy_to_clipboard_button(edited_text, f"Copy {emotion} Text")
    with col2:
        if st.button(f"Select for Translation", key=f"select_{emotion}"):
            st.session_state.selected_for_translation = emotion
            # Store the edited text for translation
            st.session_state[f"edited_{emotion}"] = edited_text

def get_read_more_translation(language: str) -> str:
    """Get 'Read More' text in different languages"""
    translations = {
        "English": "Read More",
        "Spanish": "Leer Más",
        "French": "Lire Plus",
        "German": "Mehr Lesen",
        "Turkish": "Devamını Oku",
        "Azerbaijani": "Daha Ətraflı",
        "Arabic": "اقرأ المزيد",
        "Russian": "Читать Далее",
        "Portuguese": "Ler Mais"
    }
    return translations.get(language, "Read More")
