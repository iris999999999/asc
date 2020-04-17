from django.db import models
from persons_card.models import Persons_Card
from datetime import datetime, date, time
from django.utils import timezone


class Device_Message(models.Model):
    persons_card    = models.ForeignKey(Persons_Card, on_delete=models.CASCADE, blank=False)

    date_f           = models.DateField()
    time_f           = models.TimeField()
    readerID         = models.TextField()