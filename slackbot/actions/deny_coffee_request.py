from .base import Action


class DenyCoffeeRequest(Action):
    def execute(self, *, user_id, block_id, response_url):
        denied_match = self.matcher.deny_request(user_id, block_id, response_url)
        self.client.post_to_response_url(
            response_url, replace=True, text="Oh snap! Maybe next time. :shrug:"
        )

        # Create new request
        coffee_request = denied_match.coffee_request
        self.matcher.create_match(coffee_request)
