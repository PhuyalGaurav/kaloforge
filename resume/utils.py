from openai import OpenAI
from django.conf import settings
import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
import boto3
from botocore.exceptions import ClientError
from io import BytesIO
import uuid

API_KEY = settings.OPENAI_API_KEY
client = OpenAI(
    api_key=API_KEY,
)

formats = [
    {
        "name": "",
        "image": "",  # Profile picture URL
        "contact": {"email": "", "phone": ""},
        "professional_summary": "",  # Profile section
        "skills": [],  # List of skills in sidebar
        "languages": [],  # List of languages in sidebar
        "work_history": [
            {
                "job_title": "",
                "company_name": "",
                "time_employed": "",
                "description": "",  # Single description instead of responsibilities list
            }
        ],
        "education": [
            {
                "school_name": "",
                "time_period": "",  # Only school name and time period needed
            }
        ],
        "projects": [
            {
                "project_name": "",
                "description": "",
                "technologies": [],  # List of technologies used
            }
        ],
    },
    {
        "name": "",
        "image": "",  # Added for profile picture
        "contact": {"email": "", "phone": ""},
        "professional_summary": "",
        "skills": [],  # List of skill strings
        "education": [{"degree": "", "school_name": "", "time_period": ""}],
        "work_history": [
            {
                "job_title": "",
                "company_name": "",
                "time_employed": "",
                "responsibilities": [],  # List of responsibility strings
            }
        ],
        "projects": [
            {
                "project_name": "",
                "description": "",
                "technologies": [],  # List of technology strings
            }
        ],
    },
]


def generate_data(details, resume_format):
    try:
        # Format input details into clear key-value pairs
        formatted_details = {}
        for line in details.split(","):
            line = line.strip()
            if ":" not in line:
                continue
            parts = line.split(":", 1)  # Split only on first colon
            if len(parts) == 2:
                key, value = parts
                formatted_details[key.strip()] = value.strip()

        # Create structured data matching the resume format
        result = resume_format.copy()
        result.update(
            {
                "name": formatted_details.get("Name", ""),
                "image": formatted_details.get("image", ""),
                "contact": {
                    "email": formatted_details.get("Email", ""),
                    "phone": formatted_details.get("Phone", ""),
                },
                "professional_summary": formatted_details.get("Summary", ""),
                "skills": [
                    skill.strip()
                    for skill in formatted_details.get("Skills", "").split(";")
                    if skill.strip()
                ],
                "languages": [
                    lang.strip()
                    for lang in formatted_details.get("Languages", "").split(";")
                    if lang.strip()
                ],
                "work_history": (
                    [
                        {
                            "job_title": formatted_details.get("Experience", "")
                            .split(" at ")[0]
                            .strip(),
                            "company_name": (
                                formatted_details.get("Experience", "")
                                .split(" at ")[-1]
                                .split(" - ")[0]
                                .strip()
                                if " at " in formatted_details.get("Experience", "")
                                else ""
                            ),
                            "time_employed": (
                                formatted_details.get("Experience", "")
                                .split(" - ")[-1]
                                .strip()
                                if " - " in formatted_details.get("Experience", "")
                                else ""
                            ),
                            "responsibilities": [
                                formatted_details.get("Experience", "")
                            ],
                        }
                    ]
                    if formatted_details.get("Experience")
                    else []
                ),
                "education": (
                    [
                        {
                            "school_name": formatted_details.get("Education", "")
                            .split(" - ")[0]
                            .strip(),
                            "time_period": (
                                formatted_details.get("Education", "")
                                .split(" - ")[-1]
                                .strip()
                                if " - " in formatted_details.get("Education", "")
                                else ""
                            ),
                        }
                    ]
                    if formatted_details.get("Education")
                    else []
                ),
                "projects": [
                    {
                        "project_name": proj.split(":")[0].strip(),
                        "description": proj.split(":")[-1].strip(),
                        "technologies": [],
                    }
                    for proj in formatted_details.get("Projects", "").split(";")
                    if ":" in proj
                ],
            }
        )

        # Create enhancement prompt with the structured data
        enhancement_prompt = (
            f"Enhance this resume content while maintaining the structure:\n{json.dumps(result, indent=2)}\n\n"
            "Instructions:\n"
            "1. Keep all existing information\n"
            "2. Enhance the language to be more professional\n"
            "3. Add impactful details where possible\n"
            "4. Return the enhanced content as valid JSON\n"
            "5. Match the exact structure provided"
        )

        enhancement_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert resume writer. Enhance the content while maintaining accuracy and structure.",
                },
                {"role": "user", "content": enhancement_prompt},
            ],
            max_tokens=2000,
            temperature=0.7,
        )

        response_text = enhancement_response.choices[0].message.content.strip()
        print(f"Enhancement response: {response_text}")

        try:
            enhanced_data = json.loads(response_text)
            if validate_resume_data(enhanced_data):
                return enhanced_data
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing enhanced data: {str(e)}")
            return result

        return result

    except Exception as e:
        print(f"Error in generate_data: {str(e)}")
        return resume_format


