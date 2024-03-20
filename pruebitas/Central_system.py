import asyncio
import websockets
from datetime import datetime

from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus, AuthorizationStatus
from ocpp.v16 import call_result
from ocpp.v16 import datatypes


class ChargePoint(cp):
    @on(Action.BootNotification)
    def on_boot_notitication(self, **kwargs):
        print("on_boot_notification")

        print(kwargs)
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )

    @on(Action.DiagnosticsStatusNotification)
    def on_diagnostics_status_notification(self, **kwargs):
        print("on_diagnostics_status_notification")
        print(kwargs)
        return call_result.DiagnosticsStatusNotificationPayload()

    @on(Action.Authorize)
    def on_authorize(self, **kwargs):
        print("on_authorize")
        print(kwargs)
        return call_result.AuthorizePayload(
        id_tag_info= datatypes.IdTagInfo(
            status= AuthorizationStatus.accepted
        )
        )

async def on_connect(websocket, path):
    """ For every new charge point that connects, create a ChargePoint instance
    and start listening for messages.

    """
    print('A charger has connected')
    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)
    await cp.start()


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp1.6']
    )

    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())