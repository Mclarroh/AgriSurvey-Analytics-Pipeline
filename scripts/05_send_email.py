import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime

# ------------------------------------------
# SETTINGS – CHANGE THESE
# ------------------------------------------
SENDER_EMAIL = "onyango.larry@gmail.com"          # ← your Gmail address
SENDER_PASSWORD = "ysyy qubg xrdq ghos"          # ← Gmail App Password (not normal password)
RECEIVER_EMAIL = "machiratimothy4@gmail.com"        # ← your supervisor’s email

SUBJECT = "Agriculture Survey Analysis Report – Ready for Review"
BODY = f"""
Dear Supervisor,

Please find attached the full mixed-methods analysis report from the agriculture survey.

The report includes:
• Cleaned data summary
• Quantitative findings and charts
• Correlation analysis with plain-language explanations
• Interactive map of farmers
• Qualitative insights from MAXQDA
• Clear recommendations suitable for funding discussions

Generated on: {datetime.now().strftime('%d %B %Y, %H:%M')}

Best regards,
Your Name
"""

# ------------------------------------------
# File to attach
# ------------------------------------------
BASE_DIR = Path(__file__).parent.parent
REPORT_FILE = BASE_DIR / "outputs" / "Agriculture_Survey_Report.docx"

def send_report():
    if not REPORT_FILE.exists():
        print("ERROR: Report file not found. Please run 04_make_report.py first.")
        return

    # Create the email
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = SUBJECT

    msg.attach(MIMEText(BODY, "plain"))

    # Attach the report
    with open(REPORT_FILE, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename=Agriculture_Survey_Report.docx"
        )
        msg.attach(part)

    # Send
    try:
        print("Connecting to Gmail...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("SUCCESS! Report emailed to supervisor.")
    except Exception as e:
        print("Failed to send email.")
        print("Error:", e)
        print("\nCommon fixes:")
        print("1. Make sure you are using a Gmail App Password (not your normal password)")
        print("2. Enable 2-Step Verification in your Google account")
        print("3. Check that the email addresses are correct")

if __name__ == "__main__":
    send_report()