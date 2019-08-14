from celery import shared_task

from .client import get_client
from .match import accept_request, create_request, deny_request


@shared_task
def process_create(*, user_id, response_url):
    match = create_request(user_id=user_id, response_url=response_url)
    get_client().send_invite(receiver_id=match.user_id, block_id=match.block_id)


@shared_task
def process_accept(*, user_id, block_id, response_url):
    accept_request(user_id=user_id, block_id=block_id, response_url=response_url)


@shared_task
def process_deny(*, user_id, block_id, response_url):
    deny_request(user_id=user_id, block_id=block_id, response_url=response_url)
