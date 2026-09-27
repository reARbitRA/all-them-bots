# Zero-Touch Autonomous Freelance Pipeline — compliant implementation

> **Important boundary:** this project deliberately does **not** bypass Cloudflare, CAPTCHAs, rate limits, platform rules, or access controls. It uses Playwright only to attach to a Chrome session that the account holder has already opened and authenticated. If a challenge is detected, the worker stops that platform and records an error; the operator must resolve it manually or use the platform's sanctioned API.

An asynchronous Python 3.11+ microservice that can, for explicitly authorized freelance accounts and platforms:

1. attach to an existing Chrome browser through CDP at `http://localhost:9222`;
2. discover job detail pages through modular platform DOM strategies;
3. use a fast OpenAI-compatible LLM endpoint to conservatively qualify bounded software jobs and draft a short Persian proposal;
4. submit the proposal through the visible, authenticated platform UI only when the operator enables automation;
5. detect awarded jobs, submit their scope to a **user-operated** coding-execution gateway, validate returned source files and a Persian `README.md`;
6. create or update a GitHub repository using **PyGithub** and atomically commit all generated source files; and
7. send this exact client message through the platform chat UI:

   ```text
   پروژه انجام شد. سورس کد و راهنمای اجرا در این لینک گیت‌هاب قرار دارد: [GITHUB_URL]
   ```

The project starts in discovery-only mode. Side effects require an intentional configuration change: `AUTOMATION_ENABLED=true`; bidding further requires `AUTO_SUBMIT_BIDS=true`.

---

## Brief research: the late-2026 design choices

### DOM abstraction for divergent marketplace UIs

The durable pattern is a **ports-and-adapters / Strategy** boundary, not a universal CSS selector. `FreelancePlatform` is the port; each marketplace owns a small adapter containing an ordered, declarative `PlatformSelectors` manifest plus URL ownership and semantic methods (`discover_jobs`, `submit_bid`, `is_awarded`, `send_delivery`). The orchestration layer never references a site selector.

This approach works with normal UI evolution because it:

- prefers stable accessibility roles, `data-testid`, names, and labels before visual classes;
- keeps multiple fallbacks per semantic field, rather than scattering selectors through workflow code;
- isolates a changed DOM to one adapter and makes it testable from saved, permissioned fixtures;
- models *capabilities* (find jobs, bid, award state, message client), not a shared page shape;
- persists a normalized `FreelanceJob` and idempotent state transitions, so a selector failure cannot create duplicate bids or deliveries; and
- uses visible, authorized UI interaction only. Official platform APIs/webhooks are preferable where a platform offers them.

