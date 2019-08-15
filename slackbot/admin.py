from django.contrib import admin

from .models import CoffeeRequest, Match, SlackMessage, Member, Recommendation


admin.site.register(CoffeeRequest)
admin.site.register(Match)
admin.site.register(SlackMessage)
admin.site.register(Member)
admin.site.register(Recommendation)
