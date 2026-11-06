import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request, jsonify

TOKEN = os.environ.get("BOT_TOKEN")
# Keep health checks available before BOT_TOKEN is configured.
bot = telebot.TeleBot(TOKEN, parse_mode="HTML", threaded=False) if TOKEN else None
app = Flask(__name__)

WEBHOOK_PATH = "/api/webhook"
PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL", "https://ethio-online-marketing-bot.vercel.app").rstrip("/")
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
    """Use standard Unicode emoji so every Telegram user can render the message."""
    return fallback

BUTTON_EMOJI = {
    "stars": "✨", "accept": "🤝", "cancel": "❌", "back": "⬅️",
    "support": "💬", "orders": "🛍️", "info": "ℹ️", "help": "❔",
    "payment": "🔐", "telebirr": "📱", "dashen": "🏦", "ticket": "🎫",
    "warning": "⚠️", "telegram": "✈️",
}

def make_button(text, emoji_key=None, callback_data=None, url=None, style=None):
    # Keep the keyboard compatible: use ordinary emoji in button text rather
    # than Premium-only custom emoji icons or newer button-style parameters.
    if emoji_key:
        emoji = BUTTON_EMOJI.get(emoji_key, "")
        if emoji:
            text = f"{emoji} {text}"
    kwargs = {"text": text}
    if callback_data:
        kwargs["callback_data"] = callback_data
    if url:
        kwargs["url"] = url
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
    f'{premium("stars", "✨")} <b>WELCOME TO ETHIO ONLINE MARKET!</b>\n'
    '<i>Your trusted marketplace for discovering, buying, and selling Ethiopian social-media assets with escrow-supported transactions.</i> 🌸\n\n'
    'Welcome! Ethio Online Market (EOM) connects buyers and sellers of social-media channels and accounts. Browse available listings, compare details, or publish your own listing and reach interested buyers.\n\n'
    f'{premium("orders", "🛍️")} <b>BUY & EXPLORE</b>\n'
    'Discover YouTube channels, TikTok accounts, Telegram channels, Instagram pages, Facebook pages, and X (Twitter) accounts. Review listing details, audience size, engagement information, category, and asking price before choosing what fits your goals.\n\n'
    f'{premium("accept", "🤝")} <b>SELL YOUR SOCIAL-MEDIA ASSET</b>\n'
    'Have a channel or account you want to sell? Create an account on our website, submit your listing with the required details and ownership/analytics evidence, and wait for the review process. Approved listings can be shown to potential buyers.\n\n'
    f'{premium("payment", "🔐")} <b>ESCROW-SUPPORTED TRANSACTIONS</b>\n'
    'When a buyer places an order, the platform guides the payment and escrow process. Supported payment options include Telebirr, Commercial Bank of Ethiopia (CBE), and Bank of Abyssinia. Payment evidence and transaction steps are subject to administrator verification; sending a receipt alone does not mean payment is approved.\n\n'
    f'{premium("info", "📊")} <b>MANAGE YOUR ACTIVITY</b>\n'
    'After signing in on the website, use your account and dashboard to follow your activity, review orders and transaction updates, manage listings, and access the marketplace features available to your account. The community area and AI assistant can also help you explore the platform.\n\n'
    f'{premium("support", "💬")} <b>NEED HELP?</b>\n'
    'Choose “Get Support” in this bot or contact our official team: @mr_ebek (Lead Administrator & Escrow Officer) and @EXO_SMM (Operations & Moderation). Never share your password, Telegram login code, or other sensitive account information.\n\n'
    f'{premium("stars", "🚀")} <b>READY TO GET STARTED?</b>\n'
    'Tap the button below to visit our official website, create an account or sign in, explore the marketplace, and take your next step.\n\n'
    '<b>Choose an option below.</b> Send /start anytime to return to this menu.'
)

def send_welcome(message):
    bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=main_menu())

def services_command(message):
    show_services(message.chat.id)

def help_command(message):
    show_help(message.chat.id)

def show_services(chat_id):
    text = (
        f'{premium("orders", "🛍️")} <b>ETHIO ONLINE MARKETPLACE</b>\n\n'
        '<b>1. Buy social-media channels and accounts</b>\n'
        'Browse listings for YouTube, TikTok, Telegram, Instagram, Facebook, and X (Twitter). Compare audience details, category, listing information, and price.\n\n'
        '<b>2. Sell your channel or account</b>\n'
        'Register or sign in on the website, submit your listing and supporting ownership/analytics information, and follow the review process.\n\n'
        '<b>3. Escrow-supported orders</b>\n'
        'Follow the order and payment steps. Supported methods include Telebirr, CBE, and Bank of Abyssinia. An administrator must verify payment evidence before it is treated as approved.\n\n'
        '<b>4. Account and marketplace tools</b>\n'
        'Use your dashboard to follow listings, orders, and transaction updates. Explore the community and AI assistant on the website.\n\n'
        f'{premium("info", "ℹ️")} <i>Open the official website for current listings, full details, registration, and available features.</i>'
    )
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(make_button("Open Official Website", "stars", url=WEBSITE_URL, style="primary"))
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
