from django.contrib import admin
from apps.trends.models import Channel,Commit,ImgInfo,Trends
# Register your models here.
admin.site.register(Trends)
admin.site.register(Commit)
admin.site.register(Channel)
admin.site.register(ImgInfo)