import random

from django.utils import timezone

from .client import Client
from .models import CoffeeRequest, Match


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
            return None

        return Match.objects.create(
            user_id=member, coffee_request=coffee_request, expiration=timezone.now()
        )

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

    def deny_request(self, user_id, block_id, response_url):
        match = Match.objects.get(user_id=user_id, block_id=block_id)

        match.is_accepted = False
        match.response_url = response_url
        match.save()

        return match
