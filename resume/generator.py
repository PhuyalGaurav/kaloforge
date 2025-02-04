from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS


def generate_pdf_template_1(
    data, template_path="./templates/generator/template1.html", output_path="output.pdf"
):
    env = Environment(
        loader=FileSystemLoader("resume/templates/generator"),
        trim_blocks=False,
        lstrip_blocks=False,
    )
    template = env.get_template("template1.html")
    print(data)
    html_out = template.render(item=data)

    css = CSS(
        string="""
        @page { size: A4; margin: 0; }
        body { width: 210mm; height: 297mm; margin: 0; padding: 0; }
        img { max-width: 100%; }
    """
    )

    HTML(string=html_out, base_url=".").write_pdf(
        output_path,
        stylesheets=[css],
        zoom=1,
    )

    print("PDF generated successfully!")
