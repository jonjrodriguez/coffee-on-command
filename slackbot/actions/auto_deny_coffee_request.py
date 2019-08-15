from .base import Action


class AutoDenyCoffeeRequest(Action):
    def execute(self, *, user_id, block_id, response_url):
        self.matcher.deny_request(user_id, block_id, response_url)
        self.client.post_to_private(
            receiver_id=user_id,
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "Sorry, you took too long"},
                }
            ],
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
