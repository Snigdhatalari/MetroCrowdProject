from django.db import models

class CrowdRecord(models.Model):
    station = models.CharField(max_length=100)   # ❗ NO unique=True

    people_count = models.IntegerField()

    crowd_status = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.station} - {self.people_count}"