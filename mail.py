import imaplib, json, bir
import config
import email
from email.header import decode_header

def Mail1():

    imap_server = "imap.yandex.ru"


    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(config.email_adress1, config.password1)


    mail.select("INBOX")


    i = 0
    while i < 3:
        result, data = mail.search(None, "ALL")
        if data == [b'']:
            pass
        else:
            ids = data[0]
            id_list = ids.split()
            mail_id = id_list[0]
            latest_email_id = id_list[-1]
            status, data = mail.fetch(latest_email_id, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            Subject = decode_header(msg["Subject"])[0][0].decode()
            if Subject.find('C98'):
                index = Subject.find('{')
                s_msg = Subject[index:]
                msg = json.loads(s_msg)
                bir.Signal(msg)           
            mail.store(mail_id, '+FLAGS', '\\Deleted')
            mail.expunge()
            
        i += 1
