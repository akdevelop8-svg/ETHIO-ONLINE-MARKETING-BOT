import os
import logging
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
SUPPORT_ADMIN_ID = int(os.environ.get("SUPPORT_ADMIN_ID", "7176155928"))
ADMIN_IDS = {SUPPORT_ADMIN_ID, 1894231439}
ENABLE_PREMIUM_EMOJI = os.environ.get("ENABLE_PREMIUM_EMOJI", "false").lower() == "true"

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

def premium(key, fallback=""):
    """Render custom emoji only after the bot owner has Premium and enables it."""
    emoji_id = EMOJI.get(key)
    if ENABLE_PREMIUM_EMOJI and emoji_id:
        return f'<tg-emoji emoji-id="{emoji_id}">{fallback or " "}</tg-emoji>'
    return ""

def make_button(text, emoji_key=None, callback_data=None, url=None, style=None):
    kwargs = {"text": text}
    if callback_data:
        kwargs["callback_data"] = callback_data
    if url:
        kwargs["url"] = url
    if style in {"primary", "success", "danger"}:
        kwargs["style"] = style
    if ENABLE_PREMIUM_EMOJI and emoji_key and EMOJI.get(emoji_key):
        kwargs["icon_custom_emoji_id"] = EMOJI[emoji_key]
    return InlineKeyboardButton(**kwargs)

def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        make_button("🛍️ Explore Services", "orders", callback_data="services", style="primary"),
        make_button("📘 How It Works", "info", callback_data="how_it_works", style="danger"),
    )
    markup.add(
        make_button("💬 Get Support", "support", callback_data="support", style="success"),
        make_button("❔ FAQs & Help", "help", callback_data="help"),
    )
    markup.add(
        make_button("🌐 Visit Our Website", "stars", url=WEBSITE_URL)
    )
    return markup

def back_menu():
    markup = InlineKeyboardMarkup()
    markup.add(make_button("↩️ Back to Main Menu", "back", callback_data="main_menu", style="danger"))
    return markup

WELCOME_TEXT = (
    f'{premium("stars", "✨")} <b>WELCOME TO ETHIO ONLINE MARKET!</b>\n'
    '<i>Your trusted marketplace for discovering, buying, and selling Ethiopian social-media assets with escrow-supported transactions.</i>\n\n'
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

def render_screen(chat_id, message_id, text, markup):
    if message_id:
        try:
            bot.edit_message_text(
                text, chat_id=chat_id, message_id=message_id,
                reply_markup=markup, parse_mode="HTML"
            )
            return
        except Exception as exc:
            if "message is not modified" in str(exc).lower():
                return
            logging.exception("Could not edit menu message; sending a replacement")
    bot.send_message(chat_id, text, reply_markup=markup)

def send_welcome(message):
    bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=main_menu())

def services_command(message):
    show_services(message.chat.id)

def help_command(message):
    show_help(message.chat.id)

def show_services(chat_id, message_id=None):
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
    markup.add(make_button("🌐 Open Official Website", "stars", url=WEBSITE_URL, style="primary"))
    markup.add(make_button("💬 Ask a Question", "support", callback_data="support", style="success"))
    markup.add(make_button("Back to Main Menu", "back", callback_data="main_menu"))
    render_screen(chat_id, message_id, text, markup)

def show_how_it_works(chat_id, message_id=None):
    text = (
        f'{premium("info", "ℹ️")} <b>HOW IT WORKS</b>\n\n'
        f'{premium("accept", "1.")} <b>Explore:</b> Open our website and review the information.\n'
        f'{premium("accept", "2.")} <b>Decide:</b> Choose the service or option that fits your goal.\n'
        f'{premium("accept", "3.")} <b>Connect:</b> Contact us through this bot if you need guidance.\n'
        f'{premium("stars", "4.")} <b>Get started:</b> Follow the instructions shared by our team.\n\n'
        'Simple, clear, and one step at a time. We are here to help you find your way.'
    )
    render_screen(chat_id, message_id, text, back_menu())

def show_support(chat_id, message_id=None):
    text = (
        f'{premium("support", "💬")} <b>WE’RE HERE TO HELP</b>\n\n'
        'Tell us what you need help with by sending your question in this chat. '
        'For a faster response, include the service you are interested in and '
        'a short description of your request.\n\n'
        f'{premium("ticket", "🎫")} <i>Please do not send passwords, verification '
        'codes, or other sensitive account information.</i>\n\n'
        'Our team can review your message and guide you on the next step.'
    )
    render_screen(chat_id, message_id, text, back_menu())

