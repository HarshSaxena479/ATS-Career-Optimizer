import base64
import io

from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')      #pdf into image
    response = model.generate_content([input, pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## convert the pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]  #first page is the content of the image

        #convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() #encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("no file uploaded")

## streamlit app
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader('Upload your Resume(pdf)....',type=['pdf'])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

submit1 = st.button("Tell me about the resume")
submit2 = st.button("Percentage matched")
submit3 = st.button("Resume Improvement Suggestions")
submit4 = st.button("Skill Improvement Guidance")
# submit3 = st.button("What are the keywords that are missing")

input_prompt1="""You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements."""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

input_prompt3 = """You are an expert career coach and ATS specialist. Given a resume and a job description, analyze how well the 
resume aligns with the job. Suggest concise improvements to optimize it for ATS and increase relevance. Focus on missing keywords,
alignment of experience with job requirements, use of measurable achievements, formatting issues that may affect ATS parsing,
and stronger action verbs or soft skills. Return actionable suggestions in bullet points."""

input_prompt4 = """Review the resume and suggest personalized ways the candidate can improve their skills based on their experience and target role.
Recommend high-impact skills to develop, tools or technologies to learn, relevant courses or certifications, and project ideas.
Also include soft skills and learning habits that would enhance their profile in the context of the job market."""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The response is ")
        st.write(response)
    else:
        st.write('Please upload the resume')

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit4:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt4,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")