from slackbot.models import Recommendation
from slackbot.strings import COFFEE_REQUEST, LETTING_YOUR_BUDDY_KNOW, SEARCHING_FOR_COFFEE_BUDDY, SUCCESS_MESSAGE
from .base import Action


class AcceptCoffeeRequest(Action):
    def execute(self, *, user_id, block_id, response_url):
        match = self.matcher.accept_request(user_id, block_id, response_url)

        requested_user = match.coffee_request.user_id
        matched_user = match.user_id

        recommendation = Recommendation.objects.order_by('?').first()

        self.client.post_to_channel(
            f"<@{requested_user}> is grabbing coffee with <@{matched_user}>"
        )

        self.client.post_to_response_url(
            response_url,
            replace=True,
            color=True,
            text=COFFEE_REQUEST,
            blocks=[
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": LETTING_YOUR_BUDDY_KNOW,
                        }
                    ],
                },
            ],
        )
        self.client.post_to_private(
            matched_user,
            text=f"<@{requested_user}> is your buddy!\n"
            f"We recommend {recommendation.name} and trying {recommendation.specialty}.\n"
            f"{recommendation.link}"
        )

        self.client.update(
            channel=match.coffee_request.initial_message.channel,
            ts=match.coffee_request.initial_message.ts,
            text=SEARCHING_FOR_COFFEE_BUDDY,
            color=True,
            blocks=[
                {
                    "type": "context",
                    "elements": [
                        {"type": "mrkdwn", "text": SUCCESS_MESSAGE}
                    ],
                },
            ],
        )
        self.client.post_to_private(
            requested_user,
            text=f"<@{matched_user}> is your buddy!\n"
            f"We recommend {recommendation.name} and trying {recommendation.specialty}.\n"
            f"{recommendation.link}"
        )
