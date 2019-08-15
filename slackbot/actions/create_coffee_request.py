from slackbot.strings import HANG_IN_THERE, SEARCHING_FOR_COFFEE_BUDDY
from .base import Action
from ..models import CoffeeRequest, SlackMessage


class CreateCoffeeRequest(Action):
    def execute(self, *, user_id: str, response_url: str):
        if not self.client.assert_channel_member(user_id):
            return

        if CoffeeRequest.objects.filter(
            user_id=user_id, status=CoffeeRequest.STATUS_PENDING
        ).exists():
            self.client.post_to_private(
                receiver_id=user_id,
                text=HANG_IN_THERE,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": HANG_IN_THERE,
                        },
                    }
                ],
            )
            return

        coffee_request = self.matcher.create_request(user_id, response_url)
        match = self.matcher.create_match(coffee_request)
        if not match:
            return

        response = self.client.post_to_private(
            receiver_id=user_id,
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

        message = SlackMessage.objects.create(
            ts=response["ts"], channel=response["channel"]
        )
        coffee_request.initial_message = message
        coffee_request.save()
