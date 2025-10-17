from celery import shared_task
import pandas as pd
from .models import Customer, Loan
from datetime import datetime

@shared_task
def import_customers_from_excel(file_path):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        approved_limit = round(row['monthly_salary'] * 36 / 100000) * 100000  # nearest lakh
        Customer.objects.update_or_create(
            id=row['customer_id'],
            defaults={
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'phone': str(row['phone_number']),
                'monthly_income': row['monthly_salary'],
                'approved_limit': approved_limit,
            }
        )

@shared_task
def import_loans_from_excel(file_path):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        customer = Customer.objects.get(id=row['customer id'])
        Loan.objects.update_or_create(
            id=row['loan id'],
            defaults={
                'customer': customer,
                'amount': row['loan amount'],
                'term_months': row['tenure'],
                'interest_rate': row['interest rate'],
                'monthly_installment': row['monthly repayment (emi)'],
                'created_at': pd.to_datetime(row['start date']),
                'updated_at': pd.to_datetime(row['end date']),
            }
        )
