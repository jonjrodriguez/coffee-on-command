from ..client import Client, get_client
from ..match import Matcher, get_matcher


class Action:
    client: Client
    matcher: Matcher

    def __init__(self):
        self.client = get_client()
        self.matcher = get_matcher(client=self.client)
