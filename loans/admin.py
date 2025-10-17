from django.contrib import admin
from .models import Customer, Loan

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'amount', 'term_months', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('customer__first_name', 'customer__last_name', 'customer__email')
