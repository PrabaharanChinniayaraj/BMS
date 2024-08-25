from django.contrib import admin

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from.models import*

# Register your models here.
admin.site.register(Product)

admin.site.register(Customer)
admin.site.register(Supplier)

admin.site.register(Transaction_Sale)
admin.site.register(Transaction_Buy)
admin.site.register(CustomUser)
