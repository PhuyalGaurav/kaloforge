from django.conf import settings
import openai

openai.api_key = settings.API_KEY

def generate_resume(job_title, user_details):

    response = openai.Completion.create(
        model="gpt-4o-mini",
        prompt=f"Generate a resume for a {job_title} with the following details: {user_details}",
        max_tokens=150
    )

    return response.choices[0].text.strip()

# Example usage
print(generate_resume("Software Engineer", "Name: John Doe, Experience: 5 years, Skills: Python, Django, React"))