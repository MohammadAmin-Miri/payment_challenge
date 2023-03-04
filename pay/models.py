from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

user_model = get_user_model()


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        DONE = 'Done', _('Done')

    title = models.CharField(max_length=255)
    status = models.CharField(choices=PaymentStatus.choices, default=PaymentStatus.PENDING, max_length=31)
    total_payment = models.PositiveIntegerField(default=0)
    payment_date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    employer = models.ForeignKey(to=user_model, on_delete=models.CASCADE)


class EmployeePayment(models.Model):
    user = models.ForeignKey(to=user_model, on_delete=models.CASCADE)
    payment = models.ForeignKey(to=Payment, on_delete=models.CASCADE, related_name='employees')
    work_hours = models.PositiveIntegerField(default=0)
    hourly_wage = models.PositiveIntegerField(default=0)
    final_payment = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
