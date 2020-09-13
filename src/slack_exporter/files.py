# -*- coding: utf-8 -*-

__all__ = ["download_files_for_export_path"]

import os
import json
from pathlib import Path
from typing import List, Optional

import asyncio
from aiohttp import ClientSession

import tqdm


async def fetch(
    bar: tqdm.tqdm, session: ClientSession, filename: str, url: str
) -> None:
    async with session.get(url) as response:
        data = await response.read()
        with open(filename, "wb") as f:
            f.write(data)
        bar.update()


async def bound_fetch(
    bar: tqdm.tqdm,
    sem: asyncio.Semaphore,
    session: ClientSession,
    filename: str,
    url: str,
) -> None:
    async with sem:
        await fetch(bar, session, filename, url)


async def execute_downloads(
    bar: tqdm.tqdm, filenames: List[str], urls: List[str]
) -> None:
    tasks = []
    sem = asyncio.Semaphore(10)
    async with ClientSession() as session:
        for fn, url in zip(filenames, urls):
            task = asyncio.ensure_future(
                bound_fetch(bar, sem, session, fn, url)
            )
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses


def download_files(filenames: List[str], urls: List[str]) -> None:
    with tqdm.tqdm(total=len(filenames)) as bar:
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(execute_downloads(bar, filenames, urls))
        loop.run_until_complete(future)


def find_files(obj: dict) -> List[str]:
    try:
        keys = obj.keys()
    except AttributeError:
        # It's a list or a plain object
        if isinstance(obj, str):
            return []
        try:
            return [link for blob in obj for link in find_files(blob)]
        except TypeError:
            return []

    if "url_private_download" in keys:
        return [obj["url_private_download"]]

    return [link for k in keys for link in find_files(obj[k])]


def download_files_for_export_path(
    path: str, output_directory: Optional[str] = None
) -> None:
    output_dir: str = output_directory if output_directory else "."

    files: List[str] = []
    for name in Path(path).rglob("*.json"):
        with open(name, "r") as f:
            blob = json.load(f)
        files += find_files(blob)

    filenames = []
    for url in files:
        filenames.append(
            os.path.join(output_dir, url.split("//")[-1].split("?")[0])
        )
        os.makedirs(os.path.split(filenames[-1])[0], exist_ok=True)

    download_files(filenames, files)
