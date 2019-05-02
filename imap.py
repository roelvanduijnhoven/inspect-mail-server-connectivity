from imapclient import IMAPClient
import socket
import imaplib
import ssl
from config import MAIL_HOSTNAME, MAIL_USERNAME, MAIL_PASSWORD, OPEN_PORTS

TIMEOUT = 3

socket.setdefaulttimeout(TIMEOUT)

def test_imap(port, secure, starttls):
    try:
        server = IMAPClient(MAIL_HOSTNAME, ssl=secure, port=port, timeout=TIMEOUT)

        if starttls:
            server.starttls()

        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        return 'EXISTS'.encode('utf-8') in server.select_folder('INBOX')
    except imaplib.IMAP4.error:
        return False
    except imaplib.IMAP4.abort:
        return False
    except ssl.SSLError:
        return False
    except socket.error:
        return False    
    except socket.timeout:
        return False

for port in OPEN_PORTS:
    for secure in [True, False]:
        for starttls in [True, False]:
            result = test_imap(port, secure, starttls);
            print('[{}] IMAP via port {} using an {} initial connection {}'.format('success' if result else 'fail', port, 'secure' if secure else 'insecure', 'and requesting TLS after connection' if starttls else ''))