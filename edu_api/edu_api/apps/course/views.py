from rest_framework.generics import ListAPIView,RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from course.models import CourseCategory, Course, CourseChapter
from course.pagination import CoursePageNumber
from course.serializer import CourseCategorySerializer, CourseModelSerializer, CourseLessonModelSerializer, \
    CourseChapterModelSerializer


class CourseCategoryListAPIView(ListAPIView):
    queryset = CourseCategory.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseCategorySerializer


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseModelSerializer


class CourseFilterListAPIView(ListAPIView):
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ("course_category",)
    ordering_fields = ("id", "students", "price")
    pagination_class = CoursePageNumber

class CourseDetailListAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_show=True,is_delete=False).order_by("orders")
    serializer_class = CourseModelSerializer
    lookup_field = "id"

class CourseLessonListAPIView(ListAPIView):
    queryset = CourseChapter.objects.filter(is_show=True,is_delete=False).order_by("orders","id")
    serializer_class = CourseChapterModelSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields=['course']
    # print(queryset)