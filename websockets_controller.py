import sys
import ssl
import websockets
import threading
import asyncio

import views.main_window
from charge_point import ChargePoint

class OCPPThread(threading.Thread):
    message_received = asyncio.Queue()

    def __init__(self, parent):
        super().__init__()
        self.url = None
        self.loop = asyncio.new_event_loop()
        self.websocket = None
        self.parent_window = parent
        self.charge_point: ChargePoint = None

    def run(self):
        async def ws_handler():
            while self.websocket is None:
                if self.url is not None:
                    try:
                        ssl_context = ssl.SSLContext()
                        ssl_context.check_hostname = False
                        ssl_context.verify_mode = ssl.CERT_NONE
                        self.websocket = await websockets.connect(self.url, subprotocols=['ocpp1.6'],ssl=ssl_context)
                    except Exception as e:
                        print(e)
                        self.websocket = None
                        self.url = None

            print('Connected')
            self.parent_window.btn_connect.setDisabled(True)
            self.parent_window.btn_close_connection.setEnabled(True)
            self.charge_point = ChargePoint('id',self.websocket)
            try:
                await self.charge_point.start()
            except:
                print('Connection closed')

        asyncio.set_event_loop(self.loop)

        self.loop.run_until_complete(ws_handler())

    def stop(self):
        asyncio.run_coroutine_threadsafe(self.websocket.close(), self.loop)



    def send_boot_notification(self):
        # Using asyncio.run() to await the async function
        async def send_boot_notification():
            await self.charge_point.send_boot_notification(self.parent_window.txt_serial.text())

        if self.loop.is_running():
            asyncio.run_coroutine_threadsafe(send_boot_notification(), self.loop)
        else:
            print("Event loop is not running.")

    def send_heart_beat(self):
        async def force_heart_beat():
            await self.charge_point.force_heart_beat()

        if self.loop.is_running():
            asyncio.run_coroutine_threadsafe(force_heart_beat(), self.loop)
        else:
            print("Event loop is not running.")

    def send_status(self):
        async def send_status():
            await self.charge_point.send_status_notification(
                connector_id=self.parent_window.spin_conn_id.value(),
                error_code=self.parent_window.cmb_err_code.currentText(),
                info=self.parent_window.txt_info_code.text(),
                status=self.parent_window.cmb_sts_code.currentText(),
                timestamp=self.parent_window.ck_time_stamp_id.checkState(),
                vendor_id=self.parent_window.txt_vndr_id.text(),
                vendor_error_code=self.parent_window.txt_vndr_err_code.text()
            )

        if self.loop.is_running():
            try:
                asyncio.run_coroutine_threadsafe(send_status(), self.loop)
            except:
                print('se rompio :(')
        else:
            print("Event loop is not running.")