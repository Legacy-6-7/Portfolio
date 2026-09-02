from django.shortcuts import render, redirect, get_object_or_404
from .models import Portfolio, Skill, Project, Experience
from .forms import PortfolioForm, SkillForm, ProjectForm, ExperienceForm
from django.conf import settings
from django.contrib import messages
from django.utils.html import escape
from django.core.mail import send_mail
from django.shortcuts import redirect
import resend


def home(request):
    return render(request, 'home.html')

def contact(request):
    if request.method != 'POST':
        return redirect('home')

    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    message = request.POST.get('message', '').strip()

    # Escape user input to prevent HTML injection
    safe_name = escape(name)
    safe_email = escape(email)
    safe_message = escape(message).replace('\n', '<br>')

    try:
        # Resend API key
        resend.api_key = settings.RESEND_API_KEY

        # =====================================================
        # EMAIL 1 — NOTIFICATION TO YOU
        # =====================================================

        notification_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>

        <body style="
            margin:0;
            padding:0;
            background:#111111;
            font-family:Arial, Helvetica, sans-serif;
        ">

            <div style="
                width:100%;
                padding:35px 10px;
                background:#111111;
            ">

                <div style="
                    max-width:620px;
                    margin:0 auto;
                    background:#181818;
                    border:3px solid #ff5722;
                    box-shadow:
                        8px 8px 0 #000000,
                        0 0 25px rgba(255,87,34,0.25);
                ">

                    <!-- TOP BAR -->
                    <div style="
                        height:8px;
                        background:#ff5722;
                        box-shadow:0 5px 0 #111111;
                    "></div>

                    <!-- HEADER -->
                    <div style="
                        padding:35px 30px;
                        background:#202020;
                        border-bottom:3px solid #ff5722;
                        text-align:center;
                    ">

                        <div style="
                            display:inline-block;
                            padding:7px 12px;
                            margin-bottom:18px;
                            background:#ff5722;
                            color:#ffffff;
                            font-size:11px;
                            font-weight:bold;
                            letter-spacing:3px;
                            border:2px solid #ffffff;
                            box-shadow:4px 4px 0 #000000;
                        ">
                            NEW MESSAGE
                        </div>

                        <h1 style="
                            margin:0;
                            color:#ffffff;
                            font-size:30px;
                            letter-spacing:1px;
                        ">
                            CONTACT INCOMING
                        </h1>

                        <p style="
                            margin:12px 0 0;
                            color:#aaaaaa;
                            font-size:13px;
                        ">
                            A visitor has contacted your portfolio
                        </p>

                    </div>

                    <!-- STATUS -->
                    <div style="
                        padding:18px 25px;
                        background:#151515;
                        border-bottom:2px solid #333333;
                    ">

                        <span style="
                            display:inline-block;
                            width:10px;
                            height:10px;
                            background:#ff5722;
                            margin-right:8px;
                            box-shadow:2px 2px 0 #000000;
                        "></span>

                        <span style="
                            color:#ff5722;
                            font-size:12px;
                            font-weight:bold;
                            letter-spacing:2px;
                        ">
                            NEW CONTACT REQUEST
                        </span>

                    </div>

                    <!-- CONTENT -->
                    <div style="
                        padding:30px;
                        background:#181818;
                    ">

                        <!-- CONTACT DETAILS -->
                        <div style="
                            border:2px solid #333333;
                            background:#202020;
                            box-shadow:5px 5px 0 #0a0a0a;
                            margin-bottom:30px;
                        ">

                            <div style="
                                padding:12px 18px;
                                background:#292929;
                                border-bottom:2px solid #333333;
                                color:#ff5722;
                                font-size:12px;
                                font-weight:bold;
                                letter-spacing:2px;
                            ">
                                // CONTACT_DETAILS
                            </div>

                            <div style="padding:20px;">

                                <p style="
                                    margin:0 0 20px;
                                    color:#888888;
                                    font-size:11px;
                                    letter-spacing:1px;
                                ">
                                    NAME
                                </p>

                                <p style="
                                    margin:-12px 0 22px;
                                    color:#ffffff;
                                    font-size:17px;
                                    font-weight:bold;
                                ">
                                    {safe_name}
                                </p>

                                <p style="
                                    margin:0 0 20px;
                                    color:#888888;
                                    font-size:11px;
                                    letter-spacing:1px;
                                ">
                                    EMAIL
                                </p>

                                <p style="margin:-12px 0 0;">

                                    <a href="mailto:{safe_email}" style="
                                        color:#ff5722;
                                        font-size:15px;
                                        text-decoration:none;
                                        font-weight:bold;
                                    ">
                                        {safe_email}
                                    </a>

                                </p>

                            </div>

                        </div>

                        <!-- MESSAGE -->
                        <div style="
                            border:2px solid #333333;
                            background:#202020;
                            box-shadow:5px 5px 0 #0a0a0a;
                        ">

                            <div style="
                                padding:12px 18px;
                                background:#292929;
                                border-bottom:2px solid #333333;
                                color:#ff5722;
                                font-size:12px;
                                font-weight:bold;
                                letter-spacing:2px;
                            ">
                                // MESSAGE
                            </div>

                            <div style="padding:25px;">

                                <p style="
                                    margin:0;
                                    color:#dddddd;
                                    font-size:15px;
                                    line-height:1.8;
                                ">
                                    {safe_message}
                                </p>

                            </div>

                        </div>

                    </div>

                    <!-- FOOTER -->
                    <div style="
                        padding:22px;
                        background:#111111;
                        border-top:3px solid #ff5722;
                        text-align:center;
                    ">

                        <p style="
                            margin:0;
                            color:#ff5722;
                            font-size:11px;
                            font-weight:bold;
                            letter-spacing:2px;
                        ">
                            SAMARTH VERMA // PORTFOLIO
                        </p>

                        <p style="
                            margin:8px 0 0;
                            color:#666666;
                            font-size:10px;
                        ">
                            Automated contact notification
                        </p>

                    </div>

                </div>

            </div>

        </body>
        </html>
        """

        notification_text = f"""
