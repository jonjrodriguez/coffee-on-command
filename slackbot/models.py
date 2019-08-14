from datetime import time

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now


class Member(models.Model):
    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"
    STATUS_CHOICES = (
        (STATUS_ACTIVE, _("Active")),
        (STATUS_INACTIVE, _("Inactive")),
    )

    user_id = models.CharField(max_length=255)
    is_bot = models.BooleanField(default=False)
    created = models.DateTimeField(default=now)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    coffee_per_day = models.IntegerField(default=1)
    start_time = models.TimeField(default=time(9))
    end_time = models.TimeField(default=time(17))


class CoffeeRequest(models.Model):
    STATUS_PENDING = "pending"
    STATUS_MATCHED = "matched"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = (
        (STATUS_PENDING, _("Pending")),
        (STATUS_MATCHED, _("Matched")),
        (STATUS_CANCELLED, _("Cancelled")),
    )

    user_id = models.CharField(max_length=255)
    response_url = models.CharField(max_length=255)
    created = models.DateTimeField(default=now)
    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default=STATUS_PENDING
    )


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


class Recommendation(models.Model):
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)

