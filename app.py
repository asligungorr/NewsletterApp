import streamlit as st
from copy_clipboard import add_copy_to_clipboard_button
from openai_api import (
    summarize_newsletter, 
    translate_text, 
    generate_title, 
    translate_multiple,
    Summary,
    format_summary_with_localized_link
)
import PyPDF2
import docx
from typing import Optional

def read_pdf(file) -> str:
    """Read and extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def read_docx(file) -> str:
    """Read and extract text from DOCX file"""
    try:
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return ""

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

def format_summary_with_localized_link(summary: Summary, language: str) -> str:
    """Format summary with bold title and localized read more link"""
    # Remove any existing markdown formatting from the title
    clean_title = summary.title.replace('*', '')
    # Format the text with the bold title
    formatted_text = f"**{clean_title}**\n\n{summary.content}"
    if summary.url:
        read_more_text = get_read_more_translation(language)
        formatted_text += f"\n\n[{read_more_text}]({summary.url})"
    return formatted_text
def display_summary(emotion: str, emoji: str, summary: Summary, language: str):
    """Display a single summary with its controls and make it editable"""
    st.markdown(f"### {emoji} {emotion}")
    
    # Format the text for the text area with bold title and read more link
    formatted_text = format_summary_with_localized_link(summary, language)
    
    # Create an editable text area with the formatted content
    edited_text = st.text_area(
        f"Edit {emotion} Summary",
        value=formatted_text,
        height=200,
        key=f"editable_{emotion}"
    )
    
    # Create three columns for the controls and link
    col1, col2 = st.columns([1, 1])
    
    # Copy button in first column
    with col1:
        add_copy_to_clipboard_button(edited_text, f"Copy {emotion} Text")
    
    # Select for Translation button in second column
    with col2:
        if st.button(f"Select for Translation", key=f"select_{emotion}"):
            st.session_state.selected_for_translation = emotion
            st.session_state[f"edited_{emotion}"] = edited_text
    
    # Read More link in third column
    
    read_more_text = get_read_more_translation(language)
    if summary.url:
        st.markdown(f"[{read_more_text}]({summary.url})")
    else:
            # If no URL, show disabled link style
        st.markdown(
            f"""
            <span style="color: #808080; text-decoration: none; cursor: not-allowed;">
                {read_more_text}
            </span>
            """,
            unsafe_allow_html=True
            )
def main():
    st.set_page_config(layout="wide")
    st.title("BeamSec AI Tool - Customizable Weekly Bulletin")

    # Define emotions and emoji mapping
    emotions = ["Excitement", "Interesting", "Confusion"]
    emoji_map = {
        "Excitement": "😊",
        "Interesting": "🤔",
        "Confusion": "😕"
    }

    # Initialize session state
    if 'summaries' not in st.session_state:
        st.session_state.summaries = {}
    if 'selected_for_translation' not in st.session_state:
        st.session_state.selected_for_translation = None
    if 'generate_clicked' not in st.session_state:
        st.session_state.generate_clicked = False

    # Input section
    st.subheader("Choose input method:")
    input_method = st.radio(
        "Input Method Selection",
        ["Text Input", "Upload PDF/DOCX"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # Get input based on selected method
    newsletter_text = ""
    url = st.text_input("Source URL (Optional)", placeholder="https://example.com/news-article")
    
    if input_method == "Text Input":
        newsletter_text = st.text_area(
            "Paste the newsletter here:",
            height=150,
            key="newsletter_input"
        )
    else:
        uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx", "txt"])
        if uploaded_file:
            try:
                if uploaded_file.type == "application/pdf":
                    newsletter_text = read_pdf(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    newsletter_text = read_docx(uploaded_file)
                elif uploaded_file.type == "text/plain":
                    newsletter_text = str(uploaded_file.read(), "utf-8")
                st.success("File uploaded successfully!")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")

    # Configuration section
    col1, col2 = st.columns(2)
    with col1:
        length_options = st.radio(
            "Summary Length",
            ["30", "50", "100"],
            horizontal=True,
            format_func=lambda x: f"<{x} words"
        )
    with col2:
        title_length = st.slider(
            "Select title length (words):",
            1, 10, 4
        )

    initial_language = st.radio(
        "Select primary language:",
        ["English", "Spanish", "French", "German", "Turkish", "Azerbaijani", "Arabic", "Russian", "Portuguese"],
        horizontal=True
    )

    # Generate summaries
    if st.button("Generate Summaries", type="primary"):
        if newsletter_text:
            st.session_state.generate_clicked = True
            summary_length = int(length_options)
            
            for emotion in emotions:
                # Generate title and summary
                title = generate_title(newsletter_text, title_length, emotion.lower())
                content = summarize_newsletter(newsletter_text, summary_length, emotion.lower())
                
                # Translate if needed
                if initial_language != "English":
                    title = translate_text(title, initial_language)
                    content = translate_text(content, initial_language)
                
                # Store in session state
                st.session_state.summaries[emotion] = Summary(
                    title=title,
                    content=content,
                    url=url
                )

    # Display summaries
    if st.session_state.get('generate_clicked', False) and st.session_state.summaries:
        cols = st.columns(3)
        for emotion, col in zip(emotions, cols):
            with col:
                if emotion in st.session_state.summaries:
                    display_summary(
                        emotion,
                        emoji_map[emotion],
                        st.session_state.summaries[emotion],
                        initial_language
                    )

    # Translation section
    st.markdown("---")
    st.subheader("Translate Final Summaries")

    if st.session_state.selected_for_translation:
        st.info(f"Currently selected for translation: {st.session_state.selected_for_translation}")

    # Target languages selection
    st.write("Select target languages for translation:")
    target_langs = ["English", "Spanish", "French", "German", "Turkish", "Azerbaijani", "Arabic", "Russian", "Portuguese"]
    
    num_cols = 3
    rows = [target_langs[i:i + num_cols] for i in range(0, len(target_langs), num_cols)]
    selected_langs = []
    
    for row in rows:
        cols = st.columns(num_cols)
        for lang, col in zip(row, cols):
            with col:
                if st.checkbox(lang, key=f"trans_lang_{lang}"):
                    selected_langs.append(lang)

    # Translation button
    if st.button("Translate to Selected Languages", type="primary"):
        if not st.session_state.selected_for_translation:
            st.warning("Please select a summary for translation using the buttons above.")
        elif not selected_langs:
            st.warning("Please select at least one target language.")
        else:
            selected_emotion = st.session_state.selected_for_translation
            # Use the edited text if available
            original_text = st.session_state.get(
                f"edited_{selected_emotion}",
                format_summary_with_localized_link(
                    st.session_state.summaries[selected_emotion],
                    initial_language
                )
            )
            
            # Get translations
            translations = translate_multiple(original_text, selected_langs)
            
            # Display translations
            st.markdown("### Translations")
            cols = st.columns(min(3, len(translations)))
            for idx, (lang, trans_text) in enumerate(translations.items()):
                with cols[idx % 3]:
                    st.markdown(f"#### {lang}")
                    
                    # Make translation editable
                    edited_translation = st.text_area(
                        f"Edit {lang} Translation",
                        value=trans_text,
                        height=200,
                        key=f"edit_trans_{lang}"
                    )
                    
                    add_copy_to_clipboard_button(edited_translation, f"Copy {lang} Translation")

if __name__ == "__main__":
    main()