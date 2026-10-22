# Travel Planner app

Public, empty app shell. Plans and credentials stay private.

[Open the app](https://basixmaster.github.io/Travel_Planner_App/travel_planner.html) · [Download the small app ZIP](https://github.com/BasixMaster/Travel_Planner_App/raw/refs/heads/main/downloads/Travel_Planner_App.zip)

Extract the ZIP and open START_HERE.html. Windows, macOS and Linux can open the local overview; on Android/iOS use the HTTPS link for reliable browser storage and offline reopening. ZIP extraction does not guarantee local HTML execution. No EXE or server is required.

The ZIP contains only the app and instructions, without itineraries, passwords, tokens or encrypted access bundles. Obtain the access JSON privately, import it once in the app, and download private plans with the download password. Set up iOS Home Screen apps inside the installed instance. Browser clearing/eviction can remove downloads; live detail/weather needs internet.

## Package maintenance

The source workflow renders this empty shell and builds a deterministic ZIP with a SHA-256 sidecar. CI tests and refreshes it when app inputs change; unchanged bytes cause no commit. The download link reads main directly, so a workflow-generated package commit does not depend on another Pages build. No private-repository token is used by this packaging workflow.

Manual rebuild: `python3 tools/app_package.py --app-root .`; verify with `--check` and `python3 tools/app_package_test.py`. Never add plans or access bundles to this public repository.
