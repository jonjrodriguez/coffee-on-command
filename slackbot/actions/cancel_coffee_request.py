from .base import Action
from ..models import CoffeeRequest


class CancelCoffeeRequest(Action):
    def execute(self, *, user_id, block_id, response_url):
        coffee_request = CoffeeRequest.objects.filter(
            status=CoffeeRequest.STATUS_PENDING, user_id=user_id, block_id=block_id
        ).first()

        if not coffee_request:
            return

        coffee_request.status = CoffeeRequest.STATUS_CANCELLED
        coffee_request.save()

        self.client.post_to_response_url(
            response_url,
            replace=True,
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
                    "type": "context",
                    "elements": [{"type": "mrkdwn", "text": "Cancelled"}],
                },
            ],
        )

        for match in coffee_request.matches.all():
            match.is_accepted = False
            match.save()

            self.client.update(
                channel=match.message.channel,
                ts=match.message.ts,
                color=True,
                as_user=True,
                blocks=[
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": "*Coffee Time!*"},
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Are you free to grab a coffee?",
                        },
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": "Sorry, the person cancelled their request.",
                            }
                        ],
                    },
                ],
            )

