#copy_clipboard.py
import streamlit.components.v1 as components

def add_copy_to_clipboard_button(text, button_label="Copy Text"):
    # Escape any single quotes and newlines in the text to prevent JS errors
    text = text.replace("'", "\\'").replace("\n", "\\n")
    
    copy_code = f"""
    <style>
    .copy-button {{
        background-color: #FF4B4B;
        border: none;
        color: white;
        padding: 8px 16px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
        margin: 4px 2px;
        transition-duration: 0.3s;
        cursor: pointer;
        border-radius: 4px;
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 600;
        width: auto;
        min-width: 120px;
    }}
    
    .copy-button:hover {{
        background-color: #FF6B6B;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}

    .copy-button:active {{
        transform: translateY(0px);
    }}

    .success-message {{
        color: #4CAF50;
        margin-left: 10px;
        display: none;
        font-size: 14px;
        font-family: 'Source Sans Pro', sans-serif;
    }}

    .button-container {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    </style>
    
    <div class="button-container">
        <button class="copy-button" id="copyButton_{button_label.replace(' ', '_')}">
            {button_label}
        </button>
        <span class="success-message" id="successMessage_{button_label.replace(' ', '_')}">
            ✓ Copied
        </span>
    </div>

    <script>
    document.getElementById('copyButton_{button_label.replace(' ', '_')}').addEventListener('click', function() {{
        const text = '{text}';
        navigator.clipboard.writeText(text)
            .then(() => {{
                const button = this;
                const successMessage = document.getElementById('successMessage_{button_label.replace(' ', '_')}');
                successMessage.style.display = 'inline';
                button.style.backgroundColor = '#4CAF50';
                
                setTimeout(() => {{
                    button.style.backgroundColor = '#FF4B4B';
                    successMessage.style.display = 'none';
                }}, 2000);
            }})
            .catch(err => {{
                console.error('Failed to copy text: ', err);
                alert('Failed to copy text. Please try again.');
            }});
    }});
    </script>
    """
    components.html(copy_code, height=50)

