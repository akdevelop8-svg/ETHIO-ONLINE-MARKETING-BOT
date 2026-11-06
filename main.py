import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request, jsonify

TOKEN = os.environ.get("BOT_TOKEN")
# Keep health checks available before BOT_TOKEN is configured.
bot = telebot.TeleBot(TOKEN, parse_mode="HTML") if TOKEN else None
app = Flask(__name__)

WEBHOOK_PATH = "/api/webhook"
PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")
WEBSITE_URL = "https://ethio-online-marketing.vercel.app/"

# General-purpose Telegram Premium custom emoji IDs (no game-specific emoji).
EMOJI = {
    "stars": "5954135079662916434",
    "accept": "6221736233970700254",
    "cancel": "6224185666704511761",
    "back": "5352759161945867747",
    "support": "5307746710682869587",
    "orders": "5217877998937595307",
    "info": "5452002597592382164",
    "help": "6222116634929140568",
    "payment": "5961054379350955385",
    "telebirr": "5960632377339285724",
    "dashen": "5960773097647771692",
    "ticket": "5285376730003954510",
    "warning": "6222095018358740369",
    "telegram": "5866355487255039002",
}

def premium(key, fallback):
    """Return Telegram's custom-emoji HTML tag with a readable fallback."""
    emoji_id = EMOJI.get(key)
    if not emoji_id:
        return fallback
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'

def make_button(text, emoji_key=None, callback_data=None, url=None, style=None):
    kwargs = {"text": text}
    if callback_data:
        kwargs["callback_data"] = callback_data
    if url:
        kwargs["url"] = url
    if emoji_key:
        kwargs["icon_custom_emoji_id"] = EMOJI[emoji_key]
    if style:
        kwargs["style"] = style
    return InlineKeyboardButton(**kwargs)

def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        make_button("Explore Services", "orders", callback_data="services", style="primary"),
        make_button("How It Works", "info", callback_data="how_it_works", style="primary"),
    )
    markup.add(
        make_button("Get Support", "support", callback_data="support", style="success"),
        make_button("FAQs & Help", "help", callback_data="help"),
    )
    markup.add(
        make_button("Visit Our Website", "stars", url=WEBSITE_URL, style="primary")
    )
    return markup

def back_menu():
    markup = InlineKeyboardMarkup()
    markup.add(make_button("Back to Main Menu", "back", callback_data="main_menu"))
    return markup

WELCOME_TEXT = (
    f'{premium("stars", "✨")} <b>WELCOME TO ETHIO ONLINE MARKETING!</b>\n'
    '<i>Your next step towards a stronger digital presence starts here.</i> 🌸\n\n'
    'We are happy to have you with us! Whether you are discovering us for the '
    'first time or coming back to explore more, this is your simple starting '
    'point for learning about Ethio Online Marketing.\n\n'
    f'{premium("accept", "✅")} <b>Discover</b> — explore our website and learn more '
    'about the services and opportunities available.\n'
    f'{premium("orders", "🛍️")} <b>Choose</b> — find the information that matches '
    'your goals and what you want to achieve online.\n'
    f'{premium("support", "💬")} <b>Connect</b> — need a hand? Use the support '
    'option and tell us what you are looking for.\n\n'
    '🚀 <b>Let’s make your online journey count!</b> A clear goal is a great '
    'place to start. We are excited to help you take the next step, discover '
    'new possibilities, and move forward with confidence.\n\n'
    f'{premium("stars", "🌟")} <b>Choose an option below to get started.</b> '
    'You can return to this menu anytime by sending /start.'
)

def send_welcome(message):
    bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=main_menu())

def services_command(message):
    show_services(message.chat.id)

def help_command(message):
    show_help(message.chat.id)

def show_services(chat_id):
    text = (
        f'{premium("orders", "🛍️")} <b>EXPLORE OUR SERVICES</b>\n\n'
        'Visit our official website to see the latest information about our '
        'services, available options, and how to get started. If you already '
        'have a goal in mind, send us a message here and tell us what you need.\n\n'
        f'{premium("info", "ℹ️")} <i>For accurate details and current offers, '
        'please check the website.</i>'
    )
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(make_button("View Services on Website", "stars", url=WEBSITE_URL, style="primary"))
    markup.add(make_button("Ask a Question", "support", callback_data="support", style="success"))
    markup.add(make_button("Back to Main Menu", "back", callback_data="main_menu"))
    bot.send_message(chat_id, text, reply_markup=markup)

