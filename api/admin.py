from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(User)
class User(admin.ModelAdmin):
    list_display=['fullname','mobile_no','gst_no','drug_lic_no',
                  'email','tel_no','business_name','business_logo',
                  'business_address','password'
                 ]

@admin.register(ConfirmOrder)
class ConfirmOreder(admin.ModelAdmin):
    list_display = ['user','total_amount','total_quantity','order_date']

@admin.register(Order)
class Orderlist(admin.ModelAdmin):
    list_display=['id','product_name','product_type','manufacturer',
                'hsncode','pack','scm1','scm2','qty','rate','mrp','cgst',
                'sgst','status','amount','craete_date']
    list_filter=['craete_date'] 
    search_fields =['product_name']
      
@admin.register(ProductList)
class Productlst(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['id','product_name','product_type','manufacturer',
                'hsncode','pack','scm1','scm2','rate','mrp','cgst',
                'sgst',
                ]
    search_fields =['product_name']
  
