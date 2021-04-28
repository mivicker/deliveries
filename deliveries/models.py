from django.db import models
from django.urls import reverse

class Delivery(models.Model):
    stop_num = models.SmallIntegerField()
    route = models.ForeignKey('Route', on_delete=models.CASCADE, null=True, blank=False)
    main_contact = models.CharField(
        max_length=200, default='CLIENT', blank=False, null=False)
    status_choices = [
        (1, 'Not delivered'),
        (2, 'Delivered'),
        (3, 'Failed')
    ]
    status = models.SmallIntegerField(
        choices=status_choices, default=1, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Deliveries'

    def get_absolute_url(self):
    	return reverse('stop_view', args=(str(self.stop_num)))

class Route(models.Model):
	driver = models.CharField(max_length=100)