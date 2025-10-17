from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoanEligibilitySerializer, LoanEligibilityResponseSerializer
from .models import Customer
from .utils import calculate_credit_score, get_corrected_interest, calculate_emi
from .models import Loan
from .utils import calculate_credit_score, get_corrected_interest, calculate_emi


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    filterset_fields = ['status', 'customer']  # Filter by status or customer

    def perform_create(self, serializer):
        loan = serializer.save()
        loan.approve_or_reject()  # Auto approve/reject on creation

    def perform_update(self, serializer):
        loan = serializer.save()
        loan.approve_or_reject()  # Auto approve/reject on update

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerRegisterSerializer

@api_view(['POST'])
def register_customer(request):
    serializer = CustomerRegisterSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def check_eligibility(request):
    serializer = LoanEligibilitySerializer(data=request.data)
    if serializer.is_valid():
        customer_id = serializer.validated_data['customer_id']
        amount = serializer.validated_data['loan_amount']
        interest_rate = serializer.validated_data['interest_rate']
        tenure = serializer.validated_data['tenure']

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        score = calculate_credit_score(customer)
        approval, corrected_interest = get_corrected_interest(score, interest_rate)
        monthly_installment = calculate_emi(amount, tenure, corrected_interest)

        response = {
            "customer_id": customer_id,
            "approval": approval,
            "interest_rate": interest_rate,
            "corrected_interest_rate": corrected_interest,
            "tenure": tenure,
            "monthly_installment": monthly_installment
        }

        return Response(response, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def create_loan(request):
    serializer = LoanCreateSerializer(data=request.data)
    if serializer.is_valid():
        customer_id = serializer.validated_data['customer_id']
        amount = serializer.validated_data['loan_amount']
        interest_rate = serializer.validated_data['interest_rate']
        tenure = serializer.validated_data['tenure']

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        score = calculate_credit_score(customer)
        approval, corrected_interest = get_corrected_interest(score, interest_rate)
        monthly_installment = calculate_emi(amount, tenure, corrected_interest)

        if approval:
            loan = Loan.objects.create(
                customer=customer,
                amount=amount,
                term_months=tenure,
                interest_rate=corrected_interest,
                monthly_installment=monthly_installment,
                status='APPROVED'
            )
            response = {
                "loan_id": loan.id,
                "customer_id": customer.id,
                "loan_approved": True,
                "message": "Loan approved",
                "monthly_installment": monthly_installment
            }
        else:
            response = {
                "loan_id": None,
                "customer_id": customer.id,
                "loan_approved": False,
                "message": "Loan not approved due to credit score or debt limit",
                "monthly_installment": monthly_installment
            }

        return Response(response, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = LoanDetailSerializer(loan)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['GET'])
def view_loans_by_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    loans = Loan.objects.filter(customer=customer)
    serializer = LoanDetailSerializer(loans, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
