from django.contrib import admin
from .models import User, Test, Result, Response, Stimulus

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('last_login',)
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:  # If obj is None, it means we're creating a new object
            fields.remove('last_login')  # Hide the field during creation
        return fields

class TestAdmin(admin.ModelAdmin):
    readonly_fields = ('link','created_at','completed_at')
    
admin.site.register(User, UserAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Result)
admin.site.register(Stimulus)
admin.site.register(Response)
