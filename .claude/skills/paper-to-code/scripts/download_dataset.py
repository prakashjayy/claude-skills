#!/usr/bin/env python3
"""
Dataset download helper for paper-to-code.

Supports: torchvision, huggingface datasets, direct URL (tgz/zip), kaggle.

Usage:
    uv run python scripts/download_dataset.py --source torchvision --name CIFAR10 --target data/cifar10
    uv run python scripts/download_dataset.py --source hf_hub --id cifar10 --target data/cifar10
    uv run python scripts/download_dataset.py --source direct --url https://... --target data/mydata
    uv run python scripts/download_dataset.py --source kaggle --id user/dataset-name --target data/mydata
    uv run python scripts/download_dataset.py --check data/cifar10
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


# ---------------------------------------------------------------------------
# Disk space check
# ---------------------------------------------------------------------------

def check_disk_space(path: str, required_gb: float) -> bool:
    total, used, free = shutil.disk_usage(path)
    free_gb = free / (1024 ** 3)
    print(f"  Free disk: {free_gb:.1f}GB  Required: {required_gb:.1f}GB")
    if free_gb < required_gb * 1.2:
        print(f"  ⚠️  Low disk space: need {required_gb * 1.2:.1f}GB, have {free_gb:.1f}GB", file=sys.stderr)
        return False
    return True


# ---------------------------------------------------------------------------
# Download methods
# ---------------------------------------------------------------------------

def download_torchvision(name: str, target: str):
    """
    Download a torchvision dataset by class name.
    Supported: CIFAR10, CIFAR100, STL10, Flowers102, OxfordIIITPet,
               FashionMNIST, MNIST, ImageNet (requires manual), etc.
    """
    import torchvision.datasets as D
    import torchvision.transforms as T

    target_path = Path(target)
    target_path.mkdir(parents=True, exist_ok=True)
    t = T.ToTensor()

    cls = getattr(D, name, None)
    if cls is None:
        print(f"  ✗ torchvision.datasets.{name} not found", file=sys.stderr)
        sys.exit(1)

    print(f"  Downloading {name} (train)...")
    try:
        # Try standard split API
        cls(root=str(target_path), split='train', download=True, transform=t)
        cls(root=str(target_path), split='val',   download=True, transform=t)
    except TypeError:
        try:
            # Older API: train=True/False
            cls(root=str(target_path), train=True,  download=True, transform=t)
            cls(root=str(target_path), train=False, download=True, transform=t)
        except Exception as e:
            print(f"  ✗ Download failed: {e}", file=sys.stderr)
            sys.exit(1)

    print(f"  ✓ Downloaded to {target_path}")


def download_hf_hub(dataset_id: str, target: str, config_name: str | None = None):
    """Download a HuggingFace dataset."""
    try:
        from datasets import load_dataset
    except ImportError:
        print("  Installing datasets...", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "datasets", "-q"])
        from datasets import load_dataset

    target_path = Path(target)
    target_path.mkdir(parents=True, exist_ok=True)

    print(f"  Downloading {dataset_id} from HuggingFace Hub...")
    kwargs = {"cache_dir": str(target_path)}
    if config_name:
        kwargs["name"] = config_name
    try:
        ds = load_dataset(dataset_id, **kwargs)
        print(f"  ✓ Downloaded: {ds}")
    except Exception as e:
        print(f"  ✗ HF download failed: {e}", file=sys.stderr)
        print("  If this is a gated dataset (e.g. ImageNet), run: huggingface-cli login", file=sys.stderr)
        sys.exit(1)


def download_direct(url: str, target: str):
    """Download and extract a direct URL (tgz, tar.gz, zip)."""
    target_path = Path(target)
    target_path.mkdir(parents=True, exist_ok=True)

    ext = url.split("?")[0]  # strip query params
    if ext.endswith(".tgz") or ext.endswith(".tar.gz"):
        archive_suffix = ".tgz"
    elif ext.endswith(".tar.bz2"):
        archive_suffix = ".tar.bz2"
    elif ext.endswith(".zip"):
        archive_suffix = ".zip"
    else:
        archive_suffix = ".download"

    with tempfile.NamedTemporaryFile(suffix=archive_suffix, delete=False) as tmp:
        tmp_path = tmp.name

    print(f"  Downloading {url}...")
    result = subprocess.run(
        ["curl", "-L", "--progress-bar", url, "-o", tmp_path],
        check=False
    )
    if result.returncode != 0:
        # fallback to wget
        result = subprocess.run(["wget", "-q", "--show-progress", url, "-O", tmp_path], check=False)
    if result.returncode != 0:
        print("  ✗ Download failed (tried curl and wget)", file=sys.stderr)
        os.unlink(tmp_path)
        sys.exit(1)

    print(f"  Extracting to {target_path}...")
    if archive_suffix in (".tgz", ".tar.gz"):
        subprocess.check_call(["tar", "-xzf", tmp_path, "-C", str(target_path), "--strip-components=1"])
    elif archive_suffix == ".tar.bz2":
        subprocess.check_call(["tar", "-xjf", tmp_path, "-C", str(target_path), "--strip-components=1"])
    elif archive_suffix == ".zip":
        import zipfile
        with zipfile.ZipFile(tmp_path, 'r') as z:
            # strip one top-level directory if all paths share a common prefix
            names = z.namelist()
            prefix = os.path.commonprefix(names)
            for member in z.infolist():
                member_path = member.filename
                if prefix and member_path.startswith(prefix):
                    member_path = member_path[len(prefix):]
                if not member_path:
                    continue
                dest = target_path / member_path
                if member.is_dir():
                    dest.mkdir(parents=True, exist_ok=True)
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    with z.open(member) as src, open(dest, 'wb') as dst:
                        shutil.copyfileobj(src, dst)
    else:
        shutil.move(tmp_path, target_path / "download")

    os.unlink(tmp_path)
    print(f"  ✓ Extracted to {target_path}")


def download_kaggle(dataset_id: str, target: str):
    """Download a Kaggle dataset. Requires KAGGLE_USERNAME and KAGGLE_KEY env vars."""
    for key in ("KAGGLE_USERNAME", "KAGGLE_KEY"):
        if not os.environ.get(key):
            print(f"  ✗ Missing env var: {key}", file=sys.stderr)
            print("  Set KAGGLE_USERNAME and KAGGLE_KEY from https://www.kaggle.com/account", file=sys.stderr)
            sys.exit(1)

    try:
        import kaggle  # noqa
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle", "-q"])

    target_path = Path(target)
    target_path.mkdir(parents=True, exist_ok=True)
    print(f"  Downloading {dataset_id} from Kaggle...")
    subprocess.check_call(["kaggle", "datasets", "download", "-d", dataset_id,
                           "-p", str(target_path), "--unzip"])
    print(f"  ✓ Downloaded to {target_path}")


# ---------------------------------------------------------------------------
# Verify / count
# ---------------------------------------------------------------------------

def verify_download(target: str) -> int:
    """Count image files and print directory structure."""
    target_path = Path(target)
    extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff", ".JPEG", ".JPG", ".PNG"}
    count = sum(1 for f in target_path.rglob("*") if f.suffix in extensions)

    print(f"\n  Image files found: {count}")
    print("  Directory structure (2 levels):")
    for item in sorted(target_path.iterdir()):
        print(f"    {item.name}/")
        if item.is_dir():
            sub_items = sorted(item.iterdir())[:5]
            for sub in sub_items:
                n_files = sum(1 for _ in sub.rglob("*") if _.is_file()) if sub.is_dir() else 1
                print(f"      {sub.name}  ({n_files} files)")
            if len(sorted(item.iterdir())) > 5:
                print(f"      ... ({len(sorted(item.iterdir())) - 5} more)")
    return count


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Download a dataset for paper-to-code.")
    parser.add_argument("--source", choices=["torchvision", "hf_hub", "direct", "kaggle"],
                        help="Download source")
    parser.add_argument("--name",   help="torchvision class name (e.g. CIFAR10)")
    parser.add_argument("--id",     help="HuggingFace dataset ID or Kaggle dataset slug")
    parser.add_argument("--url",    help="Direct download URL")
    parser.add_argument("--target", help="Target directory", default="data/dataset")
    parser.add_argument("--size-gb", type=float, default=0.5,
                        help="Expected download size in GB (for disk check)")
    parser.add_argument("--check",  help="Only verify an existing download at this path")
    args = parser.parse_args()

    if args.check:
        count = verify_download(args.check)
        sys.exit(0 if count > 0 else 1)

    print(f"\nTarget: {args.target}")
    if not check_disk_space(".", args.size_gb):
        sys.exit(1)

    if args.source == "torchvision":
        download_torchvision(args.name, args.target)
    elif args.source == "hf_hub":
        download_hf_hub(args.id, args.target)
    elif args.source == "direct":
        download_direct(args.url, args.target)
    elif args.source == "kaggle":
        download_kaggle(args.id, args.target)
    else:
        parser.print_help()
        sys.exit(1)

    count = verify_download(args.target)
    if count == 0:
        print("\n  ⚠️  No image files found — check extraction", file=sys.stderr)
        sys.exit(1)
    print(f"\n✓ Dataset ready: {args.target}  ({count} images)")


if __name__ == "__main__":
    main()
