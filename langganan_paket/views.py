# Create your views here.
from django.shortcuts import render, redirect
from .models import Package, Transaction
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def package_list(request):
    packages = Package.objects.all()
    return render(request, 'packages.html', {'packages': packages})

@login_required
def payment(request, package_id):
    package = Package.objects.get(id=package_id)
    if request.method == 'POST':
        payment_method = request.POST.get('payment-method')
        now = timezone.now()
        end_date = now + timezone.timedelta(days=package.duration * 30)
        Transaction.objects.create(
            user=request.user,
            package=package,
            start_date=now,
            end_date=end_date,
            payment_method=payment_method,
            amount_paid=package.price
        )
        return redirect('history')
    return render(request, 'payment.html', {'package': package})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'history.html', {'transactions': transactions})