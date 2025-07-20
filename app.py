import streamlit as st
from bs4 import BeautifulSoup
import html
import streamlit.components.v1 as components
from streamlit_quill import st_quill
import json

# App title
st.set_page_config(page_title="Nainsi's Post Formatter", layout="centered")
st.markdown("""
    <h1 style='color: deeppink; text-align: center; font-family: "Comic Sans MS", cursive, sans-serif;'>
        Nainsi's Post Formatter 💅✨
    </h1>
""", unsafe_allow_html=True)

# Apply obnoxiously pretty pink styling
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            background: pink !important;
            background-image: radial-gradient(white 1px, transparent 0) !important;
            background-size: 20px 20px !important;
            animation: sparkle 4s linear infinite !important;
        }

        @keyframes sparkle {
            0% { background-position: 0 0; }
            100% { background-position: 100px 100px; }
        }

        .stButton>button {
            background-color: hotpink;
            color: white;
            font-size: 16px;
            border-radius: 12px;
            padding: 10px 24px;
            font-family: "Comic Sans MS", cursive, sans-serif;
        }
        .stCodeBlock {
            background-color: lavenderblush !important;
            color: deeppink !important;
            font-family: "Comic Sans MS", cursive, sans-serif !important;
        }
    </style>
""", unsafe_allow_html=True)

# Rich Text Input from Google Docs
raw_html_input = st_quill(placeholder="Paste rich text from Google Docs here...", html=True)
convert_clicked = st.button("Convert!")

# Function to clean pasted Google Docs HTML
def clean_google_docs_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")

    for tag in soup(["style", "script", "meta"]):
        tag.decompose()

    for tag in soup.find_all(True):
        for attr in ["style", "class", "id"]:
            tag.attrs.pop(attr, None)

        # Add line break before headings (except H1)
        if tag.name in ["h2"]:
            br_tag = soup.new_tag("br")
            tag.insert_before(br_tag)

    return str(soup)

# Function to extract title and body
def extract_title_and_body(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    h1 = soup.find("h1")
    title = h1.get_text() if h1 else ""
    if h1:
        h1.decompose()
    body_html = str(soup)
    return title, body_html

# Updated Author footer
author_html = '''<p>&nbsp;</p>
<div style="border-top: 2px solid #ddd; margin-top: 20px; padding-top: 20px;">
<h3 style="font-family: Arial, sans-serif; font-size: 14pt; color: rgb(67, 67, 67); margin-bottom: 10px;">About the Author</h3>
<div style="display: flex; align-items: center;"><img alt="Ciaran Kilbride" src="https://media.licdn.com/dms/image/C4D03AQFNEzfdqeSeBA/profile-displayphoto-shrink_200_200/0/1632302846265?e=2147483647&amp;v=beta&amp;t=PZ2iCKBctTPBOuF4e5P1KPTwbe_Wo42wgpvRExbC54Y" style="border-radius: 50%; width: 80px; height: 80px; margin-right: 15px;" />
<p style="font-family: Arial, sans-serif; font-size: 11pt; color: rgb(0, 0, 0); line-height: 1.38;"><strong>Ciaran Kilbride</strong> is the CEO and Founder of Caterboss, Ireland's leading supplier of catering equipment. With years of experience in the food and hospitality industry, Ciaran established Caterboss in 2017 to provide high-quality, reliable equipment tailored to the needs of food service professionals. His commitment to innovation and customer service has helped Caterboss grow into a trusted name, known for anticipating industry trends and consistently meeting the needs of its clients.</p>
</div>
</div>'''

# Conversion
if convert_clicked and raw_html_input is not None and raw_html_input.strip() != "":
    cleaned_html = clean_google_docs_html(raw_html_input)
    title, body_html = extract_title_and_body(cleaned_html)
    body_html += author_html

    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    st.subheader("Title")
    st.code(title, language="text")

    safe_title = json.dumps(title)
    components.html(f"""
        <script>
            function copyTitle() {{
                navigator.clipboard.write([
                  new ClipboardItem({{
                    'text/plain': new Blob([{safe_title}], {{ type: 'text/plain' }})
                  }})
                ]);
                const btn = document.getElementById('copy-title-btn');
                const original = btn.innerHTML;
                btn.innerHTML = 'Copied!';
                setTimeout(() => btn.innerHTML = original, 1000);
            }}
        </script>
        <div style="text-align: left; margin-top: 10px;">
            <button id="copy-title-btn" onclick="copyTitle()"
            style='background-color: hotpink; color: white; padding: 10px 20px; 
                   border: none; border-radius: 8px; font-family: "Comic Sans MS"; 
                   cursor: pointer; font-size: 14px;'>
                Copy Title to Clipboard
            </button>
        </div>
    """, height=100)

    st.subheader("HTML Body")
    st.code(body_html, language="html")

    safe_body_text = json.dumps(body_html)
    components.html(f"""
        <script>
            function copyBody() {{
                navigator.clipboard.write([
                  new ClipboardItem({{
                    'text/plain': new Blob([{safe_body_text}], {{ type: 'text/plain' }})
                  }})
                ]);
                const btn = document.getElementById('copy-body-btn');
                const original = btn.innerHTML;
                btn.innerHTML = 'Copied!';
                setTimeout(() => btn.innerHTML = original, 1000);
            }}
        </script>
        <div style="text-align: left; margin-top: 10px;">
            <button id="copy-body-btn" onclick="copyBody()"
            style='background-color: hotpink; color: white; padding: 10px 20px; 
                   border: none; border-radius: 8px; font-family: "Comic Sans MS"; 
                   cursor: pointer; font-size: 14px;'>
                Copy Body to Clipboard
            </button>
        </div>
    """, height=100)
