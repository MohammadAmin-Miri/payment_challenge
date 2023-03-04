from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    PaymentDetailSerializer,
    PaymentCreateSerializer,
    PaymentListSerializer,
    FinalizePaymentSerializer
)
from .models import Payment


class GetPaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(employer=self.request.user)


class CreatePaymentAPIView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]


class GetPaymentDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Payment.objects.get(id=self.kwargs.get('pk'), employer=self.request.user)
        except Payment.DoesNotExist:
            raise ValidationError(detail='Payment id is invalid')


class FinalizePaymentAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = FinalizePaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Payment.objects.get(id=self.kwargs.get('pk'), employer=self.request.user, status='PENDING')
        except Payment.DoesNotExist:
            raise ValidationError(detail='Payment id is invalid')
