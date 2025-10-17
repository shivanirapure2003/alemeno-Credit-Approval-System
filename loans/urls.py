from rest_framework import routers
from .views import CustomerViewSet, LoanViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'loans', LoanViewSet)

urlpatterns = router.urls
