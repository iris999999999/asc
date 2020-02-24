from django.db import models
from persons.models import Persons

class Persons_Card(models.Model):
    persons   = models.ForeignKey(Persons, on_delete=models.CASCADE, blank=False)
    card_code = models.IntegerField()
    active    = models.IntegerField()
    
