# Credit Approval System - Backend

This is a **backend system for credit approval** built with **Django** and **Django REST Framework**. The system allows you to register customers, check loan eligibility, create loans, and view loan details — all based on past customer data and credit scores.

The project is **fully dockerized**, uses **PostgreSQL** for database storage, and includes **Celery** for background data processing.

---

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Getting Started](#getting-started)
4. [API Endpoints](#api-endpoints)
5. [Data Ingestion](#data-ingestion)
6. [Testing the APIs](#testing-the-apis)
7. [Tech Stack](#tech-stack)
8. [Quickstart: Common Commands](#quickstart-common-commands)

---

## Features

* Register new customers and calculate approved credit limit based on salary.
* Check loan eligibility using a credit score algorithm.
* Automatically correct interest rates based on customer credit rating.
* Create loans and save them in the database.
* View individual loan details or all loans for a customer.
* Load initial customer and loan data from Excel files using background tasks.
* Fully dockerized environment for easy setup.

---

## Project Structure

```
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
```

---

## Getting Started

### Prerequisites

* Docker & Docker Compose installed
* Git installed

### Steps

1. Clone the repository:

```bash
git clone https://github.com/shivanirapure2003/alemeno-Credit-Approval-System.git
cd alemeno-Credit-Approval-System
```

2. Build and start the Docker containers:

```bash
docker compose up --build
```

3. Access the Django admin panel:

```
http://localhost:8000/admin/
```

4. Start Celery worker for background tasks:

```bash
docker compose exec web bash
celery -A credit_system worker -l info
```

---

## API Endpoints

| Endpoint                         | Method | Description                                    |
| -------------------------------- | ------ | ---------------------------------------------- |
| `/api/register/`                 | POST   | Register a new customer                        |
| `/api/check-eligibility/`        | POST   | Check if a customer is eligible for a loan     |
| `/api/create-loan/`              | POST   | Process and create a loan based on eligibility |
| `/api/view-loan/<loan_id>/`      | GET    | View details of a specific loan                |
| `/api/view-loans/<customer_id>/` | GET    | View all loans for a customer                  |

> All API responses include proper status codes and error messages for invalid inputs.

---

## Data Ingestion

Initial customer and loan data are provided in Excel files located in:

```
credit_system/data/customer_data.xlsx
credit_system/data/loan_data.xlsx
```

To load the data:

1. Ensure Celery worker is running.
2. Trigger background tasks:

```bash
docker compose exec web bash
python manage.py shell
>>> from loans.tasks import import_customers_from_excel, import_loans_from_excel
>>> import_customers_from_excel()
>>> import_loans_from_excel()
```

Once completed, data will be available in the Django admin panel.

---

## Testing the APIs

* Use **Postman** or **curl** to test endpoints.
* Recommended order:

  1. `/register/` → create a customer
  2. `/check-eligibility/` → check loan eligibility
  3. `/create-loan/` → create a loan
  4. `/view-loan/<loan_id>/` → view loan details
  5. `/view-loans/<customer_id>/` → view all customer loans

---

## Tech Stack

* **Python 3.11**
* **Django 5.2+**
* **Django REST Framework**
* **PostgreSQL**
* **Celery + Redis** for background tasks
* **Docker & Docker Compose** for containerization

---

## Quickstart: Common Commands

### Build and start the project
```bash
docker compose build --no-cache web
docker compose up -d
```

### Run migrations and create a superuser
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

### Import Excel data
```bash
docker compose exec web python manage.py import_excel
```

### Run tests
```bash
docker compose exec web python manage.py test loans
```

### API endpoint tests (curl examples)

Register a customer:
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "phone": "1234567890", "monthly_salary": 50000}'
```

Check eligibility:
```bash
curl -X POST http://localhost:8000/api/check-eligibility/ \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1, "loan_amount": 100000, "interest_rate": 10, "tenure": 12}'
```

Create a loan:
```bash
curl -X POST http://localhost:8000/api/create-loan/ \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1, "loan_amount": 100000, "interest_rate": 10, "tenure": 12}'
```

View a loan:
```bash
curl http://localhost:8000/api/view-loan/1/
```

View all loans for a customer:
```bash
curl http://localhost:8000/api/view-loans/1/
```

List all customers (ViewSet):
```bash
curl http://localhost:8000/api/customers/
```

List all loans (ViewSet):
```bash
curl http://localhost:8000/api/loans/
```

---

## Notes

* The system calculates **approved limit** as: `approved_limit = 36 * monthly_salary`
* Loan approval is determined based on **credit score** calculated from past loans.
* The **interest rate** may be adjusted automatically according to credit score slabs.
* All dependencies are included in `requirements.txt` for reproducibility.
