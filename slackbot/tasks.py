from .match import create_coffee_request
from celery import shared_task
from .client import get_client


@shared_task
def process_new_request(*, user_id, response_url):
    match = create_coffee_request(user_id=user_id, response_url=response_url)
    get_client().send_invite(receiver_id=match.user_id, block_id=match.block_id)
