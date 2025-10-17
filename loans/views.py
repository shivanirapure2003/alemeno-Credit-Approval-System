from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        loan = serializer.save()
        loan.approve_or_reject()  # Auto approve/reject on creation

    def perform_update(self, serializer):
        loan = serializer.save()
        loan.approve_or_reject()  # Auto approve/reject on update

