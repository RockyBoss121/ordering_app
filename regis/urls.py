
from django.contrib import admin
from django.db import router
from django.urls import path,include
from django.conf import settings
from django.conf.urls. static import static
from rest_framework import viewsets
from api import views
from api.views import ChangePasswordView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('register',views.RegisterViewset,basename='register')
router.register('login',views.LogiViewset,basename='login')
router.register('productlist',views.ProductListView,basename='productlist')
router.register('productlist_serach',views.ProductView,basename='productlist_serach')
router.register('order',views.OrderView,basename='order')
router.register('confirm',views.ConfirOrderViewSet,basename='confirm')
router.register('confirm_order_list',views.ConfirmOrderListViewSet,basename='confirm_order_list')
router.register('client_confirm_orderlist',views.ClientConfrimOrderlistView,basename='client_confirm_orderlist')
# router.register('pendind_order',views.PendingOrder,basename='pendind_order')
# router.register('approved',views.ApprovedOrder,basename='approved')
router.register('admin_confirm_order_list',views.AdminConfirmOrderlistView,basename='admin_confirm_order_list')
router.register('admin_order_cancle_list',views.AdminCancleOrderListView,basename='admin_order_cancle_list')
router.register('AdminAllListView',views.AdminAllListView,basename='AdminAllListView')
admin.site.site_header="Connexial Healthcare"
# admin.site.site_title = "Connexial"
admin.site.index_title="Welcome To Connexial Healthcare Dashboard "

from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name='index.html')),
    path('api/',include(router.urls)),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('productsearch/',views.ProductSearchView.as_view(),name='productsearch'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('confirm_order_search/',views.ConfirmOrderFilter.as_view(),name='confirm_order_search'),
    path('confirm_date_filter/',views.Confirm_dateListView.as_view(),name='confirm_date_filter'),
    
       
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
