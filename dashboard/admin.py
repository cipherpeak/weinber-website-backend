from django.contrib import admin
from .models import CustomUser, Product, ProductImage, ProductFeature, AboutBanner, SiriusBanner, DaxDetailingBanner, DaxSolutionsBanner,AdvantageBanner,WarrantyRegistration,WarrantyProductItem

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductFeature)
admin.site.register(AboutBanner)
admin.site.register(SiriusBanner)
admin.site.register(DaxDetailingBanner)
admin.site.register(DaxSolutionsBanner)
admin.site.register(AdvantageBanner)
admin.site.register(WarrantyRegistration)
admin.site.register(WarrantyProductItem)
