import random

from celery import app
from django.utils import timezone

from client import get_client
from slackbot.models import CoffeeRequest, Match


def find_a_match():
    members = get_client().get_channel_participants()
    member = random.choice(members)

    return member


def create_coffee_request(*, user_id, response_url):
    coffee_request = CoffeeRequest.objects.create(user_id=user_id, response_url=response_url)

    member = find_a_match()
    match = Match.objects.create(user_id=member, coffee_request=coffee_request, expiration=timezone.now())
    on_match_success(match)


def on_match_success(match):
    coffee_request = match.coffee_request

    requested_user = coffee_request.user_id
    matched_user = match.user_id

    get_client().post_to_channel(f"<@{requested_user}> is going to grab coffee with <@{matched_user}>")

