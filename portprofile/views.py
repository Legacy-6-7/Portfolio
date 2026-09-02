from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.html import escape
from django.views.decorators.http import require_POST
import resend
import uuid



def home(request):
    return render(request, 'home.html')

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

    notification_html = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2>New Portfolio Contact</h2>

        <p><strong>Name:</strong> {safe_name}</p>
        <p><strong>Email:</strong> {safe_email}</p>

        <p><strong>Message:</strong></p>

        <div style="
            background: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        ">
            {safe_message}
        </div>

        <hr>

        <p>
            <strong>Submission ID:</strong> {submission_id}
        </p>

        <p>
            Reply directly to this email to respond to the visitor.
        </p>
    </div>
    """

    notification_text = f"""
New Portfolio Contact

Name: {name}
Email: {email}

Message:
{message}

Submission ID: {submission_id}

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