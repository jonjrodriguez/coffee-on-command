from slackbot.strings import SEARCHING_FOR_COFFEE_BUDDY, COFFEE_REQUEST, RAN_OUT_OF_TIME, MAYBE_NEXT_TIME
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
            else "I canceled your request"
        )

        self.client.post_to_response_url(
            response_url=response_url,
            replace=True,
            color=True,
            text=SEARCHING_FOR_COFFEE_BUDDY,
            blocks=[
                {
                    "type": "context",
                    "elements": [{"type": "mrkdwn", "text": cancel_text}],
                },
            ],
        )

        self.client.post_to_private(
            receiver_id=user_id, text=MAYBE_NEXT_TIME
        )

        for match in coffee_request.matches.filter(is_accepted=None):
            match.is_accepted = False
            match.save()

            self.client.update(
                channel=match.initial_message.channel,
                ts=match.initial_message.ts,
                text=COFFEE_REQUEST,
            )
            self.client.post_to_private(
                match.user_id,
                text=RAN_OUT_OF_TIME,
            )

