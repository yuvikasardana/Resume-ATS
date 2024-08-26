from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ##convert pdf into image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        #convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format = 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type":"image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode(),

            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded...")


##Streamlit app
st.set_page_config(page_title = "MY ATS Resume Expert")
st.header("MY ATS")
# st.text("ola")
input_text = st.text_area("Job Description: ", key = "input")
uploaded_file = st.file_uploader("Uploaded your Resume : ", type = ["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

submit1 = st.button("Tell me About the Resume")
submit2 = st.button("How can I improve the resume")
submit3 = st.button("match the resume")

input_prompt_1 = """
You are an experienced HR with Tech Experience in the field of any job role in the field of Data Science, Full Stack, Data Analyst, DEVOPS, Big Data Engineering.
Your job is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with  Highlight the strengths and weaknesses of the applicant in relation to the specified job Role

"""
input_prompt_2 = """
You are an experienced HR with Tech Experience in the field of any job role in the field of Data Science, Full Stack, Data Analyst, DEVOPS, Big Data Engineering.
Your job is to review the provided resume against the job description for these profiles.
Please provide constructive feedback on how the candidate can improve their skills or experience to better fit the job
"""
input_prompt_3 = """
You are a skilled Application Tracking System scanner with a deep understanding of Data Science, FUll Stack, Web Development, Big Data Engineering, DEVOPS, Data Analyst and deep ATS functionalities. Your task is to evaluate the resume against the provided job description , giving me the percentage of match if the resume matches the job description.
The output should give first the percentage then keywords missing and last final output
"""

if submit1 :
    if uploaded_file is not None :
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt_1, pdf_content, input_text)
        st.subheader("The response is :")
        st.write(response)
    else:
        st.write("Please upload the resume first")

if submit3 :
    if uploaded_file is not None :
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt_3, pdf_content, input_text)
        st.subheader("The response is :")
        st.write(response)
    else:
        st.write("Please upload the resume first")

if submit2 :
    if uploaded_file is not None :
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt_2, pdf_content, input_text)
        st.subheader("The response is :")
    else:
        st.write("Please upload the resume first")