def show_help(chat_id, message_id=None):
    text = (
        f'{premium("help", "❔")} <b>QUICK HELP & FAQ</b>\n\n'
        '<b>How do I start?</b> Send /start to open the main menu.\n\n'
        '<b>Where can I see service details?</b> Tap “Explore Services” or visit our website.\n\n'
        '<b>How can I ask a question?</b> Tap “Get Support” and write your question here.\n\n'
        '<b>How do I return to the menu?</b> Send /start at any time.\n\n'
        f'{premium("warning", "⚠️")} Never share your password or Telegram login code.'
    )
    render_screen(chat_id, message_id, text, back_menu())

def handle_menu_callback(call):
    bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if call.data == "main_menu":
        render_screen(chat_id, message_id, WELCOME_TEXT, main_menu())
    elif call.data == "services":
        show_services(chat_id, message_id)
    elif call.data == "how_it_works":
        show_how_it_works(chat_id, message_id)
    elif call.data == "support":
        show_support(chat_id, message_id)
    elif call.data == "help":
        show_help(chat_id, message_id)

def _ticket_customer_id(message):
    if not message or not getattr(message, "text", None):
        return None
    import re
    match = re.search(r"Customer ID: (\d+)", message.text)
    return int(match.group(1)) if match else None

def _is_admin_ticket_reply(message):
    return bool(
        message and message.chat and message.chat.id in ADMIN_IDS
        and message.reply_to_message and _ticket_customer_id(message.reply_to_message)
    )

def forward_customer_question(message):
    customer = message.from_user
    customer_name = " ".join(part for part in [customer.first_name, customer.last_name] if part)
    username = f"@{customer.username}" if customer.username else "Not set"
    ticket_id = f"{message.chat.id}-{message.message_id}"
    content = (message.text or message.caption or "").strip()
    if not content:
        content = f"[{message.content_type} message]"
    import html
    ticket_text = (
        f'{premium("ticket", "🎫") or "🎫"} <b>NEW CUSTOMER SUPPORT REQUEST</b>\n'
        f"<b>Ticket:</b> <code>{ticket_id}</code>\n"
        f"<b>Name:</b> {html.escape(customer_name or 'Customer')}\n"
        f"<b>Username:</b> {html.escape(username)}\n"
        f"<b>Customer ID:</b> <code>{message.chat.id}</code>\n\n"
        "<b>Question:</b>\n"
        f"{html.escape(content[:2500])}\n\n"
        "<i>Reply directly to THIS ticket message to send your answer to this customer only.</i>"
    )
    delivered = 0
    # Telegram only permits private bot messages after the admin opens the bot and presses Start.
    for admin_id in [SUPPORT_ADMIN_ID]:
        try:
            ticket_message = bot.send_message(admin_id, ticket_text, parse_mode="HTML")
            if message.content_type != "text":
                bot.copy_message(
                    chat_id=admin_id, from_chat_id=message.chat.id,
                    message_id=message.message_id,
                    reply_to_message_id=ticket_message.message_id
                )
            delivered += 1
        except Exception:
            logging.exception("Support ticket delivery failed for admin %s", admin_id)
    if delivered:
        bot.send_message(
            message.chat.id,
            f'{premium("accept", "📨") or "📨"} Your question has been received by our support team. '
            "An administrator will reply here as soon as possible."
        )
    else:
        bot.send_message(
            message.chat.id,
            "Your message could not be delivered to our support team yet. "
            "Please try again shortly."
        )

def deliver_admin_reply(message):
    customer_id = _ticket_customer_id(message.reply_to_message)
    try:
        bot.copy_message(
            chat_id=customer_id, from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        bot.reply_to(message, f'{premium("accept", "✅") or "✅"} Your reply was delivered to the customer.')
    except Exception:
        bot.reply_to(
            message,
            "I could not deliver this reply. Check that the customer has not blocked the bot."
        )

if bot:
    bot.message_handler(commands=["start"])(send_welcome)
    bot.message_handler(commands=["services"])(services_command)
    bot.message_handler(commands=["help"])(help_command)
    bot.message_handler(func=_is_admin_ticket_reply, content_types=["text", "photo", "video", "document", "audio", "voice", "animation", "sticker", "video_note"])(deliver_admin_reply)
    customer_content_types = [
        "text", "photo", "video", "document", "audio", "voice",
        "animation", "sticker", "video_note", "location", "contact",
        "venue", "poll", "dice"
    ]
    bot.message_handler(
        func=lambda message: message.chat.type == "private" and message.chat.id not in ADMIN_IDS,
        content_types=customer_content_types
    )(forward_customer_question)
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
