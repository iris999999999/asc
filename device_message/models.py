from django.db import models
from persons_card.models import Persons_Card

class Device_Message(models.Model):
    
    persons_card    = models.ForeignKey(Persons_Card, on_delete=models.CASCADE, blank=False)

    date_f           = models.TextField()
    time_f           = models.TextField()
    readerID         = models.TextField()
