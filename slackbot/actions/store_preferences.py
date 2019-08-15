from datetime import time

from slackbot.strings import PREFERENCES_RECEIVED
from .base import Action
from ..models import Member


class StorePreferencesAction(Action):
    def execute(self, *, user_id, callback_id, data, response_url):
        member = Member.objects.get(user_id=user_id)
        member.start_time = time(int(data.get('start_time')))
        member.end_time = time(int(data.get('end_time')))
        member.coffee_count = data.get('coffee_count')
        member.save()

        self.client.post_to_response_url(
            response_url=response_url,
            replace=True,
            text=PREFERENCES_RECEIVED
        )