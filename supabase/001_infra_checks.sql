-- Run once in Supabase -> SQL Editor. Table for the end-to-end infrastructure check.
create table if not exists public.infra_checks (
  id bigint generated always as identity primary key,
  message text not null,
  author text not null default 'anonymous',
  created_at timestamptz not null default now()
);
alter table public.infra_checks enable row level security;
drop policy if exists "infra_checks read" on public.infra_checks;
drop policy if exists "infra_checks insert" on public.infra_checks;
create policy "infra_checks read" on public.infra_checks for select using (true);
create policy "infra_checks insert" on public.infra_checks for insert with check (true);
