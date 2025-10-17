from django.test import TestCase
from .models import Customer, Loan
from .utils import calculate_credit_score


class TestCalculateCreditScore(TestCase):
	def test_no_loans_returns_100(self):
		customer = Customer.objects.create(
			first_name='Alice', last_name='NoLoans', email='alice@example.com',
			phone='1111111111', date_of_birth='1990-01-01'
		)
		score = calculate_credit_score(customer)
		self.assertEqual(score, 100)

	def test_current_debt_exceeds_limit_returns_0(self):
		customer = Customer.objects.create(
			first_name='Bob', last_name='OverLimit', email='bob@example.com',
			phone='2222222222', date_of_birth='1990-01-01'
		)
		# set approved_limit attribute dynamically for test
		customer.approved_limit = 1000.0
		customer.save()

		Loan.objects.create(customer=customer, amount=1500.0, term_months=12, status='APPROVED')
		score = calculate_credit_score(customer)
		self.assertEqual(score, 0)

	def test_mixed_loans_scores_between_0_and_100(self):
		customer = Customer.objects.create(
			first_name='Carol', last_name='Mixed', email='carol@example.com',
			phone='3333333333', date_of_birth='1990-01-01'
		)
		customer.approved_limit = 10000.0
		customer.save()

		# create two loans, one approved, one pending
		l1 = Loan.objects.create(customer=customer, amount=1000.0, term_months=12, status='APPROVED')
		l2 = Loan.objects.create(customer=customer, amount=500.0, term_months=6, status='PENDING')

		score = calculate_credit_score(customer)
		self.assertTrue(0 <= score <= 100)
