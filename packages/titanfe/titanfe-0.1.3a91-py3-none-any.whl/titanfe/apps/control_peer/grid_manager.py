#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#
"""GridManager communication"""

import asyncio
import json
from http import HTTPStatus
from aiohttp.client_exceptions import ClientError
from aiohttp_requests import requests
from titanfe import log as logging
from titanfe.config import configuration
from titanfe.utils import Flag

log = logging.getLogger(__name__)


class GridManager:
    """GridManager """

    def __init__(self, gridmanager_address=None):
        self.address = gridmanager_address or configuration.gridmanager_address
        self._closing = Flag()

    def close(self):
        self._closing.set()
        # TODO: unregister?

    async def register(self, control_peer_address):
        """Register controlpeer at GridManager"""

        def registration_success():
            log.info("Registered ControlPeerApi (%s) at GridManager", control_peer_address)
            return True

        def registration_bad_request():
            log.error("Registration failed with status BadRequest")
            raise ValueError("Registration failed")

        def registration_conflict():
            log.error("Registration failed with status Conflict")
            raise ValueError("Registration failed, address already registered")

        response_handlers = {
            HTTPStatus.OK: registration_success,
            HTTPStatus.CREATED: registration_success,
            HTTPStatus.BAD_REQUEST: registration_bad_request,
            HTTPStatus.CONFLICT: registration_conflict,
        }

        registration = json.dumps(control_peer_address).strip('"')

        while not self._closing:
            try:
                response = await requests.post(self.address+"/controlpeers", json=registration)
                response_handler = response_handlers.get(response.status)
                if response_handler:
                    return response_handler()
            except ClientError:
                log.debug("Could not register at GridManager", exc_info=True)
            else:
                log.debug("Could not register at GridManager: %r", response)

            await asyncio.sleep(0.1)
