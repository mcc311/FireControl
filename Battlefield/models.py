from django.db import models


# Create your models here.
class Battlefield(models.Model):
    situation = models.JSONField()
    policy = models.JSONField()