def generate_html_template_1(data, num=1):
    env = Environment(
        loader=FileSystemLoader("resume/templates/generator"),
        trim_blocks=False,
        lstrip_blocks=False,
    )
    template = env.get_template(f"template{num}.html")
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
            # Upload without ACL
            s3_client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=s3_key,
                Body=pdf_data,
                ContentType="application/pdf",
                ContentDisposition=f'inline; filename="{filename}"',
            )

            # Generate permanent URL
            url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}"
            return url

        except ClientError as e:
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


def upload_image_to_s3(image_file, filename=None):
    """Generate image URL from file and upload to S3."""
    try:
        if filename is None:
            file_extension = image_file.name.split(".")[-1].lower()
            if file_extension not in ["jpg", "jpeg", "png", "gif"]:
                print(f"Invalid file extension: {file_extension}")
                return None
            filename = f"profile_{uuid.uuid4()}.{file_extension}"

        # Match the same path structure as PDF uploads
        s3_key = (
            f"media/resumes/images/{filename}"  # Changed path to match PDF structure
        )

        # Create S3 client with basic configuration
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
            config=boto3.session.Config(signature_version="s3v4"),
        )

        try:
            # Reset file pointer
            image_file.seek(0)

            # Upload using exact same configuration as PDF
            s3_client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=s3_key,
                Body=image_file.read(),
                ContentType=f"image/{file_extension}",
                ContentDisposition=f'inline; filename="{filename}"',
            )

            # Use exact same URL format as PDF
            url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}"
            print(f"Successfully uploaded image: {url}")
            return url

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            error_message = e.response.get("Error", {}).get("Message", str(e))
            print(f"S3 upload failed: {error_code} - {error_message}")
            return None

    except Exception as e:
        print(f"Unexpected error in upload_image_to_s3: {str(e)}")
        return None


def validate_resume_data(data):
    """Validate resume data to ensure no placeholder content exists."""
    placeholder_patterns = [
        r"\[.*?\]",  # Matches anything in square brackets
        r"company name",
        r"job title",
        r"month, year",
        r"specific project",
        r"quantifiable",
        r"number",
        r"percentage",
    ]

    def check_text(text):
        if not isinstance(text, str):
            return True
        text = text.lower()
        return not any(pattern in text.lower() for pattern in placeholder_patterns)

    def validate_dict(d):
        for value in d.values():
            if isinstance(value, dict):
                if not validate_dict(value):
                    return False
            elif isinstance(value, list):
                if not validate_list(value):
                    return False
            elif not check_text(value):
                return False
        return True

    def validate_list(lst):
        for item in lst:
            if isinstance(item, dict):
                if not validate_dict(item):
                    return False
            elif isinstance(item, list):
                if not validate_list(item):
                    return False
            elif not check_text(item):
                return False
        return True

    return validate_dict(data)
