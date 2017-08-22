
# REFERENCE:
#----------------------------------------------------------------------------------------------
# http://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email/
# https://docs.python.org/3/library/email-examples.html
#----------------------------------------------------------------------------------------------

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# Params:
#   recipient: string email address of the recipient
#   team: string id for the team
#   lab: string id for the lab
#   url: string of the repo's url
# Purpose:
#   Send an email notification that the repo has been assigned. 
def send_notification(recipient, team, lab, url):
    msg = "This is a notification:\n"
    msg += "Your team, {}, has been assigned a repo for {}.\n".format(team, lab)
    msg += "The url for your repo is: {}\n".format(url)
    msg = MIMEText(msg)

    # me == the sender's email address
    # you == the recipient's email address
    # TODO: update this with ualberta CMPUT 229 email account.
    sender = "hoye@cs.ualberta.ca"
    msg['Subject'] = "Repos assigned for {}".format(lab)
    msg['From'] = sender
    msg['To'] = recipient

    # Send the message via our own SMTP server.
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    server.login("hoye@ualberta.ca", "H0YE57Uar7")
    print msg
    # server.login("stuarthoye@gmail.com", "xdcnlpnheslbfilb")
    
    # server.sendmail(sender, [recipient], msg.as_string())
    server.quit()

def main():
    send_notification("hoye@ualberta.ca", "team0", "lab0", "www.google.com")

if __name__ == "__main__":
    main()
