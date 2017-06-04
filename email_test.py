# http://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email/
# https://docs.python.org/3/library/email-examples.html

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

msg = MIMEText("HELLO WORLD!")

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'The contents of %s' % msg
msg['From'] = "hoye@ualberta.ca"
msg['To'] = "hoye@ualberta.ca"

# Send the message via our own SMTP server.
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("hoye@gmail.com", "H0YE57Uar7")
s.send_message(msg)
s.quit()