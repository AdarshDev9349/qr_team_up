from django.contrib import admin
from .models import User
from .models import AdminInput


admin.site.register(User)
admin.site.register(AdminInput)