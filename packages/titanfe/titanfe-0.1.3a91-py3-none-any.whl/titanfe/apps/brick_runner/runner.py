#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""The actual brick runner"""

import asyncio
import signal
import json
from datetime import datetime, timedelta


from titanfe import log as logging
from titanfe.utils import cancel_tasks, get_ip_address, parse_yaml
from titanfe.messages import BrickDescription, Message
from titanfe.connection import Connection

from .input import Input
from .metrics import MetricEmitter
from .output import Output, Consumer
from .brick import Brick
from .packet import Packet
from .grid_manager import GridManager


class BrickRunner:
    """The BrickRunner will create an Input, get a setup from the control peer,
       create corresponding outputs and then start processing packets from the input.

    Arguments:
        uid (str): a unique id for the runner
    """

    def __init__(self, uid, config_file):
        self.uid = uid
        self.config_file = config_file
        self.log = logging.getLogger(f"{__name__}.{self.uid}", context=logging.global_context)
        self.loop = asyncio.get_event_loop()

        # done async in setup
        self.input = None
        self.output = None
        self.brick = None
        self.server = None
        self.address = (None, None)
        self.gridmanager = None

        self.setup_completed = asyncio.Event()

        self.metric_emitter = None
        self.tasks = []

    @classmethod
    async def create(cls, uid, config_file):
        """Creates a brick runner instance and does the initial setup phase before returning it"""
        br = cls(uid, config_file)  # pylint: disable=invalid-name
        await br.setup()
        return br

    async def setup(self):
        """does the inital setup parts that have to be awaited"""
        await self.start_server()
        self.metric_emitter = await MetricEmitter.create_from_brick_runner(self)
        self.input = Input(self)
        self.output = await Output.create_from_brick_runner(self)

        config = parse_yaml(self.config_file)
        self.brick = Brick(BrickDescription(**config["brick"]), self.metric_emitter, self.log)
        self.gridmanager = GridManager(self)

        available_input_sources = await self.gridmanager.register_runner()
        if available_input_sources:
            self.log.info("input sources %s", available_input_sources)
            self.input.add_sources(available_input_sources)

        self.metric_emitter.assign_brick_flow_attributes(self)

        if config["output_connections"]:
            self.output.add_targets(
                self.brick.uid, config["output_connections"], self.gridmanager.send_slow_queue_alert
            )
            self.tasks.append(asyncio.create_task(self.output_results()))

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        self.setup_completed.set()

    async def run(self):
        """process items from the input"""
        self.log.info("start runner: %s", self.uid)

        if self.brick.is_inlet:
            # trigger processing
            await self.input.put(Packet())

        if not self.brick.is_inlet:
            self.tasks.append(asyncio.create_task(self.exit_when_idle()))

        await self.process_input()
        await self.shutdown()
        self.log.info("Exit")

    async def start_server(self):
        """start server"""
        self.server = await asyncio.start_server(
            self.handle_incoming_connection, host=get_ip_address()
        )
        self.address = self.server.sockets[0].getsockname()

    async def handle_incoming_connection(self, reader, writer):
        """create consumers for incoming connections and dispatch the connection to them"""
        await self.setup_completed.wait()

        connection = Connection(reader, writer, self.log)

        # We can remove this once the Gridmanager starts sending UJO Messages
        try:
            msg_len = await connection.reader.readexactly(4)
        except (asyncio.IncompleteReadError, ConnectionError):
            self.log.debug("Stream at EOF - close connection.")
            # self.log.debug('', exc_info=True)
            await connection.close()
            return

        rawmsg = await connection.reader.readexactly(int.from_bytes(msg_len, "big"))

        try:
            msg = connection.decode(rawmsg)
            message = Message(*msg)
        except TypeError:
            self.log.error("Received unknown Message format: %s", rawmsg)
            return
        except Exception:   # pylint: disable=broad-except
            # self.log.error("Failed to decode %r", msg, exc_info=True)
            # raise ValueError(f"Failed to decode {msg}")
            # TODO: # Use UJO Encoding and appropriate msg format in GridManager
            self.log.info("new input source available: %s", json.loads(rawmsg))
            self.input.add_source(json.loads(rawmsg))
        else:
            self.log.info("new consumer entered: %s", message.content)
            brick_instance_id, port = message.content
            self.output[port].add_consumer(Consumer(port, brick_instance_id, connection))

    async def process_input(self):
        with self.brick:
            async for packet in self.input:
                packet.update_input_exit()
                self.log.debug("process packet: %s", packet)
                await self.brick.process(packet)

    def handle_signal(self, sig, frame):  # pylint: disable=unused-argument
        asyncio.create_task(self.shutdown())

    async def stop_processing(self):
        """stop processing bricks"""
        self.log.info("Stop Processing")
        await self.gridmanager.deregister_runner()
        await self.input.close()
        self.brick.terminate()
        self.server.close()
        await self.server.wait_closed()
        await self.output.close()
        await self.metric_emitter.stop()

    async def shutdown(self):
        """shuts down the brick runner"""
        self.log.info("Initiating Shutdown")
        await cancel_tasks(self.tasks, wait_cancelled=True)
        await self.metric_emitter.stop()
        self.log.info("Shutdown sequence complete - should exit soon")

    async def output_results(self):
        """get results from the brick execution and add them to the output queues of this runner"""
        async for packet, port in self.brick.get_results():
            await self.output[port].enqueue(packet)
            packet.update_output_entry()

    @property
    def is_idle(self):
        return self.input.is_empty and self.output.is_empty and not self.brick.is_processing

    async def exit_when_idle(self):
        """Schedule as task to initiate shutdown if the configured maximum idle time is reached"""

        # check at least once per second:
        interval = min(self.brick.exit_after_idle_seconds * 0.1, 1)

        idle_since = None
        idle_time = timedelta(seconds=0)
        max_idle_time = timedelta(seconds=self.brick.exit_after_idle_seconds)

        while idle_time <= max_idle_time:
            await asyncio.sleep(interval)

            if not self.is_idle:
                idle_since = None
                continue

            if idle_since is None:
                idle_since = datetime.now()
                continue

            idle_time = datetime.now() - idle_since

        self.log.warning("Max idle time reached. Scheduling shutdown")
        await self.stop_processing()
