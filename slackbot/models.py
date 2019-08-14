from django.db import models
from django.utils.timezone import now


class CoffeeRequest(models.Model):
    user_id = models.CharField(max_length=255)
    response_url = models.CharField(max_length=255)
    created = models.DateTimeField(default=now)


class Match(models.Model):
    user_id = models.CharField(max_length=255)
    is_accepted = models.BooleanField(null=True)
    expiration = models.DateTimeField()
    coffee_request = models.ForeignKey(
        to="slackbot.CoffeeRequest",
        on_delete=models.CASCADE,
        related_name="matches",
        null=True,
    )
    response_url = models.CharField(max_length=255, blank=True)
    block_id = models.CharField(max_length=255, default="")
