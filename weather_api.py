import requests
from pprint import pprint
from datetime import datetime

# Словарь перевода значений направления ветра
DIRECTION_TRANSFORM = {
    'n': 'северное',
    'nne': 'северо - северо - восточное',
    'ne': 'северо - восточное',
    'ene': 'восточно - северо - восточное',
    'e': 'восточное',
    'ese': 'восточно - юго - восточное',
    'se': 'юго - восточное',
    'sse': 'юго - юго - восточное',
    's': 'южное',
    'ssw': 'юго - юго - западное',
    'sw': 'юго - западное',
    'wsw': 'западно - юго - западное',
    'w': 'западное',
    'wnw': 'западно - северо - западное',
    'nw': 'северо - западное',
    'nnw': 'северо - северо - западное',
    'c': 'штиль',
}


def current_weather(lat:float, lon:float) -> dict:
    """
    lat - type float
    lan - type float
    return dict
    """
    token = 'd1f5b98b5da04203a78154941252904'  # Вставить ваш токен из api.weatherapi.com
    url = f"https://api.weatherapi.com/v1/current.json?key={token}&q={lat},{lon}"
    response = requests.get(url)
    data = response.json()

    # Данная реализация приведена для api.weatherapi.com
    result = {
        'city': data['location']['name'],  # Город
        'time': data['current']['last_updated'],  # Время обновления данных
        'temp': data['current']['temp_c'],  # TODO Реализовать вычисление температуры из данных полученных от API
        'feels_like_temp': data['current']['feelslike_c'],  # TODO Реализовать вычисление ощущаемой температуры из данных полученных от API
        'pressure': round(data['current']['pressure_mb'] * 0.75, 1),  # TODO Реализовать вычисление давления из данных полученных от API
        'humidity': data['current']['humidity'],  # TODO Реализовать вычисление влажности из данных полученных от API
        'wind_speed': round(data['current']['wind_kph'] / 3.6, 1),  # TODO Реализовать вычисление скорости ветра из данных полученных от API
        'wind_gust': round(data['current']['gust_kph'] / 3.6, 1),  # TODO Реализовать вычисление скорости порывов ветка из данных полученных от API
        'wind_dir': DIRECTION_TRANSFORM.get(data['current']['wind_dir'].lower()),  # Направление ветра
    }
    return result


if __name__ == "__main__":
    pprint(current_weather(59.93, 30.31))  # Проверка работы для координат Санкт-Петербурга
