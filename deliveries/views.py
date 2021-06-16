import io
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Delivery, Route, Token
from .forms import UploadFileForm

def validate_token(token):
	route = get_object_or_404(Route, token=token)
	return route.token_set.first() == token

def route_view(request, token_value):
	template = 'deliveries/route.html'

	token = get_object_or_404(Token, value=token_value)
	if not validate_token(token):
		return redirect('stale_token')
	route = token.route
	
	context = {'route': route}
	return render(request, template, context)

def stop_view(request, token_value, stop_num):
	template = 'deliveries/stop.html'

	token = get_object_or_404(Token, value=token_value)
	if not validate_token(token):
		return redirect('stale_token')
	route = get_object_or_404(Route, token=token)
	delivery = route.delivery_set.get(stop_num=stop_num)
	if request.method == 'POST':
		delivery.status = request.POST['status']
		if delivery.clean_fields():
			delivery.save()
		
		return redirect(delivery.get_absolute_url())
	
	context = {'delivery': delivery}
	return render(request, template, context)

def stale_token_view(request):
	template = 'deliveries/stale_token.html'
	context = {}

	return render(request, template, context)

@login_required
def upload_view(request):
	template = 'deliveries/upload.html'

	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			date = form.cleaned_data['date']

			#This is the file handler 'function'.
			csv_file = request.FILES['file']
			data = csv_file.read().decode('UTF-8')
			io_string = io.StringIO(data)

			route_nums = []
			for stop in csv.DictReader(io_string):
				if stop['route_num'] not in route_nums:
					route_nums.append(stop['route_num'])
					route = Route.objects.create(date=date)

				Delivery.objects.update_or_create(
						route = route,
						stop_num = stop['stop_num'],
						main_contact = stop['main_contact'],
						status = 1
					)

			return redirect('upload_success')
	else:
		form = UploadFileForm()
	
	context = {'form':form}

	return render(request, template, context)


def upload_success_view(request):
	template = 'deliveries/upload_success.html'
	context = {}
	
	return render(request, template, context)