from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, Product,HomeBannerSlide,AdvantageBanner, ProductBanner, ProductImage, ProductFeature, WarrantyRegistration,AboutBanner, SiriusBanner, DaxDetailingBanner, DaxSolutionsBanner, WarrantyClaim

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


class HeroSectionsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')

        # Ensure single-instance models exist
        product_banner, _ = ProductBanner.objects.get_or_create(id=1)
        about_banner, _ = AboutBanner.objects.get_or_create(id=1)
        sirius_banner, _ = SiriusBanner.objects.get_or_create(id=1)
        dax_detailing_banner, _ = DaxDetailingBanner.objects.get_or_create(id=1)
        dax_solutions_banner, _ = DaxSolutionsBanner.objects.get_or_create(id=1)
        advantage_banner, _ = AdvantageBanner.objects.get_or_create(id=1)

        # Build cards list
        # We need to manually construct the "Home" card object since it's a collection of slides
        # We'll use the first active slide for preview
        first_slide = HomeBannerSlide.objects.filter(is_active=True).first()
        
        home_obj = {
            'title': 'Home Page Banners',
            'description': 'Manage the rotating banner slides for the home page.',
            'media_type': 'image',
            'image': first_slide.image if first_slide else None,
            'is_virtual': True # Flag to distinguish in template
        }

        hero_cards = [
            {'type': 'home', 'badge': 'Home Page', 'obj': home_obj},
            {'type': 'product_banner', 'badge': 'Product Banner', 'obj': product_banner},
            {'type': 'about_banner', 'badge': 'About Banner', 'obj': about_banner},
            {'type': 'sirius_banner', 'badge': 'Sirius PPF', 'obj': sirius_banner},
            {'type': 'dax_detailing_banner', 'badge': 'Dax Detailing', 'obj': dax_detailing_banner},
            {'type': 'dax_solutions_banner', 'badge': 'Dax Solutions', 'obj': dax_solutions_banner},
            {'type': 'advantage_banner', 'badge': 'Advantage Banner', 'obj': advantage_banner},
        ]

        return render(request, 'dashboard/hero_sections.html', {'hero_cards': hero_cards})

class HomeBannerListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        slides = HomeBannerSlide.objects.all().order_by('display_order', '-created_at')
        return render(request, 'dashboard/home_banner_slides.html', {'slides': slides})

class AddHomeBannerSlide(View):
    @method_decorator(never_cache)
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('admin-login')
        
        try:
            HomeBannerSlide.objects.create(
                title1=request.POST.get('title1'),
                title2=request.POST.get('title2'),
                description=request.POST.get('description'),
                image=request.FILES.get('image'),
                link=request.POST.get('link'),
                display_order=request.POST.get('display_order', 0),
                is_active=request.POST.get('is_active') == 'on'
            )
            messages.success(request, 'Banner slide added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding slide: {str(e)}')
            
        return redirect('home-banner-list')

class EditHomeBannerSlide(View):
    @method_decorator(never_cache)
    def post(self, request, slide_id):
        if not request.user.is_authenticated:
            return redirect('admin-login')
        
        try:
            slide = HomeBannerSlide.objects.get(id=slide_id)
            slide.title1 = request.POST.get('title1')
            slide.title2 = request.POST.get('title2')
            slide.description = request.POST.get('description')
            slide.link = request.POST.get('link')
            slide.display_order = request.POST.get('display_order', 0)
            slide.is_active = request.POST.get('is_active') == 'on'
            
            if request.FILES.get('image'):
                slide.image = request.FILES.get('image')
                
            slide.save()
            messages.success(request, 'Banner slide updated successfully!')
        except HomeBannerSlide.DoesNotExist:
            messages.error(request, 'Slide not found.')
        except Exception as e:
            messages.error(request, f'Error updating slide: {str(e)}')
            
        return redirect('home-banner-list')

class DeleteHomeBannerSlide(View):
    @method_decorator(never_cache)
    def post(self, request, slide_id):
        if not request.user.is_authenticated:
            return redirect('admin-login')
        
        try:
            slide = HomeBannerSlide.objects.get(id=slide_id)
            slide.delete()
            messages.success(request, 'Banner slide deleted successfully!')
        except HomeBannerSlide.DoesNotExist:
             messages.error(request, 'Slide not found.')
             
        return redirect('home-banner-list')

