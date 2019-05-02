import socket
import ssl
import smtplib
from config import SEND_TEST_MAIL, SEND_TEST_MAIL_TO, MAIL_HOSTNAME, MAIL_USERNAME, MAIL_PASSWORD, OPEN_PORTS

TIMEOUT = 10

def test_smtp(port, secure, starttls):
    try:
        if secure:
            server = smtplib.SMTP_SSL(MAIL_HOSTNAME, port=port, timeout=TIMEOUT)
        else:
            server = smtplib.SMTP(MAIL_HOSTNAME, port=port, timeout=TIMEOUT)

        if starttls:
            server.starttls()

        server.login(MAIL_USERNAME, MAIL_PASSWORD)

        if SEND_TEST_MAIL:
            summary = 'Using port {} using an {} initial connection {}'.format(port, 'secure' if secure else 'insecure', 'and requesting TLS after connection' if starttls else '')
            msg = ("From: %s\r\nSubject: %s\r\nTo: %s\r\n\r\n"
                % (MAIL_USERNAME, summary, SEND_TEST_MAIL_TO))

            msg += "Ik ben een bericht!\r\n"            

            server.sendmail(MAIL_USERNAME, SEND_TEST_MAIL_TO, msg)

        server.quit()
        
        return True
    except ssl.SSLError:
        return False
    except socket.error:
        return False    
    except socket.timeout:
        return False        

for port in OPEN_PORTS:
    for secure in [True, False]:
        for starttls in [True, False]:
            result = test_smtp(port, secure, starttls);
            print('[{}] SMTP via port {} using an {} initial connection {}'.format('success' if result else 'fail', port, 'secure' if secure else 'insecure', 'and requesting TLS after connection' if starttls else ''))