from .base import Action
from ..models import CoffeeRequest


class CancelCoffeeRequest(Action):
    def execute(self, *, user_id, block_id, response_url, expired=False):
        coffee_request = CoffeeRequest.objects.filter(
            status=CoffeeRequest.STATUS_PENDING, user_id=user_id, block_id=block_id
        ).first()

        if not coffee_request:
            return

        coffee_request.status = CoffeeRequest.STATUS_CANCELLED
        coffee_request.save()

        cancel_text = (
            "Sorry, looks like everyone is too busy for coffee. Please try again later!"
            if expired
            else "Cancelled"
        )

        self.client.update(
            channel=coffee_request.initial_message.channel,
            ts=coffee_request.initial_message.ts,
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
                    "elements": [{"type": "mrkdwn", "text": cancel_text}],
                },
            ],
        )

        self.client.post_to_private(
            receiver_id=user_id, text="Oh snap! Maybe next time. :shrug:"
        )

        for match in coffee_request.matches.filter(is_accepted=None):
            match.is_accepted = False
            match.save()

            self.client.update(
                channel=match.initial_message.channel,
                ts=match.initial_message.ts,
                color=True,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Need a little stretch? :ok_woman: Let's grab a coffee?",
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

