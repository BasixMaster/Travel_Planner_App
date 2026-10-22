# Travel Planner app

Public, empty app shell. Itineraries stay private.

[Open Travel Planner](https://basixmaster.github.io/Travel_Planner_App/travel_planner.html)

Share this HTTPS link to use the app on Windows, Linux, macOS, Android or iOS. No installer or local server is required. The local overview remains available in the private source repository; local-file execution and storage vary across browsers and phone file managers.

## Access private plans

Browser-key access requests are reviewed in [the owner dashboard](owner.html), the primary management interface. Owners can alternatively approve through Codex and the private Manage access GitHub workflow. GitHub Actions publishes encrypted plans for approved browser keys; no repository token is delivered to visitors. Sharing requires one-time private workflow secret configuration before approval publication can succeed.

A Request access by email button unlocks an encrypted contact address with the shared download password. It prepares a draft with the visitor's public browser key and an owner-review link; sending it does not unlock downloads. The email contact envelope contains no repository token. Unlocked addresses can be read or shared.

No plaintext itineraries, passwords or tokens belong in this public repository. Downloads stay in this browser profile, not an ordinary local plans folder.

Download before travelling and keep large downloads foregrounded. On iOS, complete setup inside the Safari or installed Home Screen instance you intend to use. Clearing browser data or storage eviction can remove saved plans; live map detail and weather need internet.

## Maintenance

Render the empty shell with the private source skill scripts/app_release.py and validate it with scripts/app_release_test.py plus overview, inline HTML and browser-sync checks. Publish only the reviewed reviewed runtime files and this README. Preserve private/public boundaries and verify Pages after release.
