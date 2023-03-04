from django.db import IntegrityError
from django.db.models import Sum
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Payment, EmployeePayment


class PaymentEmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePayment
        fields = ['id', 'user', 'work_hours', 'hourly_wage', 'final_payment']
        read_only_fields = ['id', 'final_payment']


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ['employer']


class PaymentDetailSerializer(serializers.ModelSerializer):
    employees = PaymentEmployeeListSerializer(many=True)

    class Meta:
        model = Payment
        exclude = ['employer']


class PaymentCreateSerializer(serializers.ModelSerializer):
    employees = PaymentEmployeeListSerializer(many=True)

    class Meta:
        model = Payment
        fields = ['title', 'payment_date', 'employees', 'total_payment', 'status']
        read_only_fields = ['total_payment']

    def create(self, validated_data):
        employees = validated_data.pop('employees')
        payment = Payment.objects.create(**validated_data, employer=self.context.get('request').user)
        for employee in employees:
            employee_payment = EmployeePayment(payment=payment, **employee)
            employee_payment.final_payment = employee_payment.hourly_wage * employee_payment.work_hours
            employee_payment.save()
        payment.total_payment = payment.employees.aggregate(total_payment=Sum('final_payment')).get('total_payment')
        payment.status = Payment.PaymentStatus.PENDING
        payment.save()
        return payment


class FinalizePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['status']

    def update(self, instance, validated_data):
        employer = instance.employer
        if validated_data.pop('status') != Payment.PaymentStatus.DONE or instance.status == Payment.PaymentStatus.DONE:
            return instance
        try:
            employer.balance -= instance.total_payment
            employer.save()
        except IntegrityError:
            raise ValidationError(detail='Please charge your balance.')
        else:
            instance.status = Payment.PaymentStatus.DONE
            instance.save()
            # Need to implement payment action ????
            return instance
