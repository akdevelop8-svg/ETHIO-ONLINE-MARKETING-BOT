DEPLOY STEPS

1. Upload all files to GitHub:
   main.py
   requirements.txt
   vercel.json
   api/index.py

2. Vercel settings:
   Build Command: empty / Override OFF
   Output Directory: empty / N/A
   Install Command: pip install -r requirements.txt

3. Add Environment Variables:
   BOT_TOKEN = your NEW BotFather token
   PUBLIC_BASE_URL = https://ethio-online-marketing-bot-qvm8.vercel.app

4. Redeploy.

5. Open once:
   https://ethio-online-marketing-bot-qvm8.vercel.app/api/set-webhook

6. Check:
   https://ethio-online-marketing-bot-qvm8.vercel.app/api/webhook-info

IMPORTANT: Regenerate the old Telegram token because it was exposed.
