# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""Routes for Flow management"""

from fastapi import APIRouter


# Routes
def create_flow_router(control_peer):
    """Setup the routing for flow management

    Arguments:
        control_peer (ControlPeer): an instance of the ControlPeer

    Returns:
        APIRouter: router/routes to manage the control peer's flows
    """

    router = APIRouter()

    @router.put("/{flow_uid}")
    async def change_flow_state(  # pylint: disable=unused-variable
            flow_uid: str
    ):
        await control_peer.stop_flow(flow_uid)
        return

    return router
