import logging

from edu_api.settings import constants
from edu_api.utils.send_msg import Message
from my_task.main import app

logger=logging.getLogger('django')

@app.task(name="send_sms")
def send_sms(mobile,code):
    print("这是发送短信的方法")
    message = Message(constants.API_KEY)
    status=message.send_message(mobile,code)
    if not status:
        logger.error("用户发送短信失败，手机号为：%s" % mobile)
    return "hello"
@app.task(name="send_mail")
def send_mail():
    print("这是发送邮件的方法")
    return "mail"