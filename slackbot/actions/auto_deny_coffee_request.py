from .base import Action


class AutoDenyCoffeeRequest(Action):
    def execute(self, *, user_id, block_id, ts, channel):
        denied_match = self.matcher.deny_request(user_id, block_id)
        self.client.update(
            channel=channel,
            ts=ts,
            color=True,
            as_user=True,
            blocks=[
                {"type": "section", "text": {"type": "mrkdwn", "text": "*Coffee Time!*"}},
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "Are you free to grab a coffee?"},
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "Sorry, it looks like you were busy."},
                },
            ]
        )

        # Create new request
        coffee_request = denied_match.coffee_request
        self.matcher.create_match(coffee_request)