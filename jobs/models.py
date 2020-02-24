from django.db import models
from departaments.models import Departaments

class Jobs(models.Model):
    departaments = models.ForeignKey(Departaments, on_delete=models.CASCADE, blank=False)
    name = models.TextField()
