from my_task.main import app
from order.models import Order


@app.task(name="check_order")
def check_order():
    print("根据时间点判断订单支付时间是否超时")
    out_time="2020-07-20"
    pass