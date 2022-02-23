import datetime
from rest_framework.generics import GenericAPIView
from rest_framework import status,permissions,viewsets
from django.contrib.auth import authenticate,login

from rest_framework.authtoken.models import Token

from .models import Booking, Plug, Station, User, Vehicle, Slot
from .serializers import RegisterSerializer,LoginSerializer, StationSerializer,VehicleSerializer, BookingSerializer
from .Utils import Util

from rest_framework.response import Response

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

class RegisterAPI(GenericAPIView):
	
	serializer_class = RegisterSerializer
	
	def post(self,request,*args,**kwargs):
		data = request.data
		serializer = self.serializer_class(data=data)
		serializer.is_valid(raise_exception = True)
		user = serializer.save()
		token = Token.objects.create(user=user)
		current_site = get_current_site(request).domain
		relative_link = reverse('email-verify')
		link = 'http://'+current_site+relative_link+'?token='+ token.key
		data = {'email_body': f'Use this link to get verified {link}.', 'subject':'Email Verification', 'to' : user.email}
		Util.send_email(data)
		return Response({'Success':'Your account is successfully created,please check your mail for verification.'},status=status.HTTP_201_CREATED)

class LoginAPI(GenericAPIView):
	
	serializer_class = LoginSerializer
	
	def post(self,request,*args,**kwargs ):
		email = request.data.get('email',None)
		password = request.data.get('password',None)
		user = authenticate(email = email, password = password)
		if user :
			login(request,user)
			serializer = self.serializer_class(user)
			token = Token.objects.get(user=user)
			return Response({'token' : token.key,'email' : user.email},status = status.HTTP_200_OK)
		return Response('Invalid Credentials',status = status.HTTP_404_NOT_FOUND)

class EmailVerify(GenericAPIView):
	def get(self,request):
		token = request.GET.get('token')
		user = User.objects.get(auth_token = token)
		if not user.is_active:
			user.is_active = True
			user.save()
		return Response('Account Verified', status=status.HTTP_200_OK)

class VehicleDetails(viewsets.ModelViewSet):
	queryset = Vehicle.objects.all()
	serializer_class = VehicleSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Vehicle.objects.filter(owner=self.request.user)
	
	def perform_create(self,serializer):
		serializer.save(owner = self.request.user)
	
	def update(self, request, *args, **kwargs):
		kwargs['partial'] = True
		return super().update(request, *args, **kwargs)

class SlotAPI(GenericAPIView):
	queryset = Booking.objects.all()
	serializer_class = BookingSerializer
	permission_classes = [permissions.IsAuthenticated]
	
	def get(self):
		return Booking.objects.filter(owner=self.request.user)
	
	def post(self,request):
		owner = self.request.user
		date = self.request.data['date']
		duration = int(self.request.data['duration'])
		capacity = self.request.data['capacity']
		plug_id = self.request.data['plug']
		plug = Plug.objects.get(id=plug_id)
		station = Station.objects.get(id = plug.station_name.id)
		time = datetime.time(0,0,0,0)
		slot_list = []
		str = ''
		count = 0
		while(time <= datetime.time(23,0,0,0)):
			if count==duration:
					count = 0
					str += f'{time}'
					slot_list.append(str)
			try:
				slot = Slot.objects.get(date = date, start_time = time)
				time = slot.end_time
				str = ''
				count = 0
			except:
				if count == 0:
					str = f'{time}' + '-'
				hr = time.hour
				if hr != 23:
					time = datetime.time(hr+1,0,0,0)
					count += 1
				else:
					break
		return Response({'slots':f'{slot_list}'})	

		'''date = self.request.data['date']
		starttime = self.request.data['start_time']
		endtime = self.request.data['end_time']
		booking,k = Booking.objects.get_or_create(station = station,plug = plug,date = date,start_time = starttime,end_time = endtime)
		booking.owner = owner
		booking.save()
		print(k)
		serializer.save(owner = self.request.user,plug = plug, station = station)
		plug.booking_status = True
		plug.save()'''

class StationAPI(viewsets.ModelViewSet):
	queryset = Station.objects.all()
	serializer_class = StationSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		owner = self.request.user
		vehicle = Vehicle.objects.get(owner = owner)
		plug = Plug.objects.filter(charger_type = vehicle.plug_type)
		return Station.objects.filter(id__in = plug)