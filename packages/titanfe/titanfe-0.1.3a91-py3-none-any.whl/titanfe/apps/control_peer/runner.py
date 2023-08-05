#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""Encapsulate brick runner related things"""
import os
import signal
import subprocess
import sys

from titanfe import log as logging
from titanfe.config import configuration

from titanfe.utils import create_uid, Flag


class BrickRunner:
    """The BrickRunner can be used to start brick runner processes and hold corresponding data

    Arguments:
        controlpeer_address (NetworkAddress): the address on which the control peer is listening
    """

    def __init__(self, brick):
        self.uid = create_uid(prefix="R-")
        self.brick = brick

        self.log = logging.getLogger(__name__, context=logging.FlowContext.from_brick(brick))
        self.available = Flag()

        self.known_sources = set()

        self.process = None
        self.output_address = None
        self.connection = None
        self.send = None

    def __repr__(self):
        return (
            f"BrickRunner(id={self.uid},"
            f"brick={self.brick},"
            f"output_address={self.output_address})"
        )

    def start(self) -> "BrickRunner":
        """Start a new brick runner process"""
        br_command = [
            sys.executable,
            "-m",
            "titanfe.apps.brick_runner",
            "-id",
            str(self.uid),
            "-kafka",
            configuration.kafka_bootstrap_servers,
            "-gridmanager",
            configuration.gridmanager_address,
            "-reposervice",
            configuration.reposervice_address,
            "-config",
            self.brick.config_file
        ]

        self.log.debug("command: %r", br_command)
        self.process = subprocess.Popen(br_command)
        br_exitcode = self.process.poll()
        if br_exitcode is not None:
            self.log.error("Failed to start runner. (%s)", br_exitcode)
            return None

        return self

    async def stop(self):
        """request and await runner termination"""
        self.log.info("stop %r", self)
        os.kill(self.process.pid, signal.SIGINT)
