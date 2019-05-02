import getpass, poplib
import socket
import ssl
from config import MAIL_HOSTNAME, MAIL_USERNAME, MAIL_PASSWORD, OPEN_PORTS

TIMEOUT = 3

def test_pop3(port, secure, starttls):
    try:    
        if secure:
            M = poplib.POP3_SSL(MAIL_HOSTNAME, port=port, timeout=TIMEOUT)
        else:
            M = poplib.POP3(MAIL_HOSTNAME, port=port, timeout=TIMEOUT)

        if starttls:
            M.stls();

        M.user(MAIL_USERNAME)
        M.pass_(MAIL_PASSWORD)
        numMessages = len(M.list()[1])
        return numMessages >= 0
    except poplib.error_proto:
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
            result = test_pop3(port, secure, starttls);
            print('[{}] POP3 via port {} using an {} initial connection {}'.format('success' if result else 'fail', port, 'secure' if secure else 'insecure', 'and requesting TLS after connection' if starttls else ''))