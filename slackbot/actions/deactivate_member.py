from .base import Action
from ..models import Member


class DeactivateMemberAction(Action):
    def execute(self, *, user_id: str):
        member = Member.objects.get(user_id=user_id)
        member.status = Member.STATUS_INACTIVE
        member.save()
