from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

import pandas as pd


from .models import Product
from .serializers import ProductSerializer, ProductUploadSerializer

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    REQUIRED_COLUMNS = ['sku', 'name', 'category', 'price', 'stock_qty', 'status']


    @action(detail=False, methods=['post'], url_path='upload')
    def upload(self, request):
        serializer = ProductUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            try:
                #check file type
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.name.endswith(('.xlsx','.xls')):
                    df = pd.read_excel(file)
                else:
                    return Response({"error":"Unsupported file format.", "status":status.HTTP_400_BAD_REQUEST})
                
                #check for missing columns
                missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
                if missing_cols:
                    return Response(
                        {"error": f"Missing required columns: {', '.join(missing_cols)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                #check for missing values
                if  df.isnull().any().any(): 
                    return Response({'error':'Some rows have missing values.'},
                         status=status.HTTP_400_BAD_REQUEST)
                
                #check for invalid values
                errors = []
                for index, row in df.iterrows():
                    row_errors = {}

                    try:
                        price = float(row['price'])
                        if price < 0:
                            row_errors['price'] = "Price must be non-negative"
                    except Exception:
                        row_errors['price'] = "Invalid price"

                    try:
                        if int(row['stock_qty']) < 0:
                            row_errors['stock_qty'] = "Stock must be non-negative"
                    except Exception:
                        row_errors['stock_qty'] = "Invalid stock quantity"

                    if str(row['status']).lower() not in ["active", "inactive"]:
                        row_errors['status'] = "Must be 'active' or 'inactive'"

                    if row_errors:
                        errors.append({"row": int(index) + 2, "errors": row_errors})
                
                if errors:
                    return Response({"validation_errors": errors}, status=status.HTTP_400_BAD_REQUEST)
                
                #store into the database
                for _, row in df.iterrows():
                    Product.objects.update_or_create(
                        sku = row['sku'],
                        defaults={
                            'name': row['name'],
                            'category': row['category'],
                            'price': row['price'],
                            'stock_qty': row['stock_qty'],
                            'status': row['status']
                        }
                    )
                
                return Response({"message": "Products uploaded successfully."}, status=status.HTTP_200_OK)

            
            except  Exception as e:
                return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


