from django.shortcuts import render, redirect
from .models import Policyholder, InsurancePolicy, InsuranceClaim
from .forms import PolicyholderForm, InsurancePolicyForm, ClaimForm

# Create your views here.


def home(request):
    policyholders = Policyholder.objects.all()
    context = {'policyholders': policyholders}
    return render(request, 'base/home.html', context)


def policyholder_detail(request, pk):
    policyholder = Policyholder.objects.get(id=pk)
    insurance_policies = policyholder.insurancepolicy_set.all()
    context = {'policyholder': policyholder, 'insurance_policies': insurance_policies}
    return render(request, 'base/policyholder_detail.html', context)


def insurance_policy_detail(request, pk):
    insurance_policy = InsurancePolicy.objects.get(id=pk)
    claims = insurance_policy.insuranceclaim_set.all()
    context = {'insurance_policy': insurance_policy, 'claims': claims}
    return render(request, 'base/insurance_policy_detail.html', context)


def insurance_policy_page(request):
    insurance_policies = InsurancePolicy.objects.all()
    context = {'insurance_policies': insurance_policies}
    return render(request, 'base/insurance_policy.html', context)


def create_policyholder(request):
    form = PolicyholderForm()
    if request.method == 'POST':
        form = PolicyholderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/input_form.html', context)


def update_policyholder(request, pk):
    policyholder = Policyholder.objects.get(id=pk)
    form = PolicyholderForm(instance=policyholder)

    if request.method == 'POST':
        form = PolicyholderForm(request.POST, instance=policyholder)
        if form.is_valid():
            form.save()
            return redirect('policyholder-detail', policyholder.id)

    context = {'form': form}
    return render(request, 'base/input_form.html', context)


def delete_policyholder(request, pk):
    policyholder = Policyholder.objects.get(id=pk)

    if request.method == 'POST':
        policyholder.delete()
        return redirect('home')
    context = {'obj': policyholder, 'notice': "A všechna jeho pojištění!"}
    return render(request, 'base/delete.html', context)


def create_insurance_policy(request, pk):
    form = InsurancePolicyForm()
    policyholder = Policyholder.objects.get(id=pk)

    if request.method == 'POST':
        form = InsurancePolicyForm(request.POST)
        if form.is_valid():
            insurance_policy = form.save(commit=False)
            insurance_policy.holder = policyholder
            insurance_policy.save()
            return redirect('policyholder-detail', policyholder.id)
    context = {'form': form, 'policyholder': policyholder}
    return render(request, 'base/input_form.html', context)


def update_insurance_policy(request, pk):
    insurance_policy = InsurancePolicy.objects.get(id=pk)
    form = InsurancePolicyForm(instance=insurance_policy)

    if request.method == 'POST':
        form = InsurancePolicyForm(request.POST, instance=insurance_policy)
        if form.is_valid():
            form.save()
            return redirect('policyholder-detail', insurance_policy.holder.id)

    context = {'form': form}
    return render(request, 'base/input_form.html', context)


def delete_insurance_policy(request, pk):
    insurance_policy = InsurancePolicy.objects.get(id=pk)
    if request.method == 'POST':
        insurance_policy.delete()
        return redirect('policyholder-detail', insurance_policy.holder.id)
    context = {'obj': insurance_policy, 'notice': f'Pojištěnce: {insurance_policy.holder}'}
    return render(request, 'base/delete.html', context)


def claims_page(request):
    claims = InsuranceClaim.objects.all()
    context = {'claims': claims}
    return render(request, 'base/claims.html', context)


def create_claim(request, pk):
    form = ClaimForm()
    insurance_policy = InsurancePolicy.objects.get(id=pk)

    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.policy = insurance_policy
            claim.holder = insurance_policy.holder
            claim.save()
            return redirect('claims')
    context = {'form': form, 'insurance_policy': insurance_policy}
    return render(request, 'base/input_form.html', context)


def update_claim(request, pk):
    claim = InsuranceClaim.objects.get(id=pk)
    form = ClaimForm(instance=claim)

    if request.method == 'POST':
        form = ClaimForm(request.POST, instance=claim)
        if form.is_valid():
            form.save()
            return redirect('insurance-policy-detail', claim.policy.id)

    context = {'form': form}
    return render(request, 'base/input_form.html', context)


def delete_claim(request, pk):
    claim = InsuranceClaim.objects.get(id=pk)
    if request.method == 'POST':
        claim.delete()
        return redirect('insurance-policy-detail', claim.policy.id)
    context = {'obj': claim, 'notice': f'Pojištěnce: {claim.holder}'}
    return render(request, 'base/delete.html', context)
