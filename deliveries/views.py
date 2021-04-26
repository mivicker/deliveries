from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Delivery

def stop_view(request):
	delivery = Delivery.objects.first()
	if request.method == 'POST':
		delivery.status = request.POST['status']
		delivery.save()
		return redirect('stop_view')
	return render(request, 'deliveries/stop.html', {'delivery': delivery})