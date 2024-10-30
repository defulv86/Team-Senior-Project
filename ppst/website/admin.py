from django.contrib import admin
from .models import User, Test, Result, Response, Stimulus, Aggregate, Stimulus_Type, Notification, Ticket

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('last_login',)
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:  # If obj is None, it means we're creating a new object
            fields.remove('last_login')  # Hide the field during creation
        return fields

class TestAdmin(admin.ModelAdmin):
    readonly_fields = ('link','created_at','started_at','finished_at')

class TestResponse(admin.ModelAdmin):
    readonly_fields = ('time_submitted',)


admin.site.register(Test, TestAdmin)
admin.site.register(Result)
admin.site.register(Stimulus)
admin.site.register(Response, TestResponse)
admin.site.register(Aggregate)
admin.site.register(Stimulus_Type)
admin.site.register(Notification)
admin.site.register(Ticket)
