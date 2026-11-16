# Software Engineer Moodle (LMS)

[![Docker](https://img.shields.io/badge/Docker-Docker%20Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Supabase](https://img.shields.io/badge/Database-Supabase%20%2F%20PostgreSQL-3ECF8E?logo=supabase&logoColor=white)](https://supabase.com/)
[![Google AI Studio](https://img.shields.io/badge/AI-Google%20AI%20Studio%20%2F%20Gemini-4285F4?logo=google&logoColor=white)](https://aistudio.google.com/)
[![Architecture](https://img.shields.io/badge/Architecture-Microservices%20Monorepo-orange)](#monorepo-architecture--structure)

---

## 1. System Overview

**Software Engineer Moodle** is a modern, modular, cloud-connected Learning Management System (LMS) inspired by Moodle, engineered by a multi-disciplinary software engineering team under the **Scaled Agile Framework (SAFe / Scaled Scrum)** with weekly rotating leadership (*Weekly Program Lead / Chief PO*).

The system addresses the challenges of remote and hybrid academic learning by coupling traditional course and assignment management with an intelligent, generative AI assistant and real-time academic analytics.

### Target Personas & Core Capabilities

| Role | Responsibilities & Capabilities |
| :--- | :--- |
| **Student** | Browse enrolled courses, view syllabi and lecture slides, submit assignments, receive automated AI feedback, interact with the AI tutor for Q&A, and monitor personal academic progress and grades. |
| **Lecturer** | Create and manage courses, upload syllabus and presentation materials, publish assignments with deadlines and rubrics, review and grade submissions, and track class-wide engagement analytics. |
| **Teaching Assistant (TA)** | Assist with assignment grading, student communications, office hour coordination, and course material maintenance. |
| **Administrator** | Supervise system-wide user onboarding, role-based access control (RBAC), two-factor authentication (2FA) enforcement, security policies, and containerized service health. |

### Architectural Pillars

* **End-to-End System Integrity:** Seamless data flow across the client application, independent microservices, cloud-hosted Supabase PostgreSQL, and Google AI Studio APIs.
* **Unified UX/UI Experience:** Standardized design system ensuring consistent navigation, responsive layouts, and intuitive workflows across all feature domains.
* **Intelligent AI Augmentation:** Native integration with Google AI Studio (Gemini) providing automated assignment review, instant study summaries, and interactive pedagogical simulation.
* **Containerized Microservices:** Isolated, independently deployable services orchestrated with Docker Compose for consistent development and reliable production releases.

---

## 2. Monorepo Architecture & Structure

The repository is organized as a unified **Monorepo** containing the frontend web client, three specialized backend microservices, shared container configurations, and environment templates.

```
SoftwareEngineerMoodle/
├── frontend/                  # Unified web client application (React / Next.js / Vue)
│   ├── Dockerfile             # Multi-stage Docker build for frontend
│   └── ...                    # Components, state stores, views, assets
├── backend-core/              # Identity, Authentication & User Management Service
│   ├── Dockerfile             # Container configuration for Core service
│   └── ...                    # Auth endpoints, RBAC, 2FA, session/token management
├── backend-courses/           # Academic Course & Assignment Management Service
│   ├── Dockerfile             # Container configuration for Courses service
│   └── ...                    # Course catalog, file uploads, submissions, grading
├── backend-ai/                # AI Smart Assistant & Tutor Integration Service
│   ├── Dockerfile             # Container configuration for AI service
│   └── ...                    # Google AI Studio / Gemini API integration, prompt engines
├── docker-compose.yml         # Container orchestrator linking all services & networks
├── .env.example               # Sanitized template for environment variables
├── .gitignore                 # Enforces security by preventing secrets from being tracked
├── project_instructions.md    # Comprehensive academic & organizational specifications
└── README.md                  # Project documentation & execution guide
```

### Feature Team & Service Ownership

Development is distributed across 4 permanent Feature Teams (3–5 developers each), mapped to architectural domains:

1. **Team 1: Core & User Management (`backend-core`)**
   * User registration, login, and profile lifecycle.
   * Role-Based Access Control (RBAC): Student, Lecturer, TA, Administrator.
   * Security hardening: Two-Factor Authentication (2FA) and JWT/token verification.
2. **Team 2: Course Content & Assignments (`backend-courses`)**
   * Course creation, syllabus and presentation uploads.
   * Assignment creation, rubric definition, deadline scheduling.
   * Student file submissions and submission status tracking.
3. **Team 3: AI Smart Assistant (`backend-ai`)**
   * Google AI Studio (Gemini) API orchestration.
   * Automated grading assistance and constructive feedback generation.
   * Lecture summary generator and interactive 24/7 AI student tutor.
4. **Team 4: Analytics & Notifications (Cross-service integration)**
   * Real-time notification delivery (assignment postings, grades, reminders).
   * Visual performance dashboards and grade statistics for students and lecturers.
   * Academic progress monitoring and engagement metrics.

---

## 3. Non-Functional Requirements (NFRs) & Quality Standards

In compliance with project specifications, all features adhere to strict Non-Functional Requirements, verified via automated checks, performance testing, and Azure DevOps tracking tags (`SECURITY`, `PERFORMANCE`, `SCALABILITY`, `CAPACITY`):

* **Performance:** Maximum response time of **under 2.0 seconds** for all standard API queries, course listings, and dashboard loads under normal operating conditions.
* **Scalability & Concurrency:** Backend services and database connection pools are architected to support **at least 1,000 concurrent active users** during high-traffic peaks (e.g., assignment submission deadlines) without service degradation.
* **Security & Compliance:**
  * Strict RBAC preventing unauthorized cross-role or cross-course data access.
  * Mandatory 2FA verification for elevated actions.
  * Secrets management: zero credentials, tokens, or API keys committed to source control (strictly loaded via `.env`).
* **Reliability & Logging:** Structured JSON logging, microservice health-check probes, graceful error degradation, and retry policies for external AI API calls.

### Definition of Done (DoD)

A User Story or Task is only considered **Done** and eligible to be merged into `main` when:

- [x] Code is written in accordance with group style standards and clean code conventions.
- [x] Unit test coverage of **at least 80%** is achieved and passing with zero failures.
- [x] Feature is manually verified end-to-end against all specified **Acceptance Criteria**.
- [x] No open High or Critical severity bugs remain.
- [x] Code passes peer Code Review with **double sign-off**: Feature Team Lead + Weekly Program Lead.
- [x] Clean merge build and passing CI pipeline on the target branch.
- [x] The feature executes cleanly inside the unified Docker Compose environment (`docker compose up --build`).
- [x] Azure DevOps Work Items, Wiki, and documentation (`README.md`) are updated.
- [x] Product Owner (PO) signs off on completion.

---

## 4. Setup & Execution Instructions for Developers

### Prerequisites

Ensure the following tools are installed on your host machine before getting started:

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Version 20.10+ recommended, engine running)
* [Git](https://git-scm.com/) (Version 2.30+)
* Optional for local scripting/tooling: [Node.js](https://nodejs.org/) (v18+) and [Python](https://www.python.org/) (3.11+)

---

### Step 1: Clone the Repository

Clone the repository to your local workspace:

```bash
git clone <repository-url>
cd SoftwareEngineerMoodle
```

---

### Step 2: Configure Environment Variables

The project uses a root `.env` file to inject secrets and connection parameters into the containerized services.

1. Create your local `.env` file from the provided template:
   ```bash
   cp .env.example .env
   ```
   *(On Windows PowerShell: `Copy-Item .env.example .env`)*

2. Open `.env` and fill in the required credentials:
   ```env
   # Supabase Cloud Database & Storage Credentials
   SUPABASE_URL=https://<your-project-id>.supabase.co
   SUPABASE_KEY=<your-supabase-service-or-anon-key>

   # Google AI Studio / Gemini API Key
   GOOGLE_AI_KEY=<your-google-ai-studio-api-key>
   ```

> [!WARNING]
> **Never commit your `.env` file to Git.** The `.gitignore` file is configured to exclude `.env` to protect sensitive database tokens and AI keys.

---

### Step 3: Build & Launch with Docker Compose

To build all container images and launch the entire microservice ecosystem, execute:

```bash
docker compose up --build
```

#### Running in Detached Mode (Background)
If you prefer running the containers in the background so your terminal remains free:

```bash
docker compose up --build -d
```

#### Useful Docker Commands

* **View live logs across all services:**
  ```bash
  docker compose logs -f
  ```
* **View logs for a specific service:**
  ```bash
  docker compose logs -f backend-core
  docker compose logs -f backend-courses
  docker compose logs -f backend-ai
  docker compose logs -f frontend
  ```
* **Stop all containers:**
  ```bash
  docker compose down
  ```
* **Rebuild a single service after code changes:**
  ```bash
  docker compose up --build -d <service-name>
  ```
* **Stop and remove containers, networks, and orphaned volumes:**
  ```bash
  docker compose down -v
  ```

---

### Step 4: Verify Running Services & Access Endpoints

Once the containers are healthy, access the services via the following default local ports:

| Service | Container Name | Local Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **Frontend UI** | `frontend` | [http://localhost:3000](http://localhost:3000) | Web client portal for students, lecturers, and admins |
| **Core Service** | `backend-core` | [http://localhost:8000](http://localhost:8000) | Auth, RBAC, users, and session management |
| **Courses Service** | `backend-courses` | [http://localhost:8001](http://localhost:8001) | Courses, materials, submissions, and grades |
| **AI Assistant** | `backend-ai` | [http://localhost:8002](http://localhost:8002) | Gemini AI integration, feedback & summarization |

> [!TIP]
> Ensure ports `3000`, `8000`, `8001`, and `8002` are free on your host machine before starting Docker Compose.

---

## 5. Testing & Quality Assurance

Quality assurance is verified at multiple levels before code reaches the `main` branch.

### Unit Tests
Each backend service and the frontend includes unit testing frameworks (e.g., PyTest / Jest):
* **Requirement:** Minimum **80% code coverage** per service.
* Tests validate business logic, token validation, permission checks, and AI response sanitization.

### System & Integration Testing (E2E)
The project mandates at least **10 automated End-to-End integration tests** built using **Playwright** or **Selenium**, verifying cross-module system journeys:

1. **User Onboarding & 2FA Flow:** Registration &rarr; 2FA verification &rarr; Role assignment.
2. **Course Creation & Publishing:** Lecturer creates course &rarr; uploads syllabus &rarr; student views course in catalog.
3. **Assignment Publication:** Lecturer publishes assignment with rubric & deadline &rarr; notification sent.
4. **Student File Submission:** Student uploads homework file &rarr; backend validates format & stores in Supabase &rarr; status updates to "Submitted".
5. **AI Feedback Generation:** Student submission triggers `backend-ai` &rarr; automated review report generated and presented.
6. **Lecturer Review & Grade Sync:** Lecturer overrides/approves AI score &rarr; grade registered in database.
7. **Analytics Dashboard Sync:** Grade recorded &rarr; Analytics dashboard reflects new average and progress bar.
8. **Interactive AI Tutor Chat:** Student asks question regarding lecture slides &rarr; AI tutor returns contextual response.
9. **Role Permission Boundary Check:** Student attempts to access lecturer grading endpoint &rarr; access denied (HTTP 403).
10. **Peak Concurrency Simulation:** Multiple simulated users concurrently submitting assignments without HTTP 500 errors.

To run the automated E2E test suite:
```bash
# Example test invocation (Playwright)
npm run test:e2e
```

---

## 6. Git Branching Strategy & Scaled Agile Workflow

To ensure stability across 4 teams and weekly leadership rotations, the project enforces a standardized Git and Agile protocol:

### Branching Convention
* Work is strictly isolated in feature branches:
  ```
  feature/team<TeamNumber>-<StoryID>-<short-description>
  ```
  *Example:* `feature/team1-US102-user-2fa-verification`
  *Example:* `feature/team3-US305-gemini-assignment-feedback`

### Pull Request (PR) Policy
* **Direct pushes to `main` are strictly prohibited.**
* Every Pull Request requires **two mandatory approvals**:
  1. **Feature Team Lead:** Validates domain correctness and unit test coverage.
  2. **Weekly Program Lead:** Validates inter-service compatibility, green CI tests, and that `docker compose up --build` succeeds without errors.

### Weekly Agile Cadence
* **Daily Scrum:** 15-minute intra-team sync led by the internal Scrum Master.
* **Scrum of Scrums:** Bi-daily inter-team alignment led by the Weekly Program Lead to clear blockers.
* **Sprint Planning & Retrospective:** Bi-weekly / weekly sprints, velocity tracking, and comprehensive handover reporting on Azure DevOps Wiki.