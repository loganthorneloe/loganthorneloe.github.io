"""Build web assets from the pinned logan-style Git submodule (no fetching)."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def build_brand(root=ROOT):
    root = Path(root)
    installer = root / "vendor/logan-style/scripts/install_web.py"
    if not installer.is_file():
        raise RuntimeError(
            "Initialize logan-style first: git submodule update --init vendor/logan-style"
        )
    destination = root / "static/vendor/logan-brand"
    command = [sys.executable, str(installer), str(destination)]
    if (destination / "brand-manifest.json").exists():
        command.append("--update")
    subprocess.run(command, check=True)
    subprocess.run([sys.executable, str(installer), str(destination), "--check"], check=True)


if __name__ == "__main__":
    build_brand()
