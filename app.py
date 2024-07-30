import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
import os
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Pro Response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):    
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """
You are an advanced and experienced ATS (Applicant Tracking System) with a deep understanding of the tech field, including software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the provided resume against the given job description. 

Consider the following criteria:
1. The competitive nature of the job market.
2. Providing the best possible assistance for resume improvement.
3. High accuracy in matching the job description (JD) with the resume content.
4. Identifying missing keywords that are crucial for the job role.

Evaluate the resume based on the job description and provide the following details:
- Percentage match based on the JD.
- List of missing keywords.
- Summary of the profile with suggestions for improvement.

Use the following format for your response:
{{"JD Match":"<percentage>%","MissingKeywords":["<keyword1>","<keyword2>",...],"Profile Summary":"<summary>"}}

Resume: {text}
Job Description: {jd}
"""

# Streamlit App
st.title("Resume Evaluator")
st.text("Optimize Your Resume for ATS")
jd = st.text_area("Enter the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", help="Please upload a PDF file of your resume")

submit = st.button("Evaluate Resume")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        raw_response = get_gemini_response(input_prompt.format(text=text, jd=jd))
        response = json.loads(raw_response)
        
        st.subheader("Evaluation Results")
        
        st.write(f"**Job Description Match:** {response['JD Match']}")
        st.write("**Missing Keywords:**")
        for keyword in response['MissingKeywords']:
            st.write(f"- {keyword}")
        st.write(f"**Profile Summary:** {response['Profile Summary']}")
