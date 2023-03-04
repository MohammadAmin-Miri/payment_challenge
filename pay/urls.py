from django.urls import path

from pay import views

urlpatterns = [
    path('', views.GetPaymentListAPIView.as_view(), name='payment'),
    path('add/', views.CreatePaymentAPIView.as_view(), name='create-payment'),
    path('<int:pk>/', views.GetPaymentDetailAPIView.as_view(), name='payment-detail'),
    path('<int:pk>/finalize/', views.FinalizePaymentAPIView.as_view(), name='finalize-payment'),
]
