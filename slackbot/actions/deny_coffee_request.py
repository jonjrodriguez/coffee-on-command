from .base import Action


class DenyCoffeeRequest(Action):
    def execute(self, *, user_id, block_id, response_url):
        denied_match = self.matcher.deny_request(user_id, block_id, response_url)
        self.client.post_to_response_url(
            response_url,
            body={
                "replace_original": "true",
                "text": "Oh snap! Maybe next time. :shrug:",
            },
        )

        # Create new request
        coffee_request = denied_match.coffee_request
        match = self.matcher.create_match(coffee_request)
        if match:
            self.client.send_invite(receiver_id=match.user_id, block_id=match.block_id)
            return

        self.client.post_to_private(
            receiver_id=coffee_request.user_id,
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "No coffee buddies found"},
                }
            ],
        )
