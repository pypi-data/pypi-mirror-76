#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#
"""Flow manager communication"""

from http import HTTPStatus
from aiohttp.client_exceptions import ClientError
from aiohttp_requests import requests
from titanfe import log as logging
from titanfe.config import configuration

log = logging.getLogger(__name__)


async def get_flow_config(flowuid):
    """ask the flow manager for the configuration of the flows"""
    address = configuration.flowmanager_address

    try:
        response = await requests.get(f"{address}/flows/{flowuid}/config")
        if response.status == HTTPStatus.OK:
            return await response.json()
    except ClientError:
        log.error("Requesting flow config failed", exc_info=True)
    else:
        log.error("Requesting flow config failed: %r", response)

    return []
