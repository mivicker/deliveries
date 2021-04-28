from django.contrib import admin
from .models import Delivery

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
	model = Delivery
	class Meta:
		verbose_name_plural = 'Deliveries'