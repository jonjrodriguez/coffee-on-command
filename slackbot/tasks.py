from celery import shared_task

from app.settings import SLACK_CHANNEL

from .actions import AcceptCoffeeRequest, ActivateMemberAction, CreateCoffeeRequest, DenyCoffeeRequest


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

    if event_type == 'member_joined_channel' and channel == SLACK_CHANNEL:
        user_id = event.get('user')
        ActivateMemberAction().execute(user_id=user_id)
