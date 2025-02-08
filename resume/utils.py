from openai import OpenAI
from django.conf import settings
import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
import boto3
from io import BytesIO
import uuid

API_KEY = settings.OPENAI_API_KEY
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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1500,
    )
    return json.loads(response.choices[0].message.content.strip())


def generate_html_template_1(data):
    env = Environment(
        loader=FileSystemLoader("resume/templates/generator"),
        trim_blocks=False,
        lstrip_blocks=False,
    )
    template = env.get_template("template1.html")
    html_out = template.render(item=data)
    return html_out


def generate_pdf_from_html(html_content, filename=None):
    """Generate PDF from HTML and upload to S3."""
    try:
        # Step 1: Generate PDF
        success, message, pdf_data = test_pdf_generation(html_content)
        if not success:
            return f"PDF Generation failed: {message}"

        if filename is None:
            filename = f"resume_{uuid.uuid4()}.pdf"

        # Step 2: Upload to S3
        s3_key = f"media/resumes/{filename}"

        # Create S3 client with basic configuration
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
            config=boto3.session.Config(signature_version="s3v4"),
        )

        try:
            # Upload with specific configuration
            s3_client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=s3_key,
                Body=pdf_data,
                ContentType="application/pdf",
                ServerSideEncryption="AES256",  # Enable server-side encryption
                ContentDisposition=f'inline; filename="{filename}"',
            )

            # Generate pre-signed URL for temporary access
            url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": s3_key},
                ExpiresIn=3600,  # URL expires in 1 hour
            )

            return url

        except boto3.exceptions.ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            error_message = e.response.get("Error", {}).get("Message", str(e))
            return f"S3 upload failed ({error_code}): {error_message}"

    except Exception as e:
        return f"Unexpected error: {str(e)}"


def test_aws_upload():
    """
    Test function to verify AWS S3 upload functionality.
    Returns a tuple of (success:bool, message:str)
    """
    try:
        # Create a small test file in memory
        test_content = b"Test file content"
        test_buffer = BytesIO(test_content)
        test_filename = f"test_{uuid.uuid4()}.txt"
        s3_key = f"media/test/{test_filename}"

        # Verify AWS credentials are present
        if not all(
            [
                settings.AWS_ACCESS_KEY_ID,
                settings.AWS_SECRET_ACCESS_KEY,
                settings.AWS_STORAGE_BUCKET_NAME,
                settings.AWS_S3_REGION_NAME,
            ]
        ):
            return False, "Missing AWS credentials"

        # Initialize S3 client
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        # Try uploading
        s3_client.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=s3_key,
            Body=test_buffer.getvalue(),
            ContentType="text/plain",
        )

        # Verify upload
        s3_client.head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_key)

        # Clean up - delete test file
        s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_key)

        return True, f"Successfully uploaded and deleted test file: {s3_key}"

    except Exception as e:
        return False, f"AWS Upload test failed: {str(e)}"


def test_pdf_generation(html_content=None):
    """
    Test function to verify PDF generation functionality.
    Returns a tuple of (success:bool, message:str, pdf_data:bytes|None)
    """
    try:
        # Use sample HTML if none provided
        if html_content is None:
            html_content = """
            <html>
                <body>
                    <h1>Test PDF Generation</h1>
                    <p>This is a test document.</p>
                </body>
            </html>
            """

        css = CSS(
            string="""
            @page { size: A4; margin: 0; }
            body { width: 210mm; height: 297mm; margin: 0; padding: 0; }
            img { max-width: 100%; }
            """
        )

        pdf_buffer = BytesIO()
        HTML(string=html_content, base_url=".").write_pdf(
            pdf_buffer,
            stylesheets=[css],
            zoom=1,
        )
        pdf_buffer.seek(0)

        # Read first few bytes to verify PDF header
        pdf_header = pdf_buffer.read(4)
        if pdf_header != b"%PDF":
            return False, "Generated file is not a valid PDF", None

        pdf_buffer.seek(0)
        return True, "PDF generated successfully", pdf_buffer.getvalue()

    except Exception as e:
        return False, f"PDF generation failed: {str(e)}", None
