# import smtplib


# smtp_server = "smtp.gmail.com" 
# smtp_port = 587  
# email = "nickypatle0602@gmail.com" 
# password = "mrmh lglm bqsc lcph"  

# recipient = "nickypatle006@gmail.com"  # Replace with recipient's email
# subject = "Test Email"
# body = "This is a test email sent using Python's smtplib module!"
# try:
#     # Establish connection
#     server = smtplib.SMTP(smtp_server, smtp_port)
#     server.starttls()  # Start TLS encryption
#     server.login(email, password)
#     print("SMTP connection successful!")

#     # Create email message
#     message = f"Subject: {subject}\n\n{body}"
#     server.sendmail(email, recipient, message)
#     print(f"Email sent successfully to {recipient}!")

# except Exception as e:
#     print(f"Error occurred: {e}")
# finally:
#     server.quit()