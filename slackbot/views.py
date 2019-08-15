import json

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import Payload
from .tasks import (
    process_accept,
    process_cancel,
    process_create,
    process_deny,
    process_event_webhook,
)


class IndexView(APIView):
    def post(self, request):
        user_id = request.POST.get("user_id")
        response_url = request.POST.get("response_url")

        process_create.delay(user_id=user_id, response_url=response_url)

        return Response()


class ResponseView(APIView):
    def post(self, request):
        data = json.loads(request.data.get("payload"))
        payload = Payload(data=data)
        payload.is_valid()

        user_id = payload.data.get("user").get("id")
        response_url = payload.data.get("response_url")
        action = payload.data.get("actions")[0]
        block_id = action.get("block_id")

        if action.get("value") == "APPROVE":
            process_accept.delay(
                user_id=user_id, block_id=block_id, response_url=response_url
            )
        elif action.get("value") == "DENY":
            process_deny.delay(
                user_id=user_id, block_id=block_id, response_url=response_url
            )
        elif action.get("value") == "CANCEL":
            process_cancel.delay(
                user_id=user_id, block_id=block_id, response_url=response_url
            )

        return Response()


class EventsView(APIView):
    def post(self, request):
        event = request.data.get("event")
        process_event_webhook.delay(event=event)

        challenge = request.data.get("challenge")
        if challenge:
            return Response(data={"challenge": challenge})
        return Response()
