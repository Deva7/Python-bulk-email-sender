import os
import csv
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders 
from dotenv import load_dotenv


load_dotenv()
gmail_username = os.getenv('GMAIL_USERNAME')
gmail_password = os.getenv('GMAIL_PASSWORD')

# Read csv file
# with open('Sample_data.csv', 'r') as file:
#     reader = csv.reader(file)
#     next(reader)
#     email_list = [row[2] for row in reader]

# Read the text file
with open("email_list.txt", 'r') as file:
    email_list =  [line.strip() for line in file]

# Compose the email
    subject = 'PLACE YOUR EMAIL SUBJECT'
# Message can be a plain text or HTML
    message = """<html>
            <body>
              <p>Hi</p>
            </body>
          </html>
       """

# open the file to be sent  
    filename = "REPLACE WITH THE ATTACHMENT NAME ALONG WITH FILE EXTENSION"
    attachment = open(filename, "rb")
# instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 
  
# To change the payload into encoded form 
    p.set_payload((attachment).read()) 
  
# encode into base64 
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    file = open('REPLACE WITH THE FILENAME TO WRITE OUT','w')

# Define the batch size
    batch_size = 20
    total_emails = len(email_list)

# Send emails in batches
for i in range(0, total_emails, batch_size):
    batch_recipients = email_list[i:i + batch_size]
    for recipient in batch_recipients:
        msg = MIMEMultipart()
        msg['from'] = gmail_username
        msg['To'] = recipient
        msg['Subject'] = subject
        # Define the type of the message included Plain Text or HTML
        msg.attach(MIMEText(message, 'html'))

        # attach the instance 'p' to instance 'msg' 
        msg.attach(p) 
        file.write('Sending email to '+ recipient +"\n")
    

# Connect to Gmail's SMTP SSL server
        try:
             server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
# If Using Gmail's SMTP server use .starttls() 
            #  server.starttls()
             server.login(gmail_username, gmail_password)

# send the email
             server.sendmail(gmail_username, recipient, msg.as_string())
             time.sleep(1)
# Quit the server
             server.quit()
        except Exception as e:
            print(f'Failed to send email to {recipient}: {str(e)}')
file.close()