# crowd/views.py

from django.http import JsonResponse
from .models import CrowdRecord
from .ml_model import predict_crowd


# ✅ API: Predict crowd based on hour, day, and count
def predict_view(request):
    try:
        hour = int(request.GET.get('hour'))
        day = int(request.GET.get('day'))
        count = int(request.GET.get('count'))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid parameters"}, status=400)

    result = predict_crowd(hour, day, count)
    return JsonResponse({"prediction": result})


# ✅ API: Get latest crowd data for a specific station
def get_crowd_data(request):
    station = request.GET.get("station", "Ameerpet")

    # Get the latest record for this station
    record = CrowdRecord.objects.filter(station=station).order_by('-created_at').first()

    if record:
        data = {
            "station": record.station,
            "people_count": record.people_count,
            "crowd_status": record.crowd_status,
            "updated_at": record.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        data = {"error": "No data found for this station"}

    return JsonResponse(data)