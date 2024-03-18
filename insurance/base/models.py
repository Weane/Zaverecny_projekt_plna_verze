from django.db import models

# Create your models here.


class Policyholder(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class InsurancePolicy(models.Model):
    holder = models.ForeignKey(Policyholder, on_delete=models.CASCADE)
    effective_date = models.DateField()
    expire_date = models.DateField()
    payment_option = models.CharField(max_length=20)
    total_amount = models.IntegerField()
    policy_type = models.CharField(max_length=50)

    class Meta:
        ordering = ['expire_date']

    def __str__(self):
        return self.policy_type


class InsuranceClaim(models.Model):
    holder = models.ForeignKey(Policyholder, on_delete=models.CASCADE)
    policy = models.ForeignKey(InsurancePolicy, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField()
    description = models.TextField()
    date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
