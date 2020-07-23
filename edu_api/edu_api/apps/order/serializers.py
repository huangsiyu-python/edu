from datetime import datetime

from django.db import transaction
from django_redis import get_redis_connection
from rest_framework import serializers

from course.models import Course, CourseExpire
from order.models import Order, OrderDetail


class OrderModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=Order
        fields=("id","order_number","pay_type")
        extra_kwargs={
            "id":{"read_only":True},
            "order_number":{"read_only":True},
            "pay_type":{"write_only":True}
        }
    def validate(self, attrs):
        pay_type=attrs.get("pay_type")
        try:
            Order.pay_choices[pay_type]
        except Order.DoesNotExist:
            raise serializers.ValidationError("当前支付方式不允许")
        return attrs

    def create(self, validated_data):
        redis_connection = get_redis_connection("cart")
        user_id = self.context['request'].user.id
        # user_id = 1
        incr = redis_connection.incr("order")
        order_number = datetime.now().strftime("%Y%m%d%H%M%S") + "%06d" % user_id + "%06d" % incr
        order = Order.objects.create(order_title="百知教育在线课程订单", total_price=0, real_price=0, order_number=order_number,
                                     order_status=0, pay_type=validated_data.get("pay_type"), credit=0, coupon=0,
                                     order_desc="你选择了一门很不错的课程", user_id=user_id, )
        with transaction.atomic():
            rollback_id=transaction.savepoint()
            cart_list = redis_connection.hgetall("cart_%s" % user_id)
            select_list = redis_connection.smembers("selected_%s" % user_id)

            for course_id_byte, expire_id_byte in cart_list.items():
                course_id = int(course_id_byte)
                expire_id = int(expire_id_byte)
                if course_id_byte in select_list:
                    try:
                        course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                    except Course.DoesNotExist:
                        transaction.savepoint_rollback(rollback_id)
                        return serializers.ValidationError("当前商品不存在")
                    original_price = course.price

                    try:
                        if expire_id > 0:
                            course_expire = CourseExpire.objects.get(id=expire_id)
                            original_price = course_expire.price
                    except CourseExpire.DoesNotExist:
                        pass
                    real_expire_price = course.real_expire_price(expire_id)
                    try:
                        OrderDetail.objects.create(
                            order=order,
                            course=course,
                            expire=expire_id,
                            price=original_price,
                            real_price=real_expire_price,
                            discount_name=course.discount_name
                        )
                    except:
                        transaction.savepoint_rollback(rollback_id)
                        raise serializers.ValidationError("订单生成失败")
                    order.total_price += float(original_price)
                    order.real_price += float(real_expire_price)
                    pipe = redis_connection.pipeline()
                    pipe.multi()
                    pipe.hdel('cart_%s' % user_id, course_id)
                    pipe.srem("selected_%s" % user_id, course_id)
                    pipe.execute()
                order.save()
            return order