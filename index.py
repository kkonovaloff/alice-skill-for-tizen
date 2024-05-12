import tv_api
from tv_app import tv_apps

LAUNCH_APP_KEYWORDS = (
    "включи", "включить",
    "открой", "открыть",
    "запусти", "запустить"
)

GET_TV_STATUS_KEYWORDS = (
    "статус",
    "включен",
)


def handler(event, context) -> dict:
    welcome_text = 'Привет! Я могу включать приложения на телевизоре. Например: скажите "включить ютуб" или "включить кинопоиск".'
    try_again_text = 'Скажите "включить ютуб" или "включить кинопоиск.'
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0:
        request_text = event['request']['original_utterance'].lower()
        tokens = list(
            map(lambda s: s.lower(), event['request']['nlu']['tokens']))
    else:
        return response_with_text(event, welcome_text)

    if any((keyword in tokens for keyword in LAUNCH_APP_KEYWORDS)):
        return handle_launch_app(event, request_text)

    if any((keyword in tokens for keyword in GET_TV_STATUS_KEYWORDS)):
        return handle_tv_status(event)

    return response_with_text(event, try_again_text)


def handle_launch_app(event, request_text: str) -> dict:
    tv_api.update_switch_status(True)  # Turn on the TV

    for tv_app in tv_apps:
        if not any((app_name in request_text for app_name in tv_app.names)):
            continue
        app_name = tv_app.names[0]
        if tv_api.launch_app(tv_app.id):
            return response_with_text(event, f"Включаю {app_name}")
        return response_with_text(event, f"Произошла ошибка при включении приложения {app_name}")
    return response_with_text(event, "Не могу найти приложение по вашему запросу.")


def handle_tv_status(event) -> dict:
    tv_status = tv_api.get_switch_status()
    return response_with_text(event, f"Статус телевизора: {"включен" if tv_status else "выключен"}.")


def response_with_text(event, text: str, end_session: bool = False) -> dict:
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': str(end_session).lower()
        },
    }
