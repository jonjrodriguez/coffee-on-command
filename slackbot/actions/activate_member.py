from .base import Action
from ..models import Member


class ActivateMemberAction(Action):
    def execute(self, *, user_id: str):
        member, created = Member.objects.get_or_create(user_id=user_id)

        if not created:
            member.status = Member.STATUS_ACTIVE
            member.save()
