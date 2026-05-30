import pdfplumber
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def get_role_suggestions(resume_text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""
You are a career counselor and job role expert.

Below is a candidate's resume text. Analyze it carefully and:
1. Suggest the TOP 5 most suitable job roles for this candidate
2. For each role, give:
   - Role name
   - Why they are a good fit (based on their skills/projects)
   - What skills they should improve for this role

Format your response clearly with headings for each role.

Resume:
{resume_text}
"""
            }
        ]
    )
    return response.choices[0].message.content