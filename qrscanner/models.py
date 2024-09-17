from django.db import models
import uuid

class AdminInput(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_students = models.IntegerField()
    num_teams = models.IntegerField()
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    queue_position = models.IntegerField()
    assigned_team = models.IntegerField(null=True, blank=True)
    admin_input = models.ForeignKey(AdminInput, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.phone}"
