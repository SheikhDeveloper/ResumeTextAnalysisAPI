import requests
import time
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат сообщения
    handlers=[
        logging.FileHandler('script.log'),  # Запись логов в файл
        logging.StreamHandler()  # Вывод логов в консоль
    ]
)

URL = 'http://localhost:5000/resume_analysis/predict'

while True:
    try:
        # Логируем начало запроса
        logging.info(f"Отправка запроса на {URL}")

        # Отправка запроса
        resp = requests.get(URL)
        resp.raise_for_status()  # Проверка на ошибки HTTP

        # Логируем успешный ответ
        logging.info(f"Ответ получен: {resp.status_code}")
        data = resp.json()  # Предполагаем, что ответ в формате JSON
        logging.info(f"Данные ответа: {data}")  # Логируем данные ответа

    except requests.exceptions.RequestException as e:
        # Логируем ошибку
        logging.error(f"Ошибка при запросе: {e}")

    # Логируем временную метку перед ожиданием
    logging.info(f"Ожидание 5 минут перед следующим запросом...")

    # Ожидание 5 минут
    time.sleep(300)
