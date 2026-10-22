# Travel Planner app

Public, empty app shell. Itineraries stay private.

[Open Travel Planner](https://basixmaster.github.io/Travel_Planner_App/travel_planner.html)

Share this HTTPS link to use the app on Windows, Linux, macOS, Android or iOS. No installer or local server is required. The local overview remains available in the private source repository; local-file execution and storage vary across browsers and phone file managers.

## Access private plans

Owner-approved access is configured separately. The repository token stays on the server; no encrypted token or access envelope is included in this public app. The access flow remains unavailable until its backend endpoint is configured.

A Request access by email button unlocks an encrypted contact address with the shared download password. It prepares a draft in the visitor's email app for manual review; sending it does not unlock downloads. The email contact envelope contains no repository token. Unlocked addresses can be read or shared.

No itineraries, plaintext passwords or plaintext tokens belong in this public repository. Downloads stay in this browser profile, not an ordinary local plans folder.

Download before travelling and keep large downloads foregrounded. On iOS, complete setup inside the Safari or installed Home Screen instance you intend to use. Clearing browser data or storage eviction can remove saved plans; live map detail and weather need internet.

## Maintenance

Render the empty shell with the private source skill scripts/app_release.py and validate it with scripts/app_release_test.py plus overview, inline HTML and browser-sync checks. Publish only the six reviewed runtime files and this README. Preserve private/public boundaries and verify Pages after release.
