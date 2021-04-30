from django.contrib import admin
from .models import Delivery, Route, Token

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
	model = Delivery

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
	model = Route

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
	model = Token