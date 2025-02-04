from openai import OpenAI
from django.conf import settings
from .generator import generate_pdf_template_1

API_KEY = settings.OPENAI_API_KEY
# API_KEY = "asd"
client = OpenAI(
    api_key=API_KEY,
)

formats = [
    {
        "name": "",
        "contact": {"email": ""},
        "professional_summary": "",
        "skills": ["skill 1", "skill 2", "skill 3", "skill 4", "etc..."],
        "work_history": [
            {
                "job_title": "job title 1",
                "company_name": "company name",
                "time_employed": "",
                "responsibilities": [
                    "responsibility 1",
                    "responsibility 2",
                    "responsibility 3",
                    "etc...",
                ],
            },
            {
                "job_title": "job title 2",
                "company_name": "company name",
                "time_employed": "",
                "responsibilities": [
                    "responsibility 1",
                    "responsibility 2",
                    "responsibility 3",
                ],
            },
        ],
        "education": [
            {
                "school_name": "",
                "degree": "",
                "time_period": "",
            },
            {
                "school_name": "",
                "degree": "",
                "time_period": "",
            },
        ],
        "projects": [
            {
                "project_name": "",
                "description": "",
                "technologies": ["tech 1", "tech 2", "tech 3", "etc..."],
            },
            {
                "project_name": "",
                "description": "",
                "technologies": ["tech 1", "tech 2", "tech 3", "etc..."],
            },
        ],
    }
]


def generate_data(details, resume_format=formats[0]):
    prompt = f"{details} please only keep it my details no false information, But make me look like the best pick among others and use professional language. dont give me things that i have not said so PLEASE USE NONE IF YOU DON'T HAVE ANY INFO)"
    system_content = f"You are a helpful assistant who makes resumes for only the best people. Only use the provided information and do not generate any false information. You only reply in terms of json with key value pairs where keys are in small case in the format: {resume_format} (!! IMPORTANT !! ONLY A FORMAT DON'T USE ANY OF THIS INFORMATION DON'T EVER STRAY FROM THE FORMAT (You can add more school, education, work history or less depending on the details if none give empty but don't use the template or imaginary info don't return the format itself) & NO FALSE INFO PLEASE USE NONE IF YOU DON'T HAVE ANY INFO)"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating text: {e}")
        return None
