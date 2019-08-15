from slackbot.strings import HANG_IN_THERE
from .base import Action
from ..models import CoffeeRequest


class RemindCoffeeRequester(Action):
    def execute(self, *, user_id, block_id):
        coffee_request = CoffeeRequest.objects.filter(
            status=CoffeeRequest.STATUS_PENDING, user_id=user_id, block_id=block_id
        ).first()

        if not coffee_request:
            return

        self.client.post_to_private(
            user_id,
            text=HANG_IN_THERE,
        )
