from django.contrib import admin
from .models import CustomUser, Product, ProductImage, ProductFeature, HomePage, FranchisePage, PackagesPage, ContactPage

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductFeature)
admin.site.register(HomePage)
admin.site.register(FranchisePage)
admin.site.register(PackagesPage)
admin.site.register(ContactPage)