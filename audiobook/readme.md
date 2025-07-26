# Audiobook PDF Reader

## Project Description
This is a simple web application that allows users to upload PDF files and have them read aloud using text-to-speech technology. Users can:
- Upload and view PDFs directly in the browser using an embedded iframe.
- Extract and listen to the PDF content using selectable voice options.

## Libraries Used

- **streamlit**  
  Used to build the web interface for uploading files, displaying content, and interacting with the user.

- **PyPDF2**  
  Extracts text from uploaded PDF files for audio conversion.

- **pyttsx3**  
  Converts extracted text into speech using offline text-to-speech (TTS). It supports multiple voice options and does not require internet access.

- **tempfile**  
  Creates temporary files to safely handle uploaded PDFs without storing them permanently on disk.

- **base64**  
  Encodes PDF files into base64 format so they can be displayed in an HTML `<iframe>` within the Streamlit app.
