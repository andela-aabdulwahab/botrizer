import os
from flask import Flask, request, Response
from slackclient import SlackClient
from pyteaser import SummarizeUrl
import time
import re


app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK')
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

BOT_NAME = "summarizer"


def get_url(text):
    urlexp = ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]'
              '|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls_match = re.findall(urlexp, text)
    urls = []
    if len(urls_match):
        for url in urls_match:
            urls.append(url[:-1])
        return urls
    return None


def get_summary(url):
    summary = SummarizeUrl(url)
    return '\n\n'.join(summary)


@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        if not username == BOT_NAME:
            text = request.form.get('text')
            urls = get_url(text)
            send_im(channel, get_summary(urls[0]))
    return Response(), 200


@app.route('/', methods=['GET'])
def test():
    return Response('It works!')


if __name__ == "__main__":
    app.run(debug=True)
