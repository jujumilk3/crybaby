import sys
import traceback

import requests

# package info
__version__ = "0.0.3"

from crybaby.exceptions import NoJoinChannelException


class SlackClient:
    url = "https://slack.com/api/chat.postMessage"

    def __init__(self, token: str, channel_id: str, apply_code_block: bool = True):
        self.token = token
        self.channel_id = channel_id
        self.apply_code_block = apply_code_block
        if not self.is_token_joined_at_channel(channel_id):
            raise NoJoinChannelException("Token is not joined at channel")
        self.register_exception_handler()

    def get_channel_list(self):
        url = "https://slack.com/api/conversations.list"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        response = requests.get(url=url, headers=headers)
        return response.json()

    def is_token_joined_at_channel(self, channel_id: str):
        channel_list = self.get_channel_list()
        for channel in channel_list["channels"]:
            if channel["id"] == channel_id and channel["is_member"]:
                return True
        return False

    def post_message(self, text: str):
        payload = {
            "channel": self.channel_id,
            "text": f"```{text}```" if self.apply_code_block else text,
        }
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        response = requests.post(url=self.url, headers=headers, json=payload)
        return response.json()

    def crybaby_exception_handler(self, exc_type, exc_value, exc_traceback):
        traceback_text = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.post_message(traceback_text)
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    def register_exception_handler(self):
        sys.excepthook = self.crybaby_exception_handler

    def capture_exception(self, exc_type, exc_value, exc_traceback):
        traceback_text = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.post_message(traceback_text)


slack_client: SlackClient


def setup(slack_token: str, slack_channel_id: str):
    global slack_client
    slack_client = SlackClient(slack_token, slack_channel_id)


def catch(e: Exception):
    global slack_client
    if slack_client is None:
        raise Exception("crybaby is not initialized")
    slack_client.capture_exception(*sys.exc_info())