class EditProductBanner(View):
    @method_decorator(never_cache)
    def post(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        
        try:
            banner, _ = ProductBanner.objects.get_or_create(id=1)
            
            banner.title = request.POST.get('title')
            banner.description = request.POST.get('description')
            
            if request.FILES.get('file'):
                banner.image = request.FILES.get('file')
                
            banner.save()
            messages.success(request, 'Product Banner updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating banner: {str(e)}')
            
        return redirect('hero-sections')


class EditAboutBanner(View):
    @method_decorator(never_cache)
    def post(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        
        try:
            banner, _ = AboutBanner.objects.get_or_create(id=1)
            
            banner.title = request.POST.get('title')
            banner.description = request.POST.get('description')
            
            if request.FILES.get('file'):
                banner.image = request.FILES.get('file')
                
            banner.save()
            messages.success(request, 'About Banner updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating banner: {str(e)}')
            
        return redirect('hero-sections')

class EditSiriusBanner(View):
    @method_decorator(never_cache)
    def post(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        
        try:
            banner, _ = SiriusBanner.objects.get_or_create(id=1)
            
            banner.title = request.POST.get('title')
            banner.description = request.POST.get('description')
            
            if request.FILES.get('file'):
                banner.image = request.FILES.get('file')
                
            banner.save()
            messages.success(request, 'Sirius Banner updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating banner: {str(e)}')
            
        return redirect('hero-sections')

class EditDaxDetailingBanner(View):
    @method_decorator(never_cache)
    def post(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        
        try:
            banner, _ = DaxDetailingBanner.objects.get_or_create(id=1)
            
            banner.title = request.POST.get('title')
            banner.description = request.POST.get('description')
            
            if request.FILES.get('file'):
                banner.image = request.FILES.get('file')
                
            banner.save()
            messages.success(request, 'Dax Detailing Banner updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating banner: {str(e)}')
            
        return redirect('hero-sections')

class EditDaxSolutionsBanner(View):
    @method_decorator(never_cache)
    def post(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        
        try:
            banner, _ = DaxSolutionsBanner.objects.get_or_create(id=1)
            
            banner.title = request.POST.get('title')
            banner.description = request.POST.get('description')
            
            if request.FILES.get('file'):
                banner.image = request.FILES.get('file')
                
            banner.save()
            messages.success(request, 'Dax Solutions Banner updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating banner: {str(e)}')
            
        return redirect('hero-sections')


class EditAdvantageBanner(View):
    @method_decorator(never_cache)
    def post(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        
        try:
            banner, _ = AdvantageBanner.objects.get_or_create(id=1)
            
            banner.title = request.POST.get('title')
            banner.description = request.POST.get('description')
            
            if request.FILES.get('file'):
                banner.image = request.FILES.get('file')
                
            banner.save()
            messages.success(request, 'Advantage Banner updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating banner: {str(e)}')
            
        return redirect('hero-sections')


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



















class WarrantyRegistrationList(View):
    def get(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        
        # Filter based on role
        if request.user.role == 'dealer':
            registrations = WarrantyRegistration.objects.filter(dealer_user=request.user).order_by('-created_at')
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
            # Prepare dealer info
            dealer_data = {}
            if request.user.role == 'dealer':
                dealer_data = {
                    'dealer_user': request.user,
                    'dealer_name': request.user.first_name or '',
                    'dealer_email': request.user.email or '',
                    'dealer_company_name': request.user.company_name or '',
                    # Defaults
                    'dealer_phone': '',
                    'dealer_address': '',
                    'dealer_city': '',
                    'dealer_state': '',
                    'dealer_zip': '',
                    'dealer_country': ''
                }
                
                # Check for previous registration to copy address/phone details
                last_warranty = WarrantyRegistration.objects.filter(dealer_user=request.user).order_by('-created_at').first()
                if last_warranty:
                     dealer_data['dealer_phone'] = last_warranty.dealer_phone
                     dealer_data['dealer_address'] = last_warranty.dealer_address
                     dealer_data['dealer_city'] = last_warranty.dealer_city
                     dealer_data['dealer_state'] = last_warranty.dealer_state
                     dealer_data['dealer_zip'] = last_warranty.dealer_zip
                     dealer_data['dealer_country'] = last_warranty.dealer_country

            # Create object
            warranty = WarrantyRegistration.objects.create(
                **dealer_data,
                serial_number=request.POST.get('serial_number'),
                customer_first_name=request.POST.get('first_name'),
                customer_last_name=request.POST.get('last_name'),
                customer_email=request.POST.get('email'),
                customer_phone=request.POST.get('phone'),
                installation_date=request.POST.get('installation_date'),
                chassis_number=request.POST.get('chassis_number'),
                vehicle_make_model=request.POST.get('vehicle_details'),
                proof_of_purchase=request.FILES.get('proof_of_purchase')
            )

            # Create Product Items
            product_names = request.POST.getlist('product[]')
            app_types = request.POST.getlist('application_type[]')

            if product_names:
                from .models import WarrantyProductItem
                for p_name, a_type in zip(product_names, app_types):
                    if p_name.strip(): # Ensure product name is not empty
                        WarrantyProductItem.objects.create(
                            warranty=warranty,
                            product=p_name,
                            application_type=a_type
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
            if request.user.role == 'dealer' and reg.dealer_user != request.user:
                 messages.error(request, 'Permission denied.')
                 return redirect('warranty-registration')

            # reg.product_id = request.POST.get('product') # Removed
            reg.serial_number = request.POST.get('serial_number')
            # reg.application_type = request.POST.get('application_type') # Removed
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

            # Update Product Info
            from .models import WarrantyProductItem
            
            # Clear existing items
            reg.items.all().delete()
            
            # Get lists from form
            product_names = request.POST.getlist('product[]')
            app_types = request.POST.getlist('application_type[]')
            
            # Iterate and create
            # use zip to pair them up. If lengths mismatch, it stops at shortest, which is safer than index errors
            for p_name, a_type in zip(product_names, app_types):
                if p_name.strip(): # Ensure product name is not empty
                    WarrantyProductItem.objects.create(
                        warranty=reg,
                        product=p_name.strip(),
                        application_type=a_type.strip()
                    )
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
            if request.user.role == 'dealer' and reg.dealer_user != request.user:
                 messages.error(request, 'Permission denied.')
            else:
                reg.delete()
                messages.success(request, 'Registration deleted successfully!')
        except WarrantyRegistration.DoesNotExist:
             messages.error(request, 'Registration not found.')
             
        return redirect('warranty-registration')

class ChangeDealerPassword(View):
    @method_decorator(never_cache)
    def post(self, request, user_id):
        if not request.user.is_authenticated:
            return redirect('admin-login')
        
        try:
            user_to_change = CustomUser.objects.get(id=user_id)
            
            # Authorization check
            if request.user.role not in ['admin', 'super_admin'] and request.user != user_to_change:
                 messages.error(request, 'Permission denied.')
                 return redirect('warranty-registration')

            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if new_password and confirm_password:
                if new_password == confirm_password:
                     user_to_change.set_password(new_password)
                     user_to_change.save()
                     messages.success(request, 'Password updated successfully!')
                else:
                    messages.error(request, 'Passwords do not match.')
            else:
                 messages.error(request, 'Please provide both password fields.')
                 
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found.')
            
        return redirect('warranty-registration')

class WarrantyClaimListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
             return redirect('admin-login')
        
        # Filter based on role
        if request.user.role == 'dealer':
            # Dealers can see claims for warranties they registered? 
            # Or should they only see claims they submitted?
            # Assuming claims linked to warranties they created.
            claims = WarrantyClaim.objects.filter(warranty__dealer_user=request.user).order_by('-created_at')
        else:
            claims = WarrantyClaim.objects.all().order_by('-created_at')
            
        return render(request, 'dashboard/warranty_claims_list.html', {'claims': claims})

    def post(self, request, claim_id=None):
        # Handle status update (Approve/Reject)
        if not request.user.is_authenticated:
             return redirect('admin-login')
             
        if claim_id:
             try:
                 claim = WarrantyClaim.objects.get(id=claim_id)
                 new_status = request.POST.get('status')
                 if new_status in ['pending', 'approved', 'rejected']:
                     claim.status = new_status
                     claim.save()
                     messages.success(request, f'Claim status updated to {new_status}.')
                 else:
                     messages.error(request, 'Invalid status.')
             except WarrantyClaim.DoesNotExist:
                 messages.error(request, 'Claim not found.')
                 
        return redirect('warranty-claims-list')