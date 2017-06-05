# http://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email/
# https://docs.python.org/3/library/email-examples.html

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

def send_notification(team, lab, url):
    msg = "This is a notification:/n"
    msg += "Your team, {}, has been assigned a repo for lab {}.".format(team, lab)
    msg += "The url for your repo is: {}".format(url)
    msg = MIMEText(msg)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'The contents of %s' % msg
    msg['From'] = "hoye@ualberta.ca"
    msg['To'] = "hoye@ualberta.ca"

    # Send the message via our own SMTP server.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(uname, pword)        # TODO: READ THESE FROM FILE
    s.send_message(msg)
    s.quit()