"""Where things live.

The demo source (this folder) sits inside the talks git repo. Copilot runs in a
separate "stage": a small café repo of its own, so its .github/hooks/ are the
repo-root hooks Copilot loads. Default: ~/southbank-roasters (override with
VAULT_STAGE).
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))          # .../southbank-vault/vault
DEMO = os.path.dirname(HERE)                                 # .../southbank-vault
TEMPLATE = os.path.join(DEMO, "stage")                       # files copied into the stage
REPLAYS = os.path.join(DEMO, "replays")


def stage():
    default = "~/southbank-roasters"
    if os.environ.get("SUDO_USER") and os.geteuid() == 0:  # under sudo, ~ is root's home
        default = f"~{os.environ['SUDO_USER']}/southbank-roasters"
    return os.path.abspath(os.path.expanduser(os.environ.get("VAULT_STAGE", default)))


def events():
    return os.path.join(stage(), ".vault", "events.jsonl")


def managed_settings():
    """The admin's managed settings file (Round 5). VAULT_MANAGED_PATH overrides it for tests."""
    return os.environ.get("VAULT_MANAGED_PATH",
                          "/Library/Application Support/GitHubCopilot/managed-settings.json")
