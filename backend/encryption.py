from cryptography.fernet import Fernet, InvalidToken
import hashlib
import base64


def generate_key(passkey: str) -> bytes:
    hashed = hashlib.sha256(passkey.encode('utf-8')).digest()
    fernet_key = base64.urlsafe_b64encode(hashed[:32])
    return fernet_key


def encrypt_file_message(file_bytes, message, passkey):
    try:
        fernet_key = generate_key(passkey)
        f = Fernet(fernet_key)

        encrypted_file = f.encrypt(file_bytes)
        encrypted_msg = f.encrypt(message.encode())
        
        return encrypted_file, encrypted_msg
    
    except Exception as e:
        print(f"Encryption error: {str(e)}")
        return None, None


def decrypt_file_message(encrypted_file, encrypted_msg, passkey):
    try:
        fernet_key = generate_key(passkey)
        f = Fernet(fernet_key)

        file_bytes = f.decrypt(encrypted_file)
        message = f.decrypt(encrypted_msg).decode()
        
        return file_bytes, message

    except InvalidToken:
        return None, "invalid_passkey_or_data"

    except Exception as e:
        return None, f"decryption_error: {str(e)}"
