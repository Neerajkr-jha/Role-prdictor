import streamlit as st
from utils import extract_text_from_pdf, get_role_suggestions

st.set_page_config(
    page_title="AI Resume Role Matcher",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark background */
.stApp {
    background-color: #0f1117;
    color: #e2e8f0;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Hero */
.hero {
    text-align: center;
    padding: 3rem;
    border-radius: 24px;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(99,102,241,0.3);
}

.hero h1 {
    font-size: 2.8rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: #ffffff;
}

.hero p {
    font-size: 1.1rem;
    color: #e0e7ff;
}

/* Subheader text */
h2, h3, .stSubheader {
    color: #f1f5f9 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    border: 2px dashed #6366f1;
    border-radius: 16px;
    padding: 1rem;
    background: #1e2130;
}

[data-testid="stFileUploader"] * {
    color: #cbd5e1 !important;
}

/* Metric labels and values */
[data-testid="stMetric"] {
    background: #1e2130;
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid #2d3748;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
}

[data-testid="stMetricValue"] {
    color: #f1f5f9 !important;
    font-size: 1.4rem !important;
    font-weight: 600 !important;
}

/* Result box */
.result-box {
    background: #1e2130;
    border-left: 5px solid #6366f1;
    padding: 1.8rem 2rem;
    border-radius: 12px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.3);
    color: #e2e8f0;
    line-height: 1.9;
    font-size: 0.97rem;
}

.result-box h1, .result-box h2, .result-box h3 {
    color: #a5b4fc !important;
    margin-top: 1.2rem;
}

.result-box strong, .result-box b {
    color: #c7d2fe;
}

.result-box p, .result-box li {
    color: #cbd5e1;
}

/* Badge */
.badge {
    background: #052e16;
    color: #86efac;
    padding: 6px 14px;
    border-radius: 999px;
    display: inline-block;
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 1rem;
    border: 1px solid #166534;
}

/* Success message */
.stSuccess {
    background-color: #052e16 !important;
    color: #86efac !important;
    border: 1px solid #166534 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #161b27 !important;
    border-right: 1px solid #2d3748;
}

[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}

/* Divider */
hr {
    border-color: #2d3748 !important;
}

/* Spinner text */
.stSpinner > div {
    color: #a5b4fc !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #475569;
    margin-top: 40px;
    padding: 20px;
    font-size: 0.85rem;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.title("AI Resume Matcher")
    st.markdown("""
    Upload your resume and discover:

    - Best-fit job roles
    - Career opportunities
    - AI-powered recommendations

    ---

    Powered by Groq + LLaMA 3 + Streamlit
    """)

# HERO
st.markdown("""
<div class="hero">
    <h1>AI Resume Role Matcher</h1>
    <p>Discover the best career opportunities from your resume using AI.</p>
</div>
""", unsafe_allow_html=True)

# MAIN
with st.container():

    st.subheader("Upload Resume")

    uploaded_file = st.file_uploader(
        "Drag & drop your PDF resume here",
        type=["pdf"]
    )

    if uploaded_file:

        with st.spinner("Reading resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)

        if not resume_text.strip():
            st.error("Unable to extract text from this PDF. Try another file.")
        else:

            st.markdown('<div class="badge">✓ Resume processed successfully</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Words", len(resume_text.split()))
            with col2:
                st.metric("Characters", len(resume_text))
            with col3:
                st.metric("Status", "Ready")

            st.divider()

            with st.spinner("Analyzing your profile..."):
                suggestions = get_role_suggestions(resume_text)

            st.success("Analysis complete!")
            st.subheader("Recommended Roles")

            st.markdown(
                f'<div class="result-box">{suggestions}</div>',
                unsafe_allow_html=True
            )

# FOOTER
st.markdown("""
<div class="footer">
    Built with Groq + LLaMA 3 + Streamlit
</div>
""", unsafe_allow_html=True)
