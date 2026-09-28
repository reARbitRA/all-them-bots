<!--
  FABLE OMEGA
  Multi-Tenant Telegram Scenario Runtime

  theme · Black #0A0908 · Red #D60019 · Ink #F4F1EB
  Type: Archivo Black (display) · Special Elite (prose) · JetBrains Mono (machine)

  A brutalist industrial dark theme: chalk-grained black canvas, deep-red
  signal, typewriter-white prose. Red means signal and live state, never
  danger. The background never glows — only verified claims ignite.

  KONKRED documentation standard (applies to this README):
  - Claims must be reproducible.
  - Benchmarks must reference committed reports.
  - Scenario compatibility is not presented as live deployment.
  - Proposed BotFather identities are examples, not active bots.
  - Generated reports must include environment and timestamp metadata.
  - Badges stay on-palette: label #0A0908 · message #0A0908 · logo #D60019.
  - No emoji. Red is signal. Numbers without an artifact are decoration.
-->

<div align="center">

# FABLE OMEGA

### MULTI-TENANT TELEGRAM SCENARIO RUNTIME
### 445 CATALOGUED SCENARIOS · 15 STRATEGIC HUBS · ONE ASYNC CONTROL PLANE

[![PYTHON](https://img.shields.io/badge/PYTHON-3.11%2B-0A0908?style=for-the-badge&logo=python&logoColor=D60019&labelColor=0A0908)](https://www.python.org)
[![RUNTIME](https://img.shields.io/badge/RUNTIME-ASYNCIO-0A0908?style=for-the-badge&logo=python&logoColor=D60019&labelColor=0A0908)](#05--runtime-architecture)
[![CONTROL_PLANE](https://img.shields.io/badge/CONTROL_PLANE-FASTAPI-0A0908?style=for-the-badge&logo=fastapi&logoColor=D60019&labelColor=0A0908)](https://fastapi.tiangolo.com)
[![STATE](https://img.shields.io/badge/STATE-SQLITE_WAL-0A0908?style=for-the-badge&logo=sqlite&logoColor=D60019&labelColor=0A0908)](#06--state-and-persistence)
[![DEPLOYMENT](https://img.shields.io/badge/DEPLOYMENT-DOCKER-0A0908?style=for-the-badge&logo=docker&logoColor=D60019&labelColor=0A0908)](#14--deployment)
[![VERIFICATION](https://img.shields.io/badge/VERIFICATION-REPORT_LINKED-D60019?style=for-the-badge&logo=pytest&logoColor=0A0908&labelColor=0A0908)](./tests/FULL_FLEET_TEST_REPORT.json)
[![CLAIMS](https://img.shields.io/badge/CLAIMS-REPRODUCIBLE_OR_ABSENT-0A0908?style=for-the-badge&logo=readme&logoColor=D60019&labelColor=0A0908)](#17--verified-boundaries)

<br>

> A shared execution kernel for organizing, loading, simulating, and verifying
> a large catalogue of Telegram bot scenarios without assigning a dedicated
> process to every scenario.

`in:` `A CATALOGUE OF 445 BOT SCENARIOS` → `out:` `ONE SHARED ASYNC RUNTIME`

**STATUS:** `EXPERIMENTAL RUNTIME` · `CATALOGUE: COMPATIBILITY-PASSED` · `TELEGRAM PILOT: NOT DEPLOYED`

[Definition](#00--operating-definition) ·
[Problem](#01--the-problem) ·
[Architecture](#03--system-architecture) ·
[Hubs](#04--strategic-hub-model) ·
[Verification](#09--verification) ·
[Quick Start](#12--quick-start) ·
[Boundaries](#17--verified-boundaries) ·
[License](#21--license)

</div>

---

## 00 / OPERATING DEFINITION

FABLE OMEGA is an experimental Telegram automation control plane.

It converts a large collection of bot ideas and scenario definitions into a smaller set of strategic hubs backed by shared infrastructure:

- one asynchronous runtime;
- one multi-tenant dispatcher;
- one state and persistence layer;
- one credit and payment abstraction;
- one administrative control plane;
- one catalogue and scenario registry;
- one verification interface.

The project is designed to test whether hundreds of bot scenarios can share infrastructure without requiring hundreds of permanently running Python processes.

It does **not** claim that 445 independently registered Telegram bots are currently deployed, publicly reachable, or simultaneously connected to BotFather tokens.

The number `445` refers to catalogue entries and scenario definitions indexed by the repository and exercised through a common compatibility lifecycle.

> A SCENARIO IS NOT A PROCESS. A HUB IS NOT A PRODUCT.
> A PASSING TEST IS NOT A DEPLOYMENT.

---

## 01 / THE PROBLEM

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
```

---

## 02 / DESIGN POSITION

The project separates four concepts that are often incorrectly treated as the same thing.

| Concept | Meaning |
|---|---|
| **Scenario** | A catalogue entry describing a bot workflow or product behavior |
| **Archetype** | A reusable implementation pattern shared by similar scenarios |
| **Hub** | A strategic Telegram product surface grouping related scenarios |
| **Runtime** | The shared process responsible for dispatch, state, credits, and execution |

- A scenario does not require its own process.
- A hub does not imply that every contained scenario is production-complete.
- A successful compatibility test proves that a scenario can pass the shared lifecycle contract. It does not prove availability of every external API, payment provider, Telegram identity, or third-party integration.

---

## 03 / SYSTEM ARCHITECTURE

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
│                              SQLITE WAL                                  │
│                                                                          │
│ Users · sessions · orders · credits · audit events · runtime metadata    │
└──────────────────────────────────────────────────────────────────────────┘
```

### Request lifecycle

```text
01  RECEIVE    Telegram update or simulator request enters the control plane.
02  RESOLVE    Dispatcher identifies tenant, hub, scenario, user, session.
03  ADMIT      Rate limiter and access rules decide whether execution continues.
04  LOAD       Runtime resolves the scenario implementation or archetype.
05  EXECUTE    Scenario reads state, processes input, produces a normalized result.
06  ACCOUNT    Credit or payment state is evaluated where the scenario requires it.
07  PERSIST    FSM, order, credit, and audit state are written to SQLite.
08  RESPOND    A normalized response is returned to Telegram or the web simulator.
```

---

## 04 / STRATEGIC HUB MODEL

The catalogue is organized into 15 product hubs.

The identifiers below are proposed deployment identities. They should not be interpreted as active or reserved BotFather usernames.

<!--
  NOTE: hub rows below sum to 446, not 445.
  Reconcile with the catalogue index in src/core/omni_catalog.py
  before the next verification run. Fix the source of truth first.
-->

| ID | STRATEGIC HUB | PROPOSED IDENTITY | SCENARIOS | PRIMARY SCOPE |
|:---:|---|---|---:|---|
| `01` | COMMERCE & ORDER INTAKE | `@Omni_Commerce_SuperBot` | **48** | Digital and physical storefronts, auto-invoicing, shipment tracking |
| `02` | VIP SUBSCRIPTION & ACCESS | `@Omni_Paywall_SuperBot` | **36** | Paid channels, one-shot invite links, auto-expiry, affiliate access |
| `03` | AI PRODUCTION STUDIO | `@Omni_AI_Studio_SuperBot` | **95** | Writing, translation, rewriting, coding, media assistance |
| `04` | CODE SANDBOX & KATA | `@Omni_Kata_Runner_SuperBot` | **24** | Isolated execution drills, algorithm practice, automated grading |
| `05` | COMPLIANCE & EXPIRY WATCH | `@Omni_Compliance_SuperBot` | **22** | Domains, SSL, servers, contracts, licences, insurance due dates |
| `06` | FINTECH & CRYPTO | `@Omni_Fintech_SuperBot` | **28** | USDT alerts, wallet monitoring, gold and FX signals |
| `07` | EDUCATION & SPACED REPETITION | `@Omni_Edu_Master_SuperBot` | **26** | Leitner box, competitive quizzes, online examinations |
| `08` | GROWTH & LEAD-GEN | `@Omni_Growth_SuperBot` | **21** | B2B lead scraping, referral campaigns, promotional tools |
| `09` | HEALTH & HABIT TRACKING | `@Omni_Health_Habit_SuperBot` | **18** | Calorie and macro, water tracker, habit checklist, training plans |
| `10` | PROPERTY & RENTAL OPS | `@Omni_RealEstate_SuperBot` | **15** | Rent reminders, maintenance intake, lease document archive |
| `11` | DOCUMENT INTELLIGENCE | `@Omni_Doc_Search_SuperBot` | **19** | PDF extraction, corporate summarization, document lookup |
| `12` | MEDIA UTILITIES | `@Omni_Media_Studio_SuperBot` | **17** | Compression, background removal, watermarking, conversion |
| `13` | IRANIAN LOCAL SERVICES | `@Omni_Local_Iran_SuperBot` | **35** | Card-to-card with receipt review, SMS web services, sales forms |
| `14` | GAMES & PREDICTION LEAGUES | `@Omni_Game_League_SuperBot` | **16** | Friend leagues, standings, group prediction rewards |
| `15` | AGENCY & BOT FACTORY | `@Omni_Agency_Factory_SuperBot` | **26** | One-click client delivery, auto-licensing, agency operations |

The hub model reduces Telegram identity sprawl while allowing related scenarios to reuse menus, accounts, credits, payment policies, and infrastructure.

> Full technical detail and the mapping matrix live in
> [MEGA_HUB_ARCHITECTURE_BLUEPRINT.md](./MEGA_HUB_ARCHITECTURE_BLUEPRINT.md).

---

## 05 / RUNTIME ARCHITECTURE

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

## 06 / STATE AND PERSISTENCE

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

```json
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

## 07 / CREDIT AND PAYMENT ABSTRACTION

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

## 08 / CONTROL PLANE AND SIMULATOR

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

## 09 / VERIFICATION

> Pipeline grammar used throughout this README:
> `[..]` queued · `[>>]` running · `[ok]` verified

The repository includes a catalogue-wide compatibility suite.

The main report is stored at:

```text
[ok] REPORT   tests/FULL_FLEET_TEST_REPORT.json
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

## 10 / PERFORMANCE REPORTING

The repository contains a low-resource benchmark report:

```text
[ok] REPORT   tests/LOW_RESOURCE_BENCHMARK_REPORT.json
```

Performance values in that report describe a particular test environment. They are not universal guarantees.

The following distinction matters:

| Measurement | Interpretation |
|---|---|
| Catalogue lifecycle latency | Time required for a local simulated scenario lifecycle |
| Event-loop delay | Scheduling behavior in the tested Python process |
| Request throughput | Performance of the tested local workload |
| Process memory | Memory measured under the report's runtime conditions |
| Disk-I/O reduction | Relative behavior under the benchmark's write pattern |

External Telegram latency, AI-provider latency, network behavior, database contention, and payment callbacks are not represented by a purely local compatibility benchmark.

> Numbers without an artifact are decoration, not data.

---

## 11 / REPOSITORY STRUCTURE

```text
.
├── README.md
├── MEGA_HUB_ARCHITECTURE_BLUEPRINT.md
├── LICENSE                          # phase 1: one explicit licensing model
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
│   │   └── dynamic_bot.py           # archetype runtime for 440+ catalogue entries
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py              # async SQLite, WAL
│   │   ├── dispatcher.py            # multi-tenant event routing
│   │   ├── fsm.py
│   │   ├── hub_router.py            # 15-hub classification
│   │   ├── monetization.py          # Stars / card-to-card / TON abstraction
│   │   ├── omni_catalog.py          # indexes 445 scenarios from source documents
│   │   ├── rate_limiter.py          # token bucket, layer 7
│   │   └── resource_optimizer.py    # LRU pool, batched writes, RAM telemetry
│   │
│   └── web/
│       ├── app.py                   # FastAPI control plane
│       └── templates/
│           └── dashboard.html       # simulator + telemetry HUD
│
├── docs/
│   └── original_blueprints/         # source documents (Opus, GPT, Gemini, Rubika, AI)
│
├── deploy/
│   ├── Dockerfile.slim
│   ├── docker-compose.yml
│   ├── run_optimized.sh
│   ├── provision_botfather.py       # guarded provisioning tool
│   ├── batch_set_webhook.py
│   ├── nginx/
│   │   └── all-them-bots.conf
│   └── systemd/
│       └── all-them-bots.service
│
└── tests/
    ├── test_all_445_bots.py          # 5-stage compatibility lifecycle
    ├── test_low_resource_runtime.py  # load + memory benchmark
    ├── FULL_FLEET_TEST_REPORT.json
    └── LOW_RESOURCE_BENCHMARK_REPORT.json
```

---

## 12 / QUICK START

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

## 13 / TESTING

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

## 14 / DEPLOYMENT

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

## 15 / TELEGRAM PROVISIONING

Provisioning scripts are operational tools, not an invitation to create hundreds of Telegram accounts or bypass platform limits.

Before using them:

1. Review Telegram's current terms.
2. Confirm BotFather and account limits.
3. Start with one controlled pilot hub.
4. Use manual approval for new identities.
5. Store tokens in a secret manager.
6. Never commit exported tokens.
7. Avoid unsolicited messaging.
8. Apply per-user and per-chat rate limits.

Recommended rollout:

```text
PHASE 01  [..]  DASHBOARD-ONLY SIMULATION
PHASE 02  [..]  ONE PRIVATE TELEGRAM PILOT
PHASE 03  [..]  ONE STRATEGIC HUB
PHASE 04  [..]  PAYMENT SANDBOX
PHASE 05  [..]  LIMITED EXTERNAL USERS
PHASE 06  [..]  MEASURED EXPANSION
```

---

## 16 / SECURITY MODEL

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

## 17 / VERIFIED BOUNDARIES

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
- Every scenario's third-party dependency

### Not claimed

- 445 public bots currently online
- 445 independently deployed production services
- Zero risk of Telegram restrictions
- Guaranteed memory consumption on every host
- Guaranteed throughput under external API traffic
- Guaranteed revenue or conversion
- Complete production readiness for every catalogue entry

---

## 18 / ROADMAP

- `[..]` **PHASE 01 — REPOSITORY CONSISTENCY**
  - Remove unrelated third-party documentation
  - Align `pyproject.toml` metadata with FABLE OMEGA
  - Add a single canonical application name
  - Add a license file
  - Add report-schema validation
  - Add CI under `.github/workflows`
- `[..]` **PHASE 02 — RUNTIME HARDENING**
  - Add bounded worker pools
  - Add structured cancellation
  - Add timeout budgets
  - Add tenant-level quotas
  - Add transactional credit operations
  - Add event audit records
  - Add graceful shutdown tests
- `[..]` **PHASE 03 — TELEGRAM PILOT**
  - Deploy one private hub
  - Connect one bot token
  - Verify webhook behavior
  - Measure real idle memory
  - Test recovery after restart
  - Compare simulator and Telegram results
- `[..]` **PHASE 04 — PAYMENT SANDBOX**
  - Implement one provider completely
  - Add signed callbacks
  - Add replay protection
  - Add reconciliation reports
  - Add refund and dispute states
- `[..]` **PHASE 05 — OBSERVABILITY**
  - Structured JSON logging
  - Request correlation IDs
  - Prometheus-compatible metrics
  - Runtime pool telemetry
  - Database health checks
  - Scenario failure dashboards

---

## 19 / PROJECT POSITIONING

FABLE OMEGA should be evaluated as:

- a runtime architecture experiment;
- a large scenario catalogue;
- a multi-tenant Telegram control plane;
- a compatibility-testing framework;
- a low-resource deployment study.

It should not be evaluated as evidence that hundreds of independent public bots are already operating in production.

That distinction protects the technical credibility of the project.

---

## 20 / CONTRIBUTING

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

## 21 / LICENSE

A repository-level `LICENSE` file should define the actual terms.

Until a license file is committed, users should not assume that badges or README text grant permission to copy, redistribute, or commercially deploy the source code.

Avoid presenting the project as both MIT and commercially restricted at the same time.

Choose one explicit licensing model and keep these locations consistent:

- `LICENSE`
- `README.md`
- `pyproject.toml`
- package metadata
- deployment documentation

---

<div align="center">

## FABLE OMEGA

**CATALOGUE THE WORK · SHARE THE RUNTIME · MEASURE THE CLAIMS**

[Open Architecture Blueprint](./MEGA_HUB_ARCHITECTURE_BLUEPRINT.md) ·
[Inspect Fleet Report](./tests/FULL_FLEET_TEST_REPORT.json) ·
[Inspect Benchmark](./tests/LOW_RESOURCE_BENCHMARK_REPORT.json)

<sub>
Experimental infrastructure for controlled Telegram scenario execution.<br>
No anti-spam claims. No deployment theatre. No metric without an artifact.<br><br>
`BLACK #0A0908 · RED #D60019 · INK #F4F1EB`
</sub>

</div>
