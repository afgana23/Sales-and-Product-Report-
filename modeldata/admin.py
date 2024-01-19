from django.contrib import admin
from .models import Asset,Sale

# Register your models here.
#@admin.register(Sale)
@admin.register(Asset)
class Bill(admin.ModelAdmin):
  list_display=("id","title","category","date","amount","size","description")

