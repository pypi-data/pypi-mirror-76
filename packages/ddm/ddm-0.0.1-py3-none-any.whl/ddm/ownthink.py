import json
import requests
import uuid

OWN_THINK_ROBOT_APP_ID = '96eb7af4fb61b4e5c24b4c99fe6d3583'


def get_mac():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
    return '%s:%s:%s:%s:%s:%s' % (mac[0:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:])


class OwnThinkRobot(object):
    def __init__(self, app_id: str):
        self.app_id = app_id
        mac = get_mac()
        mac.replace(':', '')
        self.user_id = mac

    def chat(self, message: str):
        response = requests.get(
            f'https://api.ownthink.com/bot?appid={self.app_id}&userid={self.user_id}&spoken={message}')
        info = json.loads(response.text)
        if info['message'] == 'success':
            return info['data']['info']['text']
        else:
            return "请求错误"


own_think_robot = OwnThinkRobot(OWN_THINK_ROBOT_APP_ID)
