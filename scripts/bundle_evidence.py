#!/usr/bin/env python3
"""
Bundle evidence files for a case into a ZIP archive.

Usage:
  python scripts/bundle_evidence.py CASE_ID /path/to/evidence_dir /path/to/output_dir

The script will create CASE_ID_evidence.zip in the output directory.
"""
import sys
import os
import zipfile


def bundle(case_id: str, evidence_dir: str, output_dir: str) -> str:
    if not os.path.isdir(evidence_dir):
        raise SystemExit(f"Evidence directory not found: {evidence_dir}")
    os.makedirs(output_dir, exist_ok=True)
    zip_name = f"{case_id}_evidence.zip"
    zip_path = os.path.join(output_dir, zip_name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(evidence_dir):
            for f in files:
                full = os.path.join(root, f)
                arcname = os.path.relpath(full, evidence_dir)
                zf.write(full, arcname)
    return zip_path


def main(argv):
    if len(argv) != 4:
        print("Usage: python scripts/bundle_evidence.py CASE_ID /path/to/evidence_dir /path/to/output_dir")
        raise SystemExit(1)
    _, case_id, evidence_dir, output_dir = argv
    zip_path = bundle(case_id, evidence_dir, output_dir)
    print(f"Created evidence bundle: {zip_path}")


if __name__ == "__main__":
    main(sys.argv)
