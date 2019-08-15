from .base import Action
from ..models import CoffeeRequest


class DenyCoffeeRequest(Action):
    def execute(self, *, user_id, block_id, response_url):
        denied_match = self.matcher.deny_request(user_id, block_id, response_url)
        self.client.post_to_response_url(
            response_url,
            replace=True,
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
                    "elements": [{"type": "mrkdwn", "text": "You replied no."}],
                },
            ],
        )
        self.client.post_to_private(user_id, text="Oh snap! Maybe next time. :shrug:")

        # Create new request
        coffee_request = denied_match.coffee_request
        match = self.matcher.create_match(coffee_request)

        if match:
            return

        coffee_request.status = CoffeeRequest.STATUS_CANCELLED
        coffee_request.save()

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
                    "elements": [{"type": "mrkdwn", "text": "No matches found!"}],
                },
            ],
        )
