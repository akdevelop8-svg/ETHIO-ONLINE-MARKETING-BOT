ETHIO ONLINE MARKETING BOT
==========================

PROJECT
-------
Telegram bot for Ethio Online Marketing. The bot provides a welcome menu,
service information, a simple guide, support contact flow, and FAQs.

OFFICIAL WEBSITE
----------------
https://ethio-online-marketing.vercel.app

DEPLOYMENT ON VERCEL
--------------------
1. Connect this GitHub repository:
   akdevelop8-svg/ETHIO-ONLINE-MARKETING-BOT

2. Use the main branch for production deployments.

3. Keep the project files in the repository root. The Vercel Python
   entrypoint is api/index.py and it imports the Flask app from main.py.

4. Configure the required environment variables in Vercel:
   BOT_TOKEN = your Telegram BotFather token
   PUBLIC_BASE_URL = https://ethio-online-marketing-bot.vercel.app

5. Install dependencies from requirements.txt:
   pyTelegramBotAPI==4.37.1
   Flask==3.0.0

6. Deploy the project. After deployment, open:
   https://ethio-online-marketing.vercel.app/api/set-webhook

7. Verify the Telegram webhook status at:
   https://ethio-online-marketing.vercel.app/api/webhook-info

IMPORTANT SECURITY NOTES
------------------------
- Keep BOT_TOKEN private. Never commit it to GitHub or share it publicly.
- If a bot token has ever been exposed, revoke it in BotFather and create
  a new token before adding it to Vercel environment variables.
- After changing environment variables, redeploy the Vercel project.
- The bot's website button points to https://ethio-online-marketing.vercel.app. The Telegram webhook uses the bot deployment URL https://ethio-online-marketing-bot.vercel.app.