def show_how_it_works(chat_id):
    text = (
        f'{premium("info", "ℹ️")} <b>HOW IT WORKS</b>\n\n'
        f'{premium("accept", "1️⃣")} <b>Explore:</b> Open our website and review the information.\n'
        f'{premium("accept", "2️⃣")} <b>Decide:</b> Choose the service or option that fits your goal.\n'
        f'{premium("accept", "3️⃣")} <b>Connect:</b> Contact us through this bot if you need guidance.\n'
        f'{premium("stars", "4️⃣")} <b>Get started:</b> Follow the instructions shared by our team.\n\n'
        'Simple, clear, and one step at a time. We are here to help you find your way.'
    )
    bot.send_message(chat_id, text, reply_markup=back_menu())

def show_support(chat_id):
    text = (
        f'{premium("support", "💬")} <b>WE’RE HERE TO HELP</b>\n\n'
        'Tell us what you need help with by sending your question in this chat. '
        'For a faster response, include the service you are interested in and '
        'a short description of your request.\n\n'
        f'{premium("ticket", "🎫")} <i>Please do not send passwords, verification '
        'codes, or other sensitive account information.</i>\n\n'
        'Our team can review your message and guide you on the next step.'
    )
    bot.send_message(chat_id, text, reply_markup=back_menu())

def show_help(chat_id):
    text = (
        f'{premium("help", "❔")} <b>QUICK HELP & FAQ</b>\n\n'
        '<b>How do I start?</b> Send /start to open the main menu.\n\n'
        '<b>Where can I see service details?</b> Tap “Explore Services” or visit our website.\n\n'
        '<b>How can I ask a question?</b> Tap “Get Support” and write your question here.\n\n'
        '<b>How do I return to the menu?</b> Send /start at any time.\n\n'
        f'{premium("warning", "⚠️")} Never share your password or Telegram login code.'
    )
    bot.send_message(chat_id, text, reply_markup=back_menu())

def handle_menu_callback(call):
    bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id
    if call.data == "main_menu":
        bot.send_message(chat_id, WELCOME_TEXT, reply_markup=main_menu())
    elif call.data == "services":
        show_services(chat_id)
    elif call.data == "how_it_works":
        show_how_it_works(chat_id)
    elif call.data == "support":
        show_support(chat_id)
    elif call.data == "help":
        show_help(chat_id)

if bot:
    bot.message_handler(commands=["start"])(send_welcome)
    bot.message_handler(commands=["services"])(services_command)
    bot.message_handler(commands=["help"])(help_command)
    bot.callback_query_handler(func=lambda call: call.data in {"main_menu", "services", "how_it_works", "support", "help"})(handle_menu_callback)

@app.get("/")
def home():
    return "Ethio Online Marketing bot is running!", 200

@app.post(WEBHOOK_PATH)
def telegram_webhook():
    if not bot:
        return jsonify({"ok": False, "error": "BOT_TOKEN is not configured"}), 503
    update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.get("/api/set-webhook")
def set_webhook():
    if not bot:
        return jsonify({"ok": False, "error": "BOT_TOKEN is not configured"}), 503
    if not PUBLIC_BASE_URL:
        return jsonify({"ok": False, "error": "PUBLIC_BASE_URL is missing"}), 500
    webhook_url = PUBLIC_BASE_URL + WEBHOOK_PATH
    result = bot.set_webhook(url=webhook_url)
    return jsonify({"ok": bool(result), "webhook_url": webhook_url}), 200 if result else 500

@app.get("/api/webhook-info")
def webhook_info():
    if not bot:
        return jsonify({"ok": False, "error": "BOT_TOKEN is not configured"}), 503
    info = bot.get_webhook_info()
    return jsonify({
        "url": info.url,
        "pending_update_count": info.pending_update_count,
        "last_error_message": info.last_error_message
    }), 200
