import sendgrid
from sendgrid.helpers.mail import *


class EMailer():

    def __init__(self, apikey=None, to=None):
        self.sg = sendgrid.SendGridAPIClient(apikey=apikey)
        self.from_email = Email("HowdyChecker@arc.com")
        self.to_email = Email(to)

    def send(self, subj=None, cont=None):
        subject = subj
        content = Content("text/html", cont)
        mail = Mail(self.from_email, subject, self.to_email, content)

        # with open('html.html', 'w') as f:
        #    f.write(cont)

        #print mail.get()

        return self.sg.client.mail.send.post(request_body=mail.get())
