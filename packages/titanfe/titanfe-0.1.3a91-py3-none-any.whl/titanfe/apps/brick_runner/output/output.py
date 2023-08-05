#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""The output with it's server and ports"""

import asyncio
from itertools import chain

from .port import Port
from ..metrics import QueueWithMetrics


class Output:
    """The output side of a brick runner creates a Server.
       It will then send packets as requested by the following inputs.

    Arguments:
        runner (BrickRunner): instance of a parent brick runner
        name (str): a name for the output destination
        address (NetworkAddress): the network address of the output server
    """

    def __init__(self, logger, create_output_queue):
        self.log = logger.getChild("Output")
        self.create_queue = create_output_queue

        self.ports = {}

    def __iter__(self):
        return iter(self.ports.values())

    def __getitem__(self, port_name):
        return self.ports[port_name]

    def __repr__(self):
        return f"Output(ports={repr(self.ports)})"

    @classmethod
    async def create_from_brick_runner(cls, runner):
        """Creates a new instance"""

        def create_new_queue(name):
            return QueueWithMetrics(runner.metric_emitter, name)

        output = cls(runner.log, create_new_queue)

        return output

    def add_targets(self, brick_id, targets, slow_queue_alert_cb):
        for target in targets:
            self.log.debug("add target: %r, %r, %r", brick_id, target, targets)
            self.add_target(brick_id, target, targets[target], slow_queue_alert_cb)

    def add_target(self, brick_id, port_name, targets, slow_queue_alert_cb):
        """add a configured output target"""
        # name, port, autoscale_queue_level = target
        for target in targets:
            target_instance_id = target["InstanceID"]
            autoscale_queue_level = target["autoscale_queue_level"]
            try:
                port = self.ports[port_name]
            except KeyError:
                port = self.ports[port_name] = Port(port_name)

            port.add_consumer_group(
                brick_id,
                target_instance_id,
                self.create_queue(target_instance_id),
                autoscale_queue_level,
                slow_queue_alert_cb,
            )

    async def close(self):
        """close all connections and the server itself"""
        if self.ports:
            await asyncio.wait({port.close() for port in self})

    @property
    def consumer_groups(self):
        return chain.from_iterable(self)

    @property
    def is_empty(self):
        """True, if no packets are waiting to be outputted"""
        return not any(group.has_unfinished_business for group in self.consumer_groups)
