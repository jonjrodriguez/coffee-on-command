from .base import Action


class AutoDenyCoffeeRequest(Action):
    def execute(self, *, user_id, block_id, ts, channel):
        denied_match = self.matcher.deny_request(user_id, block_id)
        self.client.update(
            channel=channel,
            ts=ts,
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
                    "elements": [{"type": "mrkdwn", "text": "Too slow!"}],
                },
            ],
        )
        self.client.post_to_private(
            denied_match.user_id,
            text="Looks like you ran out of time. :disappointed: If you want me to find you another buddy, let me know!",
        )

        # Create new request
        coffee_request = denied_match.coffee_request
        self.matcher.create_match(coffee_request)
