from django.db import models

# Create your models here.


class Policyholder(models.Model):
    """
    Class represents Policyholder with his name, email, phone and address. Order is ascending by the last name
    and then first name.
    """
    first_name = models.CharField("Jméno", max_length=50)
    last_name = models.CharField("Příjmení", max_length=50)
    email = models.EmailField()
    phone = models.CharField("Telefon", max_length=20)
    address = models.CharField("Adresa", max_length=100)
    city = models.CharField("Město", max_length=100)
    zip_code = models.CharField("PSČ", max_length=20)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class InsurancePolicy(models.Model):
    """
    Class represents Insurance Policies of Policyholders with its type, total amount, expire and effective date.
    Order is ascending for the first that expire is on the top.
    """
    holder = models.ForeignKey(Policyholder, on_delete=models.CASCADE)
    effective_date = models.DateField("Začátek platnosti")
    expire_date = models.DateField("Konec platnosti")
    total_amount = models.IntegerField("Celková částka")
    policy_type = models.CharField("Druh pojištění", max_length=50)

    class Meta:
        ordering = ['expire_date']

    def __str__(self):
        return self.policy_type


class InsuranceClaim(models.Model):
    """
    Class represent Insurance Claims of Policies with their description, amount and time of creation. Order descending
    by date to see last one on the top.
    """
    holder = models.ForeignKey(Policyholder, on_delete=models.CASCADE)
    policy = models.ForeignKey(InsurancePolicy, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField("Uznaná náhrada")
    description = models.TextField("Popis")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.description[0:50]
