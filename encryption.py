from cryptography.fernet import Fernet

def generate_key():
    """Генерирует ключ для шифрования"""
    return Fernet.generate_key()

def encrypt_data(data, key):
    """Шифрует данные"""
    cipher = Fernet(key)
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data, key):
    """Расшифровывает данные"""
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_data.encode()).decode()
