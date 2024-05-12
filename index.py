import tv_api
from tv_app import tv_apps

LAUNCH_APP_KEYWORDS = [
    "включи", "включить",
    "открой", "открыть",
    "запусти", "запустить"
]


def response_with_text(event, text: str, end_session: bool = False) -> dict:
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': str(end_session).lower()
        },
    }


def handler(event, context):
    welcome_text = 'Привет! Я могу включать приложения на телевизоре. Например: скажите "включить ютуб" или "включить кинопоиск".'
    try_again_text = 'Скажите "включить ютуб" или "включить кинопоиск.'
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0:
        request_text = event['request']['original_utterance'].lower()
    else:
        return response_with_text(event, welcome_text)

    # No keywords for Launch App command was found
    if not any((keyword in request_text for keyword in LAUNCH_APP_KEYWORDS)):
        return response_with_text(event, try_again_text)

    for tv_app in tv_apps:
        if not any((app_name in request_text for app_name in tv_app.names)):
            continue
        app_name = tv_app.names[0]
        if tv_api.launch_app(tv_app.id):
            return response_with_text(event, f"Включаю {app_name}")
        return response_with_text(event, f"Произошла ошибка при включении приложения {app_name}")

    return response_with_text(event, try_again_text)
