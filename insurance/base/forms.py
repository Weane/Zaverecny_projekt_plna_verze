from django.forms import ModelForm, ChoiceField, DateInput
from .models import Policyholder, InsurancePolicy, InsuranceClaim

POLICY_TYPE_CHOICES = (
    ('Sociální pojištění', 'Sociální pojištění'),
    ('Zdravotní pojištění', 'Zdravotní pojištění'),
    ('Povinné ručení', 'Povinné ručení'),
    ('Důchodové pojištění', 'Důchodové pojištění'),
    ('Pojištění majetku', 'Pojištění majetku'),
)


class MyDateInput(DateInput):
    input_type = 'date'


class PolicyholderForm(ModelForm):
    class Meta:
        model = Policyholder
        fields = '__all__'


class InsurancePolicyForm(ModelForm):
    policy_type = ChoiceField(choices=POLICY_TYPE_CHOICES)

    class Meta:
        model = InsurancePolicy
        fields = '__all__'
        exclude = ['holder']
        widgets = {
            'effective_date': MyDateInput(),
            'expire_date': MyDateInput()
        }


class ClaimForm(ModelForm):
    class Meta:
        model = InsuranceClaim
        fields = '__all__'
        exclude = ['holder', 'policy']

