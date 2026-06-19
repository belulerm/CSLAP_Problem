#!/usr/bin/env python3
import sys
import os
import re
from pathlib import Path

def print_usage():
    print("Usage: python compress.py <filepath>")

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    filepath = Path(sys.argv[1]).resolve()
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    backup_path = filepath.with_name(filepath.stem + ".original.md")

    if backup_path.exists():
        print(f"Warning: Backup already exists at: {backup_path}")
        print("Aborting to prevent overwriting existing backup.")
        sys.exit(1)

    # Backup the original content
    try:
        original_text = filepath.read_text(encoding="utf-8")
        backup_path.write_text(original_text, encoding="utf-8")
        print(f"Backup created at: {backup_path}")
    except Exception as e:
        print(f"Error creating backup: {e}")
        sys.exit(1)

    print("\nFile backed up successfully. You can now perform the compression.")
    print("Ensure the following elements are preserved exactly:")
    print("1. All Markdown headings (#, ##, etc.)")
    print("2. Code blocks (```)")
    print("3. Links and URLs")
    print("4. File paths and CLI commands")

if __name__ == "__main__":
    main()
