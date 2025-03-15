import requests
from fake_useragent import UserAgent
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Инициализация UserAgent
ua = UserAgent()

# Функция для проверки прокси
def check_proxy(proxy):
    try:
        response = requests.get('http://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=10)
        if response.status_code == 200:
            return True
    except Exception as e:
        logging.error(f'Ошибка при проверке прокси {proxy}: {e}')
    return False

# Функция для выполнения запроса с использованием прокси и User-Agent
def make_request(url, proxy=None):
    headers = {'User-Agent': ua.random}
    try:
        response = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy}, timeout=10)
        logging.info(f'Запрос к {url} через прокси {proxy} успешен. Статус: {response.status_code}')
        return response.status_code
    except Exception as e:
        logging.error(f'Ошибка при запросе к {url} через прокси {proxy}: {e}')
        return None

# Основной код
if __name__ == '__main__':
    logging.info('Скрипт запущен.')

    # Список прокси (замените на свои прокси)
    proxies = [
        'http://proxy1:port',
        'http://proxy2:port',
        'http://proxy3:port',
    ]

    # URL для запросов
    url = 'https://example.com'

    # Проверка работоспособности прокси
    working_proxies = [proxy for proxy in proxies if check_proxy(proxy)]
    logging.info(f'Рабочие прокси: {working_proxies}')

    # Многопоточные запросы
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request, url, proxy) for proxy in working_proxies]

        # Обработка результатов
        for future in as_completed(futures):
            result = future.result()
            if result:
                logging.info(f'Результат запроса: {result}')
            else:
                logging.warning('Запрос не удался.')

    logging.info('Скрипт завершен.')
