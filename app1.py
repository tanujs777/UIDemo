import streamlit as st
import docx
from io import StringIO
from PyPDF2 import PdfReader

# Initialize session state keys
if 'document_text' not in st.session_state:
    st.session_state['document_text'] = None

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = True

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
        margin-left: 0px !important; /* Align to the left */
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

    .user-icon {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 20px;
    }
    
    .user-icon img {
        width: 50px;
        border-radius: 50%;
    }

    .user-icon p {
        font-size: 1.2em;
        color: #1f77b4;
        margin-left: 10px;
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

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    full_text = []
    for page in reader.pages:
        full_text.append(page.extract_text())
    return '\n'.join(full_text)

# Simulated step extraction function
def extract_steps_from_llm(text):
    steps = f"Extracted steps from document:\n\n{text[:200]}..."
    return steps

# Sidebar with logged-in admin and logout button
with st.sidebar:
    # Logged in as admin
    st.markdown('<div class="user-icon"><img src="https://cdn-icons-png.flaticon.com/512/1077/1077012.png" alt="Admin"><p>Logged in as Admin</p></div>', unsafe_allow_html=True)
    
    # Add the company's logo
    st.image("https://etimg.etb2bimg.com/photo/105552577.cms", use_column_width=True)

    # Tabs for different file types
    tabs = st.tabs(["DOCX", "PDF", "TXT"])

    # DOCX Tab
    with tabs[0]:
        uploaded_file = st.file_uploader("Upload a DOCX file", type=["docx"])
        if uploaded_file is not None:
            document_text = extract_text_from_docx(uploaded_file)
            st.session_state['document_text'] = document_text
            st.markdown('<div class="custom-success-box">DOCX file uploaded successfully! Click \'Extract Steps\' to proceed.</div>', unsafe_allow_html=True)

    # PDF Tab
    with tabs[1]:
        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
        if uploaded_file is not None:
            document_text = extract_text_from_pdf(uploaded_file)
            st.session_state['document_text'] = document_text
            st.markdown('<div class="custom-success-box">PDF file uploaded successfully! Click \'Extract Steps\' to proceed.</div>', unsafe_allow_html=True)

    # TXT Tab
    with tabs[2]:
        uploaded_file = st.file_uploader("Upload a TXT file", type=["txt"])
        if uploaded_file is not None:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            document_text = stringio.read()
            st.session_state['document_text'] = document_text
            st.markdown('<div class="custom-success-box">TXT file uploaded successfully! Click \'Extract Steps\' to proceed.</div>', unsafe_allow_html=True)

    # Logout button clears session state
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

# Check if the user is logged in
if not st.session_state['logged_in']:
    st.markdown("<h1>Welcome to the Training Steps Extractor</h1>", unsafe_allow_html=True)
    st.markdown("<p>Please log in to continue.</p>", unsafe_allow_html=True)
else:
    # Main UI title and instructions
    st.title("📄 Training Steps Extractor")
    st.markdown('<p class="custom-blue-text">Upload your document, and this tool will extract and display the training steps.</p>', unsafe_allow_html=True)

    # Extract steps button and result display
    if st.session_state['document_text'] is not None:
        if st.button("Extract Steps"):
            with st.spinner('Extracting steps...'):
                steps = extract_steps_from_llm(st.session_state['document_text'])
                st.markdown(f"### Extracted Steps\n\n{steps}")
    else:
        st.markdown('<div class="custom-success-box">Please upload a file to proceed.</div>', unsafe_allow_html=True)
