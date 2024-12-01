from django.urls import path
from django.conf.urls.static import static    
from django.conf import settings
from . import views

urlpatterns = [
    path('products/', views.ProductListAPIView.as_view(), name='product_list'),
    path('product/create',views.ProductCreateAPIView.as_view(), name='product_create'),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='update_delete_product'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

