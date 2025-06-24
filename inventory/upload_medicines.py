import csv
import os
import sys
import django

# ✅ Add project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medstock_backend.settings")
django.setup()

from inventory.models import Medicine

def load_medicines_from_csv(filepath):
    with open(filepath, newline='', encoding='windows-1252') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            name = row['name'].strip()
            unit = row['unit'].strip()
            Medicine.objects.get_or_create(name=name, unit=unit)
    print("✔ Medicines uploaded successfully.")

# Call the function
load_medicines_from_csv("G:/medical/medstock_backend/inventory/medicines.csv")

