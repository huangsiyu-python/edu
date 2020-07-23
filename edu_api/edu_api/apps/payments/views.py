import os
from datetime import datetime
import logging
from alipay import AliPay
from django.conf import settings
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import CourseExpire
from edu_api.settings.develop import BASE_DIR
from order.models import Order
from user.models import UserCourse
log=logging.getLogger()

class AliPayAPIView(APIView):

    def get(self, request):
        order_number = request.query_params.get("order_number")
        app_private_key_string = open(os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem")).read()
        alipay_public_key_string = open(os.path.join(BASE_DIR, "apps/payments/keys/alipay_public_key.pem")).read()
        # print(alipay_public_key_string)
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            return Response({"message": "对不起，当前订单不存在"}, status=status.HTTP_400_BAD_REQUEST)

        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type=settings.ALIAPY_CONFIG["sign_type"],
            debug=settings.ALIAPY_CONFIG["debug"],
        )

        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order.order_number,
            total_amount=float(order.real_price),
            subject=order.order_title,
            return_url=settings.ALIAPY_CONFIG["return_url"],
            notify_url=settings.ALIAPY_CONFIG["notify_url"]
        )
        url = settings.ALIAPY_CONFIG["gateway_url"] + order_string

        return Response(url)

class AliPayResultAPIView(APIView):

    def get(self, request):
        app_private_key_string = open(os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem")).read()
        alipay_public_key_string = open(os.path.join(BASE_DIR, "apps/payments/keys/alipay_public_key.pem")).read()
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type=settings.ALIAPY_CONFIG["sign_type"],
            debug=settings.ALIAPY_CONFIG["debug"],
        )
        data = request.query_params.dict()
        signature = data.pop("sign")

        success = alipay.verify(data, signature)
        success = True

        if success:
            return self.order_result_pay(data)

        return Response({"message": "对不起，当前订单支付失败！"})

    def order_result_pay(self, data):
        order_number = data.get("out_trade_no")
        try:
            order = Order.objects.get(order_number=order_number, order_status=0)
        except Order.DoesNotExist:
            return Response({"message": "对不起，支付结果查询失败！有可能是订单不存在"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            savepoint = transaction.savepoint()

            try:
                order.pay_time = datetime.now()
                order.order_status = 1
                order.save()
                user = order.user
                order_detail_list = order.order_courses.all()
                course_list = []

                for order_detail in order_detail_list:
                    course = order_detail.course
                    course.students += 1
                    course.save()
                    pay_timestamp = order.pay_time.timestamp()

                    if order_detail.expire > 0:
                        expire = CourseExpire.objects.get(pk=order_detail.expire)
                        expire_timestamp = expire.expire_time * 24 * 60 * 60
                        end_time = datetime.fromtimestamp(pay_timestamp + expire_timestamp)
                    else:
                        end_time = None

                    UserCourse.objects.create(
                        user_id=user.id,
                        course_id=course.id,
                        trade_no=data.get("trade_no"),
                        buy_type=1,
                        pay_time=order.pay_time,
                        out_time=end_time,
                    )

                    course_list.append({
                        "id": course.id,
                        "name": course.name
                    })

            except:
                log.error("订单处理过程中出现问题，请检查")
                transaction.savepoint_rollback(savepoint)
                return Response({"message": "对不起，更新订单的相关信息失败了"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "支付成功",
                         "success": "success",
                         "pay_time": order.pay_time,
                         "real_price": order.real_price,
                         "course_list": course_list
                         })
