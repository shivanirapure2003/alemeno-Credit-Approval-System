Credit Approval System - Backend

This is a backend system for credit approval built with Django and Django REST Framework. The system allows you to register customers, check loan eligibility, create loans, and view loan details — all based on past customer data and credit scores.

The project is fully dockerized, uses PostgreSQL for database storage, and includes Celery for background data processing.

Table of Contents

Features

Project Structure

Getting Started

API Endpoints

Data Ingestion

Testing the APIs

Tech Stack

Features

Register new customers and calculate approved credit limit based on salary.

Check loan eligibility using a credit score algorithm.

Automatically correct interest rates based on customer credit rating.

Create loans and save them in the database.

View individual loan details or all loans for a customer.

Load initial customer and loan data from Excel files using background tasks.

Fully dockerized environment for easy setup.

Project Structure
credit_approval/
│
├─ credit_system/          # Django project settings
├─ loans/                  # Django app for loan management
│   ├─ migrations/         # Database migrations
│   ├─ tasks.py            # Background tasks for data import
│   ├─ models.py           # Customer and Loan models
│   ├─ serializers.py      # DRF serializers
│   ├─ views.py            # API views
│   ├─ urls.py             # API routes
├─ data/                   # Initial Excel files (customer_data.xlsx, loan_data.xlsx)
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
└─ README.md

Getting Started
Prerequisites

Docker & Docker Compose installed

Git installed

Steps

Clone the repository:

git clone (https://github.com/shivanirapure2003/alemeno-Credit-Approval-System.git)
cd credit_approval


Build and start the Docker containers:

docker compose up --build


Access the Django admin panel:

http://localhost:8000/admin/


Start Celery worker for background tasks:

docker compose exec web bash
celery -A credit_system worker -l info

API Endpoints
Endpoint	Method	Description
/api/register/	POST	Register a new customer
/api/check-eligibility/	POST	Check if a customer is eligible for a loan
/api/create-loan/	POST	Process and create a loan based on eligibility
/api/view-loan/<loan_id>/	GET	View details of a specific loan
/api/view-loans/<customer_id>/	GET	View all loans for a customer

All API responses include proper status codes and error messages for invalid inputs.

Data Ingestion

Initial customer and loan data are provided in Excel files located in:

credit_system/data/customer_data.xlsx
credit_system/data/loan_data.xlsx


To load the data:

Ensure Celery worker is running.

Trigger background tasks:

docker compose exec web bash
python manage.py shell
>>> from loans.tasks import import_customers_from_excel, import_loans_from_excel
>>> import_customers_from_excel()
>>> import_loans_from_excel()


Once completed, data will be available in the Django admin panel.

Testing the APIs

Use Postman or curl to test endpoints.

Recommended order:

/register/ → create a customer

/check-eligibility/ → check loan eligibility

/create-loan/ → create a loan

/view-loan/<loan_id>/ → view loan details

/view-loans/<customer_id>/ → view all customer loans

Tech Stack

Python 3.11

Django 5.2+

Django REST Framework

PostgreSQL

Celery + Redis for background tasks

Docker & Docker Compose for containerization

Notes

The system calculates approved limit as: approved_limit = 36 * monthly_salary

Loan approval is determined based on credit score calculated from past loans.

The interest rate may be adjusted automatically according to credit score slabs.

All dependencies are included in requirements.txt for reproducibility.

This README is written to help anyone set up, run, and test the system easily without confusion.