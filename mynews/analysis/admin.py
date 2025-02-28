from django.contrib import admin

from django.contrib import admin
from .models import SiteVisit, PostView, CategoryRead, UserActivity

admin.site.register(SiteVisit)
admin.site.register(PostView)
admin.site.register(CategoryRead)
admin.site.register(UserActivity)
