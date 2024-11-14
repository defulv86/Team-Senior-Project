from django.contrib import admin

from .models import Test, Result, Response, Stimulus, Aggregate, Stimulus_Type, Notification, Ticket, Registration
from django.contrib.auth.models import User

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

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'header', 'message', 'time_created', 'is_archived', 'is_read')

    def mark_as_unread(modeladmin, request, queryset):
        queryset.update(is_read=False)
        modeladmin.message_user(request, "Selected notifications have been marked as unread.")

    def mark_as_unarchived(modeladmin, request, queryset):
        queryset.update(is_archived=False)
        modeladmin.message_user(request, "Selected notifications have been marked as unarchived.")

    actions = [mark_as_unread, mark_as_unarchived]

    
# Define actions for approving or denying registrations
def approve_registration(modeladmin, request, queryset):
    for registration in queryset:
        # Check if the user already exists
        if not User.objects.filter(username=registration.username).exists():
            # Create a new user based on the registration request
            User.objects.create_user(
                username=registration.username,
                password=registration.password  # Ensure password is securely hashed
            )
            registration.approved = True
            registration.save()
        else:
            modeladmin.message_user(request, f"User {registration.username} already exists.", level='warning')

approve_registration.short_description = "Approve selected registrations"

def deny_registration(modeladmin, request, queryset):
    # Mark registration requests as denied
    queryset.update(approved=False)
deny_registration.short_description = "Deny selected registrations"

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('username', 'approved')
    actions = [approve_registration]

admin.site.register(Stimulus)
admin.site.register(Test, TestAdmin)
admin.site.register(Result)
admin.site.register(Response, TestResponse)
admin.site.register(Aggregate)
admin.site.register(Stimulus_Type)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Ticket)
admin.site.register(Registration, RegistrationAdmin)