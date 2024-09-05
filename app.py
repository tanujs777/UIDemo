import streamlit as st
import docx
from io import StringIO

# Initialize session state
if 'document_text' not in st.session_state:
    st.session_state['document_text'] = None

# CSS Styling for custom UI
st.markdown("""
    <style>
    /* Overall body styling */
    body {
        background-color: #f5f5f5;
        font-family: 'Arial', sans-serif;
        color: #333333;
    }

    /* Title styling */
    .main h1 {
        font-size: 2.8em;
        color: #1f77b4;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 10px;
    }

    /* Custom description text directly below the heading */
    .custom-blue-text {
        font-size: 1.4em;
        text-align: center;
        color: #1f77b4;  /* Set text color to a visible blue */
        margin-bottom: 30px;
        font-weight: bold;
    }

    /* File uploader styling */
    .stFileUploader {
        border: 2px dashed #1f77b4 !important;
        padding: 15px;
        margin-bottom: 25px;
        background-color: #eaf3fc;
    }

    /* Button styling with yellow background and black text */
    .stButton button {
        background-color: #FFD700 !important;  /* Set button background to yellow */
        color: #000000 !important;  /* Set button text color to black */
        padding: 12px 24px;
        font-size: 1.2em;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        margin-top: 10px;
    }

    /* Button hover effect */
    .stButton button:hover {
        background-color: #FFC107 !important;  /* Slightly darker yellow on hover */
    }

    /* Custom success message styling for light blue background and jet black text */
    .custom-success-box {
        background-color: #eaf3fc !important;  /* Light blue background */
        color: #000000 !important;  /* Jet black text */
        padding: 15px;
        border-radius: 8px;
        font-size: 1.2em;
        border-left: 6px solid #1f77b4;
        margin-top: 20px;
    }

    /* Custom spinner */
    .stSpinner {
        color: #1f77b4;
        font-size: 1.2em;
    }

    /* Result section styling */
    .stMarkdown h3 {
        color: #1f77b4;
        font-size: 1.6em;
        margin-top: 30px;
        text-align: center;
    }

    .stMarkdown p {
        font-size: 1.2em;
        color: #000000 !important;  /* Ensure the text in markdown is jet black */
        line-height: 1.8em;
    }
    </style>
    """, unsafe_allow_html=True)

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Dummy function for LLM connection (to be replaced with real LLM logic)
def extract_steps_from_llm(text):
    steps = f"Extracted steps from document:\n\n{text[:200]}..."  # Simulate extracted text
    return steps

# Streamlit App UI
st.title("📄 Training Steps Extractor")

# Blue-styled description below the title
st.markdown('<p class="custom-blue-text">Upload your document, and this tool will extract and display the training steps.</p>', unsafe_allow_html=True)

# File uploader with styled placeholder
uploaded_file = st.file_uploader("Upload a file (TXT or DOCX)", type=["txt", "docx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".txt"):
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        document_text = stringio.read()
    elif uploaded_file.name.endswith(".docx"):
        document_text = extract_text_from_docx(uploaded_file)

    # Store the extracted text in session state
    st.session_state['document_text'] = document_text
    # Custom success box for document upload
    st.markdown('<div class="custom-success-box">Document uploaded successfully! Click \'Extract Steps\' to proceed.</div>', unsafe_allow_html=True)

# Ensure session state has document text before processing
if st.session_state['document_text'] is not None:
    # Button to process the document
    if st.button("Extract Steps"):
        with st.spinner('Extracting steps...'):
            steps = extract_steps_from_llm(st.session_state['document_text'])
            # Custom success box for steps extraction
            st.markdown('<div class="custom-success-box">Steps extracted successfully!</div>', unsafe_allow_html=True)
            st.markdown(f"### Extracted Steps\n\n{steps}")
else:
    # Custom info box with black text
    st.markdown('<div class="custom-success-box">Please upload a file to proceed.</div>', unsafe_allow_html=True)
