#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""Flow config: parsing and representation"""
import asyncio
from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum

from titanfe import log as logging

from titanfe.constants import DEFAULT_PORT, DEFAULT_MAX_IDLE_TIME
from .brick import Brick


class FlowState(IntEnum):
    ACTIVE = 1
    INACTIVE = 2


@dataclass
class BrickConnection:
    """a connection between two bricks"""

    source: str
    target: str
    source_port: str
    target_port: str

    @classmethod
    def from_config(cls, connection_config, bricks_by_name):
        """create from a dict e.g. as read from yaml"""
        source = bricks_by_name[connection_config["source"]]
        target = bricks_by_name[connection_config["target"]]
        ports = defaultdict(lambda: DEFAULT_PORT)
        ports.update(connection_config.get("ports", {}))
        if not ports["source"]:
            ports["source"] = DEFAULT_PORT
        if not ports["target"]:
            ports["target"] = DEFAULT_PORT
        return cls(source, target, ports["source"], ports["target"])


class Flow:
    """Represent a flow configuration with it bricks and connections

    Arguments:
        flow_config (dict): the flow configuration as dict
        bricks_config (dict): the bricks part of the configuration as dict
        path_to_bricks (Path): path to directory holding the "./bricks" folder
    """

    def __init__(self, uid, name, control_peer, exit_after_idle_seconds, bricks):
        self.name = name
        self.uid = uid
        self.state = FlowState.INACTIVE

        self.log = logging.getLogger(__name__, context=logging.FlowContext.from_flow(self))

        self.control_peer = control_peer
        self.bricks = bricks or []
        self.exit_after_idle_seconds = exit_after_idle_seconds

    @classmethod
    def from_config(cls, control_peer, brick, path_to_bricks):
        """ create a Flow instance from the given configurations

        Args:
            control_peer (ControlPeer): the control peer
            flow_config (dict): the flow configuration
            path_to_bricks (str): path to the local folder containing the bricks' modules

        Returns: a Flow instance
        """
        # pylint: disable=too-many-locals
        flow = cls(
            brick["FlowID"],
            brick["FlowName"],
            control_peer,
            brick["Configuration"].get("exit_after_idle_seconds", DEFAULT_MAX_IDLE_TIME),
            None,
        )

        flow.append_brick(brick, path_to_bricks)
        return flow

    def append_brick(self, brick, path_to_bricks):
        """ create a Flow instance from the given configurations

        Args:
            control_peer (ControlPeer): the control peer
            flow_config (dict): the flow configuration
            path_to_bricks (str): path to the local folder containing the bricks' modules

        Returns: a Flow instance
        """
        brick_instance = Brick.from_config(
            self, brick["Configuration"], path_to_bricks
        )
        brick_instance.update_connections(
            input_connections=brick["Inbound"],
            output_connections=brick["Outbound"],
        )
        brick_instance.create_config_yaml(path_to_bricks)
        self.bricks.append(brick_instance)

    def __repr__(self):
        return f"Flow({self.name}, {self.bricks})"

    def start(self, brick_name):
        """start brick runners for each brick in the flow"""
        self.log.info("start brick: %s, of bricks %r", brick_name, self.bricks)
        self.state = FlowState.ACTIVE
        for brick in self.bricks:
            if brick.name == brick_name:
                self.log.info("start brick: %r", brick)
                brick.start()

    async def stop(self):
        """send a stop signal to all bricks"""
        self.log.info("stopping all bricks for: %s", self)
        await asyncio.gather(*[brick.stop() for brick in self.bricks])
        self.state = FlowState.INACTIVE
        self.bricks = []
        self.log.info("%s stopped", self)


def create_flow(control_peer, brick) -> Flow:
    """assemble the flows utilizing the two config sources"""
    flow = Flow.from_config(control_peer, brick, control_peer.brick_folder)
    flow.log.info("Configured Flow: %r", flow)
    return flow
