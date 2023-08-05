#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#
"""Install a Brick"""
import shutil
from http import HTTPStatus
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from aiohttp.client_exceptions import ClientError
from aiohttp_requests import requests
from titanfe import log as logging
from titanfe.config import configuration
log = logging.getLogger(__name__)


async def install_brick(brick_id, parent_folder, force_update=False):
    """ Get a brick from the package manager and install it"""
    if not isinstance(parent_folder, Path):
        parent_folder = Path(parent_folder)

    if parent_folder.stem == brick_id:
        destination = parent_folder
    else:
        destination = parent_folder / brick_id

    if destination.exists():
        log.info("Brick %s is already present", brick_id)

        if force_update:
            shutil.rmtree(destination)
        else:
            last_modified = await get_source_last_modified(brick_id)
            local_timestamp = get_local_timestamp_for_brick(destination)
            if int(last_modified) <= int(local_timestamp):
                return

    destination.mkdir(parents=True, exist_ok=True)

    source = await get_source_archive(brick_id)
    lastmodified = await get_source_last_modified(brick_id)

    if not source:
        return

    with ZipFile(BytesIO(source), 'r') as compressed:
        log.info("compressed brick content: %s", compressed.printdir())
        compressed.extractall(path=destination)
    (destination / ("lastmodified.txt")).write_text(str(int(lastmodified)), encoding="utf-8")

    log.info("installed brick %s - %s", brick_id, list(destination.iterdir()))
    return destination


async def get_source_archive(brick_id):
    """get the source files archive from the package manager"""
    pacman = configuration.packagemanager_address
    try:
        response = await requests.get(f"{pacman}/bricks/{brick_id}")
        if response.status == HTTPStatus.OK:
            return await response.read()
    except ClientError:
        log.error("Requesting brick failed", exc_info=True)
    else:
        log.error("Requesting brick failed: %r", response)


async def get_source_last_modified(brick_id):
    """get the source files archive from the package manager"""
    pacman = configuration.packagemanager_address
    # pacman = "http://192.168.178.43:8087/packagemanager"
    try:
        response = await requests.get(f"{pacman}/bricks/{brick_id}/lastmodified")
        if response.status == HTTPStatus.OK:
            return await response.read()
    except ClientError:
        log.error("Requesting brick lastmodified failed", exc_info=True)
    else:
        log.error("Requesting brick lastmodified failed: %r", response)


def get_local_timestamp_for_brick(destination):
    if (destination / ("lastmodified.txt")).exists():
        timestamp = (destination / ("lastmodified.txt")).read_text()
        return timestamp
    return 0
