import csv
import os
from config import CSV_PATH

FIELDNAMES = ['name', 'surname', 'email', 'phone', 'company', 'position', 'website']


def ensure_csv():
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def append_contact(data: dict):
    ensure_csv()
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({k: data.get(k, '') for k in FIELDNAMES})
