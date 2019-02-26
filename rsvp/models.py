from django.db import models

# Create your models here.

class Guest(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=64, blank=True)
    address = models.CharField(max_length=64, blank=True)
    attending_wedding = models.BooleanField(null=True)
    attending_welcome_dinner = models.BooleanField(null=True)
    notes = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    def get_info(self):
        return {
            "guest_id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "address": self.address,
            "attending_wedding": self.attending_wedding,
            "attending_welcome_dinner": self.attending_welcome_dinner
        }


class Party(models.Model):
    name = models.CharField(max_length=64, blank=True)
    guest = models.ManyToManyField(Guest)

    def __str__(self):
        return self.name