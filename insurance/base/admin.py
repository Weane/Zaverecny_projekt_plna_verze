from django.contrib import admin
from .models import InsurancePolicy, Policyholder, InsuranceClaim

# Register your models here.

admin.site.register(Policyholder)
admin.site.register(InsurancePolicy)
admin.site.register(InsuranceClaim)
