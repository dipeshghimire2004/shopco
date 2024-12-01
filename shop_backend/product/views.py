from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from .serializers import ProductSerializer, ProductCreateSerializer, CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.

user=get_user_model()

class ProductCreateAPIView(APIView):
    def post(self, request):
        serializer=ProductCreateSerializer(data = request.data, context={'request':request}),
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListAPIView(APIView):
    permission_classes =[AllowAny]
    queryset=Product.objects.all()
    def get(self,request):
        queryset = self.get_queryset()
        serializer=ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        category = self.request.query_params.get('category')
        if category:
            return self.queryset.filter(category__name = category)
        return self.queryset.all()
        
        # for product in serializer.data:
        #     product['image_details']=[product['image']]
    
 
class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            product=get_object_or_404(Product,pk=pk)
        except Product.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        serializer=ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product=get_object_or_404(Product, pk=pk)

        if product.user != request.user:
            return Response({'detail':'You do not have access to update the product'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer=ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk):
        product=get_object_or_404(Product, pk=pk)
        if product.user != request.user:
             return Response({'detail':'You do not have access to delete the product'}, status=status.HTTP_403_FORBIDDEN)
        product.delete()
        return Response({'message':'Product deleted!!'}, status=status.HTTP_204_NO_CONTENT)
    


       # def post(self, request):
    #     serializer=ProductSerializer(data=request.data)
    #     # serializer=ProductSerializer(data=request.data,context={'request':request})
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         # serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
