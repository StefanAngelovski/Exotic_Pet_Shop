from django.urls import path
from Store import views

app_name = 'Store'
urlpatterns = [
    path('', views.display_index, name='index'),
]