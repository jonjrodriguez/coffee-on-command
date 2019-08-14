from django.db import models


class CoffeeRequest(models.Model):
    user_id = models.CharField(max_length=255)
    response_url = models.CharField(max_length=255)


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
