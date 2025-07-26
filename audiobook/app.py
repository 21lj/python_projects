import streamlit as st
import pyttsx3
from PyPDF2 import PdfReader
import tempfile
import base64

st.set_page_config(page_title="PDF Audiobook", layout="wide")
st.title("PDF Audiobook Reader with Viewer")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    with open(tmp_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    pdf_display = f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>
    """
    st.markdown("### PDF Preview")
    st.markdown(pdf_display, unsafe_allow_html=True)

    reader = PdfReader(tmp_path)
    num_pages = len(reader.pages)
    st.success(f"PDF loaded with {num_pages} pages.")

    start_page = st.number_input("Start page", min_value=1, max_value=num_pages, value=1)
    end_page = st.number_input("End page", min_value=start_page, max_value=num_pages, value=num_pages)
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_names = [f"{v.name} ({v.languages[0]})" for v in voices]
    selected_voice = st.selectbox("Choose a voice", voice_names)
    voice_id = voices[voice_names.index(selected_voice)].id
    engine.setProperty('voice', voice_id)

    if "reading" not in st.session_state:
        st.session_state.reading = False

    read_button_disabled = st.session_state.reading
    read_button_clicked = st.button("Read Aloud", disabled=read_button_disabled)

    if read_button_clicked:
        st.session_state.reading = True
        text_output = ""

        for i in range(start_page - 1, end_page):
            page = reader.pages[i]
            text = page.extract_text()
            if text:
                text_output += text + "\n"
                engine.say(text)
                engine.runAndWait()
        st.text_area("Extracted Text", text_output, height=300)
        st.session_state.reading = False

else:
    st.info("Please upload a PDF to get started.")
