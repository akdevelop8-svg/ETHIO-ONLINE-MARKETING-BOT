import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request

# It's best practice to use environment variables for tokens.
# Set BOT_TOKEN in your Render environment variables.
TOKEN = os.environ.get('BOT_TOKEN', '8713822127:AAHFogfDb8U9CzLONvCuUDHInjQnzaOiwe0')

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    greeting_text = (
        "<tg-emoji emoji-id='5452002597592382164'>📣</tg-emoji> Hello and welcome to <b>Ethio Online Marketing</b>!\n\n"
        "<tg-emoji emoji-id='6222116634929140568'>👀</tg-emoji> This bot is designed to help you elevate your digital marketing strategy and easily access valuable resources. "
        "We are thrilled to have you here!\n\n"
        "<tg-emoji emoji-id='6221736233970700254'>💰</tg-emoji> Utilize our services to grow your business and maximize your profits!\n\n"
        "<tg-emoji emoji-id='6224175771099861191'>🚨</tg-emoji> To explore our services in detail and visit our website, simply tap the button below."
    )

    markup = InlineKeyboardMarkup()
    web_button = InlineKeyboardButton(
        text="🌐 Visit Our Website",
        url="ethio-online-marketing.vercel.app"
    )
    markup.add(web_button)

    bot.send_message(message.chat.id, greeting_text, reply_markup=markup)

# Health check endpoint for UptimeRobot
@app.route('/')
def home():
    return "Bot is running perfectly!", 200

# The polling process should run in a separate thread if using Flask to serve health checks, 
# or we use Webhooks. For simplicity on Render with Uptime Robot, running a thread for polling is easiest.

import threading

def run_bot():
    bot.remove_webhook()
    print("Bot is polling...")
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # Start bot polling in a background thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Start the Flask app
    # Render assigns a dynamic PORT via environment variables
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
