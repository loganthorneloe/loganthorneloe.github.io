"""Package only public site files for a GitHub Pages artifact."""
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
PUBLIC_FILES = ("index.html", "projects.html", "articles.html", "CNAME", "CV.md", "robots.txt", "sitemap.xml")
PUBLIC_DIRECTORIES = ("now", "about", "static")


def package_site(destination, root=ROOT):
    destination = Path(destination)
    sources = [Path(root) / name for name in (*PUBLIC_FILES, *PUBLIC_DIRECTORIES)]
    for source in sources:
        if not source.exists():
            raise ValueError(f"Missing public site asset: {source}")
        if source.is_symlink() or (source.is_dir() and any(p.is_symlink() for p in source.rglob("*"))):
            raise ValueError(f"Public site assets must not contain symlinks: {source}")
    destination.mkdir(parents=True, exist_ok=False)
    for source in sources:
        target = destination / source.name
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
    (destination / ".nojekyll").touch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="A new output directory")
    package_site(parser.parse_args().destination)
