from django.db import transaction
from rest_framework import serializers
from core.models import *
from django.contrib.auth.password_validation import validate_password
from drf_extra_fields.fields import Base64ImageField
from account.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class MarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Marka
        fields = '__all__'



class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = '__all__'
    


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions')


class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Token
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = Region
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class DetailCitySerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    class Meta:
        model = City
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class DetailRegionSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = Region
        fields = '__all__'



class LooksLikesCarSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarLookLike
        fields = '__all__'


class InteriorsCarSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarInterior
        fields = '__all__'
    

class SecutitiesCarSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarSecurity
        fields = '__all__'


class OptionsCarSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarOptipon
        fields = '__all__'


class MadelSerializer(serializers.ModelSerializer):
    marka = MarkSerializer()
    class Meta:
        model = Madel
        fields = '__all__'


class DetailMadelSerializer(serializers.ModelSerializer):
    marka = MarkSerializer()
    class Meta:
        model = Madel
        fields = '__all__'


class DetailGenerationsSerializer(serializers.ModelSerializer):
    madel = MadelSerializer()
    class Meta:
        model = Generations
        fields = '__all__'


class GenerationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generations
        fields = '__all__'



class CarSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(child=Base64ImageField(), required=False)   
    class Meta:
        model = Car
        exclude = ('user',)

    def update(self, instance, validated_data):
        images = validated_data.pop('images', [])
        car = super().update(instance, validated_data)
        for image in images:
            image_name = image.name
            image_file = image

            car_image = CarImage.objects.create(car=car)
            car_image.image.save(image_name, image_file)
        return car
    

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = '__all__'
    


class ListCarSerializer(serializers.ModelSerializer):
    registration = CountrySerializer()
    region = RegionSerializer()
    generation = DetailGenerationsSerializer()
    city = CitySerializer()
    color = ColorSerializer()
    madel = DetailMadelSerializer()
    user = UserSerializer()
    images = CarImageSerializer(many=True)
    look_likes = LooksLikesCarSerializer(many=True)
    interiors = InteriorsCarSerializer(many=True)
    securities = SecutitiesCarSerializer(many=True)
    options = OptionsCarSerializer(many=True)


    class Meta:
        model = Car
        exclude = ('content',)



class DetailCarSerializer(serializers.ModelSerializer):
    registration = CountrySerializer()
    region = RegionSerializer()
    generation = DetailGenerationsSerializer()
    city = CitySerializer()
    color = ColorSerializer()
    madel = MadelSerializer()
    user = UserSerializer()
    images = CarImageSerializer(many=True)
    look_likes = LooksLikesCarSerializer(many=True)
    interiors = InteriorsCarSerializer(many=True)
    securities = SecutitiesCarSerializer(many=True)
    options = OptionsCarSerializer(many=True)

    class Meta:
        model = Car
        fields = '__all__'




class CreateCarSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(child=Base64ImageField(), required=False)   

    class Meta:
        model = Car
        fields = '__all__'

    @transaction.atomic()
    def create(self, validated_data):
        images = validated_data.pop('images', [])
        car = super().create(validated_data)

        
        for image in images:
            image_name = image.name
            image_file = image

            car_image = CarImage.objects.create(car=car)
            car_image.image.save(image_name, image_file)

        return car
    

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'password', 'is_superuser', 'groups', 'user_permissions')

    # def to_representation(self, instance):
    #     # instance in self.context['request'].user.favorite_products.all()
    #     ret = super().to_representation(instance)
    #     ret['is_admin'] = instance.is_superuser 
    #     return ret






class RegisterSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()  # Используем Base64ImageField вместо ListSerializer
    password1 = serializers.CharField(validators=[validate_password])
    password2 = serializers.CharField()

    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'password', 'is_superuser', 'groups', 'user_permissions',)

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        
        if password1 != password2:
            raise serializers.ValidationError({
                'password2': ['Пароли не совпадают!']
            })

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        validated_data['password'] = make_password(password)

        return super().create(validated_data)
