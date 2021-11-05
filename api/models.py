from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from rest_framework.validators import ValidationError
PRODUCT_TYPE=(('INJECTION','INJECTION'),
               ('TABLETS','TABLETS'),
               ('CAPSULE','CAPSULE'),
               ('SYRUP','SYRUP')
              )
STATUS =(('Pending','Pending'),
         ('Confirm','Confirm'),
         ('Cancel','Cancel')
         
        )               

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    fullname = models.CharField(max_length=120,blank=True,null=True)
    mobile_no = models.CharField(max_length=120,blank=True,null=True)
    gst_no = models.CharField(max_length=120,blank=True,null=True)
    drug_lic_no = models.CharField(max_length=120,blank=True,null=True)
    email = models.CharField(max_length=200,blank=True,null=True,unique=True)
    tel_no = models.CharField(max_length=120,blank=True,null=True)
    business_name = models.CharField(max_length=200,blank=True,null=True)
    business_logo = models.FileField(upload_to='media',blank=True,null=True)
    business_address = models.CharField(max_length=500,blank=True,null=True)
    password = models.CharField(max_length=120,blank=True,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return str(self.fullname)

class ProductList(models.Model):
    product_name= models.CharField(max_length=300,blank=True,null=True)
    product_type = models.CharField(choices=PRODUCT_TYPE,blank=True,null=True,max_length=500)
    manufacturer =  models.CharField(max_length=200,blank=True,null=True)
    hsncode = models.CharField(max_length=120,blank=True,null=True)
    pack = models.CharField(max_length=120,blank=True,null=True)
    scm1 = models.CharField(max_length=120,blank=True,null=True)
    scm2 = models.CharField(max_length=120,blank=True,null=True)
    rate = models.DecimalField(max_digits=12,decimal_places=2)
    mrp = models.DecimalField(max_digits=12,decimal_places=2)
    cgst =models.IntegerField()
    sgst = models.IntegerField()
    qty = models.IntegerField(default=1)
    def __str__(self):
        return self.product_name

class ConfirmOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='user')
    total_amount = models.CharField(max_length=255,blank=True,null=True)
    total_quantity = models.CharField(max_length=255,blank=True,null=True)
    order_date = models.DateField(auto_now_add=True)
    
   
    def __str__(self):
        return str(self.id)

class Order(models.Model):
    users = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='users')
    confirm_order= models.ForeignKey(ConfirmOrder,on_delete=models.CASCADE,blank=True,null=True,related_name='confirm_order')
    product_name= models.CharField(max_length=300,blank=True,null=True)
    status = models.CharField(max_length=200,blank=True,choices=STATUS,default="PENDING")
    product_type = models.CharField(choices=PRODUCT_TYPE,blank=True,null=True,max_length=500)
    manufacturer =  models.CharField(max_length=200,blank=True,null=True)
    hsncode = models.CharField(max_length=120,blank=True,null=True)
    pack = models.CharField(max_length=120,blank=True,null=True)
    scm1 = models.CharField(max_length=120,blank=True,null=True)
    scm2 = models.CharField(max_length=120,blank=True,null=True)
    rate = models.DecimalField(max_digits=12,decimal_places=2)
    mrp = models.DecimalField(max_digits=12,decimal_places=2)
    cgst = models.IntegerField()
    qty = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=12,decimal_places=2,default=00)
    sgst = models.IntegerField()
    craete_date = models.DateField(auto_now_add=True)
    is_order = models.BooleanField(default=False)

    
    def __str__(self):
        return str(self.users)
   

