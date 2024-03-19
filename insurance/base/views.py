from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Policyholder, InsurancePolicy, InsuranceClaim
from .forms import PolicyholderForm, InsurancePolicyForm, ClaimForm

# Create your views here.


def home(request):
    """
    Function will get all the policyholders and render home page with list of them.
    """

    policyholders = Policyholder.objects.all()
    context = {'policyholders': policyholders}
    return render(request, 'base/home.html', context)


def policyholder_detail(request, pk):
    """
    Function will get the policyholder of id which will get as pk parameter and all policies
    of that holder and render page with policyholder details and policies
    """
    policyholder = Policyholder.objects.get(id=pk)
    insurance_policies = policyholder.insurancepolicy_set.all()  # gets all policies of policyholder instance
    context = {'policyholder': policyholder, 'insurance_policies': insurance_policies}
    return render(request, 'base/policyholder_detail.html', context)


def insurance_policy_detail(request, pk):
    """
    Function will get the insurance policy of id which will get as pk parameter and all claims
    of that policy and render page with policy details and all its claims
    """
    insurance_policy = InsurancePolicy.objects.get(id=pk)
    claims = insurance_policy.insuranceclaim_set.all()  # gets all claims of insurance_policy instance
    context = {'insurance_policy': insurance_policy, 'claims': claims}
    return render(request, 'base/insurance_policy_detail.html', context)


def insurance_policy_page(request):
    """
    Function will get all the insurance policies and render page with list of them.
    """
    insurance_policies = InsurancePolicy.objects.all()
    context = {'insurance_policies': insurance_policies}
    return render(request, 'base/insurance_policy.html', context)


def create_policyholder(request):
    """
    Function will render page with form for creation of policyholder. On submit of POST method it validates
    data and on success saves data to database and display message.
    """
    form = PolicyholderForm()
    if request.method == 'POST':
        form = PolicyholderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pojištěnec byl přidán.')
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/input_form.html', context)


def update_policyholder(request, pk):
    """
    Function will render page with form for creation of policyholder and fills it with data of policyholder with id
    passed as pk parameter. On submit of POST method it validates data and on success saves data to database,
    display message and redirect to that policyholder detail page.
    """
    policyholder = Policyholder.objects.get(id=pk)
    form = PolicyholderForm(instance=policyholder)  # Fills the form with policyholder instance data

    if request.method == 'POST':
        form = PolicyholderForm(request.POST, instance=policyholder)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pojištěnec byl aktualizován.')
            return redirect('policyholder-detail', policyholder.id)

    context = {'form': form}
    return render(request, 'base/input_form.html', context)


def delete_policyholder(request, pk):
    """
    Function will get the policyholder of id which will get as pk parameter and on submit of POST method it will delete
    policyholder, display message and redirect to homepage.
    """
    policyholder = Policyholder.objects.get(id=pk)

    if request.method == 'POST':
        policyholder.delete()
        messages.error(request, 'Pojištěnec byl smazán.')
        return redirect('home')
    context = {'obj': policyholder, 'notice': "A všechna jeho pojištění!"}
    return render(request, 'base/delete.html', context)


def create_insurance_policy(request, pk):
    """
    Function will render page with form for creation of insurance policy. On submit of POST method it validates data
    on success fills holder of the policy with instance of policyholder with id passed as pk parameter,saves data
    to database, display message and redirect to policyholder of this policy.
    """
    form = InsurancePolicyForm()
    policyholder = Policyholder.objects.get(id=pk)

    if request.method == 'POST':
        form = InsurancePolicyForm(request.POST)
        if form.is_valid():
            insurance_policy = form.save(commit=False)  # saves data to insurance_policy but don't commit to database
            insurance_policy.holder = policyholder  # fills holder of insurance_policy with policyholder data
            insurance_policy.save()
            messages.success(request, 'Pojištění bylo vytvořeno.')
            return redirect('policyholder-detail', policyholder.id)
    context = {'form': form, 'policyholder': policyholder}
    return render(request, 'base/input_form.html', context)


def update_insurance_policy(request, pk):
    """
    Function will render page with form for creation of insurance policy and fills it with data of policy with id
    passed as pk parameter. On submit of POST method it validates data and on success saves data to database,
    display message and redirect to that policyholder detail page.
    """
    insurance_policy = InsurancePolicy.objects.get(id=pk)
    form = InsurancePolicyForm(instance=insurance_policy)  # Fills the form with insurance_policy instance data

    if request.method == 'POST':
        form = InsurancePolicyForm(request.POST, instance=insurance_policy)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pojištění bylo aktualizováno.')
            return redirect('policyholder-detail', insurance_policy.holder.id)

    context = {'form': form}
    return render(request, 'base/input_form.html', context)


def delete_insurance_policy(request, pk):
    """
    Function will get the insurance policy of id which will get as pk parameter and on submit of POST method it will
    delete insurance policy, display message and redirect to detail of its policyholder.
    """
    insurance_policy = InsurancePolicy.objects.get(id=pk)
    if request.method == 'POST':
        insurance_policy.delete()
        messages.error(request, 'Pojištění bylo smazáno.')
        return redirect('policyholder-detail', insurance_policy.holder.id)
    context = {'obj': insurance_policy, 'notice': f'Pojištěnce: {insurance_policy.holder}'}
    return render(request, 'base/delete.html', context)


def claims_page(request):
    """
    Function will get all the claims and render page with list of them.
    """
    claims = InsuranceClaim.objects.all()
    context = {'claims': claims}
    return render(request, 'base/claims.html', context)


def create_claim(request, pk):
    """
    Function will render page with form for creation of claim. On submit of POST method it validates data
    on success fills insurance policy and holder of the claim with instance of insurance policy and policyholder with
    id passed as pk parameter, saves data to database, display message and redirect to insurance policy detail of this
    claim.
    """
    form = ClaimForm()
    insurance_policy = InsurancePolicy.objects.get(id=pk)

    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)  # saves data to claim but don't commit to database
            claim.policy = insurance_policy  # fills policy of the claim with insurance policy data
            claim.holder = insurance_policy.holder  # fills holder of the claim with policyholder data
            claim.save()
            messages.success(request, 'Pojistná událost byla vytvořena.')
            return redirect('claims')
    context = {'form': form, 'insurance_policy': insurance_policy}
    return render(request, 'base/input_form.html', context)


def update_claim(request, pk):
    """
    Function will render page with form for creation of claim and fills it with data of the claim with id
    passed as pk parameter. On submit of POST method it validates data and on success saves data to database,
    display message and redirect to that policy detail page.
    """
    claim = InsuranceClaim.objects.get(id=pk)  # Fills the form with insurance claim instance data
    form = ClaimForm(instance=claim)

    if request.method == 'POST':
        form = ClaimForm(request.POST, instance=claim)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pojistná událost byla aktualizována.')
            return redirect('insurance-policy-detail', claim.policy.id)

    context = {'form': form}
    return render(request, 'base/input_form.html', context)


def delete_claim(request, pk):
    """
    Function will get the claim of id which will get as pk parameter and on submit of POST method it will
    delete the claim, display message and redirect to detail of its policy .
    """
    claim = InsuranceClaim.objects.get(id=pk)
    if request.method == 'POST':
        claim.delete()
        messages.error(request, 'Pojistná událost byla smazána.')
        return redirect('insurance-policy-detail', claim.policy.id)
    context = {'obj': claim, 'notice': f'Pojištěnce: {claim.holder}'}
    return render(request, 'base/delete.html', context)
