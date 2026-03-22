from django.urls import path
from . import views

app_name = 'analyzer'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('reference/upload/', views.upload_reference, name='upload_reference'),
    path('reference/list/', views.reference_list, name='reference_list'),
    path('reference/delete/<int:pk>/', views.delete_reference, name='delete_reference'),
    path('analyze/', views.analyze_cv, name='analyze'),
    path('result/<int:pk>/', views.result, name='result'),
    path('history/', views.history, name='history'),
]