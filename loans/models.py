from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Loan(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term_months = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Loan {self.id} for {self.customer}"
    def approve_or_reject(self):
        """
        Example logic:
        - Approve if amount <= 5000
        - Reject if amount > 5000
        """
        if self.amount <= 5000:
            self.status = 'APPROVED'
        else:
            self.status = 'REJECTED'
        self.save()
