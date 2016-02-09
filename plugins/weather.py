"""
name: weather
description: "Plugin that "
priority: 100
"""
import json
import requests
import leonard

FORECAST_IO_BASE = 'https://api.forecast.io/forecast/{}/{},{}?lang={}&units={}'


def get_weather_data(token, location, language_code, units_id):
    response = requests.get(FORECAST_IO_BASE.format(
        token, location[0], location[1],
        language_code, units_id
    ))
    return json.loads(response.text)


@leonard.hooks.keywords([['погода'], ['weather']])
def weather_message(message, bot):
    location = message.sender.data['location']
    if location is None:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.set_location_text
        )
        bot.send_message(answer)
        return

    weather_data = get_weather_data(
        bot.config.get('LEONARD_FORECAST_IO_TOKEN'),
        location, message.locale.language_code, message.locale.units_id
    )

    now_temperature = (
        str(weather_data['currently']['temperature']) + message.locale.units
    )
    now_summary = weather_data['currently']['summary']
    daily_summary = weather_data['daily']['summary']

    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.base_text.format(
            now_temperature,
            now_summary,
            daily_summary
        )
    )
    bot.send_message(answer)


class EnglishLocale:
    language_code = 'en'
    units_id = 'us'
    units = ' °F'
    base_text = (
        "OK, I tell you some words about weather\n\n"
        "Now: {} - {}\n\n"
        "{}"
    )
    set_location_text = "Send your location for correct weather forecasts."


class RussianLocale:
    language_code = 'ru'
    units_id = 'si'
    units = ' °C'
    base_text = (
        "ОК, я расскажу тебе про погоду. \n\n"
        "Сейчас: {} - {}\n\n"
        "{}"
    )
    set_location_text = (
        "Отправьте ваше местоположение "
        "для корректного просмотра погоды."
    )