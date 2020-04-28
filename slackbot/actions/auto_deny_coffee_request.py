from slackbot.strings import (
    COFFEE_REQUEST,
    CONNECT_REQUEST,
    SEARCHING_FOR_COFFEE_BUDDY,
    RAN_OUT_OF_TIME,
    NO_MATCHES_FOUND,
    SEARCHING_FOR_CONNECT_BUDDY,
)
from .base import Action
from ..models import CoffeeRequest


class AutoDenyCoffeeRequest(Action):
    def execute(self, *, user_id, block_id, ts, channel):
        denied_match = self.matcher.deny_request(user_id, block_id)
        coffee_request = denied_match.coffee_request

        self.client.update(
            channel=channel,
            ts=ts,
            text=COFFEE_REQUEST
            if coffee_request.is_coffee_request()
            else CONNECT_REQUEST,
        )
        self.client.post_to_private(denied_match.user_id, text=RAN_OUT_OF_TIME)

        # Create new request
        match = self.matcher.create_match(coffee_request)

        if not match:
            self.client.update(
                channel=coffee_request.initial_message.channel,
                ts=coffee_request.initial_message.ts,
                color=True,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": SEARCHING_FOR_COFFEE_BUDDY
                            if coffee_request.is_coffee_request()
                            else SEARCHING_FOR_CONNECT_BUDDY,
                        },
                    },
                    {
                        "type": "context",
                        "elements": [{"type": "mrkdwn", "text": NO_MATCHES_FOUND}],
                    },
                ],
            )
