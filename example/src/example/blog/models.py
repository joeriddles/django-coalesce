from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=255)
