from django.urls import path
from podcast.views import dashboard, r_podcast, r_chart

app_name = 'podcast'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('r-podcast', r_podcast, name='r_podcast'),
    path('r-chart', r_chart, name='r_chart'),
]