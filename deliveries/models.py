from django.db import models

class Delivery(models.Model):
    stop_num = models.SmallIntegerField()
    main_contact = models.CharField(
        max_length=200, default='CLIENT', blank=False, null=False)
    status_choices = [
        (1, 'Not delivered'),
        (2, 'Delivered'),
        (3, 'Failed')
    ]
    status = models.SmallIntegerField(
        choices=status_choices, default=1, blank=False, null=False)
