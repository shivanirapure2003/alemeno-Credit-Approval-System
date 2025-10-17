from rest_framework import serializers
from .models import Customer, Loan

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'  # include all fields of Customer

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'  # include all fields of Loan
