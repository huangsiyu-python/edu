from rest_framework.generics import ListAPIView

from home.models import Banner,Nav
from home.serializers import BannerModelSerializer,NavModelSerializer


class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_show=True, is_delete=False).order_by("-orders")
    serializer_class = BannerModelSerializer
    # print(queryset)

class NavListAPIView(ListAPIView):
    queryset = Nav.objects.filter(is_show=True, is_delete=False,position=1).order_by("-orders")
    serializer_class = NavModelSerializer
    # print(queryset)