from pathlib import Path
import tempfile
import unittest

import package_site


class PagesArtifactTests(unittest.TestCase):
    def test_packages_public_files_without_source_or_git_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "source"
            root.mkdir()
            for name in package_site.PUBLIC_FILES:
                (root / name).write_text(name)
            for name in package_site.PUBLIC_DIRECTORIES:
                (root / name).mkdir()
                (root / name / "public.txt").write_text(name)
            (root / "vendor/logan-style").mkdir(parents=True)
            (root / "vendor/logan-style/private.txt").write_text("private source")
            (root / ".gitmodules").write_text("private URL")
            (root / "build.py").write_text("builder")
            output = Path(directory) / "output"
            package_site.package_site(output, root)
            self.assertTrue((output / "static/public.txt").exists())
            self.assertTrue((output / ".nojekyll").exists())
            for name in ["vendor", ".gitmodules", "build.py"]:
                self.assertFalse((output / name).exists())
            (root / "static/link").symlink_to(root / "vendor/logan-style/private.txt")
            with self.assertRaisesRegex(ValueError, "symlink"):
                package_site.package_site(Path(directory) / "bad-output", root)
            self.assertFalse((Path(directory) / "bad-output").exists())
