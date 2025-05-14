from django.db import models

# Create your models here.
class ProfileMatch(models.Model):
    name = models.CharField(max_length=100)
    score = models.FloatField()
    matched_data = models.JSONField()

    def __str__(self):
        return self.name