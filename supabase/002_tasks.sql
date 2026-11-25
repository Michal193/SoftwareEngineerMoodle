-- Run once in Supabase -> SQL Editor. Table for student & course tasks.
create table if not exists public.tasks (
  id bigint generated always as identity primary key,
  student_id text not null,
  course_id text not null,
  title text not null,
  due_date timestamptz,
  status text not null default 'pending' check (status in ('pending', 'in_progress', 'completed')),
  created_at timestamptz not null default now()
);

create index if not exists idx_tasks_student_course
  on public.tasks (student_id, course_id);

alter table public.tasks enable row level security;
drop policy if exists "tasks read" on public.tasks;
drop policy if exists "tasks insert" on public.tasks;
drop policy if exists "tasks update" on public.tasks;
create policy "tasks read" on public.tasks for select using (true);
create policy "tasks insert" on public.tasks for insert with check (true);
create policy "tasks update" on public.tasks for update using (true);