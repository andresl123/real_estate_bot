import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(receiver_email,body):
    sender_email = "real.estate.finder202@gmail.com"
    password = "nidx nrny zzmw qhyp"  # App Password
    subject = "Hello User"
    # body = "This is a test email sent from Python."
    # """
    # Sends an email using the given credentials and details.
    #
    # :param sender_email: The sender's email address.
    # :param password: The sender's email password or App Password.
    # :param receiver_email: The recipient's email address.
    # :param subject: The subject of the email.
    # :param body: The body of the email.
    # :return: None
    # """
    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Sending email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, password)  # Login to the email account
            server.sendmail(sender_email, receiver_email, message.as_string())  # Send email
        print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Authentication Error: Please check your email and password.")
    except Exception as e:
        print(f"Failed to send email: {e}")


