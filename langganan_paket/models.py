from django.db import models
from django.contrib.auth.models import User
import uuid

class Akun(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=50)
    nama = models.CharField(max_length=100)
    gender = models.IntegerField(choices=((0, 'Female'), (1, 'Male')))
    tempat_lahir = models.CharField(max_length=50)
    tanggal_lahir = models.DateField()
    is_verified = models.BooleanField()
    kota_asal = models.CharField(max_length=50)

class Paket(models.Model):
    jenis = models.CharField(max_length=50, primary_key=True)
    harga = models.IntegerField()

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jenis_paket = models.ForeignKey(Paket, on_delete=models.CASCADE)
    email = models.ForeignKey(Akun, on_delete=models.CASCADE)
    timestamp_dimulai = models.DateTimeField()
    timestamp_berakhir = models.DateTimeField()
    metode_bayar = models.CharField(max_length=50)
    nominal = models.IntegerField()

class Premium(models.Model):
    email = models.OneToOneField(Akun, on_delete=models.CASCADE, primary_key=True)