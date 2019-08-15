from .base import Action
from ..models import Member
from ..client import get_client


class ActivateMemberAction(Action):
    def execute(self, *, user_id: str):
        member, created = Member.objects.get_or_create(user_id=user_id)

        if not created:
            member.status = Member.STATUS_ACTIVE
            member.save()

        get_client().post_to_private(
            receiver_id=user_id,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Hey there! :wave: Thanks for joining! Let's get some things nailed down:"
                    },
                },
                {
                    "type": "actions",
                    "block_id": 'fart',
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": ":coffee: Set Coffee Preferences"},
                            "style": "primary",
                            "value": "PREFERENCES",
                        }
                    ],
                }
            ]
        )