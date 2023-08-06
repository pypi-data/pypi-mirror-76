import websockets
import asyncio
import urllib
import json
from .constants import *


class WebsocketListener:
    def __init__(self, instance: dict, access_token: str, stream="user"):
        """Initiate a WebSocket Listener

        :param instance: (dict) Mastodon.py dict of the instance
        :param access_token: (str)
        :param stream: (str)
        """

        self._instance = instance["uri"]
        try:
            self._ws_endpoint = urllib.parse.urljoin(
                instance["urls"]["streaming_api"],
                f"/api/v1/streaming?access_token={access_token}&stream={stream}",
            )
        except KeyError:
            raise Exception(
                f"The instance {instance['uri']} did not provide a WebSocket URL"
            )

    def on_update(self, status):
        """Stub method to be overwritten by bot dev"""
        pass

    def on_notification(self, notification):
        """Stub method to be overwritten by bot dev"""
        pass

    async def _stream(self):
        async with websockets.connect(self._ws_endpoint) as socket:
            while True:
                received = await socket.recv()
                # received:
                # {
                #    "event": "update|notification|...",
                #    "payload": "{\"account\":{...}}"
                # }
                # payload is a string of a JSON object, not one itself
                try:
                    response = json.loads(received)
                    event = response["event"]
                    payload = json.loads(response["payload"])
                    if event == UPDATE:
                        self.on_update(payload)
                    elif event == NOTIFICATION:
                        self.on_notification(payload)
                except json.decoder.JSONDecodeError:
                    # occasionally the server would send an empty event
                    pass

    def start_stream(self):
        asyncio.get_event_loop().run_until_complete(self._stream())

