import imaplib
import email

username = '' # email
password = '' # password

def get_inbox():
  host = 'imap.gmail.com'
  mail = imaplib.IMAP4_SSL(host)
  mail.login(username, password)
  mail.select('inbox')
  _, search_data = mail.search(None, 'UNSEEN')
  my_messages = []
  for num in search_data[0].split():
    email_data = {}
    _, data = mail.fetch(num, 'RFC822')
    _, b = data[0]
    email_message = email.message_from_bytes(b)
    for header in ['subject', 'to', 'from', 'date']:
      email_data[header] = email_message[header]
    for part in email_message.walk():
      if part.get_content_type() == 'text/plain':
        body = part.get_payload(decode=True)
        email_data['body'] = body.decode()
      elif part.get_content_type() == 'text/html':
        html_body = part.get_payload(decode=True)
        email_data['html_body'] = html_body.decode()
    my_messages.append(email_data)
  return my_messages

print(get_inbox())