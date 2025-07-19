# rcube-password-decryptor

**Decrypt IMAP passwords from Roundcube session data with the server's DES key.**  

<br>

## What is this?

This tool recovers a user's plaintext IMAP password from Roundcube webmail sessions, given access to both:
- the encrypted password (from a session file or session database), and
- the DES key (`des_key`) from `config.inc.php`.

It is useful for:
- Incident response / digital forensics
- Penetration testing (with proper authorization)
- Password recovery/migration in Roundcube environments

---
<br>
  

## ⚠️ Security Warning

> **This tool is for authorized use only!**  
> Possessing both the session data and the DES key means you have full access to all user mail accounts.  
> Never expose your server's `config.inc.php` or session files.  
> Use responsibly and with proper legal permission.

---
  <br>

## How does it work?

Roundcube encrypts a user's IMAP password before saving it in the session, using the following steps:
1. Encrypts the password with **3DES in CBC mode** (using the 24-byte `des_key`).
2. Prepends a random 8-byte **IV** to the ciphertext.
3. Stores `(IV + ciphertext)` as a base64 string in the session.

This tool:
- **Base64-decodes** the session password.
- **Splits** the IV and ciphertext.
- **Decrypts** using 3DES-CBC and the supplied key/IV.
- **Removes padding** to recover the plaintext password.

---
  <br>

## Requirements

- Python 3
- [`pycryptodome`](https://pypi.org/project/pycryptodome/)

Install pycryptodome via pip if you don't have it:

```bash
pip install pycryptodome
```

---
<br>
  
## How to use?


```bash 
python3 rcube-decrypt.py 
Paste base64 encrypted password (from session): <base64 password from session>
Paste 24-byte des_key (from config.inc.php): <des_key from config.inc.php>
```

Example from one of HackTheBox lab:  

cat /var/www/html/roundcube/config/config.inc.php  
<img width="601" height="91" alt="image" src="https://github.com/user-attachments/assets/8aee1878-c80c-4968-8698-228957695230" />

grab session from database  
<img width="1361" height="767" alt="image" src="https://github.com/user-attachments/assets/cef6251f-42c2-4ed0-863e-c627654048d1" />

decode session  
<img width="1688" height="673" alt="image" src="https://github.com/user-attachments/assets/99cdf8e5-f2e2-4713-8a4f-f3156aed0267" />

run rcube-decrypt.py  
<img width="823" height="162" alt="image" src="https://github.com/user-attachments/assets/38b2027d-31b0-47ee-b061-4a55c587eb64" />



Reference: https://www.roundcubeforum.net/index.php?topic=23399.0
