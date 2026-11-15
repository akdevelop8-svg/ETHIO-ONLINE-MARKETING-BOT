-- Initial schema proposal for a dedicated Supabase/Postgres project.
-- Apply only after creating a proper Supabase migration and reviewing RLS.
-- All access is server-side; never expose the service-role key in a browser.

create extension if not exists pgcrypto;

create table if not exists public.promo_customers (
  id uuid primary key default gen_random_uuid(),
  telegram_user_id bigint not null unique,
  telegram_username text,
  display_name text,
  created_at timestamptz not null default now()
);

create table if not exists public.promo_monitored_channels (
  id uuid primary key default gen_random_uuid(),
  customer_id uuid not null references public.promo_customers(id) on delete cascade,
  telegram_channel_id bigint,
  username text not null,
  title text,
  public_url text not null,
  is_public boolean not null default true,
  consent_status text not null default 'pending'
    check (consent_status in ('pending', 'challenge_sent', 'verified', 'revoked')),
  consent_challenge_hash text,
  consent_verified_at timestamptz,
  monitoring_status text not null default 'not_configured'
    check (monitoring_status in ('not_configured', 'waiting_for_join', 'active', 'paused', 'error')),
  last_seen_message_id bigint,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (customer_id, username)
);

create table if not exists public.promo_partner_channels (
  id uuid primary key default gen_random_uuid(),
  telegram_channel_id bigint unique,
  username text not null unique,
  title text,
  owner_contact text,
  subscriber_count bigint check (subscriber_count is null or subscriber_count >= 0),
  average_24h_views bigint check (average_24h_views is null or average_24h_views >= 0),
  placement_price_usd numeric(12,2) not null default 0 check (placement_price_usd >= 0),
  bot_can_post boolean not null default false,
  owner_approved_at timestamptz,
  posting_permission_verified_at timestamptz,
  status text not null default 'pending'
    check (status in ('pending', 'active', 'paused', 'rejected')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.promo_campaigns (
  id uuid primary key default gen_random_uuid(),
  customer_id uuid not null references public.promo_customers(id) on delete cascade,
  monitored_channel_id uuid not null references public.promo_monitored_channels(id) on delete cascade,
  source_message_id bigint not null,
  source_post_url text not null,
  idempotency_key text not null unique,
  target_views integer not null default 15000 check (target_views > 0),
  target_window_seconds integer not null default 3600 check (target_window_seconds > 0),
  baseline_views bigint check (baseline_views is null or baseline_views >= 0),
  latest_views bigint check (latest_views is null or latest_views >= 0),
  incremental_views bigint not null default 0 check (incremental_views >= 0),
  budget_reserved_usd numeric(12,2) not null default 0 check (budget_reserved_usd >= 0),
  spend_usd numeric(12,2) not null default 0 check (spend_usd >= 0),
  status text not null default 'queued'
    check (status in ('queued', 'running', 'paused', 'blocked', 'completed', 'failed', 'cancelled')),
  blocked_reason text,
  started_at timestamptz,
  deadline_at timestamptz,
  completed_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (monitored_channel_id, source_message_id)
);

create table if not exists public.promo_placements (
  id uuid primary key default gen_random_uuid(),
  campaign_id uuid not null references public.promo_campaigns(id) on delete cascade,
  partner_channel_id uuid not null references public.promo_partner_channels(id),
  price_usd numeric(12,2) not null check (price_usd >= 0),
  partner_message_id bigint,
  status text not null default 'pending'
    check (status in ('pending', 'approved', 'sent', 'confirmed', 'failed', 'cancelled')),
  approved_at timestamptz,
  sent_at timestamptz,
  confirmed_at timestamptz,
  result_notes text,
  idempotency_key text not null unique,
  created_at timestamptz not null default now(),
  unique (campaign_id, partner_channel_id)
);

create table if not exists public.promo_metric_snapshots (
  id bigserial primary key,
  campaign_id uuid not null references public.promo_campaigns(id) on delete cascade,
  cumulative_views bigint not null check (cumulative_views >= 0),
  captured_at timestamptz not null default now(),
  source text not null default 'telegram_mtproto'
    check (source in ('telegram_mtproto', 'telegram_bot_api', 'manual')),
  unique (campaign_id, captured_at)
);

create table if not exists public.promo_global_budget (
  id smallint primary key default 1 check (id = 1),
  currency char(3) not null default 'USD' check (currency = 'USD'),
  budget_cap_usd numeric(12,2) not null default 15.00 check (budget_cap_usd >= 0),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

insert into public.promo_global_budget (id, budget_cap_usd)
values (1, 15.00)
on conflict (id) do nothing;

create table if not exists public.promo_budget_ledger (
  id uuid primary key default gen_random_uuid(),
  campaign_id uuid references public.promo_campaigns(id) on delete set null,
  entry_type text not null
    check (entry_type in ('reserve', 'spend', 'release', 'top_up', 'adjustment')),
  amount_usd numeric(12,2) not null check (amount_usd > 0),
  idempotency_key text not null unique,
  notes text,
  created_at timestamptz not null default now()
);

create table if not exists public.promo_audit_logs (
  id bigserial primary key,
  actor_type text not null check (actor_type in ('operator', 'customer', 'partner', 'system')),
  actor_id text,
  action text not null,
  entity_type text not null,
  entity_id text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists promo_campaigns_status_created_idx
  on public.promo_campaigns (status, created_at desc);
create index if not exists promo_campaigns_deadline_idx
  on public.promo_campaigns (deadline_at);
create index if not exists promo_placements_campaign_status_idx
  on public.promo_placements (campaign_id, status);
create index if not exists promo_metric_snapshots_campaign_time_idx
  on public.promo_metric_snapshots (campaign_id, captured_at desc);
create index if not exists promo_monitored_channels_monitoring_idx
  on public.promo_monitored_channels (monitoring_status, consent_status);

-- Defence in depth. The browser roles receive no direct table access.
alter table public.promo_customers enable row level security;
alter table public.promo_monitored_channels enable row level security;
alter table public.promo_partner_channels enable row level security;
alter table public.promo_campaigns enable row level security;
alter table public.promo_placements enable row level security;
alter table public.promo_metric_snapshots enable row level security;
alter table public.promo_global_budget enable row level security;
alter table public.promo_budget_ledger enable row level security;
alter table public.promo_audit_logs enable row level security;

revoke all on public.promo_customers from anon, authenticated;
revoke all on public.promo_monitored_channels from anon, authenticated;
revoke all on public.promo_partner_channels from anon, authenticated;
revoke all on public.promo_campaigns from anon, authenticated;
revoke all on public.promo_placements from anon, authenticated;
revoke all on public.promo_metric_snapshots from anon, authenticated;
revoke all on public.promo_global_budget from anon, authenticated;
revoke all on public.promo_budget_ledger from anon, authenticated;
revoke all on public.promo_audit_logs from anon, authenticated;

grant all on public.promo_customers to service_role;
grant all on public.promo_monitored_channels to service_role;
grant all on public.promo_partner_channels to service_role;
grant all on public.promo_campaigns to service_role;
grant all on public.promo_placements to service_role;
grant all on public.promo_metric_snapshots to service_role;
grant all on public.promo_global_budget to service_role;
grant all on public.promo_budget_ledger to service_role;
grant all on public.promo_audit_logs to service_role;

grant usage, select on all sequences in schema public to service_role;
