// Service URLs come from docker-compose (VITE_*). Defaults are for local runs.
export const SERVICES = {
  core: import.meta.env.VITE_CORE_API_URL || 'http://localhost:8000',
  courses: import.meta.env.VITE_COURSES_API_URL || 'http://localhost:8001',
  ai: import.meta.env.VITE_AI_API_URL || 'http://localhost:8002',
  analytics: import.meta.env.VITE_ANALYTICS_API_URL || 'http://localhost:8003',
}
