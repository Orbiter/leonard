module_config = {
    "name": "test",
    "public_name": {
        "en": "Test",
        "ru": "Тест"
    },
    "description": {
        "en": "Check bot for basic operability",
        "ru": "Проверка бота на общую работоспособность"
    },
    "regexps": {
            "en": [
                "!t(est)?"
            ],
            "ru": [
                "!т(ест)?"
            ]
    },
    "command_format": {
        "en": "!test",
        "ru": "!тест"
    },
    "examples": {
        "en": [
            "!test",
            "!t"
        ],
        "ru": [
            "!тест",
            "!т"
        ]
    },
    "adapters": []
}

answer = {
    "en": "Test completed. Message: '{text}' from {name}",
    "ru": "Тест пройден. Cообщение: '{text}' от {name}"
}


def get_answer(message, lang, bot, options):
    bot.send_message(
        message_text=answer[lang].format(
            text=message["text"],
            name=message["sender_name"]
        )
    )
    return True