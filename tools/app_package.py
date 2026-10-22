"""Build a deterministic, credential-free public app ZIP (standard-library only)."""
import argparse
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path

APP_URL = 'https://basixmaster.github.io/Travel_Planner_App/travel_planner.html'
DOWNLOAD_URL = 'https://github.com/BasixMaster/Travel_Planner_App/raw/refs/heads/main/downloads/Travel_Planner_App.zip'
FILES = ('index.html', 'travel_planner.html', 'github-sync-storage.js',
         'travel-planner-sw.js', 'manifest.webmanifest', 'travel-planner.svg')
README = '''Travel Planner — app-only sharing package

Open START_HERE.html after extracting the whole ZIP, or open:
''' + APP_URL + '''

Windows, Linux and macOS: extract the ZIP and open START_HERE.html in a current
browser. Android and iOS/iPadOS can extract ZIP files too, but file managers may
preview local HTML or restrict scripts/storage. Use the HTTPS app for the reliable
phone experience, GitHub updates and installed offline reopening.

No plans, credentials, tokens, passwords or encrypted access bundles are included.
On each new device/browser, obtain your encrypted access-bundle JSON privately
from the owner. Open the HTTPS app, choose Download / update plans, import that
file once and enter the download password. Keep the bundle and password private.
Download while online before travelling; keep large downloads in the foreground.

On iPhone/iPad, first add/open the Home Screen app if that is how you will use it,
then import and download there. Safari and its installed app may use separate
storage. Downloads/favorites belong to this device/browser/profile; clearing data
or browser eviction can remove them. Live maps/weather require internet.

The unpacked local overview has no plans initially. Local file storage is
browser-dependent and cannot register a service worker; it is not equivalent to
the HTTPS app. The ZIP is portable packaging, not a native installer or an offline
copy of private itineraries. No EXE, Python, Node or local server is required.

Latest app ZIP:
''' + DOWNLOAD_URL + '\n'
START = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Start Travel Planner</title><style>
body{font:17px/1.6 system-ui,sans-serif;color:#153638;background:#f8f5ec;max-width:680px;margin:8vh auto;padding:24px}
a{color:#00665f}a.go{display:inline-block;background:#075952;color:#fff;padding:14px 22px;border-radius:12px;text-decoration:none;margin:8px 12px 8px 0}
small{display:block;margin-top:20px} @media(prefers-color-scheme:dark){body{color:#e5eeeb;background:#142526}a{color:#88ded6}}
</style><h1>Travel Planner</h1><p>Your app is ready. Private plans are downloaded separately after access setup.</p>
<a class="go" href="''' + APP_URL + '''">Open online app · recommended</a>
<a href="travel_planner.html">Open unpacked local overview</a>
<p>For Android and iPhone/iPad, use the online app. ZIP extraction works across platforms, but local HTML support varies.</p>
<ol><li>Obtain your encrypted access-bundle JSON privately from the owner.</li><li>In the app, select <b>Download / update plans</b>, import the file once and enter the download password.</li><li>Download before travelling. On iOS, do this inside your chosen Safari or Home Screen instance.</li></ol>
<small>Read <a href="README.txt">README.txt</a> for offline/storage limits. This package contains no itineraries or credentials.</small></html>'''


def safe_content(path, data):
    if re.search(rb'github_pat_[A-Za-z0-9_]{30,}|gh[pousr]_[A-Za-z0-9]{20,}', data):
        raise ValueError('Possible credential in ' + path)
    if re.search(rb'"(?:downloadVault|credentialVault|offlineInstaller)"\s*:', data):
        raise ValueError('Private encrypted payload in ' + path)
    if path == 'travel_planner.html':
        match = re.search(r'const LIBRARY=(.*?);\s*const q', data.decode('utf-8'), re.S)
        if not match:
            raise ValueError('Missing public overview registry')
        registry = json.loads(match[1])
        if registry.get('trips') != [] or registry.get('root') != '.':
            raise ValueError('App package must have an empty portable registry')


def package_entries(root):
    root = Path(root).resolve()
    entries = {}
    for name in FILES:
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise ValueError('Missing or linked app file: ' + name)
        data = path.read_bytes()
        safe_content(name, data)
        entries[name] = data
    entries['README.txt'] = README.encode('utf-8')
    entries['START_HERE.html'] = START.encode('utf-8')
    manifest = {'format': 1, 'package': 'app-only', 'plansIncluded': False,
                'files': {name: {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                          for name, data in sorted(entries.items())}}
    entries['package-manifest.json'] = (json.dumps(manifest, sort_keys=True, indent=2) + '\n').encode()
    return entries


def build_package(root, output=None, check=False):
    root = Path(root).resolve()
    output = Path(output) if output else root / 'downloads' / 'Travel_Planner_App.zip'
    entries = package_entries(root)
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(entries.items()):
            info = zipfile.ZipInfo('Travel_Planner_App/' + name, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data, compresslevel=9)
    content = stream.getvalue()
    # Compare actual entries too: different zlib versions need not rewrite a
    # byte-valid existing release whose logical files have not changed.
    if output.is_file():
        try:
            with zipfile.ZipFile(output) as previous:
                expected = {'Travel_Planner_App/' + name: data for name, data in entries.items()}
                if (set(previous.namelist()) == set(expected)
                        and len(previous.infolist()) == len(expected)
                        and all(item.compress_type == zipfile.ZIP_DEFLATED for item in previous.infolist())
                        and all(previous.read(name) == data for name, data in expected.items())):
                    content = output.read_bytes()
        except (OSError, ValueError, zipfile.BadZipFile, RuntimeError, NotImplementedError):
            pass
    checksum = hashlib.sha256(content).hexdigest() + '  ' + output.name + '\n'
    sidecar = output.with_suffix('.zip.sha256')
    changed = not output.exists() or output.read_bytes() != content
    if check:
        if changed or not sidecar.exists() or sidecar.read_text('ascii') != checksum:
            raise ValueError('App ZIP is missing or stale; run the package builder')
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        if changed:
            output.write_bytes(content)
        if not sidecar.exists() or sidecar.read_text('ascii') != checksum:
            sidecar.write_text(checksum, 'ascii')
    return {'path': str(output), 'bytes': len(content), 'sha256': checksum.split()[0],
            'changed': changed, 'entries': len(entries), 'plansIncluded': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app-root', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    print(json.dumps(build_package(args.app_root, args.output, args.check)))
