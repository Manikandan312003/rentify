import uuid
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=50, blank=True)
    image = models.ImageField(
        default="images/default.jpg", upload_to="images/", blank=True
    )
    number = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

    def getDetail(self):
        return f"""
name: {self.name}
number: {self.number}
email: {self.user.email}
location: {self.location}
"""
