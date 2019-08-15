from django.contrib import admin

from .models import CoffeeRequest, Match, Recommendation, Member


admin.site.register(CoffeeRequest)
admin.site.register(Match)
admin.site.register(Recommendation)
admin.site.register(Member)
