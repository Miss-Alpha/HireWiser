import texts
from openai import OpenAI
from dotenv import load_dotenv
import tempfile
from langchain_community.document_loaders import PyPDFLoader
import numpy as np
import streamlit as st

#load_dotenv()

# Connect to OpenAI 
#client = OpenAI()

#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def read_resume(uploaded_cv):
    # Save the uploaded file as a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_cv.read())  # Write the uploaded PDF content to a temp file
        temp_file_path = tmp_file.name
    
    # Use PyPDFLoader to read the content of the PDF from the temporary file path
    loader = PyPDFLoader(temp_file_path)
    documents = loader.load()

    # Combine all documents into a single text
    full_resume = "\n".join([doc.page_content for doc in documents])
    return full_resume
    

def summarise_resume(full_resume, openai_key):
    client = OpenAI(api_key=openai_key)
    summary_prompt = f"Summarize the following resume into one concise paragraph, highlighting the candidate's key skills, experience, and qualifications: \n\n{full_resume}."

    resume_summary = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": summary_prompt},
        ] 
    )
    summary = resume_summary.choices[0].message.content
    return summary


def extract_candidate_name(full_resume, openai_key):
    client = OpenAI(api_key=openai_key)
    extact_name_prompt = f"Based on the provided resume text, only extract the candidate's full name: \n\n {full_resume}."

    candidate_name_json = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": extact_name_prompt},
        ] 
    )
    candidate_name = candidate_name_json.choices[0].message.content
    return candidate_name


def generate_questions(interview_type, question_count, input_contents, provide_answers, resume_summary, openai_key):
    client = OpenAI(api_key=openai_key)
    if provide_answers:
    #    if len(resume_summary)>0:
            prompt_text = texts.prompt_with_answers(interview_type, question_count, input_contents, resume_summary)

    else:
        #prompt_text = f"{texts.prompt_text_without_answers}"
        prompt_text = texts.prompt_without_answers(interview_type, question_count, input_contents, resume_summary)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt_text},
        ]
        )
    message = response.choices[0].message.content
    return message


def compute_similarity(job_description, resume_summary, openai_key):
    """Compute similarity between job description and resume summary."""
    client = OpenAI(api_key=openai_key)

    similarity_prompt = f"""Based on the following job description: {job_description} and the resume summary: {resume_summary}, evaluate the similarity between them on a scale of 1 to 100, where 100 represents the highest possible similarity. Consider the relevance of skills, experience, and qualifications listed in the resume summary to the requirements in the job description. 
    Provide a brief explanation for the score, highlighting the most relevant matches or gaps between the two."""

    similarity_json = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": similarity_prompt},
        ] 
    )
    similarity_score = similarity_json.choices[0].message.content
    return similarity_score
