#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""the actual control peer"""

import asyncio
import signal
from pathlib import Path

from titanfe import log as logging
from titanfe.apps.control_peer.package_manager import install_brick
from titanfe.config import configuration
from titanfe.log import TitanLogAdapter, FlowContext
from titanfe.utils import Flag, parse_yaml
from .grid_manager import GridManager
from .webapi import WebApi
from .flow import create_flow

log = logging.getLogger(__name__)


class ControlPeer:
    """The control peer application will start runners as required for the flows/bricks
       as described in the given config file. Once the runners have registered themselves,
       they will get according assignments.

    Arguments:
        brick_folder (Path): path to the brick config yaml
    """

    def __init__(self, brick_folder):
        self.loop = asyncio.get_event_loop()
        self.brick_folder = Path(brick_folder)

        self.flows = []
        self.flows_by_uid = {}
        self.runners = {}
        self.runner_connections = {}

        self.server = None
        self.server_address = None
        self.webapi = None
        self.grid_manager = None
        self.flow_manager = None
        self.exit = Flag()

    @classmethod
    async def create(cls, brick_folder, config_file):
        """"Create control peer"""
        control_peer = cls(brick_folder)
        await control_peer.setup(config_file)
        return control_peer

    async def setup(self, config_file):
        """setup ControlPeer
        Arguments:
            config_file: YAML file with CP configuration
        """

        cp_config = parse_yaml(config_file)
        configuration.update(cp_config)

        self.setup_webapi()

        logging.initialize(service="ControlPeer")

        self.grid_manager = GridManager()

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    async def run(self):
        """run the application"""
        log.debug("running control peer")

        try:
            await self.grid_manager.register(self.webapi.address)
        except Exception:  # pylint: disable=broad-except
            log.warning("Failed to register, shutting down.")
            return await self.shutdown()

        await self.exit.wait()
        log.info("Exit")

    def handle_signal(self, sig, frame):  # pylint: disable=unused-argument
        asyncio.create_task(self.shutdown())

    async def shutdown(self):
        """shut down the controlpeer"""
        log.info("Initiating shutdown")
        await self.stop_flows()
        self.grid_manager.close()
        await self.webapi.stop()

        self.exit.set()
        log.info("Shutdown sequence complete - should exit soon")

        pending_tasks = asyncio.all_tasks()
        for task in pending_tasks:
            log.info("still pending: %r", task)
            task.cancel()
            await task

    def setup_webapi(self):
        self.webapi = WebApi(self)
        self.webapi.run()

    async def start_brick(self, brick):
        """update the configuration and start the flow"""
        try:
            await install_brick(brick["Configuration"]["id"], self.brick_folder)

            flow = self.flows_by_uid.get(brick["FlowID"])

            if not flow:
                flow = create_flow(self, brick)
                self.flows.append(flow)
                self.flows_by_uid[flow.uid] = flow
            else:
                flow.append_brick(brick, self.brick_folder)

            flow.start(brick["Configuration"]["name"])
        except Exception:  # pylint: disable=broad-except
            logger = TitanLogAdapter(log, extra=FlowContext(flowuid=brick["FlowID"]).asdict())
            logger.error("Failed to start flow %s", brick["FlowID"], exc_info=True)

    async def stop_flows(self):
        await asyncio.gather(*[flow.stop() for flow in self.flows])

    async def stop_flow(self, flowuid):
        """stop a flow"""
        log.info("Stop flow: %s, %r", flowuid, self.flows_by_uid)
        flow = self.flows_by_uid.get(flowuid)
        if not flow:
            return
        log.info("Stop flow: %s", flow)
        await flow.stop()
        return flow
