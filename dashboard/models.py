from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify



class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
        ('dealer', 'Dealer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='dealer')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"

class ProductFeature(models.Model):
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE)
    feature = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.feature} - {self.product.name}"

class HomeBannerSlide(models.Model):
    """Model for carousel banner slides on homepage"""
    
    # Required fields
    title1 = models.CharField(
        max_length=200,
        verbose_name="Main Title",
        help_text="First line of the banner title"
    )
    title2 = models.CharField(
        max_length=200,
        verbose_name="Secondary Title",
        help_text="Second line of the banner title (colored differently)"
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="Banner description text"
    )
    image = models.ImageField(
        upload_to='banners/%Y/%m/%d/',
        verbose_name="Banner Image",
        help_text="Recommended size: 1920x1080px or similar high-quality image"
    )

    link = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Custom Link",
        help_text="Optional custom URL link (overrides product link)"
    )
    
    # Display fields
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Show this slide in the banner"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order",
        help_text="Order in which slides appear (lower numbers first)"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Banner Slide"
        verbose_name_plural = "Banner Slides"
        ordering = ['display_order', '-created_at']
    
    def __str__(self):
        return f"{self.title1} - {self.title2}"
    
    def get_absolute_url(self):
        if self.link:
            return self.link
        elif self.product:
            return self.product.get_absolute_url()
        return '#'
    
    def save(self, *args, **kwargs):
        # Ensure image filenames are clean
        if self.image and hasattr(self.image, 'name'):
            # Clean up filename
            filename = slugify(f"{self.title1}-{self.title2}")
            extension = self.image.name.split('.')[-1]
            self.image.name = f"{filename}.{extension}"
        super().save(*args, **kwargs)

class ProductBanner(models.Model):    
    title = models.CharField(max_length=200, default="Franchise Opportunities")
    description = models.TextField(default="Join our growing network of franchises and be part of our success story.")
    image = models.ImageField(upload_to='product_banner/', default='images/notes/product.jpg')
    updated_at = models.DateTimeField(auto_now=True)

class AboutBanner(models.Model):
    title = models.CharField(max_length=200, default="Our Packages")
    description = models.TextField(default="Explore our carefully crafted packages designed to meet your every need.")
    image = models.ImageField(upload_to='about_banner/', default='images/notes/about.jpg')
    updated_at = models.DateTimeField(auto_now=True)

class SiriusBanner(models.Model):    
    title = models.CharField(max_length=200, default="Sirius PPF")
    description = models.TextField(default="Premium Point Protection Film.")
    image = models.ImageField(upload_to='sirius_banner/', default='images/notes/sirius.jpg')
    updated_at = models.DateTimeField(auto_now=True)

class DaxDetailingBanner(models.Model):    
    title = models.CharField(max_length=200, default="Dax Detailing")
    description = models.TextField(default="Professional Car Detailing Services.")
    image = models.ImageField(upload_to='dax_detailing_banner/', default='images/notes/dax_detailing.jpg')
    updated_at = models.DateTimeField(auto_now=True)

class DaxSolutionsBanner(models.Model):    
    title = models.CharField(max_length=200, default="Dax Solutions")
    description = models.TextField(default="Innovative Automotive Solutions.")
    image = models.ImageField(upload_to='dax_solutions_banner/', default='images/notes/dax_solutions.jpg')
    updated_at = models.DateTimeField(auto_now=True)

class AdvantageBanner(models.Model):    
    title = models.CharField(max_length=200, default="Advantage Series")
    description = models.TextField(default="Premium Automotive Solutions.")
    image = models.ImageField(upload_to='advantage_banner/', default='images/notes/advantage.jpg')
    updated_at = models.DateTimeField(auto_now=True)



class WarrantyRegistration(models.Model):
    # Dealer Info (From Form)
    dealer_company_name = models.CharField(max_length=255, default='')
    dealer_name = models.CharField(max_length=255, default='')
    dealer_email = models.EmailField(default='')
    dealer_phone = models.CharField(max_length=50, default='')
    dealer_address = models.TextField(default='')
    dealer_city = models.CharField(max_length=100, default='')
    dealer_state = models.CharField(max_length=100, default='')
    dealer_zip = models.CharField(max_length=20, default='')
    dealer_country = models.CharField(max_length=100, default='')
    
    # Link to registered dealer if available
    dealer_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='warranties')

    # Product Info Header
    serial_number = models.CharField(max_length=100, default='')
    
    # Customer Info
    customer_first_name = models.CharField(max_length=100)
    customer_last_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    
    # Vehicle Info
    installation_date = models.DateField()
    chassis_number = models.CharField(max_length=100)
    vehicle_make_model = models.CharField(max_length=200, verbose_name="Year, Make & Model")
    proof_of_purchase = models.ImageField(upload_to='warranties/proofs/')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_first_name} - {self.serial_number}"

class WarrantyProductItem(models.Model):
    warranty = models.ForeignKey(WarrantyRegistration, on_delete=models.CASCADE, related_name='items')
    product = models.CharField(max_length=255, default='')
    application_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.application_type} - {self.product}"

