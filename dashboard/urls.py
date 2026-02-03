from django.urls import path
from .views import (
    Overview, ProductList, DealerList, WarrantyClaims,
    AdminLogin, AdminLogout, AddProduct, DeleteProduct, EditProduct,
    AddDealer, DeleteDealer, EditDealer, HeroSectionsView, HomeBannerListView,
    AddHomeBannerSlide, EditHomeBannerSlide, DeleteHomeBannerSlide,
    WarrantyRegistrationList, AddWarrantyRegistration, EditWarrantyRegistration, DeleteWarrantyRegistration,
    EditProductBanner,EditAboutBanner, EditSiriusBanner, EditDaxDetailingBanner, EditDaxSolutionsBanner,EditAdvantageBanner
)


urlpatterns = [
    path('', Overview.as_view(), name='dashboard'),
    path('products/', ProductList.as_view(), name='products'),
    path('home-banner/list/', HomeBannerListView.as_view(), name='home-banner-list'),
    path('hero-sections/', HeroSectionsView.as_view(), name='hero-sections'),
    path('home-banner/add/', AddHomeBannerSlide.as_view(), name='add-home-banner'),
    path('home-banner/edit/<int:slide_id>/', EditHomeBannerSlide.as_view(), name='edit-home-banner'),
    path('home-banner/delete/<int:slide_id>/', DeleteHomeBannerSlide.as_view(), name='delete-home-banner'),
    path('product-banner/edit/', EditProductBanner.as_view(), name='edit-product-banner'),
    path('about-banner/edit/', EditAboutBanner.as_view(), name='edit-about-banner'),
    path('sirius-banner/edit/', EditSiriusBanner.as_view(), name='edit-sirius-banner'),
    path('dax-detailing-banner/edit/', EditDaxDetailingBanner.as_view(), name='edit-dax-detailing-banner'),
    path('dax-solutions-banner/edit/', EditDaxSolutionsBanner.as_view(), name='edit-dax-solutions-banner'),
    path('advantage-banner/edit/', EditAdvantageBanner.as_view(), name='edit-advantage-banner'),
    path('dealers/', DealerList.as_view(), name='dealers'),
    path('claims/', WarrantyClaims.as_view(), name='warranty-claims'),
    
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