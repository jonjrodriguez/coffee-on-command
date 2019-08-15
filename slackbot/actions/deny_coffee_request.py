from slackbot.strings import COFFEE_REQUEST, MAYBE_NEXT_TIME, SEARCHING_FOR_COFFEE_BUDDY, NO_MATCHES_FOUND, NO_REPLY
from .base import Action


class DenyCoffeeRequest(Action):
    def execute(self, *, user_id, block_id, response_url):
        denied_match = self.matcher.deny_request(user_id, block_id, response_url)
        self.client.post_to_response_url(
            response_url,
            replace=True,
            color=True,
            text=COFFEE_REQUEST,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": COFFEE_REQUEST,
                    },
                },
                {
                    "type": "context",
                    "elements": [{"type": "mrkdwn", "text": NO_REPLY}],
                },
            ],
        )
        self.client.post_to_private(user_id, text=MAYBE_NEXT_TIME)

        # Create new request
        coffee_request = denied_match.coffee_request
        match = self.matcher.create_match(coffee_request)

        if not match:
            self.client.update(
                channel=coffee_request.initial_message.channel,
                ts=coffee_request.initial_message.ts,
                color=True,
                text=SEARCHING_FOR_COFFEE_BUDDY,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": SEARCHING_FOR_COFFEE_BUDDY,
                        },
                    },
                    {
                        "type": "context",
                        "elements": [{"type": "mrkdwn", "text": NO_MATCHES_FOUND}],
                    },
                ],
            )
