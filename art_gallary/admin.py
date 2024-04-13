from django.contrib import admin
from .models import Artwork,Cart,Address,Payment,Order
# Register your models here.

admin.site.register(Artwork)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Order)
