import uuid
from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone

class Delivery(models.Model):
    route = models.ForeignKey('Route', 
        on_delete=models.CASCADE, null=True, blank=False)
    stop_num = models.SmallIntegerField()
    main_contact = models.CharField(
        max_length=200, default='CLIENT', blank=False, null=False)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=12)
    box = models.CharField(max_length=50, null=True, blank=True) #This could get its own entry eventually
    delivery_notes = models.TextField(null=True, blank=True)
    member_id = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    text_opt_int = models.BooleanField(default=False)

    status_choices = [
        (1, 'Not delivered'),
        (2, 'Delivered'),
        (3, 'Failed')
    ]
    status = models.SmallIntegerField(
        choices=status_choices, default=1, blank=False, null=False)
    status_change_time = models.DateTimeField(default=None, blank=True, null=True)
    driver_notes = models.TextField()

    class Meta:
        verbose_name_plural = 'Deliveries'
        ordering = ['stop_num']

    def get_absolute_url(self):
    	token = self.route.token_set.first()
    	return reverse('stop_view', 
    		kwargs={'token_value':str(token.value), 'stop_num': str(self.stop_num)})

    def __str__(self):
        return f'{self.stop_num} - {self.main_contact}'

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self.status == 3 and self.driver_notes is None:
            raise ValidationError(_('Please leave a short note on the failed delivery.'))

    def save(self, *args, **kwargs):
        #whole method untested
        if self.status != 1:
            self.status_change_time = timezone.now()
        else:    
            self.status_change_time = None

        super(Delivery, self).save(*args, **kwargs)

class Route(models.Model):
	date = models.DateField(default=date.today)
	driver = models.CharField(max_length=255, default='Unassigned')

	def __str__(self):
		return f"{self.date} {self.driver}"

	def get_absolute_url(self):
		token = self.token_set.first()
		return reverse('route_view', args = [token.value])

def generate_token():
    return str(uuid.uuid4())

class Token(models.Model):
    value = models.CharField(max_length=255, default=generate_token)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
