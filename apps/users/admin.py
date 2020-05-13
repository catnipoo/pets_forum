from django.contrib import admin
from apps.users.models import UserRelation,User
# Register your models here.
admin.site.register(UserRelation)
admin.site.register(User)