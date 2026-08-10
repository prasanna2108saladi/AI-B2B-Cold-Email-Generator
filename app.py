import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found. Please check your .env file.")
    st.stop()

# Create Groq client
client = Groq(api_key=api_key)

# Page configuration
st.set_page_config(
    page_title="AI Cold Email Generator",
    page_icon="📧",
    layout="centered"
)

# Application title
st.title("📧 AI Cold Email Generator")

st.write(
    "Generate personalized B2B cold emails from a client's job posting."
)

# Company name
company_name = st.text_input(
    "🏢 Client Company Name",
    placeholder="Example: Nike"
)

# Job description
job_description = st.text_area(
    "📋 Paste the Job Description",
    height=350,
    placeholder="""Paste the client's job posting here.

Example:

We are looking for a Senior Python Developer.

Requirements:
- Python
- FastAPI
- REST APIs
- PostgreSQL
- AWS
- Docker
- 5+ years of experience
"""
)

# Services company name
service_company = st.text_input(
    "💼 Your Company Name",
    placeholder="Example: ABC Technologies"
)

# Generate email
if st.button("🚀 Generate Cold Email"):

    if not company_name.strip():
        st.warning("Please enter the client company name.")
        st.stop()

    if not job_description.strip():
        st.warning("Please paste the job description.")
        st.stop()

    if not service_company.strip():
        st.warning("Please enter your company name.")
        st.stop()

    # Prompt
    prompt = f"""
You are a senior Business Development Executive working
for a software development and IT services company.

Your task is to write a professional, detailed B2B cold
email to a potential client based on their job requirement.

The client has posted a job requirement because they
currently need technical resources for their project.

Our company provides software development professionals
and technical resources on a contract, project-based,
or staff-augmentation basis.

CLIENT COMPANY:
{company_name}

OUR COMPANY:
{service_company}

CLIENT JOB REQUIREMENT:
{job_description}

Your objective:

Write a persuasive cold email explaining that we are
interested in supporting the client's project and that
our organization has professionals whose skills and
technical expertise can match the requirements mentioned
in their job posting.

The email should communicate that instead of spending
additional time recruiting full-time employees, the
client can consider using our experienced technical
resources on a flexible contract or project basis.

EMAIL REQUIREMENTS:

1. Carefully analyze the job requirement.

2. Identify the main role, technologies, technical skills,
   experience requirements, and project needs mentioned
   in the requirement.

3. Start the email by naturally referring to the client's
   job requirement.

4. Explain that our company is interested in supporting
   the client's project.

5. Explain that we have software professionals whose
   skills can align with the technologies and requirements
   mentioned in the job posting.

6. Position our employees as contract/project-based
   engineering resources rather than job applicants.

7. Explain the potential benefits of this model, such as:
   - faster access to technical talent
   - flexible scaling of engineering resources
   - reduced recruitment effort
   - project-focused technical support
   - access to specialized skills

8. Do not claim that we have worked with the client
   previously unless explicitly stated.

9. Do not invent clients, projects, certifications,
   technologies, achievements, or years of experience
   for our company.

10. Do not claim that our employees definitely possess
    a specific skill unless it can reasonably be inferred
    from the information provided.

11. The email should be detailed and persuasive, around
    250-350 words.

12. The tone should be:
    professional,
    confident,
    consultative,
    business-oriented,
    and respectful.

13. Do not make the email sound like spam or aggressive
    advertising.

14. Do not repeatedly use phrases such as "we would love
    to" or "we are the best".

15. Clearly explain how our company could help the client
    meet their technical staffing requirements.

16. End with a professional call to action suggesting
    a short discussion or meeting to understand the
    client's requirements in more detail.

17. Create a professional subject line.

Return the result exactly in this format:

Subject:
<subject>

Email:
<email body>
"""

    # Generate response
    with st.spinner("🤖 Analyzing job requirements..."):

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert B2B technology sales "
                        "and business development assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5
        )

    generated_email = response.choices[0].message.content

    # Display result
    st.subheader("📨 Generated Cold Email")

    st.text_area(
        "Email",
        generated_email,
        height=350
    )

    st.success("Cold email generated successfully!")