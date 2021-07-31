import base64

# from apiclient.discovery import build
import smtplib

# from apiclient import errors
# from httplib2 import Http
# from oauth2client import file, client, tools
# from email.mime.text import MIMEText


class TriggerEmail:

    def send_email(self, subject, body,userEmail):
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login('dashmeetk29@gmail.com', 'Dashmeetpassword')
            message = f'Subject: {subject}\n\n{body}'
            server.sendmail('dashmeet29@gmail.com',userEmail, message)
            server.quit()
        except smtplib.SMTPResponseException as er:
            print('Email error - > ' + er.smtp_error)

# class TriggerEmail:
#
#     def getService(self):
#       store = file.Storage('credentials.json')
#       creds = store.get()
#       if not creds or creds.invalid:
#         flow = client.flow_from_clientsecrets('client_secret.json', SCOPE)
#         creds = tools.run_flow(flow, store)
#       service = build('gmail', 'v1', http=creds.authorize(Http()))
#
#     def create_message(self,sender, to, subject, message_text):
#       """Create a message for an email.
#
#       Args:
#         sender: Email address of the sender.
#         to: Email address of the receiver.
#         subject: The subject of the email message.
#         message_text: The text of the email message.
#
#       Returns:
#         An object containing a base64url encoded email object.
#       """
#       message = MIMEText(message_text)
#       message['to'] = to
#       message['from'] = sender
#       message['subject'] = subject
#       return {'raw': base64.urlsafe_b64encode(message.as_string())}
#
#     def send_message(self, service, user_id, message):
#       """Send an email message.
#       Args:
#         service: Authorized Gmail API service instance.
#         user_id: User's email address. The special value "me"
#         can be used to indicate the authenticated user.
#         message: Message to be sent.
#
#       Returns:
#         Sent Message.
#       """
#       try:
#         message = (service.users().messages().send(userId=user_id, body=message)
#                    .execute())
#         print('Message Id: %s' % message['id'])
#         return message
#       # except (errors.HttpError, error):
#       except:
#         print('An error occurred ')