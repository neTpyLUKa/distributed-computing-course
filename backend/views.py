from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.renderers import AdminRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from backend.models import Product
from rest_framework.parsers import JSONParser
from rest_framework.status import *
from rest_framework.generics import ListAPIView

from backend.serializers import ProductSerializer


class ProductView(APIView):
    parser_classes = (JSONParser,)

    def get(self, request: Request):
        if 'id' not in request.data:
            return Response({"message": "id field was not provided"}, HTTP_400_BAD_REQUEST)

        try:
            id = int(request.data.get('id'))
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
        if 'title' not in request.data:
            return Response({"message": "title field was not provided"}, HTTP_400_BAD_REQUEST)

        title = request.data.get('title')
        category = ''

        if 'category' in request.data:
            category = request.data.get('category')

        product = Product(title=title, category=category)
        product.save()

        return Response({
            "id": product.id,
            "title": product.title,
            "category": product.category,
        }, status=HTTP_200_OK)

    def delete(self, request: Request):
        if 'id' not in request.data:
            return Response({"message": "id field was not provided"}, HTTP_400_BAD_REQUEST)

        try:
            id = int(request.data.get('id'))
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
        if 'id' not in request.data:
            return Response({"message": "id field was not provided"}, HTTP_400_BAD_REQUEST)

        try:
            id = int(request.data.get('id'))
        except ValueError:
            return Response({"message": "wrong id, must be a number"}, HTTP_400_BAD_REQUEST)

        try:
            instance = Product.get_product(asked_id=id)
        except Product.DoesNotExist:
            return Response({"message": "No such good id"}, HTTP_404_NOT_FOUND)

        if 'title' in request.data:
            instance.title = request.data.get('title')

        if 'category' in request.data:
            instance.category = request.data.get('category')

        instance.save()

        return Response({
            "id": instance.id,
            "title": instance.title,
            "category": instance.category,
        }, status=HTTP_200_OK)


class Pagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 10


class ListProductView(ListAPIView):
    permission_classes = ()
    pagination_class = Pagination
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


@api_view(["PUT"])
def InitView(request: Request):
    for i in range(1, 11):
        instance = Product(title=str(i), category=str(i + 200))
        instance.save()
    return Response(status=HTTP_200_OK)
