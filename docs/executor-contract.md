# Coding execution gateway contract (v1)

## Why a gateway exists

Arena.ai Agent Mode is an interactive product and its official help currently documents session workspaces and GitHub-connected branches, not a public endpoint that accepts a freelance job and returns files. The pipeline therefore uses a **user-operated gateway**. This prevents a deployment from relying on undocumented vendor routes or placing browser/session credentials in the worker.

The gateway can dispatch a task to an approved Arena workflow, a private coding-agent sandbox, or another internal implementation. It must authenticate the caller, apply its own policy and sandbox controls, and return only generated artifacts. The pipeline's `ArenaExecutionGatewayClient` implements the following contract exactly.

> Version: `v1` • Transport: HTTPS • Authentication: Bearer token • Encoding: JSON UTF-8

## Create a task

`POST $ARENA_EXECUTOR_URL`

Required request headers:

```http
Authorization: Bearer <ARENA_EXECUTOR_TOKEN>
Content-Type: application/json
Idempotency-Key: <platform>:<external_id>
```

Request body shape:

```json
{
  "idempotency_key": "ponisha:12345",
  "task": {
    "title": "عنوان پروژه",
    "description": "متن کامل شرح پروژه",
    "budget_text": "بودجه درج‌شده در پلتفرم یا null",
    "language": "fa",
    "instructions": "متن دستور کامل برای کدنویسی، تست و README فارسی"
  },
  "output": {
    "format": "files",
    "required_files": ["README.md"],
    "readme_language": "fa",
    "tests_required": true
  }
}
```

A gateway may immediately return an inline completed result (`200`/`201`), or an accepted task (`202` is preferred):

```json
{
  "task_id": "task_01J...",
  "status": "queued",
  "status_url": "https://executor.example.com/v1/tasks/task_01J..."
}
```

`status_url` must use exactly the same scheme and origin as `ARENA_EXECUTOR_URL`. This deliberate restriction prevents the gateway from turning the worker into an SSRF client.

## Poll a task

`GET <status_url>` with the same `Authorization` header. The client polls at `ARENA_EXECUTOR_POLL_SECONDS`, bounds the overall wait by `ARENA_EXECUTOR_TIMEOUT_SECONDS`, and handles transient `408`, `429`, and `5xx` responses by waiting for the next poll.

In-progress example:

```json
{"task_id": "task_01J...", "status": "running"}
```

Terminal failed example:

```json
{"task_id": "task_01J...", "status": "failed", "error": "sandbox test failure"}
```

Terminal successful inline result:

```json
{
  "task_id": "task_01J...",
  "status": "completed",
  "files": [
    {"path": "README.md", "content": "# راهنمای اجرا\n..."},
    {"path": "src/main.py", "content": "def main():\n    pass\n"},
    {"path": "tests/test_main.py", "content_base64": "ZGVmIHRlc3Rf..."}
  ]
}
```

`content` is UTF-8 text. `content_base64` is strict RFC 4648 base64 and is useful for binary fixtures. Every path is relative POSIX syntax.

## Optional ZIP result

A terminal successful result may instead contain:

```json
{
  "task_id": "task_01J...",
  "status": "completed",
  "artifact_url": "https://executor.example.com/v1/tasks/task_01J.../artifact.zip"
}
```

The pipeline downloads it with bearer authentication only from the executor's same origin. It rejects non-ZIP data, symlinks, traversal paths, duplicate paths, more than 2,000 files, files above 10 MiB, and an expanded project above 50 MiB.

## Required gateway behaviors

1. Treat `Idempotency-Key` as idempotent for at least the task retention window. Repeated creates must return the same task, not bill/re-run it.
2. Never return private infrastructure URLs, local paths, credentials, or files outside the task sandbox.
3. Run generated code in an isolated environment and enforce time, network, CPU, memory, and output limits.
4. Preserve the supplied task description for traceability but do not log secrets.
5. Return a root `README.md` with Persian installation and execution instructions; otherwise the pipeline refuses delivery.
6. Auth failures use `401`/`403`; policy rejection should use `422` with a machine-readable error; throttling should use `429`.
