from django.http import JsonResponse
from weather_api import current_weather

# TODO из weather_api импортируйте функцию current_weather


def weather_view(request):
    if request.method == "GET":
        lat = request.GET.get("lat")
        lon = request.GET.get("lon")
        if lat and lon:
            data = current_weather(lat=lat, lon=lon)
        else:
            data = current_weather(59.93, 30.31)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})
# Create your views here.
