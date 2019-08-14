from rest_framework.views import APIView
from rest_framework.response import Response


class IndexView(APIView):
    def get(self, request):
        return Response("Hello from Slackbot!")

    def post(self, request):
        return Response("Hello, Coffee Buddy!")
