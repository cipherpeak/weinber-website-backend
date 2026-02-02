from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, Product, HomePage, FranchisePage, PackagesPage, ContactPage, ProductImage, ProductFeature, WarrantyRegistration

class Overview(View):
    def get(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        total_products = Product.objects.count()
        context = {
            'total_products': total_products,
        }
        return render(request, 'dashboard/overview.html', context)

class ProductList(View):
    def get(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        products = Product.objects.all().prefetch_related('images').order_by('-created_at')
        return render(request, 'dashboard/products.html', {'products': products})


class EditHeroCard(View):
    @method_decorator(never_cache)
    def post(self, request, card_type):
        if not request.user.is_authenticated:
            return redirect('admin-login')
        
        model_map = {
            'home': HomePage,
            'franchise': FranchisePage,
            'packages': PackagesPage,
            'contact': ContactPage
        }
        
        ModelClass = model_map.get(card_type)
        if not ModelClass:
             messages.error(request, 'Invalid card type.')
             return redirect('manage-content')

        obj, _ = ModelClass.objects.get_or_create(id=1)
        
        obj.title = request.POST.get('title')
        obj.description = request.POST.get('description')
        obj.media_type = request.POST.get('media_type')
        
        if request.FILES.get('file'):
            if obj.media_type == 'video':
                obj.video = request.FILES.get('file')
            else:
                obj.image = request.FILES.get('file')
        
        obj.save()
        messages.success(request, f'{obj._meta.verbose_name} updated successfully!')
            
        return redirect('manage-content')


class WarrantyClaims(View):
    def get(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        return render(request, 'dashboard/claims.html')

class AddProduct(View):
    @method_decorator(never_cache)
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('admin-login')
        
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        description = request.POST.get('description')
        images = request.FILES.getlist('images')
        features = request.POST.getlist('features')

        product = Product.objects.create(
            name=name,
            brand=brand,
            description=description
        )

        for image in images:
            ProductImage.objects.create(product=product, image=image)

        for feature in features:
            if feature.strip(): # Avoid empty features
                ProductFeature.objects.create(product=product, feature=feature)

        messages.success(request, 'Product added successfully!')
        return redirect('products')

class DeleteProduct(View):
    @method_decorator(never_cache)
    def post(self, request, product_id):
        if not request.user.is_authenticated:
            return redirect('admin-login')
        
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            messages.success(request, 'Product deleted successfully!')
        except Product.DoesNotExist:
            messages.error(request, 'Product not found.')
        
        return redirect('products')

class EditProduct(View):
    @method_decorator(never_cache)
    def post(self, request, product_id):
        if not request.user.is_authenticated:
            return redirect('admin-login')
        
        try:
            product = Product.objects.get(id=product_id)
            
            # Update basic info
            product.name = request.POST.get('name')
            product.brand = request.POST.get('brand')
            product.description = request.POST.get('description')
            product.save()

            # Handle Images (Append new ones)
            images = request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(product=product, image=image)

            # Handle Features (Replace all)
            features = request.POST.getlist('features')
            # Clear existing features
            product.features.all().delete()
            # Add new features
            for feature in features:
                if feature.strip():
                    ProductFeature.objects.create(product=product, feature=feature)

            # Handle Deleted Images
            deleted_images = request.POST.get('deleted_images', '')
            if deleted_images:
                deleted_ids = [id for id in deleted_images.split(',') if id.strip().isdigit()]
                if deleted_ids:
                    ProductImage.objects.filter(id__in=deleted_ids, product=product).delete()

            messages.success(request, 'Product updated successfully!')
        except Product.DoesNotExist:
            messages.error(request, 'Product not found.')
        
        return redirect('products')

# Create your views here.
class AdminLogin(View):
    @method_decorator(never_cache)
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'dashboard/login.html')
    
    @method_decorator(never_cache)
    def post(self, request):
        # Get form data
        username = request.POST.get('username') 
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is None:
            try:
                user_obj = CustomUser.objects.get(username=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                user = None
        
        if user is not None:
            if self.can_user_login(user):
                login(request, user)
            
                messages.success(request, 'Login successful!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Access denied. Only admin users are allowed to login.')
                return render(request, 'dashboard/login.html')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'dashboard/login.html')
    
    def can_user_login(self, user):
        if hasattr(user, 'is_superuser') and user.is_superuser:
            return True
            
        if hasattr(user, 'is_deleted') and user.is_deleted:
            return False
        
        if hasattr(user, 'role'):
            return user.role in ['admin', 'super_admin', 'dealer']
        
        return False
    

class AdminLogout(View):
    @method_decorator(never_cache)
    def get(self, request):
        logout(request)
        return redirect('admin-login')





class DealerList(View):
    def get(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        
        dealers = CustomUser.objects.filter(role='dealer', is_deleted=False).order_by('-date_joined')
        return render(request, 'dashboard/dealers.html', {'dealers': dealers})

class AddDealer(View):
    @method_decorator(never_cache)
    def post(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        
        full_name = request.POST.get('full_name')
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if CustomUser.objects.filter(username=email).exists():
            messages.error(request, 'User with this email already exists.')
            return redirect('dealers')
            
        try:
            user = CustomUser.objects.create_user(username=full_name, email=email, password=password)
            user.first_name = full_name 
            user.company_name = company_name
            user.role = 'dealer'
            user.save()
            messages.success(request, 'Dealer added successfully!')
        except Exception as e:
            messages.error(request, f'Error creating dealer: {str(e)}')
            
        return redirect('dealers')

class DeleteDealer(View):
    @method_decorator(never_cache)
    def post(self, request, dealer_id):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        
        try:
            dealer = CustomUser.objects.get(id=dealer_id, role='dealer')
            dealer.is_deleted = True
            dealer.save()
            messages.success(request, 'Dealer deleted successfully!')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Dealer not found.')
            
        return redirect('dealers')

class EditDealer(View):
    @method_decorator(never_cache)
    def post(self, request, dealer_id):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        
        try:
            dealer = CustomUser.objects.get(id=dealer_id, role='dealer')
            
            # Update info
            dealer.first_name = request.POST.get('full_name')
            dealer.company_name = request.POST.get('company_name')
            email = request.POST.get('email')
            
            # Check email uniqueness if changed
            if email != dealer.email and CustomUser.objects.filter(email=email).exists():
                 messages.error(request, 'Email already in use by another user.')
                 return redirect('dealers')
            
            dealer.email = email
            dealer.username = email # Keep username in sync with email
            dealer.save()

            messages.success(request, 'Dealer updated successfully!')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Dealer not found.')
            
        return redirect('dealers')




class HeroContent(View):
    def get(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        
        # Ensure singletons exist
        home_card, _ = HomePage.objects.get_or_create(id=1)
        franchise_card, _ = FranchisePage.objects.get_or_create(id=1)
        packages_card, _ = PackagesPage.objects.get_or_create(id=1)
        contact_card, _ = ContactPage.objects.get_or_create(id=1)

        # Prepare list for template with type identifier
        hero_cards = [
            {'type': 'home', 'obj': home_card, 'badge': 'Home Page'},
            {'type': 'franchise', 'obj': franchise_card, 'badge': 'Franchise Page'},
            {'type': 'packages', 'obj': packages_card, 'badge': 'Packages Page'},
            {'type': 'contact', 'obj': contact_card, 'badge': 'Contact Page'},
        ]
        
        return render(request, 'dashboard/hero_sections.html', {'hero_cards': hero_cards})

class WarrantyRegistrationList(View):
    def get(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        
        # Filter based on role
        if request.user.role == 'dealer':
            registrations = WarrantyRegistration.objects.filter(dealer=request.user).order_by('-created_at')
        else:
            registrations = WarrantyRegistration.objects.all().order_by('-created_at')
            
        products = Product.objects.all()
        return render(request, 'dashboard/warranty_registration.html', {
            'registrations': registrations,
            'products': products
        })

class AddWarrantyRegistration(View):
    @method_decorator(never_cache)
    def post(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        
        try:
            # Create object
            WarrantyRegistration.objects.create(
                dealer=request.user,
                product_id=request.POST.get('product'),
                serial_number=request.POST.get('serial_number'),
                application_type=request.POST.get('application_type'),
                customer_first_name=request.POST.get('first_name'),
                customer_last_name=request.POST.get('last_name'),
                customer_email=request.POST.get('email'),
                customer_phone=request.POST.get('phone'),
                installation_date=request.POST.get('installation_date'),
                chassis_number=request.POST.get('chassis_number'),
                vehicle_make_model=request.POST.get('vehicle_details'),
                proof_of_purchase=request.FILES.get('proof_of_purchase')
            )
            messages.success(request, 'Warranty registered successfully!')
        except Exception as e:
            messages.error(request, f'Error creating registration: {str(e)}')
            
        return redirect('warranty-registration')

class EditWarrantyRegistration(View):
    @method_decorator(never_cache)
    def post(self, request, reg_id):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        
        try:
            reg = WarrantyRegistration.objects.get(id=reg_id)
            # Ensure dealer can only edit their own
            if request.user.role == 'dealer' and reg.dealer != request.user:
                 messages.error(request, 'Permission denied.')
                 return redirect('warranty-registration')

            reg.product_id = request.POST.get('product')
            reg.serial_number = request.POST.get('serial_number')
            reg.application_type = request.POST.get('application_type')
            reg.customer_first_name = request.POST.get('first_name')
            reg.customer_last_name = request.POST.get('last_name')
            reg.customer_email = request.POST.get('email')
            reg.customer_phone = request.POST.get('phone')
            reg.installation_date = request.POST.get('installation_date')
            reg.chassis_number = request.POST.get('chassis_number')
            reg.vehicle_make_model = request.POST.get('vehicle_details')
            
            if request.FILES.get('proof_of_purchase'):
                reg.proof_of_purchase = request.FILES.get('proof_of_purchase')
                
            reg.save()
            messages.success(request, 'Registration updated successfully!')
        except WarrantyRegistration.DoesNotExist:
            messages.error(request, 'Registration not found.')
        except Exception as e:
            messages.error(request, f'Error updating: {str(e)}')
            
        return redirect('warranty-registration')

class DeleteWarrantyRegistration(View):
    @method_decorator(never_cache)
    def post(self, request, reg_id):
        if not request.user.is_authenticated:
             return redirect('admin-login')
             
        try:
            reg = WarrantyRegistration.objects.get(id=reg_id)
            if request.user.role == 'dealer' and reg.dealer != request.user:
                 messages.error(request, 'Permission denied.')
            else:
                reg.delete()
                messages.success(request, 'Registration deleted successfully!')
        except WarrantyRegistration.DoesNotExist:
             messages.error(request, 'Registration not found.')
             
        return redirect('warranty-registration')