from .match import create_coffee_request
from celery import shared_task


@shared_task
def process_new_request(*, user_id, response_url):
    return create_coffee_request(user_id=user_id, response_url=response_url)
