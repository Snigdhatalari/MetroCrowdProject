import time
import os
import sys

# ✅ Absolute path to Backend (more reliable)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Backend'))
sys.path.append(BASE_DIR)

# ✅ Correct Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from crowd.models import CrowdRecord
from detect_people import detect_people
from django.conf import settings

# ✅ Debug: confirm same DB
print("DB PATH:", settings.DATABASES['default']['NAME'])


def get_status(count):
    if count < 100:
        return "Free"
    elif count < 300:
        return "Moderate"
    return "Rush"


# ✅ Station name
station_name = "Ameerpet"


while True:
    try:
        people = detect_people()
        status = get_status(people)

        # ✅ SAFE: always fetch same record
        record = CrowdRecord.objects.filter(station=station_name).first()

        # ✅ If not exists → create once
        if not record:
            record = CrowdRecord.objects.create(
                station=station_name,
                people_count=0,
                crowd_status="Free"
            )

        # ✅ Update values
        record.people_count = people
        record.crowd_status = status
        record.save()

        print(f"Updated [{station_name}]: {people} - {status}")

        # 🚨 Alert system
        if people > 300:
            print("⚠️ ALERT: Crowd is very high!")

    except Exception as e:
        print("Error:", e)

    time.sleep(5)