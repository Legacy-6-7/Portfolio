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
        background-color: #ececec;
        font-family: Arial, Helvetica, sans-serif;
    ">

        <div style="
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.12);
        ">

            <div style="
                background-color: #23232a;
                padding: 28px 30px;
                border-bottom: 4px solid #ff7a1a;
            ">
                <h1 style="
                    margin: 0;
                    color: #ffffff;
                    font-size: 22px;
                    letter-spacing: 0.3px;
                ">
                    New Portfolio Contact
                </h1>
                <p style="
                    margin: 6px 0 0 0;
                    color: #ff9f4d;
                    font-size: 13px;
                    font-weight: bold;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                ">
                    Website Inquiry
                </p>
            </div>

            <div style="padding: 30px;">

                <p style="margin: 0 0 20px 0;">
                    <strong style="
                        display: block;
                        color: #ff7a1a;
                        font-size: 12px;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        margin-bottom: 4px;
                    ">Name</strong>
                    <span style="color: #23232a; font-size: 15px;">{safe_name}</span>
                </p>

                <p style="margin: 0 0 20px 0;">
                    <strong style="
                        display: block;
                        color: #ff7a1a;
                        font-size: 12px;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        margin-bottom: 4px;
                    ">Email</strong>
                    <span style="color: #23232a; font-size: 15px;">{safe_email}</span>
                </p>

                <strong style="
                    display: block;
                    color: #ff7a1a;
                    font-size: 12px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin-bottom: 8px;
                ">Message</strong>

                <div style="
                    background-color: #2f2f36;
                    border-left: 4px solid #ff7a1a;
                    padding: 16px 18px;
                    margin: 0 0 25px 0;
                    border-radius: 6px;
                    color: #f2f2f2;
                    font-size: 15px;
                    line-height: 1.5;
                ">
                    {safe_message}
                </div>

                <hr style="
                    border: none;
                    border-top: 1px solid #eeeeee;
                    margin: 20px 0;
                ">

                <p style="
                    font-size: 12px;
                    color: #999999;
                    margin: 0 0 20px 0;
                ">
                    <strong style="color: #ff7a1a;">Submission ID:</strong><br>
                    {submission_id}
                </p>

                <p style="
                    font-size: 13px;
                    color: #777777;
                    margin: 0;
                ">
                    You can reply directly to this email to respond to the visitor.
                </p>

            </div>

            <div style="
                background-color: #23232a;
                padding: 14px 30px;
                text-align: center;
            ">
                <p style="
                    margin: 0;
                    font-size: 11px;
                    color: #8a8a8a;
                    letter-spacing: 0.3px;
                ">
                    Sent from your portfolio contact form
                </p>
            </div>

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
        })

        print("RESEND NOTIFICATION RESULT:", result)
        print("EMAIL SENT SUCCESSFULLY")

    except Exception as e:
        print("RESEND EMAIL ERROR:", repr(e))
        raise

    return redirect("home")

