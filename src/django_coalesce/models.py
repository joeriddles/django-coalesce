from django.db import models

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField()
    
    class Meta:
        app_label = "django_coalesce.settings"
