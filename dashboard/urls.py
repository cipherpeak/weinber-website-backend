from django.urls import path
from .views import (
    Overview, ProductList, DealerList, HeroContent, WarrantyClaims,
    AdminLogin, AdminLogout, AddProduct, DeleteProduct, EditHeroCard, EditProduct,
    AddDealer, DeleteDealer, EditDealer,
    WarrantyRegistrationList, AddWarrantyRegistration, EditWarrantyRegistration, DeleteWarrantyRegistration
)


urlpatterns = [
    path('', Overview.as_view(), name='dashboard'),
    path('products/', ProductList.as_view(), name='products'),
    path('dealers/', DealerList.as_view(), name='dealers'),
    path('content/', HeroContent.as_view(), name='manage-content'),
    path('claims/', WarrantyClaims.as_view(), name='warranty-claims'),
    
    path('hero-card/<str:card_type>/edit/', EditHeroCard.as_view(), name='edit-hero-card'),
    
    path('admin-login/', AdminLogin.as_view(), name='admin-login'),
    path('admin-logout/', AdminLogout.as_view(), name='admin-logout'),
    path('add-product/', AddProduct.as_view(), name='add-products'),
    path('products/edit/<int:product_id>/', EditProduct.as_view(), name='edit-product'),
    path('delete-product/<int:product_id>/', DeleteProduct.as_view(), name='delete-product'),

    path('add-dealer/', AddDealer.as_view(), name='add-dealer'),
    path('dealers/edit/<int:dealer_id>/', EditDealer.as_view(), name='edit-dealer'),
    path('delete-dealer/<int:dealer_id>/', DeleteDealer.as_view(), name='delete-dealer'),

    path('warranty-registration/', WarrantyRegistrationList.as_view(), name='warranty-registration'),
    path('warranty-registration/add/', AddWarrantyRegistration.as_view(), name='add-warranty-registration'),
    path('warranty-registration/edit/<int:reg_id>/', EditWarrantyRegistration.as_view(), name='edit-warranty-registration'),
    path('warranty-registration/delete/<int:reg_id>/', DeleteWarrantyRegistration.as_view(), name='delete-warranty-registration'),
]