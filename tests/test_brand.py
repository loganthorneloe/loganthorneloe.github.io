import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import brand


class BrandBuildTests(unittest.TestCase):
    def test_missing_submodule_explains_initialization(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(RuntimeError, 'git submodule update --init'):
                brand.build_brand(Path(directory))

    @unittest.skipUnless((brand.ROOT / 'vendor/logan-style/scripts/install_web.py').is_file(),
                         'Private submodule is not initialized (newsletter CI uses prebuilt assets)')
    def test_clean_build_update_and_local_edit_protection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'vendor/logan-style'
            shutil.copytree(brand.ROOT / 'vendor/logan-style', source,
                            ignore=shutil.ignore_patterns('.git', '__pycache__'))
            brand.build_brand(root)
            destination = root / 'static/vendor/logan-brand'
            css = destination / 'brand.css'
            initial = css.read_bytes()
            mtime = css.stat().st_mtime_ns
            brand.build_brand(root)
            self.assertEqual(css.stat().st_mtime_ns, mtime)
            updated = initial + b'\n/* dependency update */\n'
            (source / 'assets/web/brand.css').write_bytes(updated)
            brand.build_brand(root)
            self.assertEqual(css.read_bytes(), updated)
            manifest = json.loads((destination / 'brand-manifest.json').read_text())
            self.assertEqual(manifest['sha256']['brand.css'], hashlib.sha256(updated).hexdigest())
            css.write_bytes(b'local edit')
            before = {str(p.relative_to(destination)): p.read_bytes()
                      for p in destination.rglob('*') if p.is_file()}
            with self.assertRaises(subprocess.CalledProcessError):
                brand.build_brand(root)
            self.assertEqual(before, {str(p.relative_to(destination)): p.read_bytes()
                                     for p in destination.rglob('*') if p.is_file()})


if __name__ == '__main__':
    unittest.main()
