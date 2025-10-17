from rest_framework import routers
from .views import CustomerViewSet, LoanViewSet
from django.urls import path
from .views import register_customer
from .views import check_eligibility
from .views import create_loan
from .views import view_loan
from .views import view_loans_by_customer
router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'loans', LoanViewSet)

urlpatterns = router.urls


urlpatterns = [
    path('register/', register_customer, name='register_customer'),
]




urlpatterns += [
    path('check-eligibility/', check_eligibility, name='check_eligibility'),
]

from .views import create_loan

urlpatterns += [
    path('create-loan/', create_loan, name='create_loan'),
]
urlpatterns += [
    path('view-loan/<int:loan_id>/', view_loan, name='view_loan'),
]
urlpatterns += [
    path('view-loans/<int:customer_id>/', view_loans_by_customer, name='view_loans_by_customer'),
]
