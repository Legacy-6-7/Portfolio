from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.html import escape
from django.views.decorators.http import require_POST
import resend
import uuid


def home(request):
    return render(request, "home.html")


@require_POST
def contact(request):
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    message = request.POST.get("message", "").strip()

    submission_id = request.POST.get("submission_id")

    if not submission_id:
        submission_id = str(uuid.uuid4())

    # Basic validation
    if not name or not email or not message:
        return redirect("home")

    # Escape user input before putting it into HTML
    safe_name = escape(name)
    safe_email = escape(email)
    safe_message = escape(message).replace("\n", "<br>")

    # HTML email
    notification_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>New Portfolio Contact</title>
    </head>

    <body style="
        margin: 0;
        padding: 30px;
        background-color: #f4f4f4;
        font-family: Arial, Helvetica, sans-serif;
    ">

        <div style="
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        ">

            <h1 style="
                margin-top: 0;
                color: #222222;
            ">
                New Portfolio Contact
            </h1>

            <hr style="
                border: none;
                border-top: 1px solid #eeeeee;
                margin: 20px 0;
            ">

            <p>
                <strong>Name:</strong><br>
                {safe_name}
            </p>

            <p>
                <strong>Email:</strong><br>
                {safe_email}
            </p>

            <p>
                <strong>Message:</strong>
            </p>

            <div style="
                background-color: #f7f7f7;
                border-left: 4px solid #3531C8;
                padding: 15px;
                margin: 10px 0 25px 0;
                border-radius: 6px;
                color: #333333;
            ">
                {safe_message}
            </div>

            <p style="
                font-size: 13px;
                color: #777777;
            ">
                <strong>Submission ID:</strong><br>
                {submission_id}
            </p>

            <hr style="
                border: none;
                border-top: 1px solid #eeeeee;
                margin: 20px 0;
            ">

            <p style="
                font-size: 13px;
                color: #777777;
            ">
                You can reply directly to this email to respond to the visitor.
            </p>

        </div>

    </body>
    </html>
    """

    # Plain-text fallback
    notification_text = f"""
New Portfolio Contact

Name: {name}

Email: {email}

Message:
{message}

Submission ID:
{submission_id}

Reply directly to this email to respond to the visitor.
"""

    try:
        resend.api_key = settings.RESEND_API_KEY

        result = resend.Emails.send({
            "from": settings.RESEND_FROM_EMAIL,
            "to": [settings.CONTACT_EMAIL],
            "reply_to": email,
            "subject": f"Portfolio Contact from {name} [{submission_id}]",
            "html": notification_html,
            "text": notification_text,
        })

        print("RESEND NOTIFICATION RESULT:", result)
        print("EMAIL SENT SUCCESSFULLY")

    except Exception as e:
        print("RESEND EMAIL ERROR:", repr(e))
        raise

    return redirect("home")

