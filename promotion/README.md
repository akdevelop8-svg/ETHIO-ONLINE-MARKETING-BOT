# Telegram Auto-Promotion — Foundation

This folder is an isolated first phase for the Telegram post-promotion service. It does not change the existing marketplace bot on the default branch.

## Product rules

- Each client can authorize a public Telegram channel without making the service bot an administrator.
- Telegram's Bot API bot is used for private onboarding and notifications. Telegram does not allow bots to join channels as ordinary members; bots can only be added to channels as admins.
- For no-admin monitoring, a separately operated Telegram user account must join the approved public channel and listen through Telegram's MTProto client API. The owner must explicitly authorize the channel first. The account session is a highly sensitive secret and must never be placed in source control or sent in chat.
- If MTProto credentials/session are not configured, the service must use the manual public-post-link fallback and must not claim automatic monitoring is active.
- Private channels are not part of the first MVP. Add them only after a channel owner supplies an invite and explicitly approves the monitoring account's join.
- Promotion inventory consists only of partner channels whose owners have agreed to placements. The service bot needs posting permission in partner channels where it publishes automatically; otherwise create a manual placement task for the partner owner.
- The product promotes posts to real audiences. No fake views, IP/proxy rotation, fabricated accounts, view manipulation, or false delivery claims.
- Default campaign goal: 15,000 incremental original-post views within 3,600 seconds. This is a target, not a guarantee.
- Pilot budget: one central USD 15.00 cap shared across all customers and campaigns. Reserve/spend/release operations must be atomic and idempotent.

## First-phase architecture

1. Existing Bot API bot — /start, customer instructions, channel onboarding links and campaign notifications.
2. Channel monitor worker — a persistent process using a dedicated operator-controlled MTProto user account. It monitors only public channels that have completed owner authorization.
3. Promotion dispatcher — reserves from the central budget and selects available, approved partner placements. Each placement is individually recorded.
4. Metrics worker — records snapshots of the original post's view counter where Telegram exposes it. Report incremental views against the campaign baseline; never treat ad impressions as original-post views.
5. Admin dashboard/API — manages customer consent, partners, campaign state, placement cost, budget and audit events.

A persistent MTProto listener is not a normal short-lived Vercel Function. Keep the dashboard/API and the always-on monitoring worker as separate deployable processes. Do not mark a campaign as automatically monitored until the worker has logged in and passed a connection check.

## Required environment secrets

See .env.example. Configure secrets in the hosting provider's secret manager. Never commit .env, Telegram session strings, API hashes, BotFather tokens, Supabase service-role keys, or database connection strings.

## Database

schema.sql is an initial Supabase/Postgres schema proposal. It is intentionally server-only: all tables have RLS enabled and no access is granted to the public or authenticated browser roles. Use a dedicated Supabase project for this service; do not reuse the database of another production product.

The backend must use a server-side secret and enforce operator/customer authorization before each read or write. Before applying the schema, create a Supabase migration through the Supabase CLI and review it.

## Public post links

public_post_link.py accepts public post links such as:

- https://t.me/examplechannel/123
- https://t.me/s/examplechannel/123

Private invite links and t.me/c/... links are deliberately rejected by this MVP parser.

## Pilot checklist

- [ ] Create a dedicated Telegram bot with BotFather.
- [ ] Create a separate Telegram API application for the operator-controlled monitoring account.
- [ ] Securely configure the account session in the host secret manager.
- [ ] Test channel-owner authorization on a channel controlled by the operator.
- [ ] Recruit and verify partner channels; record their placement rates and average post reach.
- [ ] Obtain partner-owner approval and only the posting permission needed for approved placements.
- [ ] Apply the schema to a dedicated Supabase project and verify RLS.
- [ ] Run a small test placement and measure original-post views, cost and delivery time.
- [ ] Only increase the pilot after measured results support the unit economics.

## Budget reality

The USD 15 cap is a pilot limit, not a promise of 15,000 views. Telegram Ads charges by sponsored-message impressions; those impressions are not the same as views on the customer's original post. Partner rates and real audience response determine the actual cost per original-post view. Stop spending when the central cap is reached.
