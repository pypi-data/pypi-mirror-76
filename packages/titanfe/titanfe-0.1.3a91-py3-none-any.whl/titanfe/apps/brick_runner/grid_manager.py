#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#
"""GridManager communication"""

import json
from aiohttp.client_exceptions import ClientError
from aiohttp_requests import requests
from titanfe import log as logging
from titanfe.config import configuration


class GridManager:
    """GridManager """

    def __init__(self, runner, gridmanager_address=None):
        self.address = gridmanager_address or configuration.gridmanager_address
        self.runner = runner

        self.log = logging.getLogger(__name__)

    async def register_runner(self):
        """register brick runner at grid manager"""
        payload = {
            "runnerID": self.runner.uid,
            "address": "%s:%s" % self.runner.address,
            "brickId": self.runner.brick.uid
        }
        response = await requests.post(
            url=f"{self.address}/brickrunners/", data=json.dumps(payload)
        )
        return await response.json()

    async def deregister_runner(self):
        """deregister brick runner at grid manager"""
        payload = {"runnerId": self.runner.uid, "brickId": self.runner.brick.uid}
        await requests.post(url=f"{self.address}/brickrunners/deregister", data=json.dumps(payload))

    async def send_slow_queue_alert(self, brick_id, group_name):
        """send brick scaling request"""
        try:
            payload = {"brickId": brick_id, "consumerId": group_name}
            self.log.info("Request scaling: %r", payload)
            await requests.post(url=f"{self.address}/brickrunners/scaling",
                                data=json.dumps(payload))
        except ClientError as error:
            self.log.info("ScalingRequest failed: %s", error)
