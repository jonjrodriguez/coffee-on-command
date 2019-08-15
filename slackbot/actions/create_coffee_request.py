from ..models import MatchSlackMessage
from .base import Action


class CreateCoffeeRequest(Action):
    def execute(self, *, user_id: str, response_url: str):
        coffee_request = self.matcher.create_request(user_id, response_url)

        match = self.matcher.create_match(coffee_request)
        if not match:
            self.client.post_to_private(
                receiver_id=user_id,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "I'm sorry, I couldn't find a buddy. :disappointed: Let's try again later.",
                        },
                    }
                ],
            )
            return

        response = self.client.send_invite(receiver_id=match.user_id, block_id=match.block_id)

        # Save the postMessage ts so we can update the message later
        ts = response["ts"]
        channel = response["channel"]
        MatchSlackMessage.objects.create(ts=ts, channel=channel, match=match)

        self.client.post_to_private(
            receiver_id=user_id,
            color=True,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "I'm searching for your coffee buddy. :coffee: Let me know if you change your mind. :wink:",
                    },
                },
                {
                    "type": "actions",
                    "block_id": str(coffee_request.block_id),
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Cancel"},
                            "style": "danger",
                            "value": "CANCEL",
                        }
                    ],
                },
            ],
        )
