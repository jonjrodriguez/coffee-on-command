from django.db import models


class CoffeeRequest(models.Model):
    user_id = models.CharField(max_length=255)
    response_url = models.CharField(max_length=255)
    # matches = models.ForeignKey(
    #     to="slackbot.Match", on_delete=models.CASCADE, related_name="coffee_request"
    # )


class Match(models.Model):
    user_id = models.CharField(max_length=255)
    is_accepted = models.BooleanField(null=True)
    expiration = models.DateTimeField()
    coffee_request = models.ForeignKey(to="slackbot.CoffeeRequest", on_delete=models.CASCADE, related_name="matches", null=True)
