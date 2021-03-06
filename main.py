from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction, StickerMessage, StickerSendMessage, ImageSendMessage
)
from random_select import random_image
from quiz import *

app = Flask(__name__)

line_bot_api = LineBotApi('**********')
handler = WebhookHandler('**********')

# @app.route("/")
# def hello_world():
#     return "hello world!"

flag=0
count=0
@app.route("/callback", methods=['POST'])
def callback():
    global count
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global QData
    global flag
    global count

    if flag==0:
        QData=ChooseQustion()
        flag+=1
    else:
        pass
    # print(flag)

    if event.message.text == "Quiz!!":
        Char = ['シンデレラ','ミッキー','ベル','ジェシー','ミニー','プルート','マックス','ドリー','ニモ','ドナルド','デイジー','チップ','デール','グーフィー','マイク','サリー','ウッディ','バズ','オーロラ姫','ピーターパン','アリエル'
                ,'ラプンツェル','プーさん']
        rnd=random.choice(Char)
        line_bot_api.reply_message(event.reply_token,
        [
            TextSendMessage(text="問題だよ！！"),
            TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url=QData[6],
                title=rnd+"からの質問",
                text=QData[0],
                actions=[
                    PostbackTemplateAction(
                        label="(1)" + QData[1],
                        text='Chose 1',
                        data='action=buy&itemid=1'
                        ),
                    PostbackTemplateAction(
                        label="(2)" + QData[2],
                        text='Chose 2',
                        data='action=buy&itemid=1'
                        ),
                    PostbackTemplateAction(
                        label="(3)" + QData[3],
                        text='Chose 3',
                        data='action=buy&itemid=1'
                        ),
                    PostbackTemplateAction(
                        label="(4)" + QData[4],
                        text='Chose 4',
                        data='action=buy&itemid=1'
                        ),
                    ]
                )
            )
        ]
        )
        flag=1
        count=1
        # print(flag)
    elif (event.message.text == "Chose 1" or event.message.text == "Chose 2" or event.message.text == "Chose 3" or event.message.text == "Chose 4"):
        if count==1:
            s=Solve(event.message.text,QData[5])
            line_bot_api.reply_message(event.reply_token,
            [
            TextSendMessage(text=s[0]),
            StickerSendMessage(
                package_id=1,
                sticker_id=s[1]
                )
            ])
            print("count==1の予定 ==> {}".format(count))
        else:
            rep=random.choice(['本当にいいの？','絶対に？','え、本当にそれで？'])
            line_bot_api.reply_message(event.reply_token,
            [
                TextSendMessage(text=rep),
                StickerSendMessage(
                    package_id=2,
                    sticker_id=175
                    )
            ])
            print("count!=1の予定 ==> {}".format(flag))
        flag=0
        count=0

    elif event.message.text == "ディズニー":
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text="https://www.tokyodisneyresort.jp/")
        )
        flag=0
        count=0

    elif event.message.text == "Usage":
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text=Usage())
        )
        flag=0
        count=0

    elif event.message.text == "Instagramが見たいよ！！":
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text="https://www.instagram.com/tokyodisneyresort_official/?hl=ja")
        )
        flag=0
        count=0

    elif event.message.text == "Twitterが見たいよ！！":
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text="https://twitter.com/tdr_pr")
        )
        flag=0
        count=0

    elif event.message.text == "占う！！":
        info=Uranai()
        line_bot_api.reply_message(event.reply_token,
        [
        TextSendMessage(text="今日のラッキーディズニーキャラクターは、、、"),
        TextSendMessage(text=info[0]+"だよ！！"),
        ImageSendMessage(
        original_content_url=info[1],
        preview_image_url=info[1])
        ])
        flag=0
        count=0

    else:
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text=event.message.text)
        )
        flag=0
        count=0

if __name__ == "__main__":
    app.run()
