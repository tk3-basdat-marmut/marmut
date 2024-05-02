from django.urls import path
from chart.views import r_chart, chart_detail

app_name = 'chart'

urlpatterns = [
    path('r-chart', r_chart, name='r_chart'),
    path('chart-detail', chart_detail, name='chart_detail')
]