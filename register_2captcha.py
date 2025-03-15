from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

# Генерация случайного email
def generate_email():
    return f"user{random.randint(1000, 9999)}@example.com"

# Основной код
if __name__ == '__main__':
    # Настройка веб-драйвера
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Запуск в фоновом режиме
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Укажите путь к chromedriver (если он не в PATH)
    driver = webdriver.Chrome(options=options)

    try:
        # Переход на страницу регистрации
        driver.get('https://2captcha.com/auth/register')

        # Заполнение формы регистрации
        email = generate_email()
        password = 'StrongPassword123!'

        driver.find_element(By.NAME, 'email').send_keys(email)
        driver.find_element(By.NAME, 'password').send_keys(password)
        driver.find_element(By.NAME, 'password_confirmation').send_keys(password)

        # Нажатие кнопки регистрации
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        # Ожидание завершения регистрации
        time.sleep(5)

        # Получение API-ключа
        driver.get('https://2captcha.com/setting')
        api_key = driver.find_element(By.XPATH, '//input[@id="apiKey"]').get_attribute('value')

        # Сохранение API-ключа в файл
        with open('2captcha_api_key.txt', 'w') as file:
            file.write(api_key)

        print(f'Регистрация завершена. API-ключ: {api_key}')
    except Exception as e:
        print(f'Ошибка при регистрации: {e}')
    finally:
        driver.quit()
