from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(VirtualNetwork)
admin.site.register(LogicalNode)
admin.site.register(SubstrateNode)
admin.site.register(SubstrateLink)
admin.site.register(LogicalLink)
admin.site.register(Mapping)

