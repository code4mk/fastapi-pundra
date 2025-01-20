from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
from .mail_templating import EmailTemplates
from fastapi_pundra.common.helpers import base_path
import os
from pydantic import EmailStr, BaseModel
from typing import List

# Load environment variables from .env file
load_dotenv()


# Configure email connection
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_FROM_ADDRESS'),  # Ensure this is a valid email address
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_SERVER=os.getenv('MAIL_HOST'),
    MAIL_STARTTLS=False,  # or False based on your configuration
    MAIL_SSL_TLS=False,   # or False based on your configuration
    USE_CREDENTIALS=True
)

def render_mail_template(template_name: str, context: dict = {}):
    # Initialize EmailTemplates with the correct directory
    template_dir = os.path.join(base_path(), 'app', 'templates', 'mails')
    templates = EmailTemplates(directory=template_dir)
    # Render the specified template with the given context
    return templates.render_template(template_name, context)

async def send_mail(subject, to, template_name, context=None):
    try:
        # Cast 'to' parameter to a list
        if not isinstance(to, list):
            to = [to]  # Convert to list
        
        # Prepare the email message
        message = MessageSchema(
            subject=subject,
            recipients=to,
            body=render_mail_template(template_name=template_name, context=context),
            subtype="html"
        )
        
        # Send the email
        fm = FastMail(conf)
        await fm.send_message(message)
        
        return "Email has been sent"
    except Exception as e:
        return f'An error occurred while sending the email: {str(e)}'