from django.contrib import admin

from .models import Payment, EmployeePayment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'total_payment', 'payment_date', 'date_created', 'date_modified',
                    'employer')


@admin.register(EmployeePayment)
class EmployeePaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment', 'work_hours', 'hourly_wage', 'final_payment', 'date_created',
                    'date_modified')
