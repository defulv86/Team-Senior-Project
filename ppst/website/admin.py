from django.contrib import admin
from website.models import Test, Result, Response, Stimulus, Aggreagate, Stimulus_Type, Ticket

class TestAdmin(admin.ModelAdmin):
    readonly_fields = ('link','created_at','started_at','finished_at')

class TestResponse(admin.ModelAdmin):
    readonly_fields = ('time_submitted',)

admin.site.register(Stimulus)
admin.site.register(Stimulus_Type)
admin.site.register(Test, TestAdmin)
admin.site.register(Result)
admin.site.register(Response, TestResponse)
admin.site.register(Aggreagate)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'description', 'created_at')
    list_filter = ('category', 'created_at')

admin.site.register(Ticket, TicketAdmin)

