# Lab 4, Task 2
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Module for file I/O operations and ZIP archiving.
"""
import os
import zipfile
from typing import List


class FileManager:
    """Handles reading, writing, and archiving text analysis results."""

    def __init__(self):
        self._last_processed = ""

    @property
    def last_processed(self):
        return self._last_processed

    def read_text(self, filepath: str) -> str:
        """Reads content from a text file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Input file not found: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            self._last_processed = filepath
            return f.read()

    def save_results(self, filepath: str, results: dict, original_text: str):
        """Saves analysis dictionary to a formatted text file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("Task 2 | Variant 27 Results\n")
            f.write(f"Source file: {self._last_processed}\n")
            f.write(f"Original length: {len(original_text)} chars\n\n")
            for k, v in results.items():
                if isinstance(v, list):
                    preview = ", ".join(map(str, v[:15]))
                    f.write(f"{k} ({len(v)} items): {preview}{'...' if len(v) > 15 else ''}\n")
                elif isinstance(v, dict):
                    f.write(f"{k}:\n")
                    for sk, sv in v.items():
                        f.write(f"  - {sk}: {sv}\n")
                else:
                    f.write(f"{k}: {v}\n")
            self._last_processed = filepath

    def archive_file(self, source_path: str, zip_path: str) -> List[str]:
        """Compresses file into ZIP and returns archive info."""
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"File to archive not found: {source_path}")

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(source_path, os.path.basename(source_path))

        info_list = []
        with zipfile.ZipFile(zip_path, 'r') as zf:
            for info in zf.infolist():
                info_list.append(
                    f"{info.filename} | Size: {info.file_size} B | "
                    f"Compressed: {info.compress_size} B | Ratio: {100 * (1 - info.compress_size / info.file_size):.1f}%"
                )
        return info_list