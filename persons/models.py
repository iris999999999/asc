from django.db import models
from departaments.models import Departaments
from jobs.models import Jobs

class Persons(models.Model):   
    departaments = models.ForeignKey(Departaments, on_delete=models.CASCADE, blank=False)
    jobs         = models.ForeignKey(Jobs, on_delete=models.CASCADE, blank=False)
    name         = models.TextField()
    sur_name     = models.TextField()
    patronymic   = models.TextField()
