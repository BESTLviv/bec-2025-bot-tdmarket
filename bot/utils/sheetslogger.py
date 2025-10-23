# # bot/utils/sheetslogger.py (ОНОВЛЕНА ВЕРСІЯ)

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import datetime
# import asyncio

# # --- Налаштування ---
# SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# CREDS_FILE = 'techshop-469612-8d17d1de7962.json'  # Шлях до вашого файлу
# SPREADSHEET_TITLE = 'TD market transactions' # Назва вашої таблиці

# def _write_to_sheet_sync(data_row):
#     """Синхронна функція для запису в таблицю."""
#     try:
#         creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
#         client = gspread.authorize(creds)
#         sheet = client.open(SPREADSHEET_TITLE).sheet1
#         sheet.append_row(data_row, value_input_option='USER_ENTERED')
#         print(f"Лог записано в Google Sheets: {data_row}")
#     except Exception as e:
#         print(f"!!! Помилка запису логу в Google Sheets: {e}")

# async def log_action(
#     action: str, 
#     user_id: int = None, 
#     username: str = None, 
#     team_name: str = None, 
#     details: str = ""
# ):
#     """
#     Асинхронно записує рядок логу в Google Sheets.
#     Тепер включає username та team_name.
#     """
#     timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
#     # Оновлений формат рядка для запису
#     data_to_log = [
#         timestamp,
#         action,
#         str(user_id) if user_id else "N/A",
#         username if username else "N/A",      # Новий стовпець
#         team_name if team_name else "N/A",    # Новий стовпець
#         details
#     ]
    
#     # Запускаємо синхронну функцію в окремому потоці, щоб не блокувати бота
#     await asyncio.to_thread(_write_to_sheet_sync, data_to_log)
import gspread
import datetime
import asyncio
import os
import json
import base64

# --- Налаштування ---
# Назва файлу більше не потрібна, але назва таблиці залишається
SPREADSHEET_TITLE = 'TD market transactions' # Назва вашої таблиці

def _write_to_sheet_sync(data_row):
    """
    Синхронна функція для запису в таблицю.
    Тепер використовує змінні оточення для автентифікації.
    """
    try:
        # +++ НОВИЙ КОД (використовуємо його) +++

        # 1. Отримуємо закодовані дані зі змінної оточення
        creds_base64 = os.getenv('GOOGLE_CREDS_BASE64')
        if not creds_base64:
            print("!!! КРИТИЧНА ПОМИЛКА: Змінна оточення GOOGLE_CREDS_BASE64 не встановлена!")
            return

        # 2. Декодуємо рядок Base64 назад у JSON-рядок
        creds_json_str = base64.b64decode(creds_base64).decode('utf-8')

        # 3. Перетворюємо JSON-рядок у словник Python
        creds_dict = json.loads(creds_json_str)

        # 4. Авторизуємося в gspread за допомогою словника, а не файлу
        client = gspread.service_account_from_dict(creds_dict)
        
        sheet = client.open(SPREADSHEET_TITLE).sheet1
        sheet.append_row(data_row, value_input_option='USER_ENTERED')
        print(f"Лог записано в Google Sheets: {data_row}")

    except Exception as e:
        print(f"!!! Помилка запису логу в Google Sheets: {e}")

async def log_action(
    action: str, 
    user_id: int = None, 
    username: str = None, 
    team_name: str = None, 
    details: str = ""
):
    """
    Асинхронно записує рядок логу в Google Sheets.
    (Ця функція залишається без змін)
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    data_to_log = [
        timestamp,
        action,
        str(user_id) if user_id else "N/A",
        username if username else "N/A",
        team_name if team_name else "N/A",
        details
    ]
    
    await asyncio.to_thread(_write_to_sheet_sync, data_to_log)