from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Delivery, Route, Token

def route_view(request, token_value):
	token = get_object_or_404(Token, value=token_value)
	route = token.route
	return render(request, 'deliveries/route.html', {'route': route})

def stop_view(request, token_value, stop_num):
	token = get_object_or_404(Token, value=token_value)
	route = get_object_or_404(Route, token=token)
	delivery = route.delivery_set.get(stop_num=stop_num)
	if request.method == 'POST':
		delivery.status = request.POST['status']
		delivery.save()
		return redirect(delivery.get_absolute_url())
	return render(request, 'deliveries/stop.html', {'delivery': delivery})