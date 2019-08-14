from celery import shared_task

from .actions import AcceptCoffeeRequest, CreateCoffeeRequest, DenyCoffeeRequest


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
