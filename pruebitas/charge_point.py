import asyncio
import websockets
import ssl
from datetime import datetime

from ocpp.v16 import call, ChargePoint as cp
from ocpp.v16.enums import RegistrationStatus, DiagnosticsStatus, AuthorizationStatus, ChargePointStatus, ChargePointErrorCode

certificate_path = "C:/Users/Ale/Documents/Certificates/certificate(2).crt"
private_key_path = "C:/Users/Ale/Documents/Certificates/certificate(2).key"
car_id = 'Autito_chiquito'
charger_serial= '123456789'
SEND_ERROR=True



class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Primo",
            charge_point_vendor="Vulletic",
            charge_point_serial_number=charger_serial,
            iccid='holabuenas',
            imsi='holabuenas',
            firmware_version='version:1.1.1',
            meter_serial_number='123456789',
            meter_type='medidor_que_mide'
        )

        response = await self.call(request)
        self.interval = 0
        if response.status ==  RegistrationStatus.accepted:
            print("Connected to central system.")
            print(f'interval: {response.interval}')
            self.interval = response.interval
            self.heart_beat_task = asyncio.create_task(self.heart_beat())
        return response.status

    async def send_diagnostics_status_notification(self):
        request = call.DiagnosticsStatusNotificationPayload(
            status=DiagnosticsStatus.uploaded
        )
        response = await self.call(request)

    async def send_meter_values(self,meter_value):
        request = call.MeterValuesPayload(
            connector_id=1,
            meter_value='IDK'
        )
        response = await self.call(request)

    async def send_authorization(self):
        request = call.AuthorizePayload(id_tag=car_id)
        response = await self.call(request)
        if response.id_tag_info['status'] == AuthorizationStatus.accepted:
            print("Authorized by central system.")
        return response.id_tag_info

    async def start_transaction(self, id_tag):
        request = call.StartTransactionPayload(
            connector_id=1,
            meter_start=0,
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
            id_tag=id_tag
        )
        response = await self.call(request)
        print(f'transactionID: {response.transaction_id}')
        return response.transaction_id

    async def stop_transaction(self, id_tag,transactionId):
        request = call.StopTransactionPayload(
            meter_stop=10,
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
            id_tag=id_tag,
            transaction_id=transactionId
        )
        response = await self.call(request)
        return response

    async def heart_beat(self):
        while True:
            await asyncio.sleep(self.interval)
            request = call.HeartbeatPayload()
            response = await self.call(request)
            print(response.currentTime)

    async def send_status_notification(self,status):
        if status == 'available':
            request = call.StatusNotificationPayload(
                connector_id=1,
                error_code=ChargePointErrorCode.noError,
                status=ChargePointStatus.available
            )
        elif status == 'charging':
            request = call.StatusNotificationPayload(
                connector_id=1,
                error_code=ChargePointErrorCode.noError,
                status=ChargePointStatus.charging
            )
        elif status == 'error':
            request = call.StatusNotificationPayload(
                connector_id=1,
                error_code=ChargePointErrorCode.weakSignal,
                status=ChargePointStatus.faulted
            )
        response = await self.call(request)
        return response

async def main():
    #ssl_context = ssl.create_default_context()
    #ssl_context.load_cert_chain(certfile=certificate_path, keyfile=private_key_path)
    ssl_context = ssl.SSLContext()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with websockets.connect(
            'ws://localhost:8180/steve/websocket/CentralSystemService/123456789', subprotocols=['ocpp1.6']
            #f'wss://wevemobility.com:1234/ws/160/3o2k4BPcOGYo2hRxQtYB3Vg1yQ23/{charger_serial}', subprotocols=['ocpp1.6'], ssl=ssl_context
            ) as ws:

        cp = ChargePoint('CP_1', ws)
        # espieza a escuchar en el puerto
        t1 = asyncio.create_task(cp.start())
        # enciendo el cargador
        t2 = asyncio.create_task(cp.send_boot_notification())

        if (await t2) !=  RegistrationStatus.accepted:
            exit()

        if not SEND_ERROR:
            for i in range(5):
                await asyncio.sleep(1)
                print('Iniciando cargador')
            # mando status idle
            t3 = asyncio.create_task(cp.send_status_notification('available'))
            await t3
            print('status notification sent')

            print('iniciando carga')
            t4 = asyncio.create_task(cp.send_authorization())
            id_tag = await t4
            print(f'idtag: {id_tag}')
            t5 = asyncio.create_task(cp.start_transaction(id_tag=car_id))
            transID = await t5
            t6 = asyncio.create_task(cp.send_status_notification('charging'))
            await t6
            print('Iniciando Carga')
            for i in range(10):
                await asyncio.sleep(1)
                print('cargando')
            t7 = asyncio.create_task(cp.stop_transaction(id_tag=car_id,transactionId = transID))
            print('fin de carga')
            await t7
            t8 = asyncio.create_task(cp.send_status_notification('available'))
            await t8
            print('status sent')
        else:
            for i in range(5):
                await asyncio.sleep(1)
                print('Iniciando cargador')
            # mando status idle
            t3 = asyncio.create_task(cp.send_status_notification('error'))
            await t3
            print('status notification sent')


        await t1 # deja de escuchar

if __name__ == '__main__':
    asyncio.run(main())