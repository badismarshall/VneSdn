from django.urls import path
from api import views

urlpatterns = [
    path('topo/', views.getTopologie),
    path('devices/', views.getDevices),
    path('statistics/', views.getStatistics),
    path('substrateNodes/', views.getSubstrateNodes),
    path('substrateLinks/', views.getSubstrateLinks),
    path('virtualNetworks/', views.getVirtualNetworks),
    path('logicalNodes/', views.getLogicalNodes),
    path('logicalLinks/', views.getLogicalLinks),
    path('mappings/', views.getMappings),
    path('Createvn/', views.postVn),
    path('Deletevn/<int:id>', views.deleteVn),
]