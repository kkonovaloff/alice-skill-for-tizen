import json
import os

import requests

DEVICE_ID = os.environ.get("DEVICE_ID", "")
TV_AUTH_TOKEN = os.environ.get("TV_AUTH_TOKEN", "")

if not DEVICE_ID:
    print("Device ID is not set. Aborting...")
    os.abort()
if not TV_AUTH_TOKEN:
    print("TV Auth Token is not set. Aborting...")
    os.abort()

API_BASEURL = "https://api.smartthings.com/v1"
API_DEVICES = API_BASEURL + "/devices/"
API_DEVICE = API_DEVICES + DEVICE_ID
API_COMMANDS = API_DEVICE + "/commands/"
API_STATUS = API_DEVICE + "/status/"

REQUEST_HEADERS = {"Authorization": "Bearer " + TV_AUTH_TOKEN}

"""
Returns TV's On/Off status
"""
def get_switch_status() -> bool:
    with requests.get(API_STATUS, headers=REQUEST_HEADERS) as result:
        if result.status_code != 200:
            print(
                f"[get_switch_status] Error: status code: {result.status_code}\n{result.content}")
            return False
        response = result.content
    try:
        response = json.loads(response)
        switch = response["components"]["main"]["switch"]["switch"]["value"]
        return switch == "on"
    except Exception as e:
        print(f"[get_switch_status] Error while parsing response: {e}")
        return False


def update_switch_status(status: bool) -> bool:
    SWITCH_COMMAND = f"""
    {{
        "commands": [
            {{
                "component": "main",
                "capability": "switch",
                "command": "{"on" if status else "off"}"
            }}
        ]
    }}
    """
    with requests.post(API_COMMANDS, data=SWITCH_COMMAND, headers=REQUEST_HEADERS) as result:
        if result.status_code == 200:
            return True
        print(
            f"[update_switch_status] Error: status code: {result.status_code}\n{result.content}")
        return False


def launch_app(app_id: int) -> bool:
    LAUNCH_APP_COMMAND = f"""
    {{
        "commands": [
            {{
                "component": "main",
                "capability": "custom.launchapp",
                "command": "launchApp",
                "arguments": [
                    "{app_id}"
                ]
            }}
        ]
    }}
    """

    with requests.post(API_COMMANDS, data=LAUNCH_APP_COMMAND, headers=REQUEST_HEADERS) as result:
        if result.status_code == 200:
            return True
        print(
            f"[open_app_on_tv] Error: status code: {result.status_code}\n{result.content}")
        return False


def set_volume(volume: int) -> bool:
    SET_VOLUME_COMMAND = f"""
    {{
        "commands": [
            {{
                "component": "main",
                "capability": "audioVolume",
                "command": "setVolume",
                "arguments": [
                    {volume}
                ]
            }}
        ]
    }}
    """
    with requests.post(API_COMMANDS, data=SET_VOLUME_COMMAND, headers=REQUEST_HEADERS) as result:
        if result.status_code == 200:
            return True
        print(
            f"[set_volume] Error: status code: {result.status_code}\n{result.content}")
        return False


def volume_up_down(up: bool) -> bool:
    VOLUME_UPDOWN_COMMAND = f"""
    {{
        "commands": [
            {{
                "component": "main",
                "capability": "audioVolume",
                "command": "{"volumeUp" if up else "volumeDown"}"
            }}
        ]
    }}
    """
    with requests.post(API_COMMANDS, data=VOLUME_UPDOWN_COMMAND, headers=REQUEST_HEADERS) as result:
        if result.status_code == 200:
            return True
        print(
            f"[volume_up_down] Error: status code: {result.status_code}\n{result.content}")
        return False
