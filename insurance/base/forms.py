from django.forms import ModelForm
from .models import Policyholder, InsurancePolicy, InsuranceClaim


class PolicyholderForm(ModelForm):
    class Meta:
        model = Policyholder
        fields = '__all__'


class InsurancePolicyForm(ModelForm):
    class Meta:
        model = InsurancePolicy
        fields = '__all__'
        exclude = ['holder']


class ClaimForm(ModelForm):
    class Meta:
        model = InsuranceClaim
        fields = '__all__'
        exclude = ['holder', 'policy']
