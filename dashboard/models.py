from django.contrib.auth.models import AbstractUser
from django.db import models

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

class HomePage(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200, default="Home Services")
    description = models.TextField(default="Professional home maintenance and repair services to keep your living space comfortable and well-maintained throughout the year.")
    image = models.ImageField(upload_to='cards/', default='images/notes/home.jpg')
    video = models.FileField(upload_to='cards/videos/', null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Home Page Card"
        verbose_name_plural = "Home Page Card"

    def get_media_url(self):
        """Return the appropriate media URL based on media type"""
        if self.media_type == 'video' and self.video:
            return self.video.url
        return self.image.url
    
    def get_media_type(self):
        """Return the media type for template rendering"""
        return self.media_type

# Update other models similarly
class FranchisePage(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200, default="Franchise Opportunities")
    description = models.TextField(default="Join our growing network of franchises and be part of our success story.")
    image = models.ImageField(upload_to='cards/', default='images/notes/franchise.jpg')
    video = models.FileField(upload_to='cards/videos/', null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    updated_at = models.DateTimeField(auto_now=True)

class PackagesPage(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200, default="Our Packages")
    description = models.TextField(default="Explore our carefully crafted packages designed to meet your every need.")
    image = models.ImageField(upload_to='cards/', default='images/notes/packages.jpg')
    video = models.FileField(upload_to='cards/videos/', null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    updated_at = models.DateTimeField(auto_now=True)

class ContactPage(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200, default="Get In Touch")
    description = models.TextField(default="Contact us for any inquiries or support. We're here to help you.")
    image = models.ImageField(upload_to='cards/', default='images/notes/contact.jpg')
    video = models.FileField(upload_to='cards/videos/', null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    updated_at = models.DateTimeField(auto_now=True)

class WarrantyRegistration(models.Model):
    dealer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='warranties')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    serial_number = models.CharField(max_length=100)
    application_type = models.CharField(max_length=100, default='PAINT PROTECTION FILMS')
    
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
        return f"{self.customer_first_name} - {self.product.name if self.product else 'Unknown'}"

