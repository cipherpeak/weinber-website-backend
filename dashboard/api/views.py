from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import json
from rest_framework.parsers import MultiPartParser, FormParser
from dashboard.models import Product, HomeBannerSlide, ProductBanner,AboutBanner, SiriusBanner, DaxDetailingBanner, DaxSolutionsBanner,AdvantageBanner, WarrantyRegistration, CustomUser
from .serializers import ProductSerializer, BannerSlideSerializer, ProductBannerSerializer,AboutBannerSerializer, SiriusBannerSerializer, DaxDetailingBannerSerializer, DaxSolutionsBannerSerializer,AdvantageBannerSerializer, WarrantyRegistrationSerializer

class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class HomeBannerAPIView(APIView):

    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        try:
            slides = HomeBannerSlide.objects.filter(
                is_active=True
            ).order_by('display_order')[:5]  
            
            if not slides.exists():
                return Response({
                    'message': 'No active banner slides found',
                    'slides': []
                }, status=status.HTTP_200_OK)
            
            # Serialize data
            serializer = BannerSlideSerializer(
                slides, 
                many=True,
                context={'request': request}
            )
            
            return Response({
                'success': True,
                'count': len(serializer.data),
                'slides': serializer.data
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductBannerAPIView(APIView):

    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        try:
            # Get the single product banner (ID=1 as established in views.py)
            banner = ProductBanner.objects.first()
            
            if not banner:
                return Response({
                    'message': 'No product banner found',
                    'data': None
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Serialize data
            serializer = ProductBannerSerializer(
                banner, 
                context={'request': request}
            )
            
            return Response({
                'success': True,
                'data': serializer.data
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AboutBannerAPIView(APIView):

    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        try:
            # Get the single product banner (ID=1 as established in views.py)
            banner = AboutBanner.objects.first()
            
            if not banner:
                return Response({
                    'message': 'No product banner found',
                    'data': None
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Serialize data
            serializer = AboutBannerSerializer(
                banner, 
                context={'request': request}
            )
            
            return Response({
                'success': True,
                'data': serializer.data
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SiriusBannerAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        try:
            banner = SiriusBanner.objects.first()
            if not banner:
                return Response({'message': 'No banner found', 'data': None}, status=status.HTTP_404_NOT_FOUND)
            serializer = SiriusBannerSerializer(banner, context={'request': request})
            return Response({'success': True, 'data': serializer.data})
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DaxDetailingBannerAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        try:
            banner = DaxDetailingBanner.objects.first()
            if not banner:
                return Response({'message': 'No banner found', 'data': None}, status=status.HTTP_404_NOT_FOUND)
            serializer = DaxDetailingBannerSerializer(banner, context={'request': request})
            return Response({'success': True, 'data': serializer.data})
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DaxSolutionsBannerAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        try:
            banner = DaxSolutionsBanner.objects.first()
            if not banner:
                return Response({'message': 'No banner found', 'data': None}, status=status.HTTP_404_NOT_FOUND)
            serializer = DaxSolutionsBannerSerializer(banner, context={'request': request})
            return Response({'success': True, 'data': serializer.data})
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AdvantageBannerAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        try:
            banner = AdvantageBanner.objects.first()
            if not banner:
                return Response({'message': 'No banner found', 'data': None}, status=status.HTTP_404_NOT_FOUND)
            serializer = AdvantageBannerSerializer(banner, context={'request': request})
            return Response({'success': True, 'data': serializer.data})
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








from rest_framework import generics, status
from rest_framework.response import Response
import json

class WarrantyRegistrationCreateAPIView(generics.CreateAPIView):
    queryset = WarrantyRegistration.objects.all()
    serializer_class = WarrantyRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            # Parse the request data
            data = request.data
            
            # Transform frontend data structure to match serializer
            transformed_data = {
                'serial_number': data.get('serialNumber', ''),
                'products': data.get('products', []),
                'customer_first_name': data.get('firstName', ''),
                'customer_last_name': data.get('lastName', ''),
                'customer_email': data.get('email', ''),
                'customer_phone': data.get('phone', ''),
                'installation_date': data.get('installationDate', ''),
                'chassis_number': data.get('chassisNo', ''),
                'vehicle_make_model': data.get('vehicleModel', ''),
                'proof_of_purchase': data.get('invoiceFile', ''),  # Base64 string from frontend
                'dealer_company_name': data.get('companyName', ''),
                'dealer_name': data.get('dealerName', ''),
                'dealer_email': data.get('dealerEmail', ''),
                'dealer_phone': data.get('dealerPhone', ''),
                'dealer_address': data.get('dealerAddress', ''),
                'dealer_city': data.get('dealerCity', ''),
                'dealer_state': data.get('dealerState', ''),
                'dealer_zip': data.get('dealerZip', ''),
                'dealer_country': data.get('dealerCountry', ''),
            }
            
            # Check for existing user or create a new one
            dealer_email = transformed_data.get('dealer_email')
            dealer_user = None
            
            if dealer_email:
                dealer_user = CustomUser.objects.filter(email=dealer_email).first()
                
                if not dealer_user:
                    try:
                        # Create new dealer user
                        # Using email as username to ensure uniqueness
                        dealer_user = CustomUser.objects.create_user(
                            username=transformed_data.get('dealer_name', ''),
                            email=dealer_email,
                            role='dealer',
                            company_name=transformed_data.get('dealer_company_name', ''),
                            first_name=transformed_data.get('dealer_name', '')
                        )
                        dealer_user.set_unusable_password()
                        dealer_user.save()
                    except Exception as user_error:
                        # Log error but continue with warranty registration
                        print(f"Error creating dealer user: {str(user_error)}")
                        dealer_user = None

            # Validate and save
            serializer = self.get_serializer(data=transformed_data)
            serializer.is_valid(raise_exception=True)
            
            # Save with dealer_user if available
            if dealer_user:
                warranty = serializer.save(dealer_user=dealer_user)
            else:
                warranty = serializer.save()
            

            
            # Return success response
            return Response({
                'success': True,
                'message': 'Warranty registration successful!',
                'warranty_id': warranty.id,
                'customer_email': warranty.customer_email
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    

from .serializers import WarrantyClaimSerializer

class WarrantyClaimCreateAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = WarrantyClaimSerializer(data=request.data)
        if serializer.is_valid():
            claim = serializer.save()
            return Response({
                "success": True,
                "message": "Warranty claim submitted successfully",
                "id": claim.id
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": "Validation error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)