from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import json
from datetime import datetime, timedelta
import base64

password = b"password"
salt = b"salt"
key = PBKDF2(password, salt, dkLen=32)

def encrypt_session(session_data, key):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(json.dumps(session_data).encode())
    return cipher.nonce + tag + ciphertext

def decrypt_session(encrypted_session_data, key):
    nonce, tag, ciphertext = encrypted_session_data[:16], encrypted_session_data[16:32], encrypted_session_data[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return json.loads(decrypted_data.decode())

def create_session(session_name, session_key):
    expiration_time = datetime.now() + timedelta(hours=1)
    session_data = {
        'session_key': session_key,
        'expiration_time': expiration_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    with open(f'{session_name}.session', 'wb') as f:
        f.write(encrypt_session(session_data, key))

def load_session(session_name):
    try:
        with open(f'{session_name}.session', 'rb') as f:
            encrypted_session_data = f.read()
        return decrypt_session(encrypted_session_data, key)
    except FileNotFoundError:
        return None

def main():
    create_session('default', key)  # Ensure key is a string

    session_data = load_session('default')
    if session_data:
        print("Session data:", session_data)
    else:
        print("Session expired or not found.")

if __name__ == "__main__":
    main()
