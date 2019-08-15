from rest_framework.serializers import Serializer, CharField


class User(Serializer):
    id = CharField()
    username = CharField()
    name = CharField()
    team_id = CharField()


class Action(Serializer):
    action_id = CharField()
    block_id = CharField()
    value = CharField(default="")


class Payload(Serializer):
    user = User()
    response_url = CharField()
    actions = Action(many=True)
    trigger_id = CharField()

