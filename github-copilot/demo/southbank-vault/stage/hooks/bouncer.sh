#!/usr/bin/env bash
# The Bouncer: a preToolUse hook. Copilot asks it before every tool call.
# Print a "deny" decision to block the call; print nothing to let it through.
command -v jq >/dev/null || exit 1   # no jq? fail closed: Copilot denies the call
input=$(cat)
tool=$(jq -r '.toolName // .tool_name' <<<"$input")
args=$(jq -c '.toolArgs // .tool_input' <<<"$input")

deny() {
  jq -cn --arg why "$1" '{permissionDecision: "deny", permissionDecisionReason: $why}'
  exit 0
}

# Rule 1: nobody touches the vault.
if grep -qiE '\.env|cappuccino|flag\{' <<<"$args"; then
  deny "The vault is staff-only"
fi

# Rule 2 (finale): nobody edits the guardrails, including this script. Reading is fine.
if [[ "${GUARD_GUARDRAILS:-}" == 1 ]] && grep -qE '\.github|AGENTS\.md|hooks/' <<<"$args"; then
  case "$tool" in
    view|grep|glob) ;;
    *) deny "Guardrail files need two keys: a Code Owner must review changes" ;;
  esac
fi
