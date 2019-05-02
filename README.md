# Test e-mail server

Will try to connect to a configured mailbox using all combinations of:

* Given ports.
* Secure and insecure connection.
* With and without STARTTLS.

## Usage: 

1. Install PIP dependencies: `pip3 install -r requirements.txt`.

2. Make a copy of `config.py.dist` to config.py, and properly configure.

3. Run actual test:

   ```
   python3 imap.py
   python3 pop3.py
   python3 smtp.py
   ```