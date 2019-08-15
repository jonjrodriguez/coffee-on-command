from .base import Action


class AutoDenyCoffeeRequest(Action):
    def execute(self, *, user_id, block_id, ts, channel):
        self.matcher.deny_request(user_id, block_id)
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
        # coffee_request = denied_match.coffee_request
        # match = self.matcher.create_match(coffee_request)
        # if match:
        #     self.client.send_invite(receiver_id=match.user_id, block_id=match.block_id)
        #     return
        #
        # self.client.post_to_private(
        #     receiver_id=coffee_request.user_id,
        #     blocks=[
        #         {
        #             "type": "section",
        #             "text": {"type": "mrkdwn", "text": "No coffee buddies found"},
        #         }
        #     ],
        # )
