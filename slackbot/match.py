from datetime import timedelta

from django.utils import timezone

from .client import Client
from .models import CoffeeRequest, Match, MatchSlackMessage


EXPIRATION_MINUTES = 2


def get_matcher(*, client):
    return Matcher(client=client)


class Matcher:
    def __init__(self, client: Client):
        self.client = client

    def create_request(self, user_id, response_url):
        return CoffeeRequest.objects.create(user_id=user_id, response_url=response_url)

    def create_match(self, coffee_request):
        member = self.find_match(coffee_request)
        if not member:
            self.send_no_matches_message_to_requesting_user(coffee_request.user_id)
            return None

        expiration = timezone.now() + timedelta(minutes=EXPIRATION_MINUTES)

        match = Match.objects.create(
            user_id=member, coffee_request=coffee_request, expiration=expiration
        )

        self.send_invite_message_to_potential_match_user(match)
        self.schedule_expiration(match.id, expiration)

        return match

    def find_match(self, coffee_request):
        members = self.client.get_channel_participants()
        if coffee_request.user_id in members:
            members.remove(coffee_request.user_id)

        while len(members):
            member = random.choice(members)
            is_bot = self.client.is_bot(user=member)
            previous_match = Match.objects.filter(
                coffee_request=coffee_request, user_id=member
            ).exists()

            if is_bot or previous_match:
                members.remove(member)
                continue

            return member

        return None

    def accept_request(self, user_id, block_id, response_url):
        match = Match.objects.get(user_id=user_id, block_id=block_id)

        match.is_accepted = True
        match.response_url = response_url
        match.save()

        coffee_request = match.coffee_request
        coffee_request.status = CoffeeRequest.STATUS_MATCHED
        coffee_request.save()

        return match

    def deny_request(self, user_id, block_id, response_url=""):
        match = Match.objects.get(user_id=user_id, block_id=block_id)

        match.is_accepted = False
        match.response_url = response_url
        match.save()

        return match

    def schedule_expiration(self, match_id, expiration):
        from .tasks import expire_a_match_if_needed

        # schedule a task with ETA of expiration time that cancels a pending match if it hasn't been accepted
        expire_a_match_if_needed.apply_async(args=[match_id], eta=expiration)

    def send_no_matches_message_to_requesting_user(self, user_id):
        self.client.post_to_private(
            receiver_id=user_id,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "I'm sorry, I couldn't find a buddy. :disappointed: Let's try again later.",
                    },
                }
            ],
        )

    def send_invite_message_to_potential_match_user(self, match):
        response = self.client.send_invite(
            receiver_id=match.user_id, block_id=match.block_id
        )

        # Save the postMessage ts so we can update the message later
        ts = response["ts"]
        channel = response["channel"]
        MatchSlackMessage.objects.create(ts=ts, channel=channel, match=match)
