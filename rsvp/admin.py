from django.contrib import admin
from rsvp.models import Guest, Party

# Register your models here.
class GuestAdmin(admin.ModelAdmin):
    model = Guest
    list_display = ("first_name", "last_name", "attending_wedding", "attending_welcome_dinner", "get_party")

    def get_party(self, obj):
        party = Party.objects.filter(guest=obj).first()
        string = "\n"
        if party:
            return "{} - {}".format(party.id, party.name)
        return "N/A"

class PartyAdmin(admin.ModelAdmin):
    model = Party
    list_display = ("id", "name", "get_guests")
    filter_horizontal = ('guest',)

    def get_guests(self, obj):
        return "\n".join([f"{g.first_name} {g.last_name}, " for g in obj.guest.all()])[:-2]

admin.site.register(Guest, GuestAdmin)
admin.site.register(Party, PartyAdmin)