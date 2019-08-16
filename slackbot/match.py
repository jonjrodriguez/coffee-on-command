from datetime import timedelta
import random

from django.db.models import F, Count, OuterRef, Subquery, Exists
from django.db.models.fields import IntegerField
from django.db.models.functions import Coalesce
from django.utils import timezone
import pytz

from slackbot.strings import COULD_NOT_FIND_MATCH
from .client import Client
from .models import CoffeeRequest, Match, SlackMessage, Member

REQUEST_EXPIRATION_MINUTES = 10
HANG_IN_THERE_MINUTES = 5
MATCH_RESPONSE_EXPIRATION_MINUTES = 2


def get_matcher(*, client):
    return Matcher(client=client)


class Matcher:
    def __init__(self, client: Client):
        self.client = client

    def create_request(self, user_id, response_url):
        coffee_request = CoffeeRequest.objects.create(
            user_id=user_id, response_url=response_url
        )

        self.schedule_request_expiration(coffee_request.id)
        self.schedule_remind_coffee_requester(coffee_request.id)

        return coffee_request

    def create_match(self, coffee_request):
        if coffee_request.status != CoffeeRequest.STATUS_PENDING:
            return None

        member = self.find_match(coffee_request)
        if not member:
            coffee_request.status = CoffeeRequest.STATUS_CANCELLED
            coffee_request.save()
            self.send_no_matches_message_to_requesting_user(coffee_request.user_id)
            return None

        expiration = timezone.now() + timedelta(
            minutes=MATCH_RESPONSE_EXPIRATION_MINUTES
        )

        match = Match.objects.create(
            user_id=member, coffee_request=coffee_request, expiration=expiration
        )

        self.send_invite_message_to_potential_match_user(match)
        self.schedule_match_expiration(match.id, expiration)

        return match

    def find_match(self, coffee_request):
        date = timezone.localdate()
        # time start/end are stored in EST
        time = timezone.localtime(timezone=pytz.timezone("US/Eastern")).time()

        coffees_drank = (
            Match.objects.filter(
                is_accepted=True, expiration__date=date, user_id=OuterRef("user_id")
            )
            .values("user_id")
            .annotate(count=Count("*"))
            .values("count")
        )

        pending_match = Match.objects.filter(
            is_accepted=None, user_id=OuterRef("user_id")
        )

        previously_matched = Match.objects.filter(
            coffee_request=coffee_request, user_id=OuterRef("user_id")
        )

        pending_request = CoffeeRequest.objects.filter(user_id=OuterRef("user_id"), status=CoffeeRequest.STATUS_PENDING)

        member = (
            Member.objects.annotate(
                coffees_drank=Coalesce(
                    Subquery(coffees_drank, output_field=IntegerField()), 0
                ),
                pending_match=Exists(pending_match),
                pending_request=Exists(pending_request),
                previously_matched=Exists(previously_matched),
            ).filter(
                is_bot=False,
                pending_match=False,
                pending_request=False,
                previously_matched=False,
                coffees_drank__lt=F("coffee_count"),
                start_time__lte=time,
                end_time__gte=time,
                status=Member.STATUS_ACTIVE,
            )
            .exclude(user_id=coffee_request.user_id)
            .order_by("?")
            .first()
        )

        if not member:
            return None
        return member.user_id

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

    def schedule_match_expiration(self, match_id, expiration):
        from .tasks import expire_a_match_if_needed

        # schedule a task with ETA of expiration time that cancels a pending match if it hasn't been accepted
        expire_a_match_if_needed.apply_async(args=[match_id], eta=expiration)

    def schedule_request_expiration(self, coffee_request_id):
        from .tasks import expire_a_request_if_needed

        expiration = timezone.now() + timedelta(minutes=REQUEST_EXPIRATION_MINUTES)
        # schedule a task with ETA of expiration time that cancels a pending match if it hasn't been accepted
        expire_a_request_if_needed.apply_async(args=[coffee_request_id], eta=expiration)

    def schedule_remind_coffee_requester(self, coffee_request_id):
        from .tasks import remind_coffee_requester

        expiration = timezone.now() + timedelta(minutes=HANG_IN_THERE_MINUTES)
        # schedule a task with ETA of expiration time that sends the requester to hold tight
        remind_coffee_requester.apply_async(args=[coffee_request_id], eta=expiration)

    def send_no_matches_message_to_requesting_user(self, user_id):
        return self.client.post_to_private(
            receiver_id=user_id,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": COULD_NOT_FIND_MATCH,
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
        message = SlackMessage.objects.create(ts=ts, channel=channel)
        match.initial_message = message
        match.save()
