import streamlit as st
import texts
import PDF_maker
import resume_handlers
import openai

from openai import OpenAI
from dotenv import load_dotenv

from streamlit_extras.stylable_container import stylable_container


#  python -m streamlit run app.py


# function for chainging the states
def set_state(i):
    st.session_state.stage = i

def back_button():
    st.session_state.stage -= 1


def create_main_frame():
    
    if 'stage' not in st.session_state:
        st.session_state.stage = 0

    st.set_page_config(page_title="HireWiser", page_icon="✨")


    # Initialize the progress bar
    progress_bar = st.progress(0)
     # progress bar color
    st.markdown(
            """
            <style>
                .stProgress > div > div > div > div {
                    background-color: #ff5400;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
    
    # color of the sidebar
    st.html(
    """
    <style>
    [data-testid="stSidebarContent"] {
        color: white;
        background-color: #83c5be;
    }
    </style>
    """
    )

    st.markdown("""
    <style>
        button {
            font-size: 14px !important;
            font-weight: bold !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # if st.session_state.stage == 0:

    #     #progress_bar.progress((st.session_state.stage+1)*15)
    #     col011, col012, col013 = st.columns([0.5, 1, 0.5])
    #     with col011: 
    #         st.markdown('')
    #         st.markdown("""
    #         <style>
    #         .reportview-container {
    #             background-color: #ff5400
    #         }
    #         </style>
    #         """, unsafe_allow_html=True)
    #     with col012: 
    #         st.image('img/logo.gif') 

    #     with col013: 
    #         st.markdown(' ')

    #     # Ask the user's api key
    #     # with st.form('form'):

    #     st.info('🗝️Please add your OpenAI API key to continue.')
    #     openai_text_area = st.text_input('Enter Your OpenAI API token:', '', type='password')
    #     st.session_state['openai_key'] = openai_text_area

    #     st.button('Submit', on_click=set_state, args=[1], use_container_width=True)
    #     #       st.session_state['openai_key'] = openai_text_area

        
     
    if st.session_state.stage == 0:
        progress_bar.progress((st.session_state.stage+1)*15)

        col011, col012, col013 = st.columns([1, 1, 1])
        with col011: 
            st.markdown('')
        with col012: 
            st.image('img/logo.gif') 
        with col013: 
            st.markdown(' ')

        st.markdown("<p style='color:#00072d; text-align: center; font-size:50px; font-family:'Pacifito', cursive;' > <b> Connecting Candidates to Their Dream Jobs </b> </p>", unsafe_allow_html=True)
        st.markdown("<p style='color:#00072d; text-align: center; font-size:20px; font-family:'Pacifito', cursive;' > <b> Find the perfect job match for your candidates with AI-powered interview preparation. </b> </p>", unsafe_allow_html=True)


        with st.sidebar:

            # openai_text_area = st.text_input('OpenAI Key', '')
            # st.session_state['openai_key'] = openai_text_area

            job_title_text_area = st.text_input('Job Title', 'Data Scientist')
            st.session_state['job_title'] = job_title_text_area
        
            job_desc_text_area = st.text_area('Job Description' , texts.job_description , height = 340)
            st.session_state['job_description'] = job_desc_text_area


        # to put the button in the middle
        col021, col022, col023 = st.columns([2, 1, 2])
        with col021:
            st.markdown(' ')
        with col022:
            with stylable_container(
                "green",
                css_styles="""
                button {
                    background-color: #FFFFFF;
                    color: #ff5400;
                }
                button:hover {
                    background-color: #ff5400;
                    color: #ff5400;
                }
                """,
            ):
                if st.button(f"Get Started", key="button", on_click=set_state, args=[1], use_container_width=True):
                    st.session_state['job_title'] = job_title_text_area
                    st.session_state['job_description'] = job_desc_text_area

        with col023:
            st.markdown(' ') 

        
    if st.session_state.stage == 2:
        progress_bar.progress((st.session_state.stage+1)*15)
        # Create a layout with two columns for back button
        cols = st.columns([1, 7])

        # Display back button
        with cols[0].container():
                st.button("← Back", on_click=back_button, use_container_width=True)

        st.header('Step 1: Upload Candidate Resume...')
        #st.write(f"You saved: {st.session_state.job_title} and {st.session_state.job_description}")

        st.markdown('Provide the candidate\'s resume, and we\'ll summarize it for a quick review.')

        resume_summary = ""

        st.info('To ensure the best results, please upload resumes in a standard format (PDF, DOCX) with clear sections like Work Experience, Skills, and Education. \n This helps our system generate an accurate summary and relevant interview questions.')

        col1, col2= st.columns([1, 1])


        with st.sidebar:
        
            uploaded_file = st.file_uploader("Upload Resume", type=['pdf', 'docx'])

        if uploaded_file:
            with st.expander('Resume Summary', expanded=True):
                st.success('Your resume is successfully uploaded!')
                with st.spinner():
                    full_resume = resume_handlers.read_resume(uploaded_file)
                    resume_summary = resume_handlers.summarise_resume(full_resume, st.session_state['openai_key'])
                    st.session_state['candidate_name'] = resume_handlers.extract_candidate_name(full_resume, st.session_state['openai_key'])
                    

                    st.button('Confirm the Summary', key="button", on_click=set_state, args=[3], use_container_width=True)                           
                                        
                    st.text_area("Resume Summary", resume_summary, height=200)
                    st.session_state['resume_summary'] = resume_summary


    if st.session_state.stage == 3:
        progress_bar.progress((st.session_state.stage+1)*15)
        
        st.sidebar.write(" ")

        # Create a layout with two columns for back button
        cols = st.columns([1, 7])

        # Display back button
        with cols[0].container():
            st.button("← Back", on_click=back_button, use_container_width=True)

        st.header("Step 2: Let's Review Candidate Information")
        st.markdown("Here’s what you’ve provided so far. Make sure everything is correct.")

        # Initialize session state if not already done
        if 'candidate_name' not in st.session_state:
            st.session_state['candidate_name'] = ""
        if 'job_title' not in st.session_state:
            st.session_state['job_title'] = ""
        if 'job_description' not in st.session_state:
            st.session_state['job_description'] = ""


        st.button('Proceed to Interview Preparation', key='proceed_button', on_click=set_state, args=[4], use_container_width=True)


        st.subheader("General Information")

        col211, col212= st.columns([1, 1])
        with col211:
            candidate_name_text_input = st.text_input('Candidate Name', value = st.session_state['candidate_name'])
        with col212:
            job_title_text_input = st.text_input('Job Title', value = st.session_state['job_title'])
        job_description_text_area = st.text_area('Job Description', value = st.session_state['job_description'], height=150)
            
        
        # Draw a horizontal line
        st.divider()

        st.subheader("Resume")
        st.text_area('Resume Summary', value = st.session_state['resume_summary'], height=200)
        

    if st.session_state.stage == 4:

        progress_bar.progress((st.session_state.stage+2)*15)

        st.sidebar.write(" ")

        # Create a layout with two columns for back button
        cols = st.columns([1, 7])

        # Display back button
        with cols[0].container():
            st.button("← Back", on_click=back_button, use_container_width=True)

        st.header("Step 3 - Finalize it...")
        st.markdown("Choose the number of questions and interview type. Get question-answer pairs and a similarity score between the job description and resume.")

        st.session_state.interview_questions = ''
        st.session_state.similarity_score = ''

        st.markdown(f"{st.session_state['candidate_name']}")

        col311, col312 = st.columns([1, 1])

        with col311: 
            interview_type = st.selectbox('Interview Type',
                                        ('General', 'Technical'),
                                        index=0)
        with col312:
            question_count = st.selectbox('Question Count', ('2', '3', '4', '5', '6', '7', '8', '9', '10'), index=0)

        provide_answers = st.checkbox('Provide Sample Answers')

        # st.markdown(f'Job title: {st.session_state.job_title}')
        # st.markdown(f'Job description: {st.session_state.job_description}')

        if st.button('Generate Questions and Evaluate', use_container_width=True):
            with st.spinner():

                input_contents = []  # let the user input all the data
                if (st.session_state.job_title != ""):
                    #st.markdown('job title provided')
                    input_contents.append(str(st.session_state.job_title))
                if (st.session_state.job_description != ""):
                    #st.markdown('job description provided')
                    input_contents.append(str(st.session_state.job_description))
                    #st.markdown(input_contents)
                if (len(input_contents) == 0):  # remind user to provide data
                    st.write('Please fill in some contents for your message!')


                if (len(input_contents) >= 1):  # initiate llm
                    if (len(interview_type) != 0) and (len(question_count) != 0):
                        #st.markdown(f'Function Inputs: {interview_type}, {question_count}, {input_contents}, {provide_answers}, {st.session_state.resume_summary}')
                        st.session_state.interview_questions = resume_handlers.generate_questions(interview_type, 
                                                                question_count, 
                                                                input_contents, 
                                                                provide_answers,
                                                                st.session_state.resume_summary, st.session_state['openai_key'])
                        st.session_state.similarity_score = resume_handlers.compute_similarity(st.session_state.job_description, st.session_state.resume_summary, st.session_state['openai_key'])
                                                                            
                    
        if st.session_state.interview_questions != "":
            with st.expander("Interview Questions", expanded=True):
                st.markdown(st.session_state.similarity_score) 
                st.markdown(st.session_state.interview_questions)
                  
                pdf_sections = [
                        ("Resume Summary",  st.session_state.resume_summary),
                        ("List of Questions", st.session_state.interview_questions),
                        ("Similarity Score", st.session_state.similarity_score)
                    ]
                
                filename = PDF_maker.generate_filename('HireWiser')
                PDF_maker.create_pdf(filename, pdf_sections, candidate_name=st.session_state['candidate_name'])

                with open(filename, 'rb') as download_file:
                    st.download_button('Download Full Report', data=download_file, file_name=filename, use_container_width=True)


if __name__ == '__main__': 
    # call main function
    create_main_frame()
