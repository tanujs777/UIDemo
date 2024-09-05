import streamlit as st
import docx
from io import StringIO

if 'document_text' not in st.session_state:
    st.session_state['document_text'] = None

# Correct background image and square file uploader styles
st.markdown("""
    <style>
    /* Apply the background image */
    .stApp {
        background-image: url('https://img.freepik.com/free-vector/gradient-3d-stairs-background_23-2149156757.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Ensure the file uploader is square and left-aligned */
    div[data-testid="stFileUploadDropzone"] {
        border: 2px dashed #1f77b4 !important;
        padding: 15px;
        background-color: #eaf3fc;
        width: 250px !important;  /* Square width */
        height: 250px !important; /* Square height */
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-left: 10px !important; /* Push further to the left */
        margin-top: 15px !important;
    }

    .stButton button {
        background-color: #FFD700 !important;
        color: #000000 !important;
        padding: 12px 24px;
        font-size: 1.2em;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        margin-top: 10px;
    }
    
    .stButton button:hover {
        background-color: #FFC107 !important;
    }

    .custom-success-box {
        background-color: #eaf3fc !important;
        color: #000000 !important;
        padding: 15px;
        border-radius: 8px;
        font-size: 1.2em;
        border-left: 6px solid #1f77b4;
        margin-top: 20px;
    }
    
    .stSpinner {
        color: #1f77b4;
        font-size: 1.2em;
    }
    
    .stMarkdown h3 {
        color: #1f77b4;
        font-size: 1.6em;
        margin-top: 30px;
        text-align: center;
    }

    .stMarkdown p {
        font-size: 1.2em;
        color: #000000 !important;
        line-height: 1.8em;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to extract text from docx
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Simulated step extraction function
def extract_steps_from_llm(text):
    steps = f"Extracted steps from document:\n\n{text[:200]}..."
    return steps

# Use the sidebar for left-aligned file uploader
st.sidebar.title("Upload your document")

# Add the company's logo above the file uploader
st.sidebar.image("https://etimg.etb2bimg.com/photo/105552577.cms", use_column_width=True)

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload a file (TXT or DOCX)", type=["txt", "docx"])

# Main UI title and instructions
st.title("📄 Training Steps Extractor")
st.markdown('<p class="custom-blue-text">Upload your document, and this tool will extract and display the training steps.</p>', unsafe_allow_html=True)

# Process the uploaded file
if uploaded_file is not None:
    if uploaded_file.name.endswith(".txt"):
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        document_text = stringio.read()
    elif uploaded_file.name.endswith(".docx"):
        document_text = extract_text_from_docx(uploaded_file)

    st.session_state['document_text'] = document_text
    st.markdown('<div class="custom-success-box">Document uploaded successfully! Click \'Extract Steps\' to proceed.</div>', unsafe_allow_html=True)

# Display extracted steps when the button is clicked
if st.session_state['document_text'] is not None:
    if st.button("Extract Steps"):
        with st.spinner('Extracting steps...'):
            steps = extract_steps_from_llm(st.session_state['document_text'])
            st.markdown(f"### Extracted Steps\n\n{steps}")
else:
    st.markdown('<div class="custom-success-box">Please upload a file to proceed.</div>', unsafe_allow_html=True)
