from django.urls import path
from api import views

urlpatterns = [
    path('login/', views.login),
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
    path('Getvn/<int:id>', views.getVn),
    path('Getsubstratelinksbyid/<int:id>', views.getSubstrateLinksbyid),
    path('Getsubstratenodesbyid/<int:id>', views.getSubstrateNodesbyid),
    path('Getflownumberofdevices/', views.getFlowNumberofDevices),
    path('NumberoflogicalNodesMapped/', views.getNumberoflogicalNodesMapped),
    path('GetNumberoflogicalLinksMapped/', views.getNumberoflogicalLinksMapped),
    path('GetMeterNumberofDevices/', views.getMeterNumberofDevices),
    path('GetNetworkInfo/', views.getNetworkInformation),
    path('GetflowsNumberofvn/', views.getflowsnumberforVn),
]