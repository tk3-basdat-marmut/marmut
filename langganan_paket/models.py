# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Package(models.Model):
    DURATION_CHOICES = [
        (1, '1 Bulan'),
        (3, '3 Bulan'),
        (6, '6 Bulan'),
        (12, '1 Tahun'),
    ]
    duration = models.IntegerField(choices=DURATION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.get_duration_display()} - Rp{self.price}"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    payment_method = models.CharField(max_length=100)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.package} - Rp{self.amount_paid}"