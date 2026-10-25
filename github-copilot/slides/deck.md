---
title: "Soft Rules vs Hard Controls"
sub_title: "Keeping Copilot CLI Agents Safe at Work"
event: "Azure Builders: GitHub Copilot Dev Days · Melbourne · 16 Nov 2026"
theme:
  name: dark
  override:
    default:
      margin:
        percent: 2
      colors:
        background: "000000"
---

<!--
Run with ./present.sh. It builds rounds.gen.md (one slide per round) for the window size, then starts presenterm.
Bonus rounds (A, B, 4+, C) and the finale (F) are for the longer cuts: skip them with the arrow keys.
-->

Talk slides go here
===

<!--
speaker_note: |
  Placeholder. The talk slides will be added before the demo section.
-->

<!-- end_slide -->

The Southbank Vault
===

<!-- column_layout: [1, 1] -->
<!-- column: 0 -->

A heist in rounds.

* **Copilot** is hired to steal the
  **Secret Cappuccino Recipe**
* Each round adds **one defence**
* Watch which ones **actually stop it**,
  and **who can switch them off**

<!-- column: 1 -->

| Round | Defence |
|---|---|
| 1 | The Sign · `AGENTS.md` |
| 2 | The Velvet Rope · `--deny-tool` |
| 3 | The Bouncer · `preToolUse` hook |
| 4 | The Laser Grid · sandbox |
| 5 | HQ Override · managed settings |

<!-- reset_layout -->

<!--
speaker_note: |
  Every attack round runs copilot --allow-all-tools --autopilot --max-autopilot-continues=5.
  Deny rules beat allow-all, so every wall holds despite allow-all.
  On each round slide, → types and runs that round's Copilot command next to the vault.
  Before the talk: ./demo setup, ./demo doctor.
-->

<!-- end_slide -->

The heist
===

Copilot vs the Southbank Vault, live.

* One slide per round: the **vault** and the **Copilot** command side by side
* On each round: **→** runs it · **→** again: next round · **n** skips it

<!--
speaker_note: |
  Each round slide: the vault is already running (left). → once: the command types itself and runs (copilot -p).
  → again: next round. Round 5 is the exception: ctrl+e (sudo password, full-screen Copilot); /exit comes back.
  Bonus rounds (A, B, 4+, C) and the finale F: skip with →.
  Backup if the deck misbehaves: ./demo watch (left pane) + ./demo live (right pane).
-->

<!-- end_slide -->

<!-- include: rounds.gen.md -->

<!-- end_slide -->

Who can switch it off?
===

| Defence | Type | Who can switch it off |
|---|---|---|
| The Sign | soft | the model, by ignoring it |
| The Velvet Rope | hard (narrow) | you, mid-session |
| The Bouncer | hard (your code) | you or your team |
| The AI Doorman | probabilistic | a model's judgement |
| The Laser Grid | hard (OS) | you, unless HQ locks it |
| HQ Override | hard (org) | only your admin |
| The Two-Key Rule | hard (github.com) | only reviewers |

<!--
speaker_note: |
  After the demo: ./demo cleanup removes the demo's sandbox rules from ~/.copilot/settings.json.
-->
