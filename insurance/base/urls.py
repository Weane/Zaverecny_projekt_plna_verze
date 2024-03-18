from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('policyholder-detail/<str:pk>/', views.policyholder_detail, name="policyholder-detail"),
    path('insurance-policy-detail/<str:pk>/', views.insurance_policy_detail, name="insurance-policy-detail"),
    path('insurance-policy/', views.insurance_policy_page, name="insurance-policy"),
    path('create-policyholder/', views.create_policyholder, name="create-policyholder"),
    path('update-policyholder/<str:pk>/', views.update_policyholder, name="update-policyholder"),
    path('delete-policyholder/<str:pk>/', views.delete_policyholder, name="delete-policyholder"),
    path('create-insurance-policy/<str:pk>/', views.create_insurance_policy, name="create-insurance-policy"),
    path('update-insurance-policy/<str:pk>/', views.update_insurance_policy, name="update-insurance-policy"),
    path('delete-insurance-policy/<str:pk>/', views.delete_insurance_policy, name="delete-insurance-policy"),
    path('claims', views.claims_page, name="claims"),
    path('create-claim/<str:pk>/', views.create_claim, name="create-claim"),
    path('update-claim/<str:pk>/', views.update_claim, name="update-claim"),
    path('delete-claim/<str:pk>/', views.delete_claim, name="delete-claim"),
]
