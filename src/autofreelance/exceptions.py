"""Typed exceptions allow the worker to record safe, actionable terminal states."""


class PipelineError(Exception):
    """Base class for expected pipeline failures."""


class ConfigurationError(PipelineError):
    """A required configuration value is absent or inconsistent."""


class BrowserUnavailable(PipelineError):
    """The approved Chrome CDP endpoint cannot be reached."""


class AccessChallengeDetected(PipelineError):
    """A site displayed a CAPTCHA, Cloudflare, or equivalent access challenge.

    The worker must stop. It deliberately contains no challenge-solving or evasion path.
    """


class PlatformInteractionError(PipelineError):
    """A platform page did not expose the expected authorized UI."""


class LLMResponseError(PipelineError):
    """The classifier returned an invalid, incomplete, or unsafe decision."""


class ExecutionError(PipelineError):
    """The configured code-execution gateway did not return valid artifacts."""


class ArtifactValidationError(PipelineError):
    """An artifact is unsafe, oversized, or does not meet delivery requirements."""


class GitHubDeliveryError(PipelineError):
    """Repository creation or artifact publishing failed."""
