from .base import Action


class CancelCoffeeRequest(Action):
    def execute(self, *, user_id, block_id, response_url):
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
