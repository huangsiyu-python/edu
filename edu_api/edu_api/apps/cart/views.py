import logging

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from course.models import Course, CourseExpire
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated

from edu_api.settings import constants

log=logging.getLogger("django")
class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    def add_cart(self,request):
        course_id=request.data.get('course_id')
        # print(course_id)
        user_id=request.user.id
        select=True
        expire=0
        # print(123)
        try:
            Course.objects.get(is_show=True,id=course_id)
            # print(234)
        except Course.DoesNotExist:
            return Response({"message":"参数有误，课程不存在"},status=status.HTTP_400_BAD_REQUEST)
        try:
            redis_connection=get_redis_connection("cart")
            pipeline=redis_connection.pipeline()
            pipeline.multi()
            pipeline.hset("cart_%s" % user_id, course_id, expire)
            pipeline.sadd("selected_%s" % user_id, course_id)
            # course_len=redis_connection.hlen('cart_%s' % user_id)
            # print("course_len",course_len)
            pipeline.execute()
            course_len = redis_connection.hlen('cart_%s' % user_id)
        except:
            log.error("购物 车数据储存失败")
            return Response({"message":"参数有误，购物车添加失败"},status=status.HTTP_507_INSUFFICIENT_STORAGE)
        return Response({"message":"购物车商品添加成功!","cart_length":course_len})

    def list_cart(self,request):
        user_id=request.user.id
        redis_connection=get_redis_connection("cart")
        cart_list_bytes=redis_connection.hgetall('cart_%s' % user_id)
        select_list_bytes=redis_connection.smembers("selected_%s" % user_id)
        # print("cart_list",cart_list)
        # print("select_list",select_list)
        data=[]
        for course_id_bytes,expire_id_bytes in cart_list_bytes.items():
            course_id=int(course_id_bytes)
            expire_id=int(expire_id_bytes)
            try:
                course=Course.objects.get(is_show=True,is_delete=False,pk=course_id)
            except Course.DoesNotExist:
                continue

            data.append(({
                "selected":True if course_id_bytes in select_list_bytes else False,
                "course_img":constants.IMAGE_SRC+course.course_img.url,
                "name":course.name,
                "id":course.id,
                "expire_id":expire_id,
                "price":course.price,
                # 购物车列表需要课程有效期
                "expire_list": course.expire_list,
                "real_price": course.real_expire_price(expire_id),
            }))
        # print(data)
        return Response(data)

    def change_select(self,request):
        user_id=request.user.id
        selected=request.data.get("selected")
        course_id=request.data.get("course_id")
        try:
            Course.objects.get(is_show=True,is_delete=False,id=course_id)
        except Course.DoesNotExist:
            return Response({"message":"参数有误，当前商品不存在"},status=status.HTTP_400_BAD_REQUEST)
        redis_connection=get_redis_connection("cart")
        if selected:
            redis_connection.sadd("selected_%s" % user_id,course_id)
        else:
            redis_connection.srem("selected_%s" % user_id,course_id)
        return Response({"message":"状态切换成功"})

    def del_cart(self,request):
        user_id=request.user.id
        course_id=request.data.get("course_id")
        redis_connection=get_redis_connection("cart")
        redis_connection.hdel(course_id)
        print(user_id,course_id)
        return Response({"message":"删除成功"})
    def change_expire(self, request):
        user_id = request.user.id
        expire_id = request.data.get("expire_id")
        course_id = request.data.get("course_id")
        print(course_id, expire_id)
        try:
            course = Course.objects.get(is_show=True, is_delete=False, id=course_id)
            if expire_id > 0:
                expire_iem = CourseExpire.objects.filter(is_show=True, is_delete=False, id=expire_id)
                if not expire_iem:
                    raise Course.DoesNotExist()
        except Course.DoesNotExist:
            return Response({"message": "课程信息不存在"}, status=status.HTTP_400_BAD_REQUEST)

        connection = get_redis_connection("cart")
        connection.hset("cart_%s" % user_id, course_id, expire_id)
        real_price = course.real_expire_price(expire_id)
        return Response({"message": "切换有效期成功", "real_price": real_price})

