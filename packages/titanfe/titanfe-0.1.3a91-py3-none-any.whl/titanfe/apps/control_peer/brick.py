#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""A Brick"""

import re

from ruamel import yaml

from titanfe import log as logging
from titanfe.messages import BrickDescription
from titanfe.constants import DEFAULT_PORT

from .runner import BrickRunner


class Brick:
    """Encapsulate the Brick functions"""

    # pylint: disable=too-many-arguments, too-many-instance-attributes
    def __init__(
        self,
        flow,
        instance_id,
        instance_name,
        brick_id,
        brick_name,
        brick_family,
        module_path,
        parameters,
        autoscale_max_instances,
        autoscale_queue_level,
        exit_after_idle_seconds,
    ):
        self.uid = instance_id
        self.flow = flow
        self.name = instance_name
        self.brick_type = brick_name
        self.brick_id = brick_id
        self.brick_family = brick_family

        self.log = logging.getLogger(__name__, context=logging.FlowContext.from_brick(self))

        self.module_path = module_path
        self.parameters = parameters

        self.autoscale_max_instances = autoscale_max_instances
        self.autoscale_queue_level = autoscale_queue_level
        self.exit_after_idle_seconds = exit_after_idle_seconds

        self.input_connections = []
        self.output_connections = {}

        self.runners = []
        self.tasks = []
        self.config_file = None

    def __repr__(self):
        return (
            f"Brick({self.name}, {self.uid}, {self.module_path}, "
            f"parameters={self.parameters},"
            f"autoscale_queue_level={self.autoscale_queue_level},"
            f"autoscale_max_instances={self.autoscale_max_instances})"
        )

    def __hash__(self):
        return hash(self.uid)

    def __eq__(self, other):
        if isinstance(other, Brick):
            return other.uid == self.uid
        return False

    @classmethod
    def from_config(cls, flow, brick_config, path_to_modul_dir):
        """Add brick configuration using default and flow-specific parameters if available"""

        brick_name = brick_config["brick"]
        brick_id = brick_config["id"]

        instance_name = brick_config["name"]
        instance_id = brick_config["instanceId"]

        module_parent = path_to_modul_dir / brick_id

        try:
            module_path = next(
                path
                for path in module_parent.iterdir()
                if re.match(f"^{brick_name}(?:\\.py)?$", path.name, re.IGNORECASE)
            )
        except StopIteration:
            raise LookupError(f"Missing module {brick_name} or {brick_name}.py")

        config_file = module_path.parent / "config.yml"
        try:
            with open(config_file) as config_file:
                parameters = yaml.safe_load(config_file)
        except FileNotFoundError:
            parameters = {}

        parameters.update(brick_config.get("parameters") or {})

        brick = cls(
            flow,
            instance_id,
            instance_name,
            brick_id,
            brick_name,
            brick_config.get("family", "General"),
            module_path,
            parameters,
            brick_config.get("autoscale_max_instances", 1),
            brick_config.get("autoscale_queue_level", 25),
            brick_config.get("exit_after_idle_seconds", flow.exit_after_idle_seconds),
        )
        return brick

    def update_connections(self, input_connections, output_connections):
        self.input_connections = input_connections
        self.output_connections = output_connections

    def start(self):
        self.start_new_runner()

    def start_new_runner(self):
        """start a new brickrunner"""
        runner = BrickRunner(self).start()
        self.runners.append(runner)
        self.log.debug("%s started runner %s", self, runner)

    async def stop(self):
        for runner in self.runners:
            await runner.stop()

    def remove_runner(self, runner):
        self.runners.remove(runner)

    def create_config_yaml(self, path_to_bricks):
        """create_config_yaml for sending Brick configuration to BR"""
        with open(r'%s/%s/%s.yaml' % (path_to_bricks, self.brick_id, self.brick_id), 'w') as file:
            setup = {}
            setup["brick"] = self.description._asdict()
            setup["output_connections"] = self.output_connections or []
            self.config_file = file.name
            yaml.dump(setup, file)

    @property
    def description(self):
        return BrickDescription(
            flowuid=self.flow.uid,
            flowname=self.flow.name,
            name=self.name,
            uid=self.uid,
            brick_type=self.brick_type,
            brick_family=self.brick_family,
            path_to_module=str(self.module_path),
            parameters=self.parameters,
            is_inlet=not bool(self.input_connections),
            exit_after_idle_seconds=self.exit_after_idle_seconds,
            default_port=next(iter(self.output_connections.keys()), DEFAULT_PORT)
        )
