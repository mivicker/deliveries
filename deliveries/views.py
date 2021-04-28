from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Delivery

def home_view(request):
	deliveries = Delivery.objects.all()
	return render(request, 'deliveries/home.html', {'deliveries': deliveries})

def stop_view(request, stop_num):
	delivery = get_object_or_404(Delivery, stop_num=stop_num)
	if request.method == 'POST':
		delivery.status = request.POST['status']
		delivery.save()
		return redirect(delivery.get_absolute_url())
	return render(request, 'deliveries/stop.html', {'delivery': delivery})