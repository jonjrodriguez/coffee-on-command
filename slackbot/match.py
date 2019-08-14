import random
from uuid import uuid4

from django.utils import timezone

from .client import get_client
from .models import CoffeeRequest, Match


def find_a_match(*, user_id):
    members = get_client().get_channel_participants()
    members.remove(user_id)

    member = random.choice(members)
    while get_client().is_bot(user=member):
        members.remove(member)
        member = random.choice(members)

    return member


def create_coffee_request(*, user_id, response_url):
    coffee_request = CoffeeRequest.objects.create(
        user_id=user_id, response_url=response_url
    )

    member = find_a_match(user_id=user_id)
    return Match.objects.create(
        user_id=member,
        coffee_request=coffee_request,
        expiration=timezone.now(),
        block_id=uuid4(),
    )

def on_match_success(match):
    coffee_request = match.coffee_request

    requested_user = coffee_request.user_id
    matched_user = match.user_id

    get_client().post_to_channel(
        f"<@{requested_user}> is going to grab coffee with <@{matched_user}>"
    )


def accept_match(user, block_id, response_url):
    match = Match.objects.get(user_id=user, block_id=block_id)

    match.is_accepted = True
    match.response_url = response_url
    match.save()

    coffee_request = match.coffee_request
    coffee_request.status = CoffeeRequest.STATUS_MATCHED
    coffee_request.save()

    on_match_success(match)


def deny_match(user, block_id, response_url):
    match = Match.objects.get(user_id=user, block_id=block_id)

    match.is_accepted = False
    match.response_url = response_url
    match.save()

    on_match_failure(match)


def on_match_failure(match):
    coffee_request = match.coffee_request

    requested_user = coffee_request.user_id
    member = find_a_match(user_id=requested_user)

    match = Match.objects.create(
        user_id=member, coffee_request=coffee_request, expiration=timezone.now(), block_id=uuid4()
    )

    get_client().send_invite(match.user_id, match.block_id)