from typing import Any
from django.db import models

from user.models import Profile
import uuid


class NearbyPlaces(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    location = models.CharField(max_length=50, default="")

    def __str__(self) -> str:
        return f"{self.type} {self.name} at {self.location}"

    def __repr__(self) -> str:
        return f"{self.type} {self.name} at {self.location}"

    class Meta:
        verbose_name_plural = "NearbyPlaces"


from django.core import validators


class Property(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    place = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    image = models.ImageField(upload_to="properties/")
    no_of_bedrooms = models.IntegerField(default=0, blank=True, validators= [validators.MinValueValidator(0, 'No of Bedrooms Must be positive')])
    no_of_bathrooms = models.IntegerField(default=0, blank=True, validators= [validators.MinValueValidator(0, 'No of Bathrooms Must be positive')])
    no_of_floor = models.IntegerField(default=1, blank=True, validators= [validators.MinValueValidator(0, 'No of Floor Must be positive')])
    no_of_likes = models.IntegerField(default=0, blank=True, validators=[validators.MinValueValidator(0, 'No of likes Must be positive')])
    url = models.URLField(null= True, blank=True)
    nearby = models.ManyToManyField(NearbyPlaces)

    def __str__(self) -> str:
        return f"{self.profile}'s {self.place}"

    class Meta:
        verbose_name_plural = "Properties"


class Like(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["property", "profile"]

    def __str__(self) -> str:
        return f"{self.property} {self.profile}"


class Interested(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["property", "profile"]
        verbose_name_plural = "Interested"

    def __str__(self) -> str:
        return f"{self.property} {self.profile}"


from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


@receiver(post_delete, sender=Like)
def deleteLikeCount(sender, instance: Like, using, **kwargs):
    instance.property.no_of_likes -= 1
    instance.property.save()


@receiver(post_save, sender=Like)
def addLikeCount(sender, instance: Like, using, **kwargs):
    if kwargs.get("created"):
        instance.property.no_of_likes += 1
        instance.property.save()
