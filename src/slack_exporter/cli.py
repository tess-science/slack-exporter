#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from .files import download_files_for_export_path


def main():
    if len(sys.argv) < 2:
        print("Usage: slack-exporter /path/to/slack/export")
        sys.exit(0)

    for path in sys.argv[1:]:
        download_files_for_export_path(path)
