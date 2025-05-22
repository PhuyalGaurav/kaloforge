# CS50W Final Project | Kaloforge  
**AI-Powered Resume & Cover Letter Generator**

## Project Overview

Kaloforge is a web application designed to streamline the job application process by automatically generating personalized resume. Users input job-related details such as the title and description, and Kaloforge uses OpenAI’s GPT-3.5 model to generate tailored application materials. This tool aims to assist job seekers in crafting professional documents with minimal effort while maintaining customization and quality.

Kaloforge also allows users to download resumes as PDFs, choose from multiple resume templates, and create accounts to save and revisit previously generated documents.

---

## Distinctiveness and Complexity

Kaloforge is distinct from all previous CS50W projects in both concept and implementation. While Project 2 (E-commerce) and Project 4 (Network) focus on user interactions, social features, or product listings, Kaloforge tackles a completely different problem: AI-powered document generation for job seekers. This focus on natural language generation using external APIs—specifically the OpenAI API—makes Kaloforge unique.

One of the most challenging and innovative parts of the project was the integration of the OpenAI API (GPT-3.5). Unlike traditional CRUD operations found in typical Django apps, Kaloforge required sending dynamic prompts to an AI model, handling large response payloads, sanitizing the output, and rendering it as structured resume content. This required careful prompt engineering and formatting logic to ensure the AI-generated text matched professional standards.

Another major area of complexity was in supporting **multiple resume templates** and generating downloadable **PDFs**. This meant developing a system that could take AI-generated content and dynamically fit it into different layouts, while maintaining visual integrity across formats. Creating printable, styled PDFs on the server-side using Django involved challenges such as HTML-to-PDF rendering and asset handling.

The application also includes full **user authentication**, allowing users to create accounts, log in securely, and view their previously generated resumes. Django's built-in auth system was extended to support user-specific resume storage and retrieval.

Frontend interactivity was implemented using **JavaScript**, which handles template switching, live previews, and dynamic updates to improve the user experience. A great deal of time was also spent on **UI/UX design**—making the site not only functional but also clean, modern, and responsive across devices using Bootstrap.

Together, these elements make Kaloforge far more complex and distinctive than any project provided in the course. It combines AI technology, back-end logic, user authentication, responsive front-end design, and PDF generation into one cohesive and practical tool.

---

## Features

- **AI-Generated Content**: Automatically create resumes and cover letters based on job descriptions.
- **PDF Download**: Download your resume in PDF format with a single click.
- **Multiple Templates**: Choose from different resume styles to match your preferences.
- **User Accounts**: Register/login to save and access past resumes.
- **Responsive UI**: Works well on desktop, tablet, and mobile devices.
- **Homepage Dashboard**: A homepage where users can view all their previously generated resumes displayed in an attractive and organized layout.

---

## **Collaborators**
- **[Gaurav Phuyal]("https://github.com/phuyalgaurav")**
- **[Shuva Aashish Gyawali]("https://github.com/shuvaaashish")**

---
  ## Acknowledgments

We would like to extend our heartfelt thanks to the entire CS50 team for designing such a well-structured and enriching course. **CS50's Web Programming with Python and JavaScript (CS50W)** has been one of the most comprehensive learning experiences we've had, covering everything required for developing a dynamic and responsive web app.

The course didn't just teach us how to code—it helped us understand how to build complete, scalable, and user-friendly web applications. From writing models in Django to handling front-end logic and deploying applications, every project challenged us to think critically and grow as developers.

A special thanks to **[Brian Yu]("https://github.com/brianyu28")**, whose clear explanations, structured lectures, and thoughtful project design made complex topics accessible and enjoyable. His teaching played a major role in helping us build the skills and confidence needed to take on independent projects like Kaloforge.

