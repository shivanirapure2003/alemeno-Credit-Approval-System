from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from loans.models import Customer, Loan
from django.utils.dateparse import parse_date


class Command(BaseCommand):
    help = 'Import customers and loans from data/customer_data.xlsx and data/loan_data.xlsx'

    def add_arguments(self, parser):
        parser.add_argument('--data-dir', type=str, default='/app/data', help='Directory containing Excel files')

    def handle(self, *args, **options):
        data_dir = options['data_dir']
        cust_path = f"{data_dir}/customer_data.xlsx"
        loan_path = f"{data_dir}/loan_data.xlsx"

        try:
            cust_df = pd.read_excel(cust_path)
        except Exception as e:
            raise CommandError(f"Failed to read customers Excel: {e}")

        try:
            loan_df = pd.read_excel(loan_path)
        except Exception as e:
            raise CommandError(f"Failed to read loans Excel: {e}")

        created_customers = 0
        # Build mapping from spreadsheet Customer ID -> Django Customer instance
        excel_to_customer = {}
        for idx, row in cust_df.iterrows():
            # Spreadsheet columns seen: 'Customer ID', 'First Name', 'Last Name', 'Phone Number', 'Approved Limit'
            excel_id = row.get('Customer ID') if 'Customer ID' in row else None
            first = row.get('First Name') or ''
            last = row.get('Last Name') or ''
            phone = None
            if pd.notna(row.get('Phone Number')):
                # cast to int then str to avoid float formatting like 9.629317944e+09
                try:
                    phone = str(int(row.get('Phone Number')))
                except Exception:
                    phone = str(row.get('Phone Number'))
            approved_limit = None
            if 'Approved Limit' in row and pd.notna(row['Approved Limit']):
                try:
                    approved_limit = float(row['Approved Limit'])
                except Exception:
                    approved_limit = None

            # Skip empty rows (no useful identifying info at all)
            if not first and not last and not phone:
                self.stdout.write(self.style.WARNING(f"Skipping empty customer row {idx}"))
                continue

            # Ensure we have a non-null, unique email for the Customer model
            placeholder_email = None
            if excel_id is not None:
                placeholder_email = f"imported_{int(excel_id)}@local.invalid"
            elif phone:
                placeholder_email = f"phone_{phone}@local.invalid"

            # Guarantee uniqueness: if placeholder exists, append counter
            email_candidate = placeholder_email
            counter = 1
            while email_candidate and Customer.objects.filter(email=email_candidate).exists():
                email_candidate = f"{placeholder_email.split('@')[0]}_{counter}@{placeholder_email.split('@')[1]}"
                counter += 1

            # derive a date_of_birth from 'Age' column if model requires it
            dob = None
            if 'Age' in row and pd.notna(row['Age']):
                try:
                    age = int(row['Age'])
                    from datetime import datetime

                    birth_year = datetime.utcnow().year - age
                    # set to Jan 1 of birth year to satisfy date field
                    dob = f"{birth_year}-01-01"
                except Exception:
                    dob = None

            defaults = {'email': email_candidate}
            if dob:
                defaults['date_of_birth'] = dob

            customer, created = Customer.objects.get_or_create(
                first_name=first,
                last_name=last,
                phone=phone or None,
                defaults=defaults,
            )

            if approved_limit is not None:
                try:
                    customer.approved_limit = approved_limit
                    customer.save()
                except Exception:
                    pass

            excel_to_customer[excel_id] = customer
            if created:
                created_customers += 1

        self.stdout.write(self.style.SUCCESS(f"Imported/updated customers. New created: {created_customers}"))

        created_loans = 0
        for _, row in loan_df.iterrows():
            # Spreadsheet headers: 'Customer ID', 'Loan Amount', 'Tenure', 'Date of Approval', 'Loan ID'
            excel_cust_id = row.get('Customer ID') if 'Customer ID' in row else None
            customer = excel_to_customer.get(excel_cust_id)
            if customer is None:
                self.stdout.write(self.style.WARNING(f"Customer not found for loan row (Customer ID={excel_cust_id}); skipping."))
                continue

            amount = float(row.get('Loan Amount') or 0.0) if 'Loan Amount' in row else float(row.get('Loan Amount') or 0.0)
            tenure = int(row.get('Tenure') or 1) if 'Tenure' in row else int(row.get('Tenure') or 1)

            created_at = None
            if 'Date of Approval' in row and pd.notna(row['Date of Approval']):
                try:
                    created_at = pd.to_datetime(row['Date of Approval'])
                except Exception:
                    created_at = None

            # Determine status: approved if Date of Approval present, else PENDING
            status = 'APPROVED' if created_at is not None else 'PENDING'

            try:
                loan = Loan.objects.create(
                    customer=customer,
                    amount=amount,
                    term_months=tenure,
                    status=status,
                )
                if created_at:
                    loan.created_at = created_at
                    loan.save()
                created_loans += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Failed to create loan for row {row}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Imported loans. New created: {created_loans}"))
