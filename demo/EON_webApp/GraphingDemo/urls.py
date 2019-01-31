from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.Index, name='GraphingDemo'),
    path('UploadCode', views.UploadCode, name='UploadCode'),
    path('RunCode', views.RunCode, name='RunCode'),
    path('DisplayGraph_Test', views.DisplayGraph_Test, name='DisplayGraph_Test'),
    path('DisplayGraph', views.DisplayGraph, name='DisplayGraph')
]
