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

# General-purpose custom emoji from the existing project emoji collection.
# Telegram requires the bot owner to have Premium to use custom emoji icons.
WEBSITE_BUTTON_EMOJI_ID = "5954135079662916434"  # stars


@bot.message_handler(commands=["start"])
def send_welcome(message):
    greeting_text = (
        "🌸 <b>Welcome to Ethio Online Marketing!</b> 🎉\n\n"
        "We are happy to have you here. This bot is your quick gateway to "
        "our digital marketing services and online resources.\n\n"
        "🚀 <b>Ready to grow your business?</b>\n"
        "Explore our website to discover how our marketing solutions can help "
        "you build your online presence, reach more customers, and take the "
        "next step toward your business goals.\n\n"
        "✨ Take a moment to visit us using the blue button below. "
        "We look forward to being part of your growth journey!\n\n"
        "💐 <i>Thank you for choosing Ethio Online Marketing.</i>"
    )

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text="🌐 Visit Our Website",
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
