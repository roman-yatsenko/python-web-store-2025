import csv
import datetime as dt

from django.contrib import admin
from django.http import HttpResponse

from .models import Order, OrderItem


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [
        field for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    # запис першого рядку з інформацією заголовку
    writer.writerow([field.verbose_name for field in fields])
    # запис рядків даних
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, dt.datetime):
                value = value.strftime("%d.%m.%Y")
            data_row.append(value)
        writer.writerow(data_row) 
    return response
export_to_csv.short_description = "Експорт в CSV"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = [export_to_csv]
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'address',
        'city',
        'paid',
        'created',
        'updated',
    ]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
