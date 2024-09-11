import sys
import ssl
import websockets
import threading
import asyncio
from datetime import datetime

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
                        if self.url[:3] == 'wss':
                            ssl_context = ssl.SSLContext()
                            ssl_context.check_hostname = False
                            ssl_context.verify_mode = ssl.CERT_NONE
                            self.websocket = await websockets.connect(self.url, subprotocols=['ocpp1.6'],
                                                                      ssl=ssl_context)
                        else:
                            self.websocket = await websockets.connect(self.url, subprotocols=['ocpp1.6'])
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
                #timestamp=self.parent_window.ck_time_stamp_id.checkState(),
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

    def send_many_status(self):
        async def send_status(connector_id):
            await self.charge_point.send_status_notification(
                connector_id=connector_id,
                error_code=self.parent_window.cmb_err_code.currentText(),
                info=self.parent_window.txt_info_code.text(),
                status=self.parent_window.cmb_sts_code.currentText(),
                # timestamp=self.parent_window.ck_time_stamp_id.checkState(),
                vendor_id=self.parent_window.txt_vndr_id.text(),
                vendor_error_code=self.parent_window.txt_vndr_err_code.text()
            )

        if self.loop.is_running():
            try:
                for connector in range(self.parent_window.spin_conn_id.value()):
                    asyncio.run_coroutine_threadsafe(send_status(connector + 1), self.loop)
            except:
                print('se rompio :(')
        else:
            print("Event loop is not running.")

    def send_start_transaction(self):
        async def send_transaction():
            transaction_id = await self.charge_point.start_transaction(
                conn_id = self.parent_window.spin_conn_id_start_trasaction.value(),
                meter_start=self.parent_window.spin_meter_start.value(),
                id_tag=self.parent_window.txt_idtag.text(),
                reservation_id=self.parent_window.spin_resrvation_id.value(),
            )
            self.parent_window.spin_transaction_id.setValue(transaction_id)
            self.parent_window.txt_transaction_id_meter_value.setValue(transaction_id)
        if self.loop.is_running():
            try:
                asyncio.run_coroutine_threadsafe(send_transaction(), self.loop)
            except Exception as e:
                print(e)
        else:
            print("Event loop is not running.")


    def send_stop_transaction(self):
        async def send_stop_transaction():
            await self.charge_point.stop_transaction(
                id_tag=self.parent_window.txt_idtag_stop_transaction.text(),
                meter_stop=self.parent_window.spin_meter_stop.value(),
                transaction_id=self.parent_window.spin_transaction_id.value(),
                reason=self.parent_window.cmb_reason.currentText()
            )

        if self.loop.is_running():
            try:
                asyncio.run_coroutine_threadsafe(send_stop_transaction(), self.loop)
            except Exception as e:
                print(e)
        else:
            print("Event loop is not running.")

    def send_authorization(self):
        async def send_authorization():
            await self.charge_point.send_authorization(
                id_tag=self.parent_window.txt_idtag_authorize.text(),
            )

        if self.loop.is_running():
            try:
                asyncio.run_coroutine_threadsafe(send_authorization(), self.loop)
            except Exception as e:
                print(e)
        else:
            print("Event loop is not running.")

    def send_data_transfer(self):
        async def send_data_transfer():
            await self.charge_point.send_data_transfer(
                vendor_id=self.parent_window.vendor_id.text(),
                message_id=self.parent_window.txt_messageId.text(),
                data=self.parent_window.txt_data.text()
            )

        if self.loop.is_running():
            try:
                asyncio.run_coroutine_threadsafe(send_data_transfer(), self.loop)
            except Exception as e:
                print(e)
        else:
            print("Event loop is not running.")

    def send_diagnostics(self):
        async def send_diagnostics():
            await self.charge_point.send_diagnostics(
                status=self.parent_window.cmb_status.currentText(),
            )

        if self.loop.is_running():
            try:
                asyncio.run_coroutine_threadsafe(send_diagnostics(), self.loop)
            except Exception as e:
                print(e)
        else:
            print("Event loop is not running.")

    def send_firmware(self):
        async def send_firmware():
            await self.charge_point.send_firmware(
                status=self.parent_window.cmb_firmware_status.currentText(),
            )

        if self.loop.is_running():
            try:
                asyncio.run_coroutine_threadsafe(send_firmware(), self.loop)
            except Exception as e:
                print(e)
        else:
            print("Event loop is not running.")

    def send_meter_values(self):
        async def send_meter_values():
            await self.charge_point.send_meter_values(
                connector_id = self.parent_window.spin_conn_id_meter_value.value(),
                meter_value = str(self.parent_window.txt_meter_value.text()),
                transaction_id = self.parent_window.txt_transaction_id_meter_value.value()
            )

        if self.loop.is_running():
            try:
                asyncio.run_coroutine_threadsafe(send_meter_values(), self.loop)
            except Exception as e:
                print(e)
        else:
            print("Event loop is not running.")
