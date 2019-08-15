from celery import shared_task
from celery.utils.log import get_task_logger

from app.settings import SLACK

from .actions import (
    AcceptCoffeeRequest,
    AutoDenyCoffeeRequest,
    ActivateMemberAction,
    CancelCoffeeRequest,
    CreateCoffeeRequest,
    DeactivateMemberAction,
    DenyCoffeeRequest,
    RemindCoffeeRequester,
    RequestPreferencesAction,
    StorePreferencesAction
)

logger = get_task_logger(__name__)


@shared_task
def process_create(*, user_id, response_url):
    CreateCoffeeRequest().execute(user_id=user_id, response_url=response_url)


@shared_task
def process_accept(*, user_id, block_id, response_url):
    AcceptCoffeeRequest().execute(
        user_id=user_id, block_id=block_id, response_url=response_url
    )


@shared_task
def process_deny(*, user_id, block_id, response_url):
    DenyCoffeeRequest().execute(
        user_id=user_id, block_id=block_id, response_url=response_url
    )


@shared_task
def process_event_webhook(*, event):
    event_type = event.get("type")
    channel = event.get("channel")

    if channel == SLACK.get("CHANNEL"):
        user_id = event.get("user")
        if event_type == "member_joined_channel":
            ActivateMemberAction().execute(user_id=user_id)
        elif event_type == "member_left_channel":
            DeactivateMemberAction().execute(user_id=user_id)


@shared_task
def process_cancel(*, user_id, block_id, response_url):
    CancelCoffeeRequest().execute(
        user_id=user_id, block_id=block_id, response_url=response_url
    )

@shared_task
def process_request_preferences(*, user_id, block_id, response_url, trigger_id):
    RequestPreferencesAction().execute(
        user_id=user_id, trigger_id=trigger_id
    )

@shared_task
def process_store_preferences(*, user_id, callback_id, data, response_url):
    StorePreferencesAction().execute(user_id=user_id, callback_id=callback_id, data=data, response_url=response_url)


@shared_task
def expire_a_match_if_needed(match_id):
    from .models import Match

    matches = Match.objects.filter(pk=match_id, is_accepted=None)

    if matches.exists():
        logger.info("Match has not been accepted but has expired.")
        match = matches.first()
        match_message = match.initial_message
        AutoDenyCoffeeRequest().execute(
            user_id=match.user_id, block_id=match.block_id, ts=match_message.ts, channel=match_message.channel
        )


@shared_task
def expire_a_request_if_needed(coffee_request_id):
    from .models import CoffeeRequest

    requests = CoffeeRequest.objects.filter(pk=coffee_request_id, status=CoffeeRequest.STATUS_PENDING)

    if requests.exists():
        coffee_request = requests.first()
        logger.info("Request has still not been fulfilled. We'll automatically cancel it.")
        CancelCoffeeRequest().execute(
            user_id=coffee_request.user_id,
            block_id=coffee_request.block_id,
            response_url=coffee_request.response_url,
            expired=True
        )


@shared_task
def remind_coffee_requester(coffee_request_id):
    from .models import CoffeeRequest

    requests = CoffeeRequest.objects.filter(pk=coffee_request_id, status=CoffeeRequest.STATUS_PENDING)

    if requests.exists():
        coffee_request = requests.first()
        logger.info("Request has still not been fulfilled. Sending requester a message to hold tight.")
        RemindCoffeeRequester().execute(
            user_id=coffee_request.user_id,
            block_id=coffee_request.block_id,
        )
