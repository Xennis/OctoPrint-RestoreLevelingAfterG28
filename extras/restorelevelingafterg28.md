---
layout: plugin

id: restorelevelingafterg28
title: Restore Leveling After G28
description: Automatically keep leveling on after G28 (Auto Home).
author: Xennis
license: MIT

date: 2020-05-27

homepage: https://github.com/Xennis/OctoPrint-RestoreLevelingAfterG28
source: https://github.com/Xennis/OctoPrint-RestoreLevelingAfterG28
archive: https://github.com/Xennis/OctoPrint-RestoreLevelingAfterG28/archive/master.zip

tags:
- leveling
- bed leveling
- marlin

compatibility:
  octoprint:
  - 1.2.0
  os:
  - linux
  - windows
  - macos
  - freebsd
  python: ">=2.7,<4"

---

Automatically keep leveling on after G28 (Auto Home).

Marlin [G28](https://marlinfw.org/docs/gcode/M420.html) disables bed leveling. Follow with [M420 S](https://marlinfw.org/docs/gcode/M420.html)
turns leveling on. That behaviour can be enabled in Marlin via `RESTORE_LEVELING_AFTER_G28` or this plugin.

**Note**: The plugin do not _restore_ the state. It always enabled the bed leveling after a `G28` regardless if it
was enabled or disabled before. If there is the demand for a actual restore please create a pull request or issue.
