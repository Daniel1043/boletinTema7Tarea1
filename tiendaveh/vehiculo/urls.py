from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.urls import path, include

urlpatterns = [
    path('marca/', views.marcaViewSet.as_view()),
    path('marca/<int:pk>/', views.marcaDetail.as_view()),
    path('vehiculo/', views.vehiculoViewSet.as_view()),
    path('vehiculo/<int:pk>/', views.vehiculoDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]