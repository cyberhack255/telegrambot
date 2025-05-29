from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "<telegrambot token>"

# Facebook Page Access Token and Page ID
FACEBOOK_PAGE_ACCESS_TOKEN = "<FB access token>"
FACEBOOK_PAGE_ID = "520852677783384"

# Webhook URL for Telegram
WEBHOOK_URL = "https://telegrambot-fbpageforwarder.glitch.me/webhook"

# Set Telegram Webhook
def set_webhook():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    try:
        response = requests.post(url, json={"url": WEBHOOK_URL})
        data = response.json()
        if data.get("ok"):
            print("Telegram webhook set successfully!")
        else:
            print("Failed to set Telegram webhook:", data)
    except Exception as e:
        print("Error setting Telegram webhook:", str(e))

# Post message to Facebook
def post_to_facebook(message):
    url = f"https://graph.facebook.com/v21.0/{FACEBOOK_PAGE_ID}/feed"
    try:
        response = requests.post(url, data={
            "message": message,
            "access_token": FACEBOOK_PAGE_ACCESS_TOKEN
        })
        if response.status_code == 200:
            print("Message posted to Facebook successfully!")
        else:
            print("Failed to post to Facebook:", response.json())
    except Exception as e:
        print("Error posting to Facebook:", str(e))

# Handle Telegram Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = request.get_json()
        if update and 'channel_post' in update and 'text' in update['channel_post']:
            text = update['channel_post']['text']
            print("New message from Telegram channel:", text)
            post_to_facebook(text)
        return '', 200
    except Exception as e:
        print("Error processing webhook:", str(e))
        return '', 500

if __name__ == '__main__':
    print("Starting server on port 3000")
    set_webhook()
    app.run(port=3000)
