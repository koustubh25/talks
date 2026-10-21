"""STAGE SCRIPT — open every pre-stage tab in one shot (talk/runbook-portal.md checklist).

Launches real Google Chrome (headful) via Playwright, signed in as
kosta250@gmail.com — already-authenticated Azure/GitHub SSO, no login prompts.
Opens tabs in the exact order the checklist wants:

  1. GitHub PR #1 - Checks tab
  2. Foundry portal -> Tracing
  3. Foundry portal -> Data Generation
  4. Foundry portal -> Evaluations
  5. Mock inventory /healthz (visual confirmation, mirrors degrade.sh status)

Nav clicks into Tracing/Data Generation/Evaluations are best-effort (the
portal's left-nav DOM isn't something we control) - if a click can't find its
target the tab is simply left on the project overview with a printed warning,
never silently wrong.

**About the Chrome profile:** this does NOT drive your live daily Chrome
profile directly (two processes on one profile dir risks lock conflicts /
corruption). On first run it makes a ONE-TIME copy of the auth-relevant slice
of your real profile ("Profile 1", kosta250@gmail.com — cookies, local
storage, IndexedDB, login data) into `.playwright-chrome-profile/`, skipping
extensions/caches (~4.3GB of the 4.9GB source profile). That copy is what
Playwright actually drives, so your real Chrome is never touched or locked.
Quit Chrome before the first run so the copy isn't made mid-write. Re-sync
later with `--refresh-profile` (e.g. if you re-auth in your main browser).

This is NOT wired into `uv`/pyproject on purpose - it's a standalone stage
tool, not part of the demo's runtime dependencies. One-time setup:

    pip install playwright && playwright install chromium   # only needed for the browser-fetch machinery; we launch real Chrome, not the bundled one

Usage:
    python3 runbook/prestage.py                    # first run: quit Chrome first, this seeds the profile copy
    python3 runbook/prestage.py --refresh-profile   # re-copy cookies/session from your real Chrome (quit Chrome first)
    python3 runbook/prestage.py --degrade on        # also flip degrade mode on first
    python3 runbook/prestage.py --degrade off       # ...or off, e.g. after rehearsal
    python3 runbook/prestage.py --keep-open         # don't wait for Enter before exiting the script (browser window stays open regardless)
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

REAL_CHROME_DIR = Path.home() / "Library/Application Support/Google/Chrome"
REAL_PROFILE_NAME = "Profile 1"  # kosta250@gmail.com, verified via Preferences account_info
COPIED_PROFILE_ROOT = Path(__file__).resolve().parent.parent / ".playwright-chrome-profile"
# skip extensions/caches - just the auth-bearing state (cookies, storage, login data)
COPY_EXCLUDES = [
    "Extensions", "Service Worker", "Local Extension Settings", "DNR Extension Rules",
    "Extension Rules", "Extension Scripts", "Shared Dictionary", "File System",
    "blob_storage", "component_crx_cache", "*Cache*", "*cache*",
]

MOCK_BASE = "https://inventory-mock-ktb-au.azurewebsites.net"
GITHUB_PR1_CHECKS = "https://github.com/koustubh25/ai-evals-talk/pull/1/checks"
FOUNDRY_WSID = (
    "/subscriptions/5d98f681-c627-4a4d-9f1d-001ae04c2358"
    "/resourceGroups/rg-evals-demo"
    "/providers/Microsoft.CognitiveServices"
    "/accounts/evalsdemo-ktb-au"
    "/projects/proj-evals-demo"
)
FOUNDRY_TID = "79fa077b-e5f3-474a-8e36-c79ac59b00ed"
FOUNDRY_OVERVIEW = f"https://ai.azure.com/foundryProject/overview?wsid={FOUNDRY_WSID}&tid={FOUNDRY_TID}"

# nav link labels straight from talk/links.md - left nav has Agents / Tracing /
# Evaluations / Data Generation. Best-effort click, not a guaranteed selector.
FOUNDRY_TABS = ["Tracing", "Data Generation", "Evaluations"]

G, R, Y, D, X = "\033[1;32m", "\033[1;31m", "\033[1;33m", "\033[2m", "\033[0m"


def chrome_is_running() -> bool:
    r = subprocess.run(["pgrep", "-x", "Google Chrome"], capture_output=True)
    return r.returncode == 0


def seed_profile(force: bool) -> None:
    dest_profile = COPIED_PROFILE_ROOT / REAL_PROFILE_NAME
    if dest_profile.exists() and not force:
        print(f"{D}using existing profile copy at {COPIED_PROFILE_ROOT} "
              f"(pass --refresh-profile to re-sync from real Chrome){X}")
        return

    src_profile = REAL_CHROME_DIR / REAL_PROFILE_NAME
    if not src_profile.exists():
        sys.exit(f"{R}real Chrome profile not found at {src_profile}{X}")

    if chrome_is_running():
        sys.exit(f"{R}Chrome is running — quit it fully before "
                  f"{'refreshing' if force else 'seeding'} the profile copy "
                  f"(avoids copying locked/partially-written cookie/session files).{X}")

    print(f"{Y}{'refreshing' if force else 'seeding'} profile copy from real Chrome "
          f"(kosta250@gmail.com, cookies/storage only, no extensions/caches)...{X}")
    COPIED_PROFILE_ROOT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REAL_CHROME_DIR / "Local State", COPIED_PROFILE_ROOT / "Local State")
    rsync_args = ["rsync", "-a", "--delete"]
    for pattern in COPY_EXCLUDES:
        rsync_args += ["--exclude", pattern]
    rsync_args += [f"{src_profile}/", f"{dest_profile}/"]
    subprocess.run(rsync_args, check=True)
    print(f"{G}✓{X} profile copy ready at {COPIED_PROFILE_ROOT}")


def degrade(action: str) -> None:
    result = subprocess.run(
        ["./runbook/degrade.sh", action], cwd=Path(__file__).resolve().parent.parent,
        capture_output=True, text=True, check=True,
    )
    print(f"{Y}degrade.sh {action}{X} -> {result.stdout.strip()}")


def open_foundry_tab(context, label: str):
    page = context.new_page()
    page.goto(FOUNDRY_OVERVIEW, wait_until="domcontentloaded")
    try:
        page.get_by_role("link", name=label, exact=True).first.click(timeout=8000)
        page.wait_for_load_state("domcontentloaded")
        print(f"{G}✓{X} Foundry -> {label}")
    except Exception as e:  # noqa: BLE001 - best-effort UI click, never fatal
        print(f"{R}!{X} couldn't click '{label}' nav link ({type(e).__name__}) "
              f"- tab left on project overview, click it manually. {D}{e}{X}")
    return page


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--degrade", choices=["on", "off"], help="flip the mock's degrade mode before opening tabs")
    ap.add_argument("--refresh-profile", action="store_true", help="re-copy cookies/session from real Chrome (quit Chrome first)")
    ap.add_argument("--keep-open", action="store_true", help="don't wait for Enter before exiting the script (browser stays open regardless)")
    args = ap.parse_args()

    print(f"{Y}== pre-stage checklist ==\n{X}")

    seed_profile(force=args.refresh_profile)

    if args.degrade:
        degrade(args.degrade)
    else:
        degrade("status")
        print(f"{D}  (pass --degrade on/off to change it from here){X}")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(COPIED_PROFILE_ROOT),
            channel="chrome",  # real Google Chrome, not bundled Chromium - matches the copied profile format
            headless=False,
            viewport={"width": 1440, "height": 900},
            args=["--start-maximized", f"--profile-directory={REAL_PROFILE_NAME}"],
        )

        # tab order matches talk/runbook-portal.md
        gh = context.new_page()
        gh.goto(GITHUB_PR1_CHECKS, wait_until="domcontentloaded")
        print(f"{G}✓{X} GitHub PR #1 -> Checks")

        for label in FOUNDRY_TABS:
            open_foundry_tab(context, label)

        mock = context.new_page()
        mock.goto(f"{MOCK_BASE}/healthz", wait_until="domcontentloaded")
        print(f"{G}✓{X} mock inventory /healthz")

        # close the blank first tab persistent contexts start with, if any
        for pg in context.pages:
            if pg.url == "about:blank":
                pg.close()

        print(f"\n{Y}Remaining manual checks:{X}")
        print("  [ ] signed into ai.azure.com (first run: log in by hand, session is saved)")
        print("  [ ] 18 hallucinated-conversation traces + Act 1 sabotage traces visible in Tracing")
        print("  [ ] dataset already created from the 18-conversation capture, as fallback")
        print("  [ ] job summary on GitHub tab scrolled to the comparison table")

        if not args.keep_open:
            input(f"\n{D}Tabs are open in the browser window. Press Enter here to end this script "
                  f"(the browser window itself stays open).{X}\n")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.exit(f"degrade.sh failed: {e.stderr}")
