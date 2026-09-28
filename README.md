
<style>
  @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Special+Elite&family=JetBrains+Mono:wght@400;700&display=swap');
  .konkred-root { background:#0a0908; color:#f4f1eb; font-family:'Special Elite','American Typewriter','Courier New',monospace; line-height:1.55; }
  .konkred-root h1,h2,h3,h4 { font-family:'Archivo Black','Arial Black','Helvetica Neue',sans-serif; color:#f4f1eb; letter-spacing:-0.5px; margin-top:2rem; border-left:4px solid #d60019; padding-left:16px; text-transform:none; }
  .konkred-root h1 { font-size:3.2rem; line-height:0.95; letter-spacing:-2px; margin-bottom:0.2rem; }
  .konkred-root h2 { font-size:1.6rem; color:#ff1a2e; border-bottom:1.5px solid #262221; padding-bottom:0.4rem; margin-top:2.5rem; }
  .konkred-root h3 { font-size:1.1rem; font-family:'JetBrains Mono',monospace; color:#b7b2a9; border-left-color:#ff1a2e; text-transform:uppercase; letter-spacing:1.5px; }
  .konkred-root p { color:#eae7e1; font-family:'Special Elite',monospace; font-size:15px; }
  .konkred-root a { color:#ff1a2e; text-decoration:none; border-bottom:1px solid #3a201f; }
  .konkred-root a:hover { color:#f4f1eb; border-bottom-color:#d60019; }
  .konkred-root code, .konkred-root pre { font-family:'JetBrains Mono',monospace; background:#100e0d; color:#f4f1eb; border:1px solid #262221; padding:2px 6px; font-size:0.9em; border-radius:0; }
  .konkred-root pre { padding:14px; overflow-x:auto; border-left:3px solid #d60019; }
  .konkred-root table { width:100%; border-collapse:collapse; font-family:'JetBrains Mono',monospace; font-size:13px; margin:1.2rem 0; }
  .konkred-root th { background:#171514; color:#f4f1eb; text-align:left; padding:8px 14px; border-bottom:1.5px solid #d60019; font-family:'Archivo Black',sans-serif; text-transform:uppercase; font-size:11px; letter-spacing:1px; }
  .konkred-root td { padding:8px 14px; border-bottom:1px solid #262221; color:#eae7e1; vertical-align:top; }
  .konkred-root tr:hover td { background:#0d0c0b; }
  .konkred-root hr { border:0; height:1px; background:#2a2624; margin:2rem 0; }
  .konkred-root blockquote { border-left:3px solid #d60019; background:#100e0d; margin:1rem 0; padding:14px 18px; color:#b7b2a9; font-style:italic; }
  .konkred-root .diamond { display:inline-block; color:#d60019; font-weight:bold; margin-right:6px; }
  .konkred-root .label-mono { font-family:'JetBrains Mono',monospace; font-size:10px; color:#7a756d; text-transform:uppercase; letter-spacing:1.2px; }
  .konkred-root img { border:1px solid #262221; background:#0c0b0a; }
</style>

<div class="konkred-root">

<!--
  FABLE OMEGA
  Multi-Tenant Telegram Scenario Runtime

  KONKRED documentation standard:
  - Claims must be reproducible.
  - Benchmarks must reference committed reports.
  - Scenario compatibility is not presented as live deployment.
  - Proposed BotFather identities are examples, not active bots.
  - Generated reports must include environment and timestamp metadata.
-->

<div align="center">

# <span style="color:#f4f1eb;">FABLE OMEGA</span>

### <span style="color:#ff1a2e;">MULTI-TENANT TELEGRAM SCENARIO RUNTIME</span>  
### <span style="color:#b7b2a9;">445 CATALOGUED SCENARIOS · 15 STRATEGIC HUBS · ONE ASYNC CONTROL PLANE</span>

<br>

[![Python](https://img.shields.io/badge/PYTHON-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=090A0D)](https://python.org)
[![FastAPI](https://img.shields.io/badge/CONTROL_PLANE-FASTAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=090A0D)](https://fastapi.tiangolo.com)
[![Runtime](https://img.shields.io/badge/RUNTIME-ASYNCIO-19D3C5?style=for-the-badge&labelColor=090A0D)](#runtime-architecture)
[![Storage](https://img.shields.io/badge/STATE-SQLITE_WAL-8B6BFF?style=for-the-badge&logo=sqlite&logoColor=white&labelColor=090A0D)](#state-and-persistence)
[![Container](https://img.shields.io/badge/DEPLOYMENT-DOCKER-2496ED?style=for-the-badge&logo=docker&logoColor=white&labelColor=090A0D)](#deployment)
[![Verification](https://img.shields.io/badge/VERIFICATION-REPORT_LINKED-A9E838?style=for-the-badge&labelColor=090A0D)](./tests/FULL_FLEET_TEST_REPORT.json)

<br>

> <span style="font-family:'Special Elite',monospace;">A shared execution kernel for organizing, loading, simulating, and verifying a large catalogue of Telegram bot scenarios without assigning a dedicated process to every scenario.</span>

</div>

---

## <span class="diamond">◆</span> 00 / OPERATING DEFINITION

<span style="font-family:'JetBrains Mono',monospace; color:#ff1a2e;">FABLE OMEGA</span> is an <strong>experimental</strong> Telegram automation control plane.

It converts a large collection of bot ideas and scenario definitions into a smaller set of strategic hubs backed by shared infrastructure:

- one asynchronous runtime;
- one multi-tenant dispatcher;
- one state and persistence layer;
- one credit and payment abstraction;
- one administrative control plane;
- one catalogue and scenario registry;
- one verification interface.

The project is designed to test whether hundreds of bot scenarios can share infrastructure without requiring hundreds of permanently running Python processes.

It does <strong>not</strong> claim that 445 independently registered Telegram bots are currently deployed, publicly reachable, or simultaneously connected to BotFather tokens.

The number <code>445</code> refers to catalogue entries and scenario definitions indexed by the repository and exercised through a common compatibility lifecycle.

---

## <span class="diamond">◆</span> 01 / THE PROBLEM

A conventional bot-per-process model scales poorly when a product catalogue grows.

For every separately deployed bot, the operator may need another:

- Python process;
- Telegram token;
- database connection;
- payment implementation;
- state machine;
- logging pipeline;
- deployment unit;
- monitoring surface;
- retry policy;
- administrator interface.

Even when most bots are idle, each service may continue consuming memory and operational attention.

The problem is not only infrastructure cost. Fragmentation creates inconsistent behavior:

- payment rules drift between bots;
- user balances become difficult to reconcile;
- bug fixes must be repeated;
- logs are distributed across deployments;
- rate limits are implemented differently;
- state recovery is unpredictable;
- catalogue-wide changes become expensive.

FABLE OMEGA explores a different model:

```text
MANY SCENARIO DEFINITIONS
          │
          ▼
A SMALL NUMBER OF PRODUCT HUBS
          │
          ▼
ONE SHARED ASYNCHRONOUS RUNTIME


---

## <span class="diamond">◆</span> 02 / DESIGN POSITION

The project separates four concepts that are often incorrectly treated as the same thing.

| Concept | Meaning |
|---|---|
| **Scenario** | A catalogue entry describing a bot workflow or product behavior |
| **Archetype** | A reusable implementation pattern shared by similar scenarios |
| **Hub** | A strategic Telegram product surface grouping related scenarios |
| **Runtime** | The shared process responsible for dispatch, state, credits, and execution |

A scenario does not require its own process.

A hub does not imply that every contained scenario is production-complete.

A successful compatibility test proves that a scenario can pass the shared lifecycle contract. It does not prove availability of every external API, payment provider, Telegram identity, or third-party integration.

---

## <span class="diamond">◆</span> 03 / SYSTEM ARCHITECTURE

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                         TELEGRAM / WEB INGRESS                           │
│                                                                          │
│  Telegram updates · Dashboard simulator · Administrative API requests    │
└─────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         MULTI-TENANT DISPATCHER                          │
│                                                                          │
│  Tenant resolution · Hub selection · Scenario lookup · Rate admission    │
└──────────────┬──────────────────────┬───────────────────────┬────────────┘
               │                      │                       │
               ▼                      ▼                       ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌──────────────────────┐
│ SCENARIO REGISTRY   │  │ SESSION / FSM       │  │ CREDIT / PAYMENT     │
│                     │  │                     │  │                      │
│ 445 catalogue items │  │ User state          │  │ Balance operations   │
│ Archetype mapping   │  │ Workflow position   │  │ Order state          │
│ Hub assignment      │  │ Expiration policy   │  │ Payment abstraction  │
└──────────┬──────────┘  └──────────┬──────────┘  └──────────┬───────────┘
           │                        │                        │
           └────────────────────────┼────────────────────────┘
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        ASYNCHRONOUS EXECUTION KERNEL                     │
│                                                                          │
│ Lazy scenario activation · LRU pool · bounded concurrency · lifecycle    │
└─────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                              SQLITE WAL                                 │
│                                                                          │
│ Users · sessions · orders · credits · audit events · runtime metadata    │
└──────────────────────────────────────────────────────────────────────────┘
```

### Request lifecycle

```text
01  RECEIVE
    Telegram update or simulator request enters the control plane.

02  RESOLVE
    Dispatcher identifies tenant, hub, scenario, user, and active session.

03  ADMIT
    Rate limiter and access rules decide whether execution may continue.

04  LOAD
    Runtime resolves the scenario implementation or reusable archetype.

05  EXECUTE
    Scenario reads state, processes input, and produces a normalized result.

06  ACCOUNT
    Credit or payment state is evaluated where the scenario requires it.

07  PERSIST
    Updated FSM, order, credit, and audit state are written to SQLite.

08  RESPOND
    A normalized response is returned to Telegram or the web simulator.
```

---

## <span class="diamond">◆</span> 04 / STRATEGIC HUB MODEL

The catalogue is organized into 15 product hubs.

The identifiers below are proposed deployment identities. They should not be interpreted as active or reserved BotFather usernames.

| ID | Strategic hub | Proposed identity | Catalogue count | Primary scope |
|:---:|---|---|---:|---|
| `01` | Commerce and order processing | `@Omni_Commerce_SuperBot` | 48 | Digital products, physical orders, invoices, shipment status |
| `02` | VIP subscription and access | `@Omni_Paywall_SuperBot` | 36 | Paid channels, temporary links, affiliate access |
| `03` | AI production studio | `@Omni_AI_Studio_SuperBot` | 95 | Writing, translation, rewriting, coding, media assistance |
| `04` | Coding sandbox and exercises | `@Omni_Kata_Runner_SuperBot` | 24 | Programming challenges, evaluation, isolated execution concepts |
| `05` | Compliance and expiry tracking | `@Omni_Compliance_SuperBot` | 22 | Domains, SSL, contracts, licences, insurance, due dates |
| `06` | Finance and cryptocurrency | `@Omni_Fintech_SuperBot` | 28 | Price alerts, portfolio scenarios, currency monitoring |
| `07` | Education and spaced repetition | `@Omni_Edu_Master_SuperBot` | 26 | Language learning, flashcards, quizzes, examination workflows |
| `08` | Growth and lead generation | `@Omni_Growth_SuperBot` | 21 | Campaigns, referrals, lead organization, promotional tools |
| `09` | Health and habit tracking | `@Omni_Health_Habit_SuperBot` | 18 | Habit lists, water tracking, calorie and routine scenarios |
| `10` | Property and rental operations | `@Omni_RealEstate_SuperBot` | 15 | Rent reminders, maintenance records, document organization |
| `11` | Document intelligence | `@Omni_Doc_Search_SuperBot` | 19 | Extraction, summarization, document lookup, knowledge workflows |
| `12` | Media utilities | `@Omni_Media_Studio_SuperBot` | 17 | Compression, watermarking, conversion, media processing concepts |
| `13` | Iranian local services | `@Omni_Local_Iran_SuperBot` | 35 | Local messaging, payment-review, SMS and form workflows |
| `14` | Games and prediction leagues | `@Omni_Game_League_SuperBot` | 16 | Group competitions, rankings, predictions, reward structures |
| `15` | Agency and bot delivery | `@Omni_Agency_Factory_SuperBot` | 26 | Client provisioning, licences, templates, agency operations |

> <span style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#5c5852;">📖 **جزئیات کامل فنی و ماتریس نگاشت را در [MEGA_HUB_ARCHITECTURE_BLUEPRINT.md](./MEGA_HUB_ARCHITECTURE_BLUEPRINT.md) مطالعه فرمایید.**</span>

---

## <span class="diamond">◆</span> 05 / RUNTIME ARCHITECTURE

### Shared AsyncIO kernel

The execution layer uses one asynchronous process rather than assigning a permanent process to every catalogue entry.

The intended benefits are:

- lower idle memory;
- centralized observability;
- shared database connections;
- reusable payment logic;
- consistent rate limiting;
- simpler deployment;
- faster catalogue-wide fixes.

### Lazy scenario activation

Scenario implementations are activated when requested rather than permanently initialized.

```text
REQUEST
   │
   ▼
REGISTRY LOOKUP
   │
   ├── Active instance exists ──► reuse
   │
   └── Not active ──────────────► load archetype
                                      │
                                      ▼
                                  initialize
                                      │
                                      ▼
                                  LRU pool
```

### LRU runtime pool

The runtime can retain frequently used scenario objects while allowing inactive entries to leave the active pool.

This controls memory growth without removing catalogue metadata.

### Bounded concurrency

Concurrent execution must remain bounded. A shared runtime should not create an unlimited task for every incoming event.

The architecture provides a place for:

- concurrency semaphores;
- per-tenant limits;
- per-user rate limits;
- hub-specific admission rules;
- timeout enforcement;
- backpressure.

### Micro-batched persistence

Where safe, low-priority persistence operations may be grouped to reduce disk churn.

Financial state, credit deductions, and order transitions must retain transactional guarantees and should not rely on unsafe delayed writes.

---

## <span class="diamond">◆</span> 06 / STATE AND PERSISTENCE

SQLite is configured for WAL-oriented operation to support the local and low-resource deployment model.

The persistence layer is responsible for:

- user records;
- tenant association;
- FSM sessions;
- active scenario state;
- balances and credits;
- orders;
- payment-review state;
- runtime events;
- audit records.

### Why SQLite

SQLite is appropriate for:

- local development;
- demonstration;
- single-host pilots;
- low-cost deployments;
- deterministic test environments.

It is not presented as a universal replacement for PostgreSQL or another network database.

A multi-instance deployment requires additional coordination, a shared database, or an explicit single-writer architecture.

### State contract

Each scenario interacts with normalized state rather than owning an independent database format.

```python
{
    "tenant_id": "hub-03",
    "scenario_id": "ai-writing-001",
    "user_id": "telegram-user-id",
    "fsm_state": "awaiting_input",
    "credits": 120,
    "metadata": {},
    "updated_at": "ISO-8601 timestamp"
}
```

---

## <span class="diamond">◆</span> 07 / CREDIT AND PAYMENT ABSTRACTION

The repository includes a shared monetization layer intended to prevent every scenario from reimplementing billing.

Supported or modelled channels may include:

- Telegram Stars;
- manually reviewed card-to-card payments;
- TON-oriented payment flows;
- VIP or temporary access links;
- internal credits.

These channels do not all provide the same level of automation or verification.

### Financial safety requirements

Before a real deployment:

- provider callbacks must be authenticated;
- payment identifiers must be unique;
- replayed confirmations must not grant credit twice;
- balance updates must be transactional;
- manual receipt approval must be recorded;
- administrator actions must be auditable;
- secrets must remain outside the repository;
- currency conversion rules must be explicit.

The shared layer provides an architectural foundation. Production use still requires provider-specific compliance, implementation, and review.

---

## <span class="diamond">◆</span> 08 / CONTROL PLANE AND SIMULATOR

The FastAPI control plane exposes an operator-facing surface for inspecting the catalogue and exercising scenario behavior.

### Dashboard capabilities

- Browse the scenario catalogue
- Filter entries by source or category
- Select a scenario
- Create a simulated user session
- Send text input
- Exercise callback-style actions
- Inspect normalized responses
- Review state changes
- Inspect runtime and memory telemetry
- View active scenario objects
- Trigger controlled cache cleanup
- Review orders and manual payment states

### Why a simulator exists

The simulator allows the shared runtime to be tested without registering hundreds of Telegram identities.

It is useful for:

- compatibility testing;
- product review;
- handler development;
- state inspection;
- demonstrations;
- regression checks.

A simulator is not proof of live Telegram deployment.

---

## <span class="diamond">◆</span> 09 / VERIFICATION

The repository includes a catalogue-wide compatibility suite.

The main report is stored at:

```text
tests/FULL_FLEET_TEST_REPORT.json
```

The suite exercises scenario definitions through a shared lifecycle.

### Compatibility lifecycle

```text
STAGE 01 — INITIALIZE
Resolve the scenario and create a compatible execution context.

STAGE 02 — STATE
Create, read, or update the scenario FSM state.

STAGE 03 — INPUT
Pass normalized user input through the scenario interface.

STAGE 04 — CREDIT
Exercise the credit-related branch where applicable.

STAGE 05 — ORDER / PAYMENT STATE
Validate the scenario's normalized commercial state transition.
```

### What a passing result means

A passing result indicates that the scenario definition:

- can be indexed;
- can be resolved;
- conforms to the runtime interface;
- can participate in the shared lifecycle;
- does not fail the tested state transitions.

### What it does not mean

A passing compatibility result does not prove that:

- a public Telegram bot is online;
- a BotFather token exists;
- every external provider is available;
- every payment channel is connected;
- every scenario is production-complete;
- live concurrent user behavior has been validated;
- third-party terms permit every proposed workflow.

### Running the verification suite

```bash
python3 tests/test_all_445_bots.py
```

### Running the resource benchmark

```bash
python3 tests/test_low_resource_runtime.py
```

Generated reports should be treated as environment-specific artifacts.

Benchmark claims must be accompanied by:

- timestamp;
- Python version;
- operating system;
- processor information;
- available memory;
- test parameters;
- concurrency level;
- commit hash.

---

## <span class="diamond">◆</span> 10 / PERFORMANCE REPORTING

The repository contains a low-resource benchmark report:

```text
tests/LOW_RESOURCE_BENCHMARK_REPORT.json
```

Performance values in that report describe a particular test environment. They are not universal guarantees.

The following distinction matters:

| Measurement | Interpretation |
|---|---|
| Catalogue lifecycle latency | Time required for a local simulated scenario lifecycle |
| Event-loop delay | Scheduling behavior in the tested Python process |
| Request throughput | Performance of the tested local workload |
| Process memory | Memory measured under the report’s runtime conditions |
| Disk-I/O reduction | Relative behavior under the benchmark’s write pattern |

External Telegram latency, AI-provider latency, network behavior, database contention, and payment callbacks are not represented by a purely local compatibility benchmark.

---

## <span class="diamond">◆</span> 11 / REPOSITORY STRUCTURE

```text
.
├── README.md
├── MEGA_HUB_ARCHITECTURE_BLUEPRINT.md
├── pyproject.toml
├── requirements.txt
├── run.py
├── .env.example
│
├── src/
│   ├── bots/
│   │   ├── bot_01_commerce.py
│   │   ├── bot_02_vip_paywall.py
│   │   ├── bot_03_ai_gateway.py
│   │   ├── bot_04_kata_runner.py
│   │   ├── bot_05_license_reminder.py
│   │   └── dynamic_bot.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dispatcher.py
│   │   ├── fsm.py
│   │   ├── hub_router.py
│   │   ├── monetization.py
│   │   ├── omni_catalog.py
│   │   ├── rate_limiter.py
│   │   └── resource_optimizer.py
│   │
│   └── web/
│       ├── app.py
│       └── templates/
│           └── dashboard.html
│
├── docs/
│   └── original_blueprints/
│
├── deploy/
│   ├── Dockerfile.slim
│   ├── docker-compose.yml
│   ├── run_optimized.sh
│   ├── provision_botfather.py
│   ├── batch_set_webhook.py
│   ├── nginx/
│   │   └── all-them-bots.conf
│   └── systemd/
│       └── all-them-bots.service
│
└── tests/
    ├── test_all_445_bots.py
    ├── test_low_resource_runtime.py
    ├── test_artifacts.py
    ├── test_bots_live.py
    ├── test_executor.py
    ├── test_llm.py
    ├── test_store.py
    ├── FULL_FLEET_TEST_REPORT.json
    └── LOW_RESOURCE_BENCHMARK_REPORT.json
```

---

## <span class="diamond">◆</span> 12 / QUICK START

### Requirements

- Python 3.11 or newer
- Linux, macOS, or a compatible container environment
- Git
- Optional: Docker and Docker Compose

### Clone

```bash
git clone https://github.com/reARbitRA/all-them-bots.git
cd all-them-bots
```

### Create an isolated environment

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
```

### Install dependencies

Use the dependency path supported by the repository:

```bash
python -m pip install -r requirements.txt
```

For development dependencies defined in `pyproject.toml`:

```bash
python -m pip install -e '.[dev]'
```

### Configure the environment

```bash
cp .env.example .env
```

Do not commit `.env`.

Review every default before enabling:

- Telegram integrations
- payment behavior
- administrator access
- public network binding
- webhook registration
- external AI providers

### Start the application

```bash
python run.py
```

Or use the optimized launcher:

```bash
./deploy/run_optimized.sh
```

The local control plane is expected to become available at:

```text
http://localhost:8000
```

---

## <span class="diamond">◆</span> 13 / TESTING

Run the complete test suite:

```bash
pytest -q
```

Run the catalogue compatibility suite directly:

```bash
python3 tests/test_all_445_bots.py
```

Run the low-resource benchmark:

```bash
python3 tests/test_low_resource_runtime.py
```

Run static lint checks when development dependencies are installed:

```bash
ruff check src tests
```

A production CI pipeline should run:

```text
01  dependency installation
02  static analysis
03  unit tests
04  catalogue compatibility
05  report-schema validation
06  container build
07  local health check
08  artifact retention
```

---

## <span class="diamond">◆</span> 14 / DEPLOYMENT

### Docker Compose

```bash
docker compose -f deploy/docker-compose.yml up -d
```

Inspect logs:

```bash
docker compose -f deploy/docker-compose.yml logs -f
```

Stop the stack:

```bash
docker compose -f deploy/docker-compose.yml down
```

### Systemd

The repository contains an example service unit:

```text
deploy/systemd/all-them-bots.service
```

Treat it as a deployment template. Before installing it, review:

- service user;
- working directory;
- environment file;
- writable paths;
- memory limits;
- restart behavior;
- network permissions.

### Nginx

An example reverse-proxy configuration is available at:

```text
deploy/nginx/all-them-bots.conf
```

Production deployment requires:

- a real hostname;
- TLS certificates;
- restricted administrative routes;
- trusted proxy configuration;
- request-size limits;
- rate limits;
- secure headers;
- log-retention policy.

---

## <span class="diamond">◆</span> 15 / TELEGRAM PROVISIONING

Provisioning scripts are operational tools, not an invitation to create hundreds of Telegram accounts or bypass platform limits.

Before using them:

1. Review Telegram’s current terms.
2. Confirm BotFather and account limits.
3. Start with one controlled pilot hub.
4. Use manual approval for new identities.
5. Store tokens in a secret manager.
6. Never commit exported tokens.
7. Avoid unsolicited messaging.
8. Apply per-user and per-chat rate limits.

Recommended rollout:

```text
PHASE 01  Dashboard-only simulation
PHASE 02  One private Telegram pilot
PHASE 03  One strategic hub
PHASE 04  Payment sandbox
PHASE 05  Limited external users
PHASE 06  Measured expansion
```

---

## <span class="diamond">◆</span> 16 / SECURITY MODEL

### Secrets

Secrets must be loaded through environment variables or an external secret manager.

Do not commit:

- Telegram bot tokens;
- payment credentials;
- administrator keys;
- AI-provider keys;
- webhook secrets;
- session exports;
- user data.

### Administrative control plane

Before exposing the dashboard:

- require authentication;
- separate read and write permissions;
- restrict payment approval;
- log administrator actions;
- disable development routes;
- configure trusted origins;
- place the service behind TLS;
- prevent public access to debug endpoints.

### Rate limiting

Rate limits should exist at multiple levels:

- source IP;
- Telegram user;
- Telegram chat;
- tenant;
- strategic hub;
- scenario;
- external provider.

### Payment integrity

Credit grants must be idempotent.

A repeated payment callback, repeated administrator click, or replayed request must not grant balance more than once.

### Data protection

Production deployment should define:

- retention periods;
- account deletion;
- log redaction;
- backup policy;
- encryption policy;
- operator access;
- incident response;
- user-consent boundaries.

---

## <span class="diamond">◆</span> 17 / VERIFIED BOUNDARIES

The following boundaries are intentional.

### Verified in the repository

- Catalogue indexing
- Hub classification
- Shared lifecycle compatibility
- Async runtime structure
- SQLite-oriented persistence
- FastAPI control-plane implementation
- Test and benchmark report generation
- Docker and deployment templates

### Requires deployment-specific verification

- Real Telegram webhook behavior
- External AI providers
- Payment-provider callbacks
- BotFather provisioning
- High-concurrency public traffic
- Multi-instance database behavior
- Long-running memory stability
- Platform terms and legal compliance
- Every scenario’s third-party dependency

### Not claimed

- 445 public bots currently online
- 445 independently deployed production services
- Zero risk of Telegram restrictions
- Guaranteed memory consumption on every host
- Guaranteed throughput under external API traffic
- Guaranteed revenue or conversion
- Complete production readiness for every catalogue entry.

---

## <span class="diamond">◆</span> 18 / ROADMAP

### Phase 1 — Repository consistency

- Remove unrelated Autofreelance documentation
- Align `pyproject.toml` metadata with FABLE OMEGA
- Add a single canonical application name
- Add a license file
- Add report-schema validation
- Add CI under `.github/workflows`

### Phase 2 — Runtime hardening

- Add bounded worker pools
- Add structured cancellation
- Add timeout budgets
- Add tenant-level quotas
- Add transactional credit operations
- Add event audit records
- Add graceful shutdown tests

### Phase 3 — Telegram pilot

- Deploy one private hub
- Connect one bot token
- Verify webhook behavior
- Measure real idle memory
- Test recovery after restart
- Compare simulator and Telegram results

### Phase 4 — Payment sandbox

- Implement one provider completely
- Add signed callbacks
- Add replay protection
- Add reconciliation reports
- Add refund and dispute states

### Phase 5 — Observability

- Structured JSON logging
- Request correlation IDs
- Prometheus-compatible metrics
- Runtime pool telemetry
- Database health checks
- Scenario failure dashboards

---

## <span class="diamond">◆</span> 19 / PROJECT POSITIONING

FABLE OMEGA should be evaluated as:

- a runtime architecture experiment;
- a large scenario catalogue;
- a multi-tenant Telegram control plane;
- a compatibility-testing framework;
- a low-resource deployment study.

It should not be evaluated as evidence that hundreds of independent public bots are already operating in production.

That distinction protects the technical credibility of the project.

---

## <span class="diamond">◆</span> 20 / CONTRIBUTING

Contributions should preserve the shared scenario contract.

A new scenario should include:

- stable identifier;
- title and category;
- strategic hub assignment;
- source attribution;
- normalized input contract;
- normalized output contract;
- initial FSM state;
- credit behavior where applicable;
- lifecycle compatibility coverage;
- explicit external dependencies.

Suggested workflow:

```bash
git checkout -b feature/scenario-name
ruff check src tests
pytest -q
python3 tests/test_all_445_bots.py
git commit -m "Add scenario: scenario-name"
```

Do not include secrets, production user data, private Telegram exports, or unlicensed source material.

---

## <span class="diamond">◆</span> 21 / LICENSE

A repository-level `LICENSE` file should define the actual terms.

Until a license file is committed, users should not assume that badges or README text grant permission to copy, redistribute, or commercially deploy the source code.

Avoid presenting the project as both MIT and commercially restricted at the same time.

Choose one explicit licensing model and keep these locations consistent:

- `LICENSE`
- `README.md`
- `pyproject.toml`
- package metadata;
- deployment documentation

---

<div align="center" style="font-family:'Archivo Black',sans-serif; color:#f4f1eb; letter-spacing:-1px; font-size:2rem; border-top:1.5px solid #d60019; padding-top:2rem; margin-top:3rem;">

## <span style="color:#ff1a2e;">FABLE OMEGA</span>

**<span style="color:#b7b2a9;">CATALOGUE THE WORK · SHARE THE RUNTIME · MEASURE THE CLAIMS</span>**

</div>

<div align="center" style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#5c5852; margin-top:10px;">

[Open Architecture Blueprint](./MEGA_HUB_ARCHITECTURE_BLUEPRINT.md) ·
[Inspect Fleet Report](./tests/FULL_FLEET_TEST_REPORT.json) ·
[Inspect Benchmark](./tests/LOW_RESOURCE_BENCHMARK_REPORT.json)

<sub>
Experimental infrastructure for controlled Telegram scenario execution.<br>
No anti-spam claims. No deployment theatre. No metric without an artifact.
</sub>

</div>

</div>
```
