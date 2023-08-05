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
from pathlib import Path

import titanfe.log
from titanfe.apps.control_peer.controlpeer import ControlPeer

log = titanfe.log.getLogger(__name__)


async def run_app(args):
    """run the application"""
    cp = await ControlPeer.create(args.brick_folder,  # pylint: disable=invalid-name
                                  args.config_file)
    await cp.run()


def main():
    """parse args and run the application"""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        # TODO: deprecate
        "-brick_config", help="Brick configuration file", default="../../../examples/demo_flow.yml"
    )
    arg_parser.add_argument(
        "-brick_folder", help="Brick folder", default=str(Path.home() / "titanfe/bricks")
    )
    arg_parser.add_argument(
        "-config_file",
        help="Location of the config file",
        default=Path(__file__).parent/"config.yaml",
    )
    args = arg_parser.parse_args()

    asyncio.run(run_app(args))


if __name__ == "__main__":

    if "win" in sys.platform:
        # see: https://docs.python.org/dev/whatsnew/3.8.html#asyncio
        # On Windows: Ctrl-C bug in asyncio (fixed in Py3.8) - TODO: workaround?
        # Windows specific event-loop policy (default in Py3.8)
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    else:
        import uvloop  # pylint: disable=import-error

        uvloop.install()

    main()
