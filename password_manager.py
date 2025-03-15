import os
import json
from encryption import encrypt_data, decrypt_data, generate_key

KEY_FILE = "key.key"
PASSWORDS_FILE = "passwords.json.enc"

def load_key():
    """Загружает или создаёт ключ"""
    if not os.path.exists(KEY_FILE):
        key = generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key

def save_password(service, username, password):
    """Сохраняет зашифрованный пароль"""
    key = load_key()
    
    passwords = load_passwords() or {}
    passwords[service] = {
        "username": encrypt_data(username, key),
        "password": encrypt_data(password, key)
    }

    with open(PASSWORDS_FILE, "w") as f:
        json.dump(passwords, f)

    print(f"✅ Пароль для {service} сохранён!")

def load_passwords():
    """Загружает зашифрованные пароли"""
    if not os.path.exists(PASSWORDS_FILE):
        return {}

    with open(PASSWORDS_FILE, "r") as f:
        passwords = json.load(f)

    key = load_key()
    for service, creds in passwords.items():
        creds["username"] = decrypt_data(creds["username"], key)
        creds["password"] = decrypt_data(creds["password"], key)

    return passwords

def get_password(service):
    """Получает пароль"""
    passwords = load_passwords()
    return passwords.get(service, None)

# Тестовый запуск
if __name__ == "__main__":
    save_password("GitHub", "my_username", "my_password")
    print(get_password("GitHub"))
