import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request, jsonify

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing.")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)

WEBHOOK_PATH = "/api/webhook"
PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")

# General-purpose custom emoji IDs selected from the existing project collection.
# Telegram requires the bot owner to have Premium for custom emoji in bot messages/buttons.
EMOJI = {
    "congrats": "5954135079662916434",  # stars
    "accept": "6221736233970700254",
    "cancel": "6224185666704511761",   # reject
    "back": "5352759161945867747",
}

WEBSITE_BUTTON_EMOJI_ID = EMOJI["congrats"]


@bot.message_handler(commands=["start"])
def send_welcome(message):
    greeting_text = (
        '<tg-emoji emoji-id="' + EMOJI["congrats"] + '">🎉</tg-emoji> '
        '<b>Welcome to Ethio Online Marketing!</b> 🌸\n\n'
        "We are delighted to welcome you! Thank you for choosing "
        "<b>Ethio Online Marketing</b>. This bot is your easy starting point "
        "for discovering our digital marketing services and helpful online resources.\n\n"
        "🚀 <b>Let’s grow your business together!</b>\n"
        "A strong online presence can help your business reach new people, "
        "connect with potential customers, and create more opportunities. "
        "We are here to help you take the next step with confidence.\n\n"
        "🌐 Visit our website to learn more about what we offer, explore our "
        "services, and find the information you need. Simply tap the blue "
        "<b>Visit Our Website</b> button below.\n\n"
        '<tg-emoji emoji-id="' + EMOJI["accept"] + '">✅</tg-emoji> '
        "<b>We’re excited to have you with us!</b>\n"
        "Thank you for being part of our journey. We look forward to supporting "
        "your growth and success. 💐"
    )

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text="Visit Our Website",
        url="https://ethio-online-marketing.vercel.app/",
        style="primary",
        icon_custom_emoji_id=WEBSITE_BUTTON_EMOJI_ID
    ))
    bot.send_message(message.chat.id, greeting_text, reply_markup=markup)


@app.get("/")
def home():
    return "Bot is running perfectly!", 200


@app.post(WEBHOOK_PATH)
def telegram_webhook():
    update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200


@app.get("/api/set-webhook")
def set_webhook():
    if not PUBLIC_BASE_URL:
        return jsonify({"ok": False, "error": "PUBLIC_BASE_URL is missing"}), 500

    webhook_url = PUBLIC_BASE_URL + WEBHOOK_PATH
    result = bot.set_webhook(url=webhook_url)
    return jsonify({"ok": bool(result), "webhook_url": webhook_url}), 200 if result else 500


@app.get("/api/webhook-info")
def webhook_info():
    info = bot.get_webhook_info()
    return jsonify({
        "url": info.url,
        "pending_update_count": info.pending_update_count,
        "last_error_message": info.last_error_message
    }), 200
