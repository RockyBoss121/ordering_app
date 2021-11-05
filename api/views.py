from django.db.models.query import QuerySet
from django.http import request
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from rest_framework import filters
from rest_framework import generics
from .serializers import *
from rest_framework import status
import jwt
import datetime
from django.db.models import Q

# class RegisterViewset(viewsets.ModelViewSet):
#     parsers_classes=[MultiPartParser,FormParser, JSONParser]
#     queryset =User.objects.all()
#     serializer_class=RegisterSerializer

class RegisterViewset(viewsets.ViewSet):
    parsers_classes=[MultiPartParser,FormParser, JSONParser]
    serializer_class=RegisterSerializer
    def create(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()   
        return Response(serializer.data)

    def list(self,request):
        queryset = User.objects.all()
        serializers = RegisterSerializer(queryset,many=True)
        return Response({'status':200,'payload':serializers.data}) 

     
    # def post(self,request,pk):
    #     queryset = User.objects.get(pk=pk)
    #     serializer = RegisterSerializer(instance=queryset,date=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #     return Response(serializer.data)     

class LogiViewset(viewsets.ViewSet):
    serializer_class= LogSerializers
    def create(self,request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email,password=password)
        user=User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('user not found')
        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')
        payload={
            'id':user.id,
            'email':user.email,
            'fullname':user.fullname,
            'mobile_no':user.mobile_no,
            'gst_no':user.gst_no,
            'drug_lic_no':user.drug_lic_no,
            'tel_no':user.tel_no,
            'business_name':user.business_name,
            'business_address':user.business_address,
            'password':user.password,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        response = Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={
            'jwt':token,
            
        }
        return response 

# All product list view 
class ProductListView(viewsets.ViewSet):
    serializer_class=productSerializers
    def create(self,request):
        serializers=productSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
        return Response(serializers.data)

    def list(self,requset):
        queryset = ProductList.objects.all()
        serializers = productSerializers(queryset,many=True)
        return Response(serializers.data)        

# product list search per word and id
class ProductView(viewsets.ViewSet):
    def list(self,request):
        return Response([])

    def retrieve(self, request, pk=None):
        data=ProductList.objects.filter(Q(product_name__icontains=pk))
        serializer=productSerializers(data,many=True)
        return Response(serializer.data)      
       
# product order create

class OrderView(viewsets.ViewSet):
    serializer_class = OrderSerializers
    # permission_classes = [AllowAny]
    def create(self,request):
        print(request.data)
        data=request.data
        a=float(data['qty'])
        b=float(data['rate'])
        
        serializers = OrderSerializers(data=request.data)
        
        if serializers.is_valid():
            serializers.save(amount=a*b)
        return Response(serializers.data)

    def list(self,request):
       
        # token =authentication.get_authorization_header(request)
        # payload= jwt.decode(token, 'secret', algorithms='HS256')
        # user=payload['id']
        # print(user)
        # obj =Order.objects.filter(user_id=user)
        queryset = Order.objects.filter(is_order='False')
        serializers = OrderSerializers(queryset,many=True)
        return Response({"list":serializers.data}) 

    def destroy(self,request,pk):
        try:
            user = Order.objects.get(pk=pk)
            user.delete()  
            return Response("deleted")
        except:return Response({'msg':"result not found"})   

    def update(self,request,pk):
        quersyset = Order.objects.get(pk=pk)
        data=request.data
        a=float(data['qty'])
        b=float(data['rate'])
        serializer= OrderSerializers(instance=quersyset,data=request.data)
        if serializer.is_valid():
            serializer.save(amount=a*b)
        return Response({'message':'update reacord successfuly','list':serializer.data})      
   
# product Search per words
class ProductSearchView(generics.ListAPIView): 
    serializer_class = productSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['^product_name']

    def get_queryset(self):
        if self.request.query_params:    
            return ProductList.objects.all()
        return ProductList.objects.none()
             
# confirm oreder after search and create oreder 
class ConfirOrderViewSet(viewsets.ViewSet):
    def create(self, request):
        token =authentication.get_authorization_header(request)
        payload= jwt.decode(token, 'secret', algorithms='HS256')
        user=payload['id']
        print(user)
        a=request.data
        c=a['totalamount']
        d=a['totalqty']
        us =a['Users']
        serializers=ConfirmOrederSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save(total_amount=c,total_quantity=d,user_id=user)

        for i in us:
            a=i['id']
            # print(type(a))
            ur=Order.objects.get(id=a)
            ur.confirm_order_id=(ConfirmOrder.objects.last()).id
            ur.users_id=user
            ur.is_order=True
            ur.save()
        return Response({"message":"Your order is palced Successfully","list":serializers.data})
        
    def list(self,request):
        token =authentication.get_authorization_header(request)
        # print(token)
        if not token:
            raise AuthenticationFailed("unauthenticated user")
        try:
            payload= jwt.decode(token, 'secret', algorithms='HS256')

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("unauthenticated ")    
        user=payload['id']
        fullname=payload['fullname']
        # print(user)
        queryset = ConfirmOrder.objects.all()
        serializers = ConfirmOrederSerializers(queryset,many=True)
        return Response({'fullname':fullname,'list':serializers.data})

    # def put(self,request):
    #     queryset =       




# confirm oreder list after order
class ConfirmOrderListViewSet(viewsets.ViewSet):
    def list(self,request):
        token =authentication.get_authorization_header(request)
        print(token)
        if not token:
            raise AuthenticationFailed("unauthenticated user")
        try:
            payload= jwt.decode(token, 'secret', algorithms='HS256')

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("unauthenticated ")    
        user=payload['id']
        queryset = Order.objects.filter(users_id=user)
        serializers=OrderSerializers(queryset,many=True)
        return Response(serializers.data)

    # def put(self,request,pk):
    #     quersyset = Order.objects.get(pk=pk)
    #     data=request.data
    #     serializer= OrderSerializers(instance=quersyset,data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #     return Response({'message':'update reacord successfuly','list':serializer.data})  
# confirm order filter with product name and status        
class ConfirmOrderFilter(generics.ListAPIView):
   
    serializer_class = OrderSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['^product_name']

    def get_queryset(self):
        request=self.request
        token =authentication.get_authorization_header(request)
        print(token)
        if not token:
            raise AuthenticationFailed("unauthenticated user")
        try:
            payload= jwt.decode(token, 'secret', algorithms='HS256')

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("unauthenticated ")    
        user=payload['id']
        
        queryset = Order.objects.filter(users_id=user)
        if queryset:    
            return queryset
        return Order.objects.none()

# confim Datefilter find data between date
from django_filters import rest_framework as filters
from django_filters import FilterSet,DateFilter
from django_filters.rest_framework import DjangoFilterBackend

class ConfirmOrderDateFilter(filters.FilterSet):
    craete_date = filters.DateFilter(lookup_expr="gt")
    craete_date_gte = filters.DateFilter(field_name="craete_date",lookup_expr="lt")
    class Meta:
        model = Order
        fields = [
            "craete_date",
            'craete_date_gte',
           
        ]

class Confirm_dateListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConfirmOrderDateFilter
    
# All orderlist For admin
class ClientConfrimOrderlistView(viewsets.ViewSet):
    def list(self,request):
        payload={}
        queryset = Order.objects.filter(Q(is_order='True') & Q(status='PENDING'))
        serializers= OrderSerializers(queryset,many=True)
        return Response(serializers.data)


# class PendingOrder(viewsets.ViewSet):
#     def list(self,request):
#         queryset=Order.objects.filter(status='PENDING')
#         serializers = OrderSerializers(queryset,many=True)
#         return Response(serializers.data)


# class ApprovedOrder(viewsets.ViewSet):
#     def list(self,request):
#         queryset = Order.objects.filter(status='APPROVED')
#         serializers =OrderSerializers(queryset,many=True)
#         return Response(serializers.data)                

class AdminConfirmOrderlistView(viewsets.ViewSet):
      def list(self,request):
        queryset = Order.objects.filter(Q(status='APPROVED') & Q(is_order='True'))
        serializers =OrderSerializers(queryset,many=True)
        return Response(serializers.data)  


class AdminCancleOrderListView(viewsets.ViewSet):
    def list(self,request):
        queryset = Order.objects.filter(Q(status='CENCLE') & Q(is_order='True'))
        serializers= OrderSerializers(queryset,many=True)
        return Response(serializers.data)

# admin see all list
class AdminAllListView(viewsets.ViewSet):

    def list(self,request):
        token =authentication.get_authorization_header(request)
        # print(token)
        if not token:
            raise AuthenticationFailed("unauthenticated user")
        try:
            payload= jwt.decode(token, 'secret', algorithms='HS256')

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("unauthenticated ")    
        user=payload['id']
        queryset = Order.objects.filter(users_id=user)
        serializers=OrderSerializers(queryset,many=True)
        return Response(serializers.data)


    def update(self,request,pk):
        quersyset = Order.objects.get(pk=pk)
        data=request.data
        print(data)
        serializer= OrderSerializers(instance=quersyset,data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'message':'update reacord successfuly','list':serializer.data})  

   


# change password view
class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer





