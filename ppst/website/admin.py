from django.contrib import admin
from .models import Test, Result, Response, Stimulus, Aggregate, Stimulus_Type, Notification, Ticket

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('last_login',)
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:  # If obj is None, it means we're creating a new object
            fields.remove('last_login')  # Hide the field during creation
        return fields

class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'administered_by', 'age', 'status', 'link', 'created_at', 'started_at', 'finished_at')
    list_filter = ('status', 'user', 'age')
    readonly_fields = ('link', 'created_at', 'started_at', 'finished_at')
    search_fields = ('user__username', 'status', 'age')
    ordering = ('-created_at',)

    def administered_by(self, obj):
        return obj.user
    administered_by.short_description = "Administered by"
    
class ResultAdmin(admin.ModelAdmin):
    list_display = ('test', 'fourdigit_accuracy_1', 'fourdigit_latency_1', 'fivedigit_accuracy_1', 'fivedigit_latency_1')
    readonly_fields = ('test',)

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
