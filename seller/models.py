from django.db import models

from user.models import Profile


class NearbyPlaces(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    location = models.CharField(max_length=50, default="")

    def __str__(self) -> str:
        return f"{self.type} {self.name} at {self.location}"

    def __repr__(self) -> str:
        return f"{self.type} {self.name} at {self.location}"


class Property(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    place = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    image = models.ImageField(upload_to="properties/")
    no_of_bedrooms = models.IntegerField(default=0, blank=True)
    no_of_bathrooms = models.IntegerField(default=0, blank=True)
    no_of_floor = models.IntegerField(default=1, blank=True)
    nearby = models.ManyToManyField(NearbyPlaces)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.profile}'s {self.place}"


class Like(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["property", "profile"]

    def __str__(self) -> str:
        return f"{self.property} {self.profile}"


class Interested(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["property", "profile"]

    def __str__(self) -> str:
        return f"{self.property} {self.profile}"
