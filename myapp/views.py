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

import json
import pandas as pd

def analytics(request):
    qs_crimes = CrimeIncident.objects.values('reason', 'latitude', 'longitude', 'date_time')
    df_crimes = pd.DataFrame(list(qs_crimes))
    
    top_reasons_chart = {'labels': [], 'values': []}
    heatmap_data_by_month = {}
    
    if not df_crimes.empty:
        top_reasons = df_crimes['reason'].value_counts().head(10)
        top_reasons_chart = {
            'labels': top_reasons.index.tolist(),
            'values': top_reasons.values.tolist(),
        }
        
        # Prepare Coordinate Data for Heatmap
        # First, ensure we have a month_year column
        df_crimes['month_year'] = df_crimes['date_time'].dt.strftime('%Y-%m')
        
        # Filter out rows with missing or 0 coordinates for safety
        df_coords = df_crimes.dropna(subset=['latitude', 'longitude'])
        df_coords = df_coords[(df_coords['latitude'] != 0) & (df_coords['longitude'] != 0)]
        
        heatmap_data_by_month['All'] = df_coords[['latitude', 'longitude']].values.tolist()
        for month, group in df_coords.groupby('month_year'):
            heatmap_data_by_month[month] = group[['latitude', 'longitude']].values.tolist()
        
    qs_weather = WeatherRecord.objects.values('temp_max', 'temp_min', 'precipitation', 'wind_speed_max')
    df_weather = pd.DataFrame(list(qs_weather))
    
    summary_stats = {}
    if not df_weather.empty:
        # describe returns metrics as index: count, mean, std, min, 25%, 50%, 75%, max
        summary_stats = df_weather.describe().round(2).to_dict()
        
    context = {
        'top_reasons_json': json.dumps(top_reasons_chart),
        'heatmap_data_by_month_json': json.dumps(heatmap_data_by_month),
        'available_months': list(heatmap_data_by_month.keys()),
        'summary_stats': summary_stats,
    }
    return render(request, 'myapp/analytics.html', context)
