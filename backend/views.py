from django.shortcuts import render

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from backend.models import Product
from django.core import serializers
from rest_framework.parsers import JSONParser
from rest_framework.status import *
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import ListModelMixin


class product_view(APIView):
    parser_classes = (JSONParser,)

    def get(self, request: Request):
        if 'id' not in request.query_params:
            return Response({"message": "id field was not provided"}, HTTP_400_BAD_REQUEST)

        try:
            id = int(request.query_params.get('id'))
        except ValueError:
            return Response({"message": "wrong id, must be a number"}, HTTP_400_BAD_REQUEST)

        try:
            res = Product.get_product(asked_id=id)
        except Product.DoesNotExist:
            return Response({"message": "No such good title"}, HTTP_404_NOT_FOUND)

        return Response({
            "id": res.id,
            "title": res.title,
            "category": res.category,
        }, status=HTTP_200_OK)

    def put(self, request: Request):
        if 'title' not in request.query_params:
            return Response({"message": "title field was not provided"}, HTTP_400_BAD_REQUEST)

        title = request.query_params.get('title')
        category = ''
        
        if 'category' in request.query_params:
            category = request.query_params.get('category')
            
        product = Product(title=title, category=category)
        product.save()

        return Response({
            "id": product.id,
            "title": product.title,
            "category": product.category,
        }, status=HTTP_200_OK)

    def delete(self, request: Request):
        if 'id' not in request.query_params:
            return Response({"message": "id field was not provided"}, HTTP_400_BAD_REQUEST)

        try:
            id = int(request.query_params.get('id'))
        except ValueError:
            return Response({"message": "wrong id, must be a number"}, HTTP_400_BAD_REQUEST)

        try:
            instance = Product.get_product(asked_id=id)
        except Product.DoesNotExist:
            return Response({"message": "No such good id"}, HTTP_404_NOT_FOUND)

        instance.delete()

        return Response({
            "id": id,
            "title": instance.title,
            "category": instance.category,
        }, status=HTTP_200_OK)

    def post(self, request: Request):
        if 'id' not in request.query_params:
            return Response({"message": "id field was not provided"}, HTTP_400_BAD_REQUEST)

        try:
            id = int(request.query_params.get('id'))
        except ValueError:
            return Response({"message": "wrong id, must be a number"}, HTTP_400_BAD_REQUEST)

        try:
            instance = Product.get_product(asked_id=id)
        except Product.DoesNotExist:
            return Response({"message": "No such good id"}, HTTP_404_NOT_FOUND)

        if 'title' in request.query_params:
            instance.title = request.query_params.get('title')

        if 'category' in request.query_params:
            instance.category = request.query_params.get('category')

        instance.save()

        return Response({
            "id": instance.id,
            "title": instance.title,
            "category": instance.category,
        }, status=HTTP_200_OK)

@api_view(["GET"])
def products_view(request: Request):
    return Response({
           "number of goods": Product.objects.count(),
          "data": Product.objects.values("title", "category", "id")
    }, status=HTTP_200_OK)