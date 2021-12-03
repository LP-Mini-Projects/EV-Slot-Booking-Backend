from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.contrib.auth import authenticate,login

from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer,LoginSerializer

from rest_framework.response import Response

'''
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
'''


class RegisterAPI(GenericAPIView):
	
	serializer_class = RegisterSerializer
	
	def post(self,request,*args,**kwargs):
            data = request.data
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception = True)
            user = serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

            '''
            token = Token.objects.create(user=user)
		    current_site = get_current_site(request).domain
		    relative_link = reverse('email-verify')
		    link = 'http://'+current_site+relative_link+'?token='+ token.key
		    data = {'email_body': f'Use this link to get verified {link}. if you are seller then you need to get seller status then please mail your seller application. we will contact you regarding same.', 'subject':'Email Verification', 'to' : user.email}
		    Util.send_email(data)
		    '''

class LoginAPI(GenericAPIView):
	
	serializer_class = LoginSerializer
	
	def post(self,request,*args,**kwargs ):
		username = request.data.get('username',None)
		password = request.data.get('password',None)
		user = authenticate(username = username, password = password)
		if user :
			login(request,user)
			serializer = self.serializer_class(user)
			token,_ = Token.objects.get_or_create(user=user)
			return Response({'token' : token.key,'username' : user.username},status = status.HTTP_200_OK)
		return Response('Invalid Credentials',status = status.HTTP_404_NOT_FOUND)