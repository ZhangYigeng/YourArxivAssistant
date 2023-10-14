import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
import re

def load_papers_from_local():
    todays_date = datetime.now().strftime("%Y-%m-%d")
    # todays_date = 'Thu, 12 Oct 2023' # test
    filename = f"/home/ubuntu/Work/paper_collections/matched_papers_{todays_date}.json"
    
    with open(filename, 'r') as file:
        papers = json.load(file)
    
    return papers


def highlight_text(text, terms, color="yellow"):
    """Highlight specific terms in a text with a given color."""
    for term in terms:
        term_pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
        text = term_pattern.sub(f'<span style="background-color: {color}">{term}</span>', text)
    return text


def generate_html_from_papers(matched_papers, interesting_authors=[], interesting_keywords=[]):
    html_content = "<html><body><h2>Today's Papers</h2><ul>"

    for paper in matched_papers:
        highlighted_title = highlight_text(paper['title'], interesting_keywords, color="#A3E4D7")
        
        authors_list = []
        for author in paper['authors']:
            if any(term.lower() in author.lower() for term in interesting_authors):
                authors_list.append(highlight_text(author, interesting_authors, color="#85C1E9"))
            else:
                authors_list.append(author)
        highlighted_authors = ", ".join(authors_list)

        html_content += "<li>"
        html_content += f"<strong>{highlighted_title}</strong><br/>"
        html_content += highlighted_authors
        html_content += f"<br/><a href='https://arxiv.org{paper['identifier']}'>Link</a>"
        html_content += "</li>"

    html_content += "</ul></body></html>"

    return html_content


def send_email(subject, body, to_email, sender_email, sender_password):
    # Gmail account credentials
    gmail_user = sender_email
    gmail_app_password = sender_password  # Use the App Password you generated earlier

    # Create email content
    msg = MIMEText(body, 'html')  # 'html' as second argument indicates the content type
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = to_email

    # Connect to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_app_password)
        server.send_message(msg)

    print('Email sent successfully!')



