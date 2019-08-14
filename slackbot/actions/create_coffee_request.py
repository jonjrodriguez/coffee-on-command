from .base import Action


class CreateCoffeeRequest(Action):
    def execute(self, *, user_id: str, response_url: str):
        coffee_request = self.matcher.create_request(user_id, response_url)
        match = self.matcher.create_match(coffee_request)

        if match:
            self.client.send_invite(receiver_id=match.user_id, block_id=match.block_id)
            return

        self.client.post_to_private(
            receiver_id=user_id,
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "No coffee buddies found"},
                }
            ],
        )
