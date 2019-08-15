from .base import Action


class AcceptCoffeeRequest(Action):
    def execute(self, *, user_id, block_id, response_url):
        match = self.matcher.accept_request(user_id, block_id, response_url)

        requested_user = match.coffee_request.user_id
        matched_user = match.user_id

        self.client.post_to_channel(
            f"<@{requested_user}> is grabbing coffee with <@{matched_user}>"
        )

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
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "Hang tight, letting your buddy know!",
                        }
                    ],
                },
            ],
        )
        self.client.post_to_private(
            matched_user, text=f"<@{requested_user}> is your buddy!"
        )

        self.client.update(
            channel=match.coffee_request.initial_message.channel,
            ts=match.coffee_request.initial_message.ts,
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
                    "elements": [
                        {"type": "mrkdwn", "text": "Woo hoo! Go get your brew!"}
                    ],
                },
            ],
        )
        self.client.post_to_private(
            requested_user, text=f"<@{matched_user}> is your buddy!"
        )
