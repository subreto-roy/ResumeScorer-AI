# analyzer/services/email_fetcher.py
import imaplib, email
import os

def fetch_cvs_from_email(username, password, folder='INBOX', save_dir='cvs'):
    os.makedirs(save_dir, exist_ok=True)
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select(folder)
    result, data = mail.search(None, 'ALL')
    ids = data[0].split()
    for i in ids:
        res, msg_data = mail.fetch(i, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            filename = part.get_filename()
            if filename:
                filepath = os.path.join(save_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))