#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

""" Brick Runner (application)
"""

import argparse
import asyncio
import sys

from titanfe.config import configuration
from titanfe import log as logging
from titanfe.apps.brick_runner.runner import BrickRunner


if "win" in sys.platform:
    # Windows specific event-loop policy
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
else:
    import uvloop  # pylint: disable=import-error

    uvloop.install()


async def run_app(args):
    """ let's do this """

    configuration.kafka_bootstrap_servers = args.kafka
    configuration.gridmanager_address = args.gridmanager
    configuration.reposervice_address = args.reposervice
    logging.initialize("BrickRunner")

    runner = await BrickRunner.create(args.id, args.config)
    await runner.run()


def main():
    """parse args and run the application"""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-id", type=str, help="Brick Runner ID")  # uuid.UUID,
    arg_parser.add_argument("-kafka", type=str, help="Kafka bootstrap servers")
    arg_parser.add_argument("-gridmanager", type=str, help="GridManager address")
    arg_parser.add_argument("-reposervice", type=str, help="Repository Service address")
    arg_parser.add_argument("-config", type=str, help="config file")

    args = arg_parser.parse_args()

    asyncio.run(run_app(args))


if __name__ == "__main__":
    main()
