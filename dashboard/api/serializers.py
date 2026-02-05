from rest_framework import serializers
from dashboard.models import Product, ProductImage, ProductFeature, HomeBannerSlide, ProductBanner,AboutBanner, SiriusBanner, DaxDetailingBanner, DaxSolutionsBanner,AdvantageBanner, WarrantyRegistration, WarrantyProductItem, WarrantyClaim, WarrantyClaimImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ['id', 'feature']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    features = ProductFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'description', 'created_at', 'images', 'features']





class BannerSlideSerializer(serializers.ModelSerializer):
    """Serializer for banner slides"""
    
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = HomeBannerSlide
        fields = [
            'id',
            'title1',
            'title2',
            'description',
            'image',
            'image_url',
            'link',
            'display_order',
            'is_active',
            'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_image_url(self, obj):
        """Get absolute image URL"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class ProductBannerSerializer(serializers.ModelSerializer):
    """Serializer for single product banner"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductBanner
        fields = ['id', 'title', 'description', 'image_url', 'updated_at']
        
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None



class AboutBannerSerializer(serializers.ModelSerializer):
    """Serializer for single product banner"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = AboutBanner
        fields = ['id', 'title', 'description', 'image_url', 'updated_at']
        
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class SiriusBannerSerializer(serializers.ModelSerializer):
    """Serializer for single sirius banner"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = SiriusBanner
        fields = ['id', 'title', 'description', 'image_url', 'updated_at']
        
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class DaxDetailingBannerSerializer(serializers.ModelSerializer):
    """Serializer for single dax detailing banner"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = DaxDetailingBanner
        fields = ['id', 'title', 'description', 'image_url', 'updated_at']
        
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class DaxSolutionsBannerSerializer(serializers.ModelSerializer):
    """Serializer for single dax solutions banner"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = DaxSolutionsBanner
        fields = ['id', 'title', 'description', 'image_url', 'updated_at']
        
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class AdvantageBannerSerializer(serializers.ModelSerializer):
    """Serializer for single advantage banner"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = AdvantageBanner
        fields = ['id', 'title', 'description', 'image_url', 'updated_at']
        
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

        return None






import base64
from django.core.files.base import ContentFile

class WarrantyProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarrantyProductItem
        fields = ['product', 'application_type']

class WarrantyRegistrationSerializer(serializers.ModelSerializer):
    # For handling multiple products
    products = WarrantyProductItemSerializer(many=True, write_only=True)
    
    # Handle file upload as base64 from frontend
    proof_of_purchase = serializers.CharField(write_only=True)
    
    class Meta:
        model = WarrantyRegistration
        fields = [
            'serial_number',
            'products',
            'customer_first_name',
            'customer_last_name',
            'customer_email',
            'customer_phone',
            'installation_date',
            'chassis_number',
            'vehicle_make_model',
            'proof_of_purchase',
            'dealer_company_name',
            'dealer_name',
            'dealer_email',
            'dealer_phone',
            'dealer_address',
            'dealer_city',
            'dealer_state',
            'dealer_zip',
            'dealer_country',
        ]
        extra_kwargs = {
            'dealer_company_name': {'required': False, 'allow_blank': True},
            'dealer_name': {'required': False, 'allow_blank': True},
            'dealer_email': {'required': False, 'allow_blank': True},
            'dealer_phone': {'required': False, 'allow_blank': True},
            'dealer_address': {'required': False, 'allow_blank': True},
            'dealer_city': {'required': False, 'allow_blank': True},
            'dealer_state': {'required': False, 'allow_blank': True},
            'dealer_zip': {'required': False, 'allow_blank': True},
            'dealer_country': {'required': False, 'allow_blank': True},
        }
    
    def create(self, validated_data):
        # Extract products data
        products_data = validated_data.pop('products')
        
        # Handle base64 file upload
        proof_of_purchase_data = validated_data.pop('proof_of_purchase')
        
        if proof_of_purchase_data:
            # Decode base64 string
            format, imgstr = proof_of_purchase_data.split(';base64,')
            ext = format.split('/')[-1]
            
            # Create file name
            import uuid
            file_name = f"{uuid.uuid4()}.{ext}"
            
            # Create ContentFile from decoded data
            data = ContentFile(base64.b64decode(imgstr), name=file_name)
            validated_data['proof_of_purchase'] = data
        
        # Create warranty registration
        warranty = WarrantyRegistration.objects.create(**validated_data)
        
        # Create product items
        for product_data in products_data:
            WarrantyProductItem.objects.create(
                warranty=warranty,
                **product_data
            )
        
        return warranty


class WarrantyClaimImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarrantyClaimImage
        fields = ['id', 'image', 'created_at']


class WarrantyClaimSerializer(serializers.ModelSerializer):
    serial_number = serializers.CharField(write_only=True)
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    uploaded_images = WarrantyClaimImageSerializer(source='images', many=True, read_only=True)
    
    class Meta:
        model = WarrantyClaim
        fields = [
            'id', 
            'serial_number', 
            'issue_date', 
            'issue_description', 
            'warranty_card_image', 
            'images',
            'uploaded_images',
            'status', 
            'created_at'
        ]
        read_only_fields = ['status', 'created_at']

    def validate_serial_number(self, value):
        try:
            registration = WarrantyRegistration.objects.get(serial_number=value)
            return registration
        except WarrantyRegistration.DoesNotExist:
            raise serializers.ValidationError("Invalid serial number. No warranty found.")

    def create(self, validated_data):
        registration = validated_data.pop('serial_number')
        images_data = validated_data.pop('images', [])
        
        claim = WarrantyClaim.objects.create(warranty=registration, **validated_data)
        
        for image in images_data:
            WarrantyClaimImage.objects.create(claim=claim, image=image)
            
        return claim