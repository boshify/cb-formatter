import streamlit as st
import markdown
from bs4 import BeautifulSoup
import pyperclip

# App title
st.set_page_config(page_title="Markdown to HTML Converter", layout="centered")
st.title("Markdown to HTML Converter")

# Markdown input
markdown_input = st.text_area("Paste your Markdown here:", height=300)

# Function to extract title and body
def extract_title_and_body(html):
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1")
    title = h1.get_text() if h1 else ""
    if h1:
        h1.decompose()
    body_html = str(soup)
    return title, body_html

# Author HTML footer
author_html = '''<p>&nbsp;</p>
<div style="border-top: 2px solid #ddd; margin-top: 20px; padding-top: 20px;">
<h3 style="font-family: Arial, sans-serif; font-size: 14pt; color: rgb(67, 67, 67); margin-bottom: 10px;">About the Author</h3>
<div style="display: flex; align-items: center;"><img alt="Ciaran Kilbride" src="https://media.licdn.com/dms/image/C4D03AQFNEzfdqeSeBA/profile-displayphoto-shrink_200_200/0/1632302846265?e=2147483647&amp;v=beta&amp;t=PZ2iCKBctTPBOuF4e5P1KPTwbe_Wo42wgpvRExbC54Y" style="border-radius: 50%; width: 80px; height: 80px; margin-right: 15px;" />
<p style="font-family: Arial, sans-serif; font-size: 11pt; color: rgb(0, 0, 0); line-height: 1.38;"><strong>Ciaran Kilbride</strong> is the CEO and Founder of Caterboss, Ireland&#39;s leading supplier of catering equipment. With years of experience in the food and hospitality industry, Ciaran established Caterboss in 2017 to provide high-quality, reliable equipment tailored to the needs of professional caterers. His commitment to innovation and customer service has helped Caterboss grow into a trusted name, known for anticipating industry trends and consistently meeting the needs of its clients.</p>
</div>
</div>'''

if markdown_input:
    # Convert Markdown to HTML
    html_output = markdown.markdown(markdown_input, extensions=[
        'extra', 'codehilite', 'toc', 'tables', 'fenced_code',
        'sane_lists', 'smarty', 'admonition', 'nl2br'
    ])
    title, body_html = extract_title_and_body(html_output)
    body_html += author_html

    st.subheader("Title")
    st.code(title, language="text")
    st.button("Copy Title to Clipboard", on_click=lambda: pyperclip.copy(title))

    st.subheader("HTML Body")
    st.code(body_html, language="html")
    st.button("Copy Body to Clipboard", on_click=lambda: pyperclip.copy(body_html))

st.markdown("---")
st.markdown("Made for [Streamlit Community Cloud](https://streamlit.io/cloud)")
