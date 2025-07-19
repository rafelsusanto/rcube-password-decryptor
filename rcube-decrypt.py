from base64 import b64decode
from Crypto.Cipher import DES3

# ---- Dynamic Input ----
enc_password_b64 = input("Paste base64 encrypted password (from session): ").strip()
key_input = input("Paste 24-byte des_key (from config.inc.php): ").strip()

key = key_input.encode('utf-8')
if len(key) != 24:
    print(f"[!] Key must be exactly 24 bytes (got {len(key)}).")
    exit(1)

# ---- Decrypt ----
data = b64decode(enc_password_b64)
iv = data[:8]
ciphertext = data[8:]

print(f"IV: {iv.hex()}")
print(f"Ciphertext: {ciphertext.hex()}")

cipher = DES3.new(key, DES3.MODE_CBC, iv)
decrypted = cipher.decrypt(ciphertext)

def try_unpad(data):
    last = data[-1]
    if 1 <= last <= 8 and all(data[-i] == last for i in range(1, last+1)):
        return data[:-last]
    return data.rstrip(b'\x00')

unpadded = try_unpad(decrypted)
print(f"Unpadded (hex): {unpadded.hex()}")

try:
    print("Decrypted password (utf-8):", unpadded.decode('utf-8'))
except Exception as e:
    print("UTF-8 decode error:", e)
    print("Decrypted password (latin1):", unpadded.decode('latin1', errors='replace'))

# Optional: show printable ASCII guess
printable = ''.join([chr(b) if 32 <= b < 127 else '.' for b in unpadded])
print("Printable ASCII:", printable)
