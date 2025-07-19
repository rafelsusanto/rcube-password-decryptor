# rcube-password-decryptor

**Decrypt IMAP passwords from Roundcube session data with the server's DES key.**


## What is this?

This tool recovers a user's plaintext IMAP password from Roundcube webmail sessions, given access to both:
- the encrypted password (from a session file or session database), and
- the DES key (`des_key`) from `config.inc.php`.

It is useful for:
- Incident response / digital forensics
- Penetration testing (with proper authorization)
- Password recovery/migration in Roundcube environments

---


## ⚠️ Security Warning

> **This tool is for authorized use only!**  
> Possessing both the session data and the DES key means you have full access to all user mail accounts.  
> Never expose your server's `config.inc.php` or session files.  
> Use responsibly and with proper legal permission.

---

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

## Requirements

- Python 3
- [`pycryptodome`](https://pypi.org/project/pycryptodome/)

Install pycryptodome via pip if you don't have it:

```bash
pip install pycryptodome
