# ETHIO ONLINE MARKETING BOT

A Telegram bot for **Ethio Online Marketing**. It helps visitors explore services, understand the next steps, find quick answers, and contact support.

## Official website

[https://ethio-online-marketing.vercel.app](https://ethio-online-marketing.vercel.app)

## Features

- Welcoming start message with clear guidance.
- Main menu with service discovery, how-it-works, support, and FAQs.
- Premium Telegram custom emoji where supported, with readable fallback emoji.
- Website links that point to the official Vercel domain.
- Telegram webhook endpoint and webhook status endpoint.
- Health-check route for deployment monitoring.

## Repository structure

- `main.py` — Flask application and Telegram bot handlers.
- `api/index.py` — Vercel Python entrypoint.
- `vercel.json` — routes incoming requests to the Vercel API entrypoint.
- `requirements.txt` — Python dependencies.

## Deploy on Vercel

1. Import **akdevelop8-svg/ETHIO-ONLINE-MARKETING-BOT** into Vercel.
2. Select the `main` branch.
3. Keep the project root directory at the repository root.
4. Add these environment variables in Project Settings → Environment Variables:

   | Name | Value |
   | --- | --- |
   | `BOT_TOKEN` | Your Telegram BotFather token |
   | `PUBLIC_BASE_URL` | `https://ethio-online-marketing-bot.vercel.app` |

5. Deploy or redeploy the project.
6. Register the Telegram webhook by opening:
   [https://ethio-online-marketing.vercel.app/api/set-webhook](https://ethio-online-marketing.vercel.app/api/set-webhook)
7. Check webhook status at:
   [https://ethio-online-marketing.vercel.app/api/webhook-info](https://ethio-online-marketing.vercel.app/api/webhook-info)

## Security

Never place your Telegram bot token in source code, README files, or public messages. If a token was exposed, revoke it through BotFather and create a replacement, then update the `BOT_TOKEN` environment variable in Vercel and redeploy.

## Local dependencies

Install the packages with:

```bash
pip install -r requirements.txt
```
