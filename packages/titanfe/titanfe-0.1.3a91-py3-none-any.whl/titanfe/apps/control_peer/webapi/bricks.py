# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""Routes for Flow management"""

from fastapi import APIRouter
from pydantic import BaseModel  # pylint: disable=no-name-in-module


# Request Parameter
class RequestStateChange(BaseModel):  # pylint: disable=too-few-public-methods
    brick: dict


# Routes
def create_brick_router(control_peer):
    """Setup the routing for flow management

    Arguments:
        control_peer (ControlPeer): an instance of the ControlPeer

    Returns:
        APIRouter: router/routes to manage the control peer's flows
    """

    router = APIRouter()

    @router.put("/{brick_uid}")
    async def change_state(                              # pylint: disable=unused-variable
            brick_uid: str, request: RequestStateChange  # pylint: disable=unused-argument
    ):
        await control_peer.start_brick(request.brick)

    return router
