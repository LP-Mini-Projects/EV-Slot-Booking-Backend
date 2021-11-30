from rest_framework import serializers
from .models import User,Vehicle,Station,Plug,Review,Booking,Payment

class RegisterSerializer(serializers.ModelSerializer):
	password=serializers.CharField(max_length=32,min_length=8,write_only = True)
	
	class Meta:
		model = User
		fields = '__all__'
		
	def validate(self,attrs):
		username = attrs.get('username',' ')
		if not username.isalnum():
			raise serializers.ValidationError('Username must be alphanumeric only')
		return attrs
		
	def create(self,validated_data):
		return User.objects.create_user(**validated_data)

class VehicleSerializer(serializers.ModelSerializer):
    pass

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