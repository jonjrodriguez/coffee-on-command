from random import choice

from slackbot.models import Recommendation
from slackbot.strings import (
    COFFEE_REQUEST,
    CONNECT_REQUEST,
    LETTING_YOUR_BUDDY_KNOW,
    SEARCHING_FOR_COFFEE_BUDDY,
    SEARCHING_FOR_CONNECT_BUDDY,
    COFFEE_SUCCESS_MESSAGE,
    CONNECT_SUCCESS_MESSAGE,
)
from .base import Action

icebreakers = [
    "share two truths and a lie!",
    "share the fun fact you shared at all hands, and what you would share if you could go back for a re-do!",
    "talk about the mission snack you miss the most :cry:",
    "what's your WFH must-haves to get you through the day?",
    "share your latest Netflix binge.",
    "what was the last thing you bought online? How wrong is the delivery ETA so far?",
    "what’s your new coworker (fam member/pet) like? anything they do that you love/hate?",
]


class AcceptCoffeeRequest(Action):
    def execute(self, *, user_id, block_id, response_url):
        match = self.matcher.accept_request(user_id, block_id, response_url)
        is_coffee_request = match.coffee_request.is_coffee_request()

        requested_user = match.coffee_request.user_id
        matched_user = match.user_id

        recommendation = (
            Recommendation.objects.order_by("?").first()
            if is_coffee_request
            else choice(icebreakers)
        )

        action = "grabbing coffee with" if is_coffee_request else "going to e-meet"
        self.client.post_to_channel(
            f"<@{requested_user}> is {action} <@{matched_user}>"
        )

        self.client.post_to_response_url(
            response_url,
            replace=True,
            color=True,
            text=COFFEE_REQUEST if is_coffee_request else CONNECT_REQUEST,
            blocks=[
                {
                    "type": "context",
                    "elements": [{"type": "mrkdwn", "text": LETTING_YOUR_BUDDY_KNOW}],
                }
            ],
        )

        buddy = "buddy" if is_coffee_request else "virtual buddy"
        recommendation_text = (
            f"We recommend {recommendation.name} and trying {recommendation.specialty}."
            if is_coffee_request
            else f"We recommend a slack video call (click on name > call > enable video) to grab a virtual coffee or jump on a phone call while going for a walk! While you're at it, try out this icebreaker - *{recommendation}*\n\nPlease make sure to follow social distancing guidelines."
        )
        recommendation_link = (
            recommendation.link
            if is_coffee_request
            else "https://www.cdc.gov/coronavirus/2019-ncov/prevent-getting-sick/social-distancing.html"
        )
        self.client.post_to_private(
            matched_user,
            text=f"<@{requested_user}> is your {buddy}!\n{recommendation_text}\n{recommendation_link}",
        )

        self.client.update(
            channel=match.coffee_request.initial_message.channel,
            ts=match.coffee_request.initial_message.ts,
            text=SEARCHING_FOR_COFFEE_BUDDY
            if is_coffee_request
            else SEARCHING_FOR_CONNECT_BUDDY,
            color=True,
            blocks=[
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": COFFEE_SUCCESS_MESSAGE
                            if is_coffee_request
                            else CONNECT_SUCCESS_MESSAGE,
                        }
                    ],
                }
            ],
        )
        self.client.post_to_private(
            requested_user,
            text=f"<@{matched_user}> is your {buddy}!\n{recommendation_text}\n{recommendation_link}",
        )
