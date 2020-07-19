from django.db import transaction
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from course.models import Course
from order.models import Order
from order.serializers import OrderModelSerializer


class OrderAPIView(CreateAPIView):
    # print(123)
    queryset = Order.objects.filter(is_delete=False, is_show=True)
    serializer_class = OrderModelSerializer

