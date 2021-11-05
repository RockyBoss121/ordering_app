from rest_framework import serializers
from rest_framework import validators
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from .models import *

class RegisterSerializer(serializers.ModelSerializer):
    # date_joined = serializers.DateTimeField(
    #     format='%Y-%m-%d', input_formats=None)
    # last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
   
    class Meta:
        model =User
        fields = ('id','fullname','mobile_no','gst_no','drug_lic_no','email','tel_no',
                 'business_name','business_logo','business_address','password')

        extra_kwargs={
            'write_only':True
        } 

    def create(self,validated_data):
        password=validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance   
   
class LogSerializers(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()  

# product Search Serializers    

class productSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductList
        fields = ('__all__')

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model =Order
        fields = ('id','product_name','product_type','manufacturer','hsncode','pack',
                  'scm1','scm2','rate','mrp','cgst','qty','sgst','amount','status'
         )        

class ConfirmOrederSerializers(serializers.ModelSerializer):
    confirm_order= OrderSerializers(many=True,read_only=True)
   
    
    class Meta:
        model = ConfirmOrder
        fields =['id','total_amount','total_quantity','confirm_order']





# change password 
class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'new_password', 'password2')

    def validate(self, attrs):
        if attrs['new_password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"new_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()

        # return instance
        response={
            'message':'update password successfuly',
            'insatnce':instance
        }
        return Response(response)

















             