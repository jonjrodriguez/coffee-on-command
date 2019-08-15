from .base import Action
from ..models import Member


class DeactivateMemberAction(Action):
    def execute(self, *, user_id: str):
        Member.objects.filter(user_id=user_id).update(status=Member.STATUS_INACTIVE)
