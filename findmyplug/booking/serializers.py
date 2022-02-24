from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Slot, User,Vehicle,Station,Plug,Review,Booking,Payment

import re

email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class RegisterSerializer(serializers.ModelSerializer):
	password=serializers.CharField(max_length=32,min_length=8,write_only = True)
	
	class Meta:
		model = User
		fields = ['email','password','phone','pincode']
		
	def validate(self,attrs):
		email = attrs.get('email',' ')

		if not email_pattern.match(email):
			raise serializers.ValidationError('Please enter a valid email!')
		return attrs
		
	def create(self,validated_data):
            validated_data['is_active'] = False
            return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=32,min_length=8,write_only = True)
    
    class Meta:
        model = User
        fields = ['email','password']


class VehicleSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    registration_no = serializers.CharField(validators=[UniqueValidator(queryset=Vehicle.objects.all(),message="Vehicle already registered by a user!")])

    class Meta:
        model = Vehicle
        fields = '__all__'

class StationSerializer(serializers.ModelSerializer):

    star_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Station
        fields = '__all__'

    def get_star_rating(self,obj):
        star_rating = int(obj.star_rating)
        reviews = Review.objects.filter(about = obj)
        count = 1
        for review in reviews:
            star_rating += int(review.rating)
            count += 1
        return int(star_rating/count)


class ReviewSerializer(serializers.ModelSerializer):
    about = StationSerializer()
    class Meta:
        model = Review
        fields = '__all__'

class PlugSerializer(serializers.ModelSerializer):
    station_name = StationSerializer()
    class Meta:
        model = Plug
        fields = '__all__'

class SlotSerializer(serializers.ModelSerializer):
    plug = serializers.ReadOnlyField(source='plug.charger_type')
    
    class Meta:
        model = Slot
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    station = serializers.ReadOnlyField(source='station.station_name')
    plug = serializers.ReadOnlyField(source='plug.charger_type')
    slot = SlotSerializer()
    class Meta:
        model = Booking
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    booking_id = serializers.ReadOnlyField(source='booking_id.id')
    class Meta:
        model = Payment
        fields = '__all__'