# OctoPrint Plugin – Restore Leveling After G28

[![Build Status](https://travis-ci.org/Xennis/OctoPrint-RestoreLevelingAfterG28.svg?branch=master)](https://travis-ci.org/Xennis/OctoPrint-RestoreLevelingAfterG28)

Automatically keep bed leveling on after `G28` (Auto Home).

Marlin code `G28` disables bed leveling. The plugin restore the prior state:

* Before a `G28` command a `M420 V` is send to check if leveling is enabled or not.
* If leveling was enabled: After the `G28` command a `M420 S1` is send to enable leveling.

That same behaviour can be enabled in the Marlin firmware via `RESTORE_LEVELING_AFTER_G28`.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

```
https://github.com/Xennis/OctoPrint-RestoreLevelingAfterG28/archive/master.zip
```

## Configuration

The plugin has no configuration and does not adjust the UI.
