from django.contrib import admin
from .models import Council, Postcode, Election


class CouncilAdmin(admin.ModelAdmin):
    list_display  = ('name', 'forms_completed')
    search_fields = ('name',)


admin.site.register(Council, CouncilAdmin)
admin.site.register(Postcode)
admin.site.register(Election)


