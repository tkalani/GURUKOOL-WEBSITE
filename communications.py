import smtplib
import threading, traceback
from email.mime.application import MIMEApplication
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys, traceback
from email.utils import COMMASPACE, formatdate
from email.mime.base import MIMEBase
from email import encoders

EmailAccount = 'donotreplygurukool@gmail.com'
EmailPassword = 'gurukool'
# fdbztwseduujgnmk

# def EmailThread(request, recipient, subject, body, files):
# 	try:
# 		msg = MIMEMultipart()
# 		msg['From'] = EmailAccount
# 		msg['To'] = recipient
# 		msg['subject'] = subject
# 		message = body
# 		msg.attach(MIMEText(message))
# 		if files:
# 			for file in files:
# 				part = MIMEBase('application', "octet-stream")
# 				part.set_payload(open(file.file.name, "rb").read())
# 				Encoders.encode_base64(part)
# 				part.add_header('Content-Disposition', 'attachment; filename="'+str(file)+'"')
# 				msg.attach(part)

# 		mailserver = smtplib.SMTP('smtp.gmail.com',587)
# 		mailserver.ehlo()
# 		mailserver.starttls()
# 		mailserver.ehlo()
# 		mailserver.login(EmailAccount, EmailPassword)

# 		mailserver.sendmail(EmailAccount,recipient,msg.as_string())

# 		mailserver.quit()
# 	except Exception as e:
# 		print(e)



# def sendEmail(request, recipient, subject, body, files):
# 	try:
# 		thread_process = threading.Thread(target=EmailThread, kwargs={
# 			"request":request,
# 			"recipient":recipient,
# 			"subject":subject,
# 			"body": body,
# 			"files":files
# 		})
# 		thread_process.start()
# 	except Exception as e:
# 		print(e)
# 	print(traceback.format_exc())