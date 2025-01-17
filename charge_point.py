from ocpp.v16 import call, ChargePoint as cp
from ocpp.v16.enums import RegistrationStatus, DiagnosticsStatus, AuthorizationStatus, ChargePointStatus, ChargePointErrorCode
from ocpp.v16.datatypes import MeterValue, SampledValue
import asyncio
from _datetime import datetime


car_id = 'Autito_chiquito'
SEND_ERROR=True

class ChargePoint(cp):
    async def send_boot_notification(self, charger_serial):
        request = call.BootNotificationPayload(
            charge_point_model="Simulator",
            charge_point_vendor="Panchisco",
            charge_point_serial_number=charger_serial,
            firmware_version='version:0.0.1',
            iccid='',
            imsi='',
            meter_serial_number='123456789',
            meter_type='Electromagnetic'
        )

        response = await self.call(request)
        self.interval = 0
        if response.status ==  RegistrationStatus.accepted:
            print("Connected to central system.")
            print(f'interval: {response.interval}')
            self.interval = response.interval
            self.heart_beat_task = asyncio.create_task(self.heart_beat())
        return response.status

    async def send_diagnostics(self,status):
        request = call.DiagnosticsStatusNotificationPayload(
            status=status
        )
        response = await self.call(request)

    async def send_firmware(self,status):
        request = call.FirmwareStatusNotificationPayload(
            status=status
        )
        response = await self.call(request)

    async def send_authorization(self,id_tag):
        request = call.AuthorizePayload(id_tag=id_tag)
        response = await self.call(request)
        if response.id_tag_info['status'] == AuthorizationStatus.accepted:
            print("Authorized by central system.")
        return response.id_tag_info

    async def start_transaction(self,conn_id,meter_start,id_tag,reservation_id):
        if reservation_id == 0:
            reservation_id = None

        request = call.StartTransactionPayload(
            connector_id=int(conn_id),
            meter_start=int(meter_start),
            timestamp=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
            id_tag=str(id_tag),
            reservation_id=reservation_id
        )
        response = await self.call(request)
        print(f'transactionID: {response.transaction_id}')
        return response.transaction_id

    async def stop_transaction(self, id_tag, meter_stop, transaction_id,reason):
        request = call.StopTransactionPayload(
            meter_stop=int(meter_stop),
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
            id_tag=str(id_tag),
            transaction_id=int(transaction_id),
            reason=str(reason)
        )
        response = await self.call(request)
        return response

    async def force_heart_beat(self):
        request = call.HeartbeatPayload()
        response = await self.call(request)

    async def heart_beat(self):
        while True:
            await asyncio.sleep(self.interval)
            request = call.HeartbeatPayload()
            response = await self.call(request)

    async def send_status_notification(self, connector_id=None, error_code=None, info=None, status=None, timestamp=None,
                                       vendor_id=None, vendor_error_code=None):

        request = call.StatusNotificationPayload(
            connector_id=connector_id,
            error_code=error_code,
            info=info,
            status=status,
            timestamp=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
            vendor_id=vendor_id,
            vendor_error_code=vendor_error_code
        )

        response = await self.call(request)
        return response

    async def send_data_transfer(self,vendor_id,message_id,data):
        request = call.DataTransferPayload(
            vendor_id='vendor_id',
            message_id='message_id',
            data='data'
        )
        response = await self.call(request)
        return response

    async def send_meter_values(self,connector_id,meter_value: str,transaction_id):
        print('sending meter values')
        request = call.MeterValuesPayload(
            connector_id=connector_id,
            meter_value=[MeterValue(
                timestamp=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
                sampled_value=[
                    SampledValue(
                        value=meter_value
                    )
                ])
            ],
            transaction_id=transaction_id
        )

        response = await self.call(request)

        print('did not crash')
        return response