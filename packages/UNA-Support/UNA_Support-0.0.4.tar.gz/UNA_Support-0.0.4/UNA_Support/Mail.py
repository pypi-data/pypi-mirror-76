import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import UNA_Support.CustomException as Except

class Mail:
    """
    Transmiterea mesajelor electronice

    Transmission of electronic messages
    """

    def __init__(self):
        """
        Initializarea datelor pentru transmiterea mesajului:
         - SMTPServer: Tipul serverului de transmitere (mail.ru, gmal.com)
         - email: addresa electronica expediator
         - password: parola expediator
         - send_to_email: addresa electronica destinatar
         - subject: subiectul mesajului
         - message: textul mesajului
         - file_location: calea catre fisierul atasat la mesaj

         Initialize the data for sending the message:
         - SMTPServer: Transmission server type (mail.ru, gmal.com)
         - email: sender's email address
         - password: the sender password
         - send_to_email: recipient's email address
         - subject: the subject of the message
         - message: the text of the message
         - file_location: the path to the file attached to the message
        """

        self.SMTPServer = 'Mail.ru'
        self.email = None
        self.password = None
        self.send_to_email = None
        self.subject = None
        self.message = None
        self.file_location = None
        self.mail_CC = None
        self.check_send = False

    def MailRuSmtplib(self, msg, toaddrs):
        """
        Expedierea mesajului prin serverul mail.ru

        Sending the message through the mail.ru server
        """

        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        server.login(self.email, self.password)
        text = msg.as_string()
        server.sendmail(self.email, toaddrs, text)
        server.quit()

    def GMailSmtplib(self, msg, toaddrs):
        """
        Expedierea mesajului prin serverul Gmail.com

        Send the message through the Gmail.com server
        """

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(self.email, self.password)
        text = msg.as_string()
        server.sendmail(self.email, toaddrs, text)
        server.quit()

    def UNAmdSmtplib(self, msg, toaddrs):
        """
        Expedierea mesajului prin serverul mail.una.md

        Sending the message through the mail.una.md server
        """

        server = smtplib.SMTP('mail.una.md')
        server.ehlo()
        server.login(self.email, self.password)
        text = msg.as_string()
        server.sendmail(self.email, toaddrs, text)
        server.quit()

    def SendMail(self):
        """
        Transmiterea mesajului prin serverul indicat de utilizator in parametrul SMTPServer

        Transmission of the message through the server indicated by the user in the SMTPServer parameter
        """

        try:
            msg = MIMEMultipart()
            toaddrs = []
            if self.email == None: raise Except.EMailIsNone
            if self.password == None: raise Except.PasswordIsNone
            if self.send_to_email == None: raise Except.ToEMailIsNone
            if self.subject == None: raise Except.SubjectIsNone
            if self.message == None: raise Except.MessageIsNone
            msg['From'] = self.email
            msg['To'] = ", ".join(self.send_to_email)
            msg['Subject'] = self.subject

            for i in self.send_to_email:
                toaddrs.append(i)

            if self.mail_CC != None:
                msg['cc'] = ", ".join(self.mail_CC)
                for i in self.mail_CC:
                    toaddrs.append(i)

            msg.attach(MIMEText(self.message, 'plain'))

            # Setup the attachment
            if self.file_location != None:
                filename = os.path.basename(self.file_location)
                attachment = open(self.file_location, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                # Attach the attachment to the MIMEMultipart object
                msg.attach(part)

            if self.SMTPServer == 'Mail.ru':
                self.MailRuSmtplib(msg, toaddrs)
            elif self.SMTPServer == 'GMail.com':
                self.GMailSmtplib(msg, toaddrs)
            elif self.SMTPServer == 'una.md':
                self.UNAmdSmtplib(msg, toaddrs)
            else:
                raise Except.SMTPServerNotRegister

            self.check_send = True
        except Except.EMailIsNone:
            result = "EMail None"
            print(result)
        except Except.PasswordIsNone:
            result = "Password None"
            print(result)
        except Except.ToEMailIsNone:
            result = "Email Receiver None"
            print(result)
        except Except.SubjectIsNone:
            result = "Subject message None"
            print(result)
        except Except.MessageIsNone:
            result = "Message None"
            print(result)
        except Except.FileLocationIsNone:
            result = "Attachment file location None"
            print(result)
        except smtplib.SMTPAuthenticationError as ex:
            result = "Error Authentication" + str(ex)
            print(result)
        except Except.SMTPServerNotRegister:
            result = self.SMTPServer + " server does not exist"
            print(result)
        else:
            result = "Message sent successfully"
            print(result)

        return result
