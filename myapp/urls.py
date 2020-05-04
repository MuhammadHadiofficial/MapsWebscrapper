from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path("data/", views.getData, name='getData'),
    path("file/", views.getFile, name='getFile'),
    path('pay',views.getPay),
    path('charge',views.charge),
    path('success/<str:args>/', views.successMsg, name="success"),
    path('non/<str:args>/', views.notfound_404),
]

