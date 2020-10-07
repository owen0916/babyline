from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import configparser

import random

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')


# line_bot_api = LineBotApi('paUdEQsH+pgMPopklLqptVCSlG+ivxQdQLvAGoHPv5woFWiKPXv78cgvF/iJFki6cNc6lmARWQjWNWz9kySd92kHdhihItbcWCMdWxYwjYrGEoZUKCkazTOkOASx/qev1akLO5PM0KTfebS9V4os9QdB04t89/1O/w1cDnyilFU=')
# handler = WebhookHandler('11de0b12d791cbd4d272971014ee0a71')
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
       abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    s=random.Random()
    msg = event.message.text
    num=s.randint(1,6)
    if "調皮" in msg:
        msg = msg.encode('utf-8')
        if num==1:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="我很乖,媽咪比較調皮"))
        elif num==2:
             line_bot_api.reply_message(event.reply_token,TextSendMessage(text="我都有乖乖聽話"))
        elif num==3:
             line_bot_api.reply_message(event.reply_token,TextSendMessage(text="今天我沒有調皮"))
        elif num==4:
             line_bot_api.reply_message(event.reply_token,TextSendMessage(text="我要玩積木"))
        elif num==5:
             line_bot_api.reply_message(event.reply_token,TextSendMessage(text="我想要出去玩"))
        else:
             line_bot_api.reply_message(event.reply_token,TextSendMessage(text="我是大姐姐"))
    #print(msg)
    else:
        msg = msg.encode('utf-8')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='♫♪♬ '+event.message.text))

if __name__ == "__main__":
    app.run(debug=True,port=5000)


