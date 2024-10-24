from django.contrib import admin
from .models import Test, Result, Response, Stimulus, Aggreagate, Stimulus_Type

class TestAdmin(admin.ModelAdmin):
    readonly_fields = ('link','created_at','started_at','finished_at')

class TestResponse(admin.ModelAdmin):
    readonly_fields = ('time_submitted',)

admin.site.register(Test, TestAdmin)
admin.site.register(Result)
admin.site.register(Stimulus)
admin.site.register(Response, TestResponse)
admin.site.register(Aggreagate)
admin.site.register(Stimulus_Type)