Playwright documents `chromium.connect_over_cdp()` for attaching to an existing Chromium instance and explicitly notes that CDP attachment has lower fidelity than its native protocol; this is why the browser module is thin and adapters avoid clever low-level browser manipulation. [Playwright CDP API](https://playwright.dev/python/docs/api/class-browsertype)

### Execution and GitHub

As of **2026-09-27**, Arena.ai's official Agent Mode help describes interactive workspace operation, downloadable artifacts, and repository-connected GitHub delivery; it does not document a public API that accepts a job and returns generated files. The code therefore refuses to invent an `arena.ai` endpoint. It implements a real, versioned HTTP client for a user-operated execution gateway contract in [`docs/executor-contract.md`](docs/executor-contract.md); that gateway can be backed by an approved Arena workflow, another authorized coding agent, or internal infrastructure. [Arena Agent Mode help](https://help.arena.ai/articles/5432423882-how-to-use-agent-mode)

Publishing uses PyGithub's Git database API to make a single commit rather than a commit for each file. A GitHub token needs repository **Contents: write** access; writing workflow files would additionally need **Workflows: write**. [GitHub repository contents permissions](https://docs.github.com/en/rest/repos/contents)

---

## Architecture

```text
Chrome (account-holder-owned, logged in)          LLM provider              Execution gateway
         │ CDP :9222                                  │                            │
         ▼                                            ▼                            ▼
┌────────────────┐      ┌────────────────┐      ┌─────────────┐          ┌─────────────────┐
│ CdpBrowser     │─────▶│ Platform        │─────▶│ FastLLM     │          │ ArenaExecution  │
│ challenge stop │      │ Strategies      │      │ classifier  │          │ Gateway client  │
└────────────────┘      │ Ponisha        │      └─────────────┘          └────────┬────────┘
                        │ Karlancer      │                                         │ validated files
                        │ ParsCoders     │                                         ▼
                        └──────┬─────────┘     ┌────────────────┐          ┌─────────────────┐
                               │               │ SQLite JobStore│◀────────▶│ Artifact guard  │
                               └──────────────▶│ CAS state flow │          │ Persian README  │
                                                └───────┬────────┘          └────────┬────────┘
                                                        │                            │
                                                        ▼                            ▼
                                                 ┌──────────────┐           ┌──────────────────┐
                                                 │ GitHub        │──────────▶│ Platform chat    │
                                                 │ PyGithub      │ repo URL  │ exact delivery   │
                                                 └──────────────┘           └──────────────────┘
```

### State machine and crash safety

`SQLite` stores every job under `(platform, external_id)`. The worker moves it using compare-and-swap transitions:

```text
DISCOVERED → INELIGIBLE
           → CLASSIFICATION_FAILED (operator retry)
           → READY_FOR_REVIEW → BIDDING → BID_SUBMITTED → AWARDED
AWARDED → EXECUTING → ARTIFACTS_READY → PUBLISHING → CODE_PUBLISHED → DELIVERING → DELIVERED
          │             │                  │                  │
          └ failed      └ failed            └ failed           └ failed
```

A second cycle or API trigger cannot claim the same action after the first worker has changed its status. Failed work is never silently retried; the authenticated retry endpoint moves it back to its immediately safe predecessor.

---

## Repository layout

```text
.
├── .env.example                         # no secrets; all runtime settings documented
├── pyproject.toml                       # Python 3.11+ package and locked dependency ranges
├── docs/
│   └── executor-contract.md             # actual HTTP contract for coding-task execution
├── src/autofreelance/
│   ├── api.py                           # optional protected FastAPI operations API
│   ├── artifacts.py                     # path, size, ZIP and Persian README validation
│   ├── browser.py                       # CDP attach and hard-stop challenge detection
│   ├── config.py                        # Pydantic environment settings
│   ├── pipeline.py                      # idempotent async orchestration/state machine
│   ├── runtime.py                       # composition root
│   ├── store.py                         # SQLite state and audit log
│   ├── clients/
│   │   ├── llm.py                       # strict JSON LLM qualification/proposal client
│   │   ├── executor.py                  # execution gateway submit/poll/artifact client
│   │   └── github.py                    # PyGithub atomic Git-tree publisher
│   └── platforms/
│       ├── base.py                      # FreelancePlatform Strategy interface
│       ├── ponisha.py                   # Ponisha selector adapter
│       ├── karlancer.py                 # Karlancer selector adapter
│       ├── parscoders.py                # ParsCoders selector adapter
│       └── registry.py                  # adapter registration for any new marketplace
└── tests/                               # unit/contract tests
```

---

## Setup

### 1. Install

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
cp .env.example .env
```

### 2. Prepare the approved Chrome session

Use a dedicated Chrome profile under the account holder's control. The debugging port is powerful local access; never bind or expose it to a network.

```bash
google-chrome \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.config/autofreelance-chrome"
```

Sign in to every permitted marketplace yourself. Confirm that the platform allows the intended automation. Complete any legitimate login or challenge manually. Do **not** expose `9222` through a tunnel, reverse proxy, container port, or public interface.

### 3. Configure `.env`

Set the following only from your own secret manager/environment:

| Setting | Required for | Notes |
|---|---|---|
| `LLM_API_URL`, `LLM_API_KEY`, `LLM_MODEL` | classification and proposal drafting | OpenAI-compatible chat-completions API with JSON output |
| `ARENA_EXECUTOR_URL`, `ARENA_EXECUTOR_TOKEN` | code generation | Gateway described below, not an invented vendor API |
| `GITHUB_TOKEN`, `GITHUB_OWNER` | publishing | Fine-grained PAT with required repository permissions |
| `GITHUB_PRIVATE=false` | a link the client can read | Keep private only if you add the client as collaborator by an authorized process |
| `AUTOMATION_ENABLED=true` | execution, publish, client delivery | Explicit side-effect switch |
| `AUTO_SUBMIT_BIDS=true` | submitting bids | Explicit, separate bid switch |
| `SERVICE_API_KEY` | FastAPI control plane | Optional bearer token; strongly recommended in a deployed service |

**Dry run:** leave both automation flags as `false`. The service attaches to Chrome, reads work, stores it, and (if LLM credentials are configured) classifies it. It will not submit, generate code, publish, or message anyone.

### 4. Run

```bash
# One bounded cycle, useful for checking selectors and configuration.
autofreelance --once

# Persistent polling worker (default five-minute interval).
autofreelance

# Optional operator API; it binds all interfaces by default, so use a firewall/reverse proxy in deployment.
autofreelance --serve --host 127.0.0.1 --port 8000
curl -H "Authorization: Bearer $SERVICE_API_KEY" http://127.0.0.1:8000/v1/jobs
```

Run checks:

```bash
ruff check src tests
pytest -q
```

---

## Add a new marketplace adapter

Implement a class with the Strategy contract, register it, and add its name to `ENABLED_PLATFORMS`. This keeps browser mechanics and workflow logic unchanged.

```python
# src/autofreelance/platforms/example.py
from urllib.parse import urlparse
from .base import FreelancePlatform, PlatformSelectors

class ExamplePlatform(FreelancePlatform):
    name = "example"
    base_url = "https://example.invalid"
    selectors = PlatformSelectors(
        listing_url="https://example.invalid/jobs",
        job_card=("[data-testid='job-card']",),
        job_link=("a[data-testid='job-link']",),
        title=("h1[data-testid='job-title']",),
        description=("[data-testid='job-description']",),
        budget=("[data-testid='job-budget']",),
        status=("[data-testid='job-status']",),
        bid_message=("textarea[name='proposal']",),
        bid_submit=("button[type='submit']",),
        bid_success=("[role='alert'][data-kind='success']",),
        chat_button=("a[data-testid='project-chat']",),
        chat_message=("textarea[name='message']",),
        chat_send=("button[type='submit']",),
        awarded_markers=("awarded",),
    )

    def accepts_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return parsed.hostname == "example.invalid" and "/jobs/" in parsed.path
```

Then call `register_platform("example", ExamplePlatform)` before `build_runtime`, or add it to the registry mapping. Verify selectors against a platform account you own, use saved sanitized HTML fixtures in tests, and retain only selectors corresponding to permitted UI automation.

---

## Operational and security controls

- **No anti-bot bypass:** browser challenge detection fails closed. There is no stealth launch, CAPTCHA solver, proxy rotation, fingerprint spoofing, or Cloudflare workaround.
- **Conservative LLM gate:** unparseable output, ambiguous work, below-threshold confidence, academic cheating, credential abuse, surveillance, or access-control-evasion work is not bid.
- **Human consent by default:** all side effects are disabled until two explicit environment flags are set.
- **Idempotency:** SQLite compare-and-swap transitions prevent duplicate bids/deliveries across restarts; gateway calls include `Idempotency-Key`.
- **Artifact boundary:** rejects traversal, symlinks, duplicate paths, `.git`/`.github`, oversized files/archives, ZIP bombs, and missing Persian execution README files.
- **Secrets:** secrets are environment-only and excluded by `.gitignore`; they are not logged. Rotate tokens and scope them to a dedicated account/repository owner.
- **Privacy:** project scopes and generated source are client data. Configure retention, encryption, access control, and a public/private repository policy before enabling delivery.
- **Selector drift:** test and version adapters. A selector failure becomes a retryable failed state; it must not trigger arbitrary fallback clicks.

See [`docs/executor-contract.md`](docs/executor-contract.md) for the complete execution API request/response contract.