NEW CONTACT MESSAGE

Name: {name}
Email: {email}

Message:
{message}

--------------------------------
Samarth Verma Portfolio
"""

        resend.Emails.send({
            "from": settings.RESEND_FROM_EMAIL,
            "to": [settings.CONTACT_EMAIL],
            "reply_to": email,
            "subject": f"Portfolio Contact from {name}",
            "html": notification_html,
            "text": notification_text,
        })

        # =====================================================
        # EMAIL 2 — AUTOMATIC RESPONSE
        # =====================================================

        auto_reply_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>

        <body style="
            margin:0;
            padding:0;
            background:#111111;
            font-family:Arial, Helvetica, sans-serif;
        ">

            <div style="
                width:100%;
                padding:35px 10px;
                background:#111111;
            ">

                <div style="
                    max-width:620px;
                    margin:0 auto;
                    background:#181818;
                    border:3px solid #ff5722;
                    box-shadow:
                        8px 8px 0 #000000,
                        0 0 30px rgba(255,87,34,0.25);
                ">

                    <!-- TOP BAR -->
                    <div style="
                        height:8px;
                        background:#ff5722;
                    "></div>

                    <!-- HEADER -->
                    <div style="
                        padding:40px 30px;
                        text-align:center;
                        background:#202020;
                    ">

                        <div style="
                            display:inline-block;
                            padding:7px 12px;
                            background:#ff5722;
                            color:#ffffff;
                            border:2px solid #ffffff;
                            box-shadow:4px 4px 0 #000000;
                            font-size:10px;
                            font-weight:bold;
                            letter-spacing:3px;
                            margin-bottom:20px;
                        ">
                            MESSAGE RECEIVED
                        </div>

                        <h1 style="
                            margin:0;
                            color:#ffffff;
                            font-size:29px;
                        ">
                            THANK YOU, {safe_name}!
                        </h1>

                        <p style="
                            margin:12px 0 0;
                            color:#aaaaaa;
                            font-size:14px;
                        ">
                            Your message has successfully reached me.
                        </p>

                    </div>

                    <!-- DIVIDER -->
                    <div style="
                        height:3px;
                        background:#ff5722;
                    "></div>

                    <!-- CONTENT -->
                    <div style="
                        padding:35px 30px;
                        background:#181818;
                    ">

                        <p style="
                            margin:0 0 20px;
                            color:#ffffff;
                            font-size:16px;
                            line-height:1.7;
                        ">
                            Hello
                            <strong style="color:#ff5722;">
                                {safe_name}
                            </strong>,
                        </p>

                        <p style="
                            margin:0 0 20px;
                            color:#bbbbbb;
                            font-size:15px;
                            line-height:1.8;
                        ">
                            Thank you for taking the time to contact me
                            through my portfolio.
                        </p>

                        <p style="
                            margin:0 0 30px;
                            color:#bbbbbb;
                            font-size:15px;
                            line-height:1.8;
                        ">
                            I've received your message and will review it.
                            I'll get back to you as soon as possible.
                        </p>

                        <!-- MESSAGE CARD -->
                        <div style="
                            border:2px solid #333333;
                            background:#202020;
                            box-shadow:5px 5px 0 #080808;
                        ">

                            <div style="
                                padding:12px 18px;
                                background:#292929;
                                border-bottom:2px solid #333333;
                                color:#ff5722;
                                font-size:11px;
                                font-weight:bold;
                                letter-spacing:2px;
                            ">
                                // YOUR_MESSAGE
                            </div>

                            <div style="padding:22px;">

                                <p style="
                                    margin:0;
                                    color:#dddddd;
                                    font-size:14px;
                                    line-height:1.8;
                                ">
                                    {safe_message}
                                </p>

                            </div>

                        </div>

                        <!-- STATUS -->
                        <div style="
                            margin-top:30px;
                            padding:18px;
                            background:#211914;
                            border:2px solid #ff5722;
                        ">

                            <p style="
                                margin:0;
                                color:#ff5722;
                                font-size:11px;
                                font-weight:bold;
                                letter-spacing:2px;
                            ">
                                STATUS: RECEIVED
                            </p>

                            <p style="
                                margin:8px 0 0;
                                color:#aaaaaa;
                                font-size:12px;
                            ">
                                No further action is required.
                            </p>

                        </div>

                        <!-- SIGNATURE -->
                        <div style="
                            margin-top:35px;
                            padding-top:25px;
                            border-top:1px solid #333333;
                        ">

                            <p style="
                                margin:0;
                                color:#777777;
                                font-size:12px;
                            ">
                                Best regards,
                            </p>

                            <p style="
                                margin:7px 0 0;
                                color:#ff5722;
                                font-size:18px;
                                font-weight:bold;
                            ">
                                Samarth Verma
                            </p>

                            <p style="
                                margin:5px 0 0;
                                color:#666666;
                                font-size:11px;
                                letter-spacing:1px;
                            ">
                                WEB DEVELOPER
                            </p>

                        </div>

                    </div>

                    <!-- FOOTER -->
                    <div style="
                        padding:22px;
                        background:#111111;
                        border-top:3px solid #ff5722;
                        text-align:center;
                    ">

                        <p style="
                            margin:0;
                            color:#ff5722;
                            font-size:11px;
                            font-weight:bold;
                            letter-spacing:2px;
                        ">
                            SAMARTH VERMA // PORTFOLIO
                        </p>

                        <p style="
                            margin:8px 0 0;
                            color:#555555;
                            font-size:10px;
                        ">
                            This is an automated confirmation email.
                        </p>

                    </div>

                </div>

            </div>

        </body>
        </html>
        """

        auto_reply_text = f"""
Hello {name},

Thank you for contacting me!

I've received your message and will get back to you as soon as possible.

Your message:

"{message}"

Best regards,
Samarth Verma
"""

        resend.Emails.send({
            "from": settings.RESEND_FROM_EMAIL,
            "to": [email],
            "subject": "Thank you for contacting me!",
            "html": auto_reply_html,
            "text": auto_reply_text,
        })

        # =====================================================
        # SUCCESS
        # =====================================================

        messages.success(
            request,
            "Message sent successfully!"
        )

    except Exception as e:
        print("RESEND EMAIL ERROR:", e)

        messages.error(
            request,
            f"Email error: {e}"
        )

    return redirect('home')
