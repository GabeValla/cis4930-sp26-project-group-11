from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import CrimeIncident, WeatherRecord, City
from .forms import CrimeIncidentForm

def home(request):
    total_incidents = CrimeIncident.objects.count()
    total_weather = WeatherRecord.objects.count()
    active_cities = City.objects.count()
    
    context = {
        'total_incidents': total_incidents,
        'total_weather': total_weather,
        'active_cities': active_cities
    }
    return render(request, 'myapp/home.html', context)

def records_list(request):
    incident_list = CrimeIncident.objects.all()
    paginator = Paginator(incident_list, 20) # Show 20 incidents per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'myapp/list.html', {'page_obj': page_obj})

def record_detail(request, pk):
    incident = get_object_or_404(CrimeIncident, pk=pk)
    return render(request, 'myapp/detail.html', {'incident': incident})

def record_create(request):
    if request.method == 'POST':
        form = CrimeIncidentForm(request.POST)
        if form.is_valid():
            incident = form.save()
            messages.success(request, "Incident successfully reported!")
            return redirect('record_detail', pk=incident.pk)
    else:
        form = CrimeIncidentForm()
        
    return render(request, 'myapp/form.html', {'form': form, 'title': 'Report New Incident'})

def record_edit(request, pk):
    incident = get_object_or_404(CrimeIncident, pk=pk)
    if request.method == 'POST':
        form = CrimeIncidentForm(request.POST, instance=incident)
        if form.is_valid():
            form.save()
            messages.success(request, "Incident successfully updated!")
            return redirect('record_detail', pk=incident.pk)
    else:
        form = CrimeIncidentForm(instance=incident)
        
    return render(request, 'myapp/form.html', {'form': form, 'title': 'Edit Incident'})

def record_delete(request, pk):
    incident = get_object_or_404(CrimeIncident, pk=pk)
    if request.method == 'POST':
        incident.delete()
        messages.success(request, "Incident successfully deleted.")
        return redirect('records_list')
        
    return render(request, 'myapp/confirm_delete.html', {'incident': incident})

from django.conf import settings
from django.http import JsonResponse
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt
import threading

@csrf_exempt
def trigger_fetch(request):
    # Verify the security token
    token = request.GET.get('token')
    if not token or token != settings.CRON_FETCH_TOKEN:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    try:
        # Spin up a thread so the HTTP request doesn't timeout waiting for the API to resolve
        thread = threading.Thread(target=call_command, args=('fetch_data',))
        thread.start()
        return JsonResponse({'status': 'Fetch initiated successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

import json
import pandas as pd

def weather(request):
    cities = City.objects.all()
    weather_by_city = {}

    for city in cities:
        records = WeatherRecord.objects.filter(city=city).order_by('date').values(
            'date', 'temp_max', 'temp_min', 'precipitation', 'wind_speed_max'
        )
        df = pd.DataFrame(list(records))
        if df.empty:
            continue
        df['date'] = df['date'].astype(str)
        weather_by_city[city.name] = {
            'dates': df['date'].tolist(),
            'temp_max': df['temp_max'].tolist(),
            'temp_min': df['temp_min'].tolist(),
            'precipitation': df['precipitation'].tolist(),
            'wind_speed_max': df['wind_speed_max'].tolist(),
            'avg_temp_max': round(df['temp_max'].mean(), 1),
            'avg_temp_min': round(df['temp_min'].mean(), 1),
            'total_precip': round(df['precipitation'].sum(), 1),
            'avg_wind': round(df['wind_speed_max'].mean(), 1),
        }

    context = {
        'weather_json': json.dumps(weather_by_city),
        'cities': list(weather_by_city.keys()),
    }
    return render(request, 'myapp/weather.html', context)

def analytics(request):
    qs_crimes = CrimeIncident.objects.values('reason', 'latitude', 'longitude', 'date_time')
    df_crimes = pd.DataFrame(list(qs_crimes))

    top_reasons_chart = {'labels': [], 'values': []}
    heatmap_data_by_month = {}
    incidents_over_time_chart = {'labels': [], 'values': []}

    if not df_crimes.empty:
        df_crimes['date_time'] = pd.to_datetime(df_crimes['date_time'], errors='coerce')
        df_crimes = df_crimes.dropna(subset=['date_time'])

        top_reasons = df_crimes['reason'].value_counts().head(10)
        top_reasons_chart = {
            'labels': top_reasons.index.tolist(),
            'values': top_reasons.values.tolist(),
        }

        df_crimes['month_year'] = df_crimes['date_time'].dt.strftime('%Y-%m')

        incidents_over_time = (
            df_crimes.groupby(df_crimes['date_time'].dt.to_period('M'))
            .size()
            .sort_index()
        )

        incidents_over_time_chart = {
            'labels': [str(x) for x in incidents_over_time.index],
            'values': incidents_over_time.tolist(),
        }

        df_coords = df_crimes.dropna(subset=['latitude', 'longitude'])
        df_coords = df_coords[(df_coords['latitude'] != 0) & (df_coords['longitude'] != 0)]

        heatmap_data_by_month['All'] = df_coords[['latitude', 'longitude']].values.tolist()
        for month, group in df_coords.groupby('month_year'):
            heatmap_data_by_month[month] = group[['latitude', 'longitude']].values.tolist()

    qs_weather = WeatherRecord.objects.values('temp_max', 'temp_min', 'precipitation', 'wind_speed_max')
    df_weather = pd.DataFrame(list(qs_weather))

    summary_stats = {}
    if not df_weather.empty:
        summary_stats = df_weather.describe().round(2).to_dict()

    context = {
        'top_reasons_json': json.dumps(top_reasons_chart),
        'incidents_over_time_json': json.dumps(incidents_over_time_chart),
        'heatmap_data_by_month_json': json.dumps(heatmap_data_by_month),
        'available_months': list(heatmap_data_by_month.keys()),
        'summary_stats': summary_stats,
    }
    return render(request, 'myapp/analytics.html', context)