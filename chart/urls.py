from django.urls import path
from chart.views import dashboard, r_chart, chart_detail, r_chart_view, r_specific_chart, d_song

app_name = 'chart'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('r-chart', r_chart, name='r_chart'),
    path('chart-detail', chart_detail, name='chart_detail'),
    path('r-chart-view/<str:id>', r_chart_view, name='r_chart_view'),
    path('r-specific-chart/<str:id_playlist>', r_specific_chart, name='r_specific_chart'),
    path('d-song/<str:id_song>', d_song, name='d_song')
]