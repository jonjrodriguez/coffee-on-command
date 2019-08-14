from .base import Action


class AcceptCoffeeRequest(Action):
    def execute(self, *, user_id, block_id, response_url):
        match = self.matcher.accept_request(user_id, block_id, response_url)

        requested_user = match.coffee_request.user_id
        matched_user = match.user_id

        self.client.post_to_channel(
            f"<@{requested_user}> is going to grab coffee with <@{matched_user}>"
        )

        self.client.post_to_response_url(
            response_url,
            body={
                "replace_original": "true",
                "text": "Hang tight, letting your buddy know! :coffee:",
            },
        )
