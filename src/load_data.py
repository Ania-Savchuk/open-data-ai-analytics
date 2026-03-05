import os
import requests
import zipfile
import io
from pathlib import Path

DATA_URL = "https://data.gov.ua/dataset/0ffd8b75-0628-48cc-952a-9302f9799ec0/resource/3f13166f-090b-499e-8e23-e9851c5a5f67/download/reestrtz2026.zip"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"
FINAL_CSV_NAME = "vehicle_registrations.csv"


def download_and_extract():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"--- Завантаження даних у: {OUTPUT_DIR} ---")

    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(DATA_URL, headers=headers, stream=True)
        response.raise_for_status()

        print("Розпакування у пам'яті...")

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            csv_files = [f for f in z.namelist() if f.endswith('.csv')]

            if not csv_files:
                print("Помилка: CSV не знайдено.")
                return

            original_filename = csv_files[0]

            z.extract(original_filename, OUTPUT_DIR)

            old_path = OUTPUT_DIR / original_filename
            new_path = OUTPUT_DIR / FINAL_CSV_NAME

            if new_path.exists():
                os.remove(new_path)

            os.rename(old_path, new_path)

            print(f"--- Успіх! Файл лежить тут: {new_path} ---")

    except Exception as e:
        print(f"Сталася помилка: {e}")


if __name__ == "__main__":
    download_and_extract()