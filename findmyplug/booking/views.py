from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from .serializers import StationSerializer
from .models import Station
from rest_framework.response import Response
# Create your views here.
class TestView(mixins.ListModelMixin,GenericAPIView):
    serializer_class = StationSerializer
    queryset = Station.objects.all()
    
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
