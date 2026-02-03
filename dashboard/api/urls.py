from django.urls import path
from .views import ProductListAPIView, HomeBannerAPIView,ProductBannerAPIView,AboutBannerAPIView, SiriusBannerAPIView, DaxDetailingBannerAPIView, DaxSolutionsBannerAPIView,AdvantageBannerAPIView, WarrantyRegistrationCreateAPIView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='api-product-list'),
    path('home/banner/', HomeBannerAPIView.as_view(), name='home-banner'),
    path('products/banner/', ProductBannerAPIView.as_view(), name='product-banner'),
    path('about/banner/', AboutBannerAPIView.as_view(), name='about-banner'),
    path('sirius/banner/', SiriusBannerAPIView.as_view(), name='sirius-banner'),
    path('daxdetailing/banner/', DaxDetailingBannerAPIView.as_view(), name='daxdetailing-banner'),
    path('daxsolutions/banner/', DaxSolutionsBannerAPIView.as_view(), name='daxsolutions-banner'),
    path('advantage/banner/', AdvantageBannerAPIView.as_view(), name='advantage-banner'),
    path('warranty-registration/', WarrantyRegistrationCreateAPIView.as_view(), name='api-warranty-registration'),

]
