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
    if request.method != 'POST':
        return redirect('home')

    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    message = request.POST.get('message', '').strip()
    submission_id = request.POST.get('submission_id')

    if not submission_id:
        submission_id = str(uuid.uuid4())

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

        result1 = resend.Emails.send({
            "from": settings.RESEND_FROM_EMAIL,
            "to": [settings.CONTACT_EMAIL],
            "reply_to": email,
            "subject": f"Portfolio Contact from {name} [{submission_id}]",
            "html": notification_html,
            "text": notification_text,
        })

        print("RESEND NOTIFICATION RESULT:", result1)
        print("EMAIL SENT SUCCESSFULLY")

    except Exception as e:
        print("RESEND EMAIL ERROR:", repr(e))
        raise
    

    return redirect('home')
