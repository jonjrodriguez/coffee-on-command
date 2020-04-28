from datetime import datetime
from hashlib import sha256
import hmac
import json

from django.views.generic import TemplateView, RedirectView
from rest_framework.views import APIView
from rest_framework.response import Response

from app.settings import SLACK, LANDING_PAGE_REDIRECT

from .serializers import Payload
from .tasks import (
    process_accept,
    process_cancel,
    process_create,
    process_deny,
    process_event_webhook,
    process_request_preferences,
    process_store_preferences,
)


class IndexView(RedirectView):
    def get_redirect_url(self, *args, **kwargs) -> None:
        return LANDING_PAGE_REDIRECT


class SlackView(APIView):
    def check_permissions(self, request):
        super().check_permissions(request)

        timestamp = int(request.headers.get("X-Slack-Request-Timestamp", 0))
        if abs(datetime.now().timestamp() - timestamp) > 60 * 5:
            self.permission_denied(request, message="Old request")

        sig_basestring = f"v0:{timestamp}:{request.body.decode()}"
        digest = hmac.digest(
            SLACK.get("SIGNING_SECRET").encode(), sig_basestring.encode(), sha256
        )
        signature = f"v0={digest.hex()}"

        x_slack_signature = request.headers.get("X-Slack-Signature")
        if not hmac.compare_digest(signature, x_slack_signature):
            self.permission_denied(request, message="Unverified request")


class CommandView(SlackView):
    def post(self, request):
        user_id = request.POST.get("user_id")
        response_url = request.POST.get("response_url")
        command = request.POST.get("command")

        process_create.delay(
            user_id=user_id, response_url=response_url, command=command
        )

        return Response()


class ResponseView(SlackView):
    def post(self, request):
        data = json.loads(request.data.get("payload"))
        payload = Payload(data=data)
        payload.is_valid()

        user_id = payload.data.get("user").get("id")
        response_url = payload.data.get("response_url")
        actions = payload.data.get("actions")
        submission = payload.data.get("submission")

        if actions:
            action = actions[0]
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
            elif action.get("value") == "PREFERENCES":
                trigger_id = payload.data.get("trigger_id")
                process_request_preferences.delay(
                    user_id=user_id,
                    block_id=block_id,
                    response_url=response_url,
                    trigger_id=trigger_id,
                )
        if submission:
            callback_id = payload.data.get("callback_id")
            process_store_preferences.delay(
                user_id=user_id,
                callback_id=callback_id,
                data=submission,
                response_url=response_url,
            )

        return Response()


class EventsView(SlackView):
    def post(self, request):
        challenge = request.data.get("challenge")
        if challenge:
            return Response(data={"challenge": challenge})

        event = request.data.get("event")
        process_event_webhook.delay(event=event)

        return Response()
