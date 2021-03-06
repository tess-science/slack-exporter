# -*- coding: utf-8 -*-

__all__ = ["__version__", "download_files_for_export_path", "main"]

from .slack_exporter_version import __version__
from .files import download_files_for_export_path
from .cli import main

__uri__ = "https://github.com/tess-science/slack-exporter"
__author__ = "Daniel Foreman-Mackey"
__email__ = "foreman.mackey@gmail.com"
__license__ = "MIT"
__description__ = "Make a static archive of your Slack workspace"
