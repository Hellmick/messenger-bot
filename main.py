from flask import Flask, request
import requests
from os import getenv
import config

app = Flask(__name__)
cfg = config.Config

FB_API_URL = cfg.FB_API_URL
VERIFY_TOKEN = cfg.VERIFY_TOKEN
USER_ACCESS_TOKEN = cfg.USER_ACCESS_TOKEN
THREAD_ID = cfg.THREAD_ID
PRODUCTION = cfg.THREAD_ID
MY_ID = cfg.MY_ID


def send_message(text):
    payload = {
        'message': {
            'text': text
        },
        "recipient": {
            "thread_key": THREAD_ID
        },
    }

    if PRODUCTION:
        payload['recipient'] = {
            "id": [MY_ID]
        }

    auth = {
        'access_token': USER_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json

def get_bot_response(message):
    return f'<bot> {message}'

def verify_webhook(req):
    print(req.args.get("challenge"))
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(message):
    send_message(get_bot_response(message))

def is_valid(message):
    return message.get('message') and message['message'].get('text') and not message['message'].get('is_echo')

@app.route('/webhook', methods=['GET','POST'])
def listen():
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        print(payload)
        event = payload['entry'][0]['messages']
        for x in event:
            if is_valid(x):
                text = x['message']['text']
                respond(text)

        return "ok"


if __name__ == '__main__':
    app.run()
