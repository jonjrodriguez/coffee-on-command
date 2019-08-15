from .base import Action
from ..models import Member


class ActivateMemberAction(Action):
    def execute(self, *, user_id: str):
        member, created = Member.objects.get_or_create(user_id=user_id)

        if not created:
            member.status = Member.STATUS_ACTIVE
            member.save()

        self.client.post_to_private(
                receiver_id=user_id,
                color=True,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Hey there! :wave: Thanks for joining! Let's get some things nailed down:"
                        },
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Coffee Count*\nHow many coffee walks would you like a day",
                        },
                        "accessory": {
                            "type": "static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select a number...",
                            },
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "1",
                                    },
                                    "value": "value-1"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "2",
                                    },
                                    "value": "value-2"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "3",
                                    },
                                    "value": "value-3"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "4",
                                    },
                                    "value": "value-4"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "5",
                                    },
                                    "value": "value-5"
                                },
                            ]
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Coffee Window*\nAt what time of day would you like to be notified?",
                        },
                        "accessory": {
                            "type": "static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select a time of day...",
                            },
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Morning (9a-12p)",
                                    },
                                    "value": "morning"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Afternoon (12p-3p)",
                                    },
                                    "value": "afternoon"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Evening (3p-5p)",
                                    },
                                    "value": "evening"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "All day (9a-5p)"
                                    }
                                }
                            ]
                        }
                    }
                ],
            )