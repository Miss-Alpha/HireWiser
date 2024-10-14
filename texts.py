job_description =  """- Advanced degree in Computer Science, Statistics, Mathematics, or a related field. 
- 5+ years of experience as a Data Scientist.
- Strong proficiency in Python, R, or other relevant programming languages.
- Expertise in machine learning algorithms (e.g., regression, classification, clustering).
- Experience with data visualization tools (e.g., Matplotlib, Seaborn).
- Knowledge of cloud platforms (e.g., AWS, GCP, Azure) is a plus.
- Excellent problem-solving and analytical skills.
- Strong communication and teamwork abilities."""


def prompt_with_answers(interview_type, question_count, input_contents, resume_summary):
    return f"""
    You are an experienced interview assistant helping managers prepare tailored interview questions. 
    The manager will provide you with a job title and a description, and you will create a list of relevant questions to guide the interview process.

    Please generate a set of {question_count} high-quality questions for a {interview_type} interview with their respective answers.

    The position and desription being interviewed for is: {input_contents} and the candidate summary is: {resume_summary}.

    Ensure the questions are thoughtful, focus on key competencies for the role, and maintain a professional tone throughout.
    Do not start the responses with sure or certainly.
    """

def prompt_without_answers(interview_type, question_count, input_contents, resume_summary):
    return f"""
    You are an experienced interview assistant helping managers prepare tailored interview questions. 
    The manager will provide you with a job title and a description, and you will create a list of relevant questions to guide the interview process.

    Please generate a set of {question_count} high-quality questions for a {interview_type} interview. 

    The position and desription being interviewed for is: {input_contents} and the candidate summary is: {resume_summary}.

    Ensure the questions are thoughtful, focus on key competencies for the role, and maintain a professional tone throughout.
    Do not start the responses with sure or certainly.
    """

tips_text = f"""<b>During the interview:</b><br />
- Dress professionally: Make a good first impression with appropriate attire. <br />
- Be punctual: Arrive on time or a few minutes early. <br />
- Maintain good eye contact: Show engagement and confidence. <br />
- Speak clearly and confidently: Project a positive and enthusiastic demeanor. <br />
- Listen attentively: Pay close attention to the interviewer's questions and respond thoughtfully. <br />
- Highlight your skills and experiences: Relate your qualifications to the job requirements. <br />
- Ask questions: Show your interest by asking questions about the role, company, and team. <br />
"""