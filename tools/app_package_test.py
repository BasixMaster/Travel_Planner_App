"""Archive extraction, integrity, no-op, stale input and public-boundary regressions."""
import hashlib
import json
import contextlib
import shutil
import uuid
import unittest
import zipfile
from pathlib import Path
from app_package import FILES, build_package


@contextlib.contextmanager
def test_directory():
    parent = Path.cwd().resolve()
    path = parent / ('app-package-test-' + uuid.uuid4().hex)
    path.mkdir()
    try:
        yield path
    finally:
        resolved = path.resolve()
        assert resolved.parent == parent and resolved.name.startswith('app-package-test-')
        shutil.rmtree(resolved)


class PackageTest(unittest.TestCase):
    def test_portability_and_update(self):
        with test_directory() as tmp:
            root = Path(tmp)
            for name in FILES:
                (root / name).write_text('synthetic public file', 'utf-8')
            page = root / 'travel_planner.html'
            page.write_text('const LIBRARY={"root":".","trips":[]}; const q=1;', 'utf-8')
            # Extra local files must never be swept into a public archive.
            (root / 'token.txt').write_text('synthetic private fixture', 'utf-8')
            first = build_package(root)
            archive = Path(first['path'])
            stamp = archive.stat().st_mtime_ns
            self.assertFalse(build_package(root)['changed'])
            self.assertEqual(stamp, archive.stat().st_mtime_ns)
            build_package(root, check=True)
            with zipfile.ZipFile(archive) as z:
                self.assertIsNone(z.testzip())
                self.assertEqual(len(z.namelist()), 9)
                for info in z.infolist():
                    self.assertFalse(info.filename.startswith('/') or '..' in Path(info.filename).parts)
                    self.assertNotIn('token.txt', info.filename)
                    self.assertEqual(info.compress_type, zipfile.ZIP_DEFLATED)
                destination = root / 'extracted'
                z.extractall(destination)
            package = destination / 'Travel_Planner_App'
            manifest = json.loads((package / 'package-manifest.json').read_text('utf-8'))
            self.assertFalse(manifest['plansIncluded'])
            for name, record in manifest['files'].items():
                data = (package / name).read_bytes()
                self.assertEqual(len(data), record['bytes'])
                self.assertEqual(hashlib.sha256(data).hexdigest(), record['sha256'])
            (root / 'travel-planner-sw.js').write_text('new public worker', 'utf-8')
            with self.assertRaisesRegex(ValueError, 'stale'):
                build_package(root, check=True)
            self.assertTrue(build_package(root)['changed'])
            page.write_text('const LIBRARY={"root":".","trips":[{"id":"private-plan"}]}; const q=1;', 'utf-8')
            with self.assertRaisesRegex(ValueError, 'empty portable'):
                build_package(root)
            page.write_text('const LIBRARY={"root":".","trips":[],"downloadVault":"synthetic"}; const q=1;', 'utf-8')
            with self.assertRaisesRegex(ValueError, 'Private encrypted'):
                build_package(root)
            page.write_text('const LIBRARY={"root":".","trips":[]}; const q=1;', 'utf-8')
            (root / 'travel-planner-sw.js').write_text('ghp_' + 'SyntheticOnly123456789012345678901234567890', 'utf-8')
            with self.assertRaisesRegex(ValueError, 'credential'):
                build_package(root)


if __name__ == '__main__':
    unittest.main()
