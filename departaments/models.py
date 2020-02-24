from django.db import models
from organizations.models import Organizations

class Departaments(models.Model):
    organizations = models.ForeignKey(Organizations, on_delete=models.CASCADE, blank=True)
    name       = models.TextField()
 
