import time
from utils import cache_string, get_cached_strings
from PyQt6.QtWidgets import (QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QSpinBox,
                             QGroupBox, QComboBox, QCheckBox, QSpacerItem, QSizePolicy, QCompleter)
from websockets_controller import OCPPThread
from views.send_status import StatusNotificationWindow
from ocpp.v16.enums import ChargePointStatus, ChargePointErrorCode, Reason, DiagnosticsStatus, FirmwareStatus
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.compose_window()
        self.var = False


    # conections methods
    def __on_click_connect_ws_server(self):
        self.ocpp_thread = OCPPThread(self)
        self.ocpp_thread.start()
        cache_string('urls',self.txt_url.text())
        self.ocpp_thread.url = f"{self.txt_url.text()}/{self.txt_serial.text()}"


    # buttons methods
    def __on_click_send_boot_notification(self):
        self.ocpp_thread.send_boot_notification()
        print('Sending boot notification')

    def __on_click_close_conection(self):
        self.ocpp_thread.stop()
        self.ocpp_thread.join()
        self.btn_connect.setDisabled(False)
        self.btn_close_connection.setDisabled(True)
        print(self.ocpp_thread.is_alive())

    def __on_click_send_heartbeat(self):
        self.ocpp_thread.send_heart_beat()
        print('Sending heartbeat')

    # status methods
    def __on_click_btn_send_status(self):
        self.ocpp_thread.send_status()
        print('sending status')

    def __on_click_btn_send_many_status(self):
        self.ocpp_thread.send_many_status()
        print('sending many status')

    def __on_click_btn_send_start_transaction(self):
        self.ocpp_thread.send_start_transaction()
        print('sending start transaction')

    def __on_click_btn_send_stop_transaction(self):
        self.ocpp_thread.send_stop_transaction()
        print('sending start transaction')

    def __on_click_btn_send_authorization(self):
        self.ocpp_thread.send_authorization()
        print('sending authorization')

    def __on_click_btn_send_data_transfer(self):
        self.ocpp_thread.send_data_transfer()
        print('sending data transfer')

    def __on_click_btn_send_diagnostics_status(self):
        self.ocpp_thread.send_diagnostics()
        print('sending diagnostics')

    def __on_click_btn_send_firmware_status(self):
        self.ocpp_thread.send_firmware()
        print('sending firmware')

    def __on_click_btn_send_meter_values(self):
        self.ocpp_thread.send_meter_values()

    # other methods
    def close_event(self):
        self.ocpp_thread.join()

    # composers
    def compose_window(self):
        self.setWindowTitle('OCPP Simulator')
        self.setMaximumSize(940,480)
        self.setMinimumSize(940, 480)

        # first row
        # call all composers
        connections_layout = self.compose_connection()
        button_layout = self.compose_buttons_column()
        status_layout = self.compose_status()
        start_transaction_layout = self.compose_start_transaction()
        stop_start_layout = self.compose_stop_transaction()

        first_row_layout = QHBoxLayout()
        first_row_layout.addLayout(button_layout)
        first_row_layout.addLayout(status_layout)
        first_row_layout.addLayout(start_transaction_layout)
        first_row_layout.addLayout(stop_start_layout)
        first_row_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))

        # second row
        # call composers
        data_transfer_layout = self.compose_data_transfer()
        diagnostics_layout = self.compose_diagnostic_status()
        firmware_status_layout = self.compose_firmware_status()
        send_meter_value_layout = self.compose_meter_value()

        second_row_layout = QHBoxLayout()
        second_row_layout.addLayout(data_transfer_layout)
        second_row_layout.addLayout(diagnostics_layout)
        second_row_layout.addLayout(firmware_status_layout)
        second_row_layout.addLayout(send_meter_value_layout)
        second_row_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))

        main_layout = QVBoxLayout()
        main_layout.addLayout(connections_layout)
        main_layout.addLayout(first_row_layout)
        main_layout.addLayout(second_row_layout)
        main_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding))

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def compose_connection(self):
        self.lbl_url = QLabel('Ingrese los datos de conexion a su sistema.')
        self.txt_url = QLineEdit()
        self.url_completer = QCompleter(get_cached_strings('urls'))
        self.txt_url.setCompleter(self.url_completer)
        self.txt_url.setPlaceholderText('URL de su sistema central')
        self.lbl_slash = QLabel('/')
        self.txt_serial = QLineEdit()
        self.txt_serial.setPlaceholderText('Numero de serie del dispositivo')
        self.txt_serial.setFixedWidth(200)

        url_layout = QHBoxLayout()
        url_layout.addWidget(self.lbl_url)
        url_layout.addWidget(self.txt_url)
        url_layout.addWidget(self.lbl_slash)
        url_layout.addWidget(self.txt_serial)

        return url_layout

    def compose_buttons_column(self):
        self.btn_connect = QPushButton("Connect")
        self.btn_connect.clicked.connect(self.__on_click_connect_ws_server)

        self.btn_close_connection = QPushButton("Disconect")
        self.btn_close_connection.setDisabled(True)
        self.btn_close_connection.clicked.connect(self.__on_click_close_conection)

        self.button_send_boot_notification = QPushButton("Send boot notification")
        self.button_send_boot_notification.clicked.connect(self.__on_click_send_boot_notification)

        self.button_sendheart_beat = QPushButton("Send heartbeat")
        self.button_sendheart_beat.clicked.connect(self.__on_click_send_heartbeat)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.btn_connect)
        buttons_layout.addWidget(self.btn_close_connection)
        buttons_layout.addWidget(self.button_send_boot_notification)
        buttons_layout.addWidget(self.button_sendheart_beat)

        authorize_group = self.compose_authorize()

        buttons_layout.addLayout(authorize_group)

        return buttons_layout

    def compose_status(self):
        group = QGroupBox('Status Notifications')
        group.setMaximumWidth(270)

        self.btn_send_status = QPushButton("Send")
        self.btn_send_many_status = QPushButton("Send many")
        self.btn_send_status.clicked.connect(self.__on_click_btn_send_status)
        self.btn_send_many_status.clicked.connect(self.__on_click_btn_send_many_status)
        group_layout = QVBoxLayout()

        # Connector ID
        conn_id_layout = QHBoxLayout()
        self.lbl_conn_id = QLabel('ConnectorId:')
        self.spin_conn_id = QSpinBox()
        self.spin_conn_id.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.spin_conn_id.setFixedWidth(150)
        conn_id_layout.addWidget(self.lbl_conn_id)
        conn_id_layout.addWidget(self.spin_conn_id)
        group_layout.addLayout(conn_id_layout)

        # Error code
        err_code_layout = QHBoxLayout()
        self.lbl_err_code = QLabel('ErrorCode:')
        self.cmb_err_code = QComboBox()
        for value in ChargePointErrorCode:
            self.cmb_err_code.addItem(str(value))
        self.cmb_err_code.setFixedWidth(150)
        err_code_layout.addWidget(self.lbl_err_code)
        err_code_layout.addWidget(self.cmb_err_code)
        group_layout.addLayout(err_code_layout)

        # Info
        info_layout = QHBoxLayout()
        self.lbl_info_code = QLabel('Info:')
        self.txt_info_code = QLineEdit()
        self.txt_info_code.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txt_info_code.setFixedWidth(150)
        info_layout.addWidget(self.lbl_info_code)
        info_layout.addWidget(self.txt_info_code)
        group_layout.addLayout(info_layout)

        # Status code
        sts_code_layout = QHBoxLayout()
        self.lbl_sts_code = QLabel('StatusCode:')
        self.cmb_sts_code = QComboBox()
        for value in ChargePointStatus:
            self.cmb_sts_code.addItem(str(value))
        self.cmb_sts_code.setFixedWidth(150)
        sts_code_layout.addWidget(self.lbl_sts_code)
        sts_code_layout.addWidget(self.cmb_sts_code)
        group_layout.addLayout(sts_code_layout)

        # time stamp
        time_stamp_layout = QHBoxLayout()
        self.lbl_time_stamp = QLabel('TimeStamp:')
        self.ck_time_stamp_status = QCheckBox()
        self.ck_time_stamp_status.setChecked(True)
        self.ck_time_stamp_status.setDisabled(True)
        self.time_spacer = QSpacerItem(80, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        time_stamp_layout.addWidget(self.lbl_time_stamp)
        time_stamp_layout.addSpacerItem(self.time_spacer)
        time_stamp_layout.addWidget(self.ck_time_stamp_status)
        group_layout.addLayout(time_stamp_layout)

        # Vendor ID
        vndr_id_layout = QHBoxLayout()
        self.lbl_vndr_id = QLabel('VendorID:')
        self.txt_vndr_id = QLineEdit()
        self.txt_vndr_id.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txt_vndr_id.setFixedWidth(150)
        vndr_id_layout.addWidget(self.lbl_vndr_id)
        vndr_id_layout.addWidget(self.txt_vndr_id)
        group_layout.addLayout(vndr_id_layout)

        # Vendor error code
        vndr_err_code_layout = QHBoxLayout()
        lbl_vndr_err_code = QLabel('VendorErrorCode:')
        self.txt_vndr_err_code = QLineEdit()
        self.txt_vndr_err_code.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txt_vndr_err_code.setFixedWidth(150)
        vndr_err_code_layout.addWidget(lbl_vndr_err_code)
        vndr_err_code_layout.addWidget(self.txt_vndr_err_code)
        group_layout.addLayout(vndr_err_code_layout)

        group_layout.addWidget(self.btn_send_status)
        group_layout.addWidget(self.btn_send_many_status)

        group.setLayout(group_layout)
        window_layout = QVBoxLayout()
        window_layout.addWidget(group)


        return window_layout

    def compose_start_transaction(self):
        group = QGroupBox('Start Transaction')
        group.setMaximumWidth(270)

        self.btn_send_start_transaction = QPushButton("Send")
        self.btn_send_start_transaction.clicked.connect(self.__on_click_btn_send_start_transaction)

        group_layout = QVBoxLayout()

        # Connector ID
        conn_id_layout = QHBoxLayout()
        lbl_conn_id_start_trasaction = QLabel('ConnectorId:')
        self.spin_conn_id_start_trasaction = QSpinBox()
        self.spin_conn_id_start_trasaction.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.spin_conn_id_start_trasaction.setFixedWidth(150)
        conn_id_layout.addWidget(lbl_conn_id_start_trasaction)
        conn_id_layout.addWidget(self.spin_conn_id_start_trasaction)
        group_layout.addLayout(conn_id_layout)

        # idTag
        idtag_layout = QHBoxLayout()
        lbl_idtag = QLabel('idTag:')
        self.txt_idtag = QLineEdit()
        self.txt_idtag.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txt_idtag.setFixedWidth(150)
        idtag_layout.addWidget(lbl_idtag)
        idtag_layout.addWidget(self.txt_idtag)
        group_layout.addLayout(idtag_layout)

        # Meter Start
        meter_start_layout = QHBoxLayout()
        lbl_idtag = QLabel('meterStart:')
        self.spin_meter_start = QSpinBox()
        self.spin_meter_start.setMaximum(9999999)
        self.spin_meter_start.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.spin_meter_start.setFixedWidth(150)
        meter_start_layout.addWidget(lbl_idtag)
        meter_start_layout.addWidget(self.spin_meter_start)
        group_layout.addLayout(meter_start_layout)

        # reservation Id
        reservation_id_layout = QHBoxLayout()
        lbl_resrvation_id = QLabel('reservationId:')
        self.spin_resrvation_id = QSpinBox()
        self.spin_resrvation_id.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.spin_resrvation_id.setFixedWidth(150)
        reservation_id_layout.addWidget(lbl_resrvation_id)
        reservation_id_layout.addWidget(self.spin_resrvation_id)
        group_layout.addLayout(reservation_id_layout)

        # timestamp
        time_stamp_layout = QHBoxLayout()
        lbl_time_stamp = QLabel('TimeStamp:')
        self.ck_time_stamp_start_transaction = QCheckBox()
        self.ck_time_stamp_start_transaction.setChecked(True)
        self.ck_time_stamp_start_transaction.setDisabled(True)
        self.time_spacer = QSpacerItem(80, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        time_stamp_layout.addWidget(lbl_time_stamp)
        time_stamp_layout.addSpacerItem(self.time_spacer)
        time_stamp_layout.addWidget(self.ck_time_stamp_start_transaction)
        group_layout.addLayout(time_stamp_layout)


        group_layout.addWidget(self.btn_send_start_transaction)

        group.setLayout(group_layout)
        window_layout = QVBoxLayout()
        window_layout.addWidget(group)


        return window_layout

    def compose_stop_transaction(self):
        group = QGroupBox('Stop Transaction')
        group.setMaximumWidth(270)

        self.btn_send_stop_transaction = QPushButton("Send")
        self.btn_send_stop_transaction.clicked.connect(self.__on_click_btn_send_stop_transaction)

        group_layout = QVBoxLayout()

        # idTag
        idtag_layout = QHBoxLayout()
        lbl_idtag = QLabel('idTag:')
        self.txt_idtag_stop_transaction = QLineEdit()
        self.txt_idtag_stop_transaction.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txt_idtag_stop_transaction.setFixedWidth(150)
        idtag_layout.addWidget(lbl_idtag)
        idtag_layout.addWidget(self.txt_idtag_stop_transaction)
        group_layout.addLayout(idtag_layout)

        # Meter Stop
        meter_start_layout = QHBoxLayout()
        lbl_idtag = QLabel('meterStop:')
        self.spin_meter_stop = QSpinBox()
        self.spin_meter_stop.setMaximum(9999999)
        self.spin_meter_stop.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.spin_meter_stop.setFixedWidth(150)
        meter_start_layout.addWidget(lbl_idtag)
        meter_start_layout.addWidget(self.spin_meter_stop)
        group_layout.addLayout(meter_start_layout)

        # time stamp
        time_stamp_layout = QHBoxLayout()
        lbl_time_stamp = QLabel('TimeStamp:')
        self.ck_time_stamp_stop_trasaction = QCheckBox()
        self.ck_time_stamp_stop_trasaction.setChecked(True)
        self.ck_time_stamp_stop_trasaction.setDisabled(True)
        time_spacer = QSpacerItem(80, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        time_stamp_layout.addWidget(lbl_time_stamp)
        time_stamp_layout.addSpacerItem(time_spacer)
        time_stamp_layout.addWidget(self.ck_time_stamp_stop_trasaction)
        group_layout.addLayout(time_stamp_layout)

        # transaction Id
        reservation_id_layout = QHBoxLayout()
        lbl_resrvation_id = QLabel('transactionId:')
        self.spin_transaction_id = QSpinBox() #ToDo: cargar automaticamente lo que se recibe de la start transaction
        self.spin_transaction_id.setMaximum(9999999)
        self.spin_transaction_id.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.spin_transaction_id.setFixedWidth(150)
        reservation_id_layout.addWidget(lbl_resrvation_id)
        reservation_id_layout.addWidget(self.spin_transaction_id)
        group_layout.addLayout(reservation_id_layout)

        # reason
        reservation_id_layout = QHBoxLayout()
        lbl_reason = QLabel('Reason:')
        self.cmb_reason= QComboBox()
        for value in Reason:
            self.cmb_reason.addItem(str(value))
        self.cmb_reason.setFixedWidth(150)
        reservation_id_layout.addWidget(lbl_reason)
        reservation_id_layout.addWidget(self.cmb_reason)
        group_layout.addLayout(reservation_id_layout)

        #ToDo: add transaction data

        group_layout.addWidget(self.btn_send_stop_transaction)

        group.setLayout(group_layout)
        window_layout = QVBoxLayout()
        window_layout.addWidget(group)

        return window_layout

    def compose_authorize(self):
        group = QGroupBox('Send authorization')
        group.setMaximumWidth(270)

        self.btn_send_authorization = QPushButton("Send")
        self.btn_send_authorization.clicked.connect(self.__on_click_btn_send_authorization)

        group_layout = QVBoxLayout()

        # idTag
        idtag_layout = QHBoxLayout()
        lbl_idtag = QLabel('idTag:')
        self.txt_idtag_authorize = QLineEdit()
        self.txt_idtag_authorize.setAlignment(Qt.AlignmentFlag.AlignRight)
        idtag_layout.addWidget(lbl_idtag)
        idtag_layout.addWidget(self.txt_idtag_authorize)
        group_layout.addLayout(idtag_layout)

        group_layout.addWidget(self.btn_send_authorization)

        group.setLayout(group_layout)
        window_layout = QVBoxLayout()
        window_layout.addWidget(group)

        return window_layout

    def compose_data_transfer(self):
        group = QGroupBox('Data transfer')
        group.setMaximumWidth(270)

        self.btn_send_data_transfer = QPushButton("Send")
        self.btn_send_data_transfer.clicked.connect(self.__on_click_btn_send_data_transfer)

        group_layout = QVBoxLayout()

        # vendorId
        vendor_id_layout = QHBoxLayout()
        lbl_vendorId = QLabel('vendorId:')
        self.txt_vendorId = QLineEdit()
        self.txt_vendorId.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txt_vendorId.setFixedWidth(150)
        vendor_id_layout.addWidget(lbl_vendorId)
        vendor_id_layout.addWidget(self.txt_vendorId)
        group_layout.addLayout(vendor_id_layout)

        # messageId
        message_id_layout = QHBoxLayout()
        lbl_messageId = QLabel('messageId:')
        self.txt_messageId = QLineEdit()
        self.txt_messageId.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txt_messageId.setFixedWidth(150)
        message_id_layout.addWidget(lbl_messageId)
        message_id_layout.addWidget(self.txt_messageId)
        group_layout.addLayout(message_id_layout)

        # data
        data_layout = QHBoxLayout()
        lbl_vendorId = QLabel('data:')
        self.txt_data = QLineEdit()
        self.txt_data.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txt_data.setFixedWidth(150)
        data_layout.addWidget(lbl_vendorId)
        data_layout.addWidget(self.txt_data)
        group_layout.addLayout(data_layout)

        group_layout.addWidget(self.btn_send_data_transfer)

        group.setLayout(group_layout)
        window_layout = QVBoxLayout()
        window_layout.addWidget(group)

        return window_layout

    def compose_diagnostic_status(self):
        group = QGroupBox('Diagnostics Stutus')
        group.setMaximumWidth(270)

        self.btn_send_diagnostics_status = QPushButton("Send")
        self.btn_send_diagnostics_status.clicked.connect(self.__on_click_btn_send_diagnostics_status)

        group_layout = QVBoxLayout()

        # status
        status_layout = QHBoxLayout()
        lbl_status = QLabel('Status:')
        self.cmb_status = QComboBox()
        for value in DiagnosticsStatus:
            self.cmb_status.addItem(str(value))
        self.cmb_status.setFixedWidth(150)
        status_layout.addWidget(lbl_status)
        status_layout.addWidget(self.cmb_status)
        group_layout.addLayout(status_layout)

        group_layout.addWidget(self.btn_send_diagnostics_status)

        group.setLayout(group_layout)
        window_layout = QVBoxLayout()
        window_layout.addWidget(group)

        return window_layout

    def compose_firmware_status(self):
        group = QGroupBox('Firmware Status')
        group.setMaximumWidth(270)

        self.btn_send_firmaware_status = QPushButton("Send")
        self.btn_send_firmaware_status.clicked.connect(self.__on_click_btn_send_firmware_status)

        group_layout = QVBoxLayout()

        # status
        status_layout = QHBoxLayout()
        lbl_status = QLabel('Status:')
        self.cmb_firmware_status = QComboBox()
        for value in FirmwareStatus:
            self.cmb_firmware_status.addItem(str(value))
        self.cmb_firmware_status.setFixedWidth(150)
        status_layout.addWidget(lbl_status)
        status_layout.addWidget(self.cmb_firmware_status)
        group_layout.addLayout(status_layout)

        group_layout.addWidget(self.btn_send_firmaware_status)

        group.setLayout(group_layout)
        window_layout = QVBoxLayout()
        window_layout.addWidget(group)

        return window_layout

    def compose_meter_value(self):
        group = QGroupBox('Meter value')
        group.setMaximumWidth(270)

        self.btn_send_meter_value = QPushButton("Send")
        self.btn_send_meter_value.clicked.connect(self.__on_click_btn_send_meter_values)

        group_layout = QVBoxLayout()

        # Connector ID
        conn_id_layout = QHBoxLayout()
        lbl_conn_id = QLabel('ConnectorId:')
        self.spin_conn_id_meter_value = QSpinBox()
        self.spin_conn_id_meter_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.spin_conn_id_meter_value.setFixedWidth(150)
        conn_id_layout.addWidget(lbl_conn_id)
        conn_id_layout.addWidget(self.spin_conn_id_meter_value)
        group_layout.addLayout(conn_id_layout)

        # Meter value
        value_layout = QHBoxLayout()
        lbl_value = QLabel('Value:')
        self.txt_meter_value = QLineEdit()
        self.txt_meter_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txt_meter_value.setFixedWidth(150)
        value_layout.addWidget(lbl_value)
        value_layout.addWidget(self.txt_meter_value)
        group_layout.addLayout(value_layout)

        # transaction Id
        reservation_id_layout = QHBoxLayout()
        lbl_resrvation_id = QLabel('transactionId:')
        self.txt_transaction_id_meter_value = QSpinBox() #ToDo: cargar automaticamente lo que se recibe de la start transaction
        self.txt_transaction_id_meter_value.setMaximum(9999999)
        self.txt_transaction_id_meter_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txt_transaction_id_meter_value.setFixedWidth(150)
        reservation_id_layout.addWidget(lbl_resrvation_id)
        reservation_id_layout.addWidget(self.txt_transaction_id_meter_value)
        group_layout.addLayout(reservation_id_layout)

        group_layout.addWidget(self.btn_send_meter_value)

        group.setLayout(group_layout)
        window_layout = QVBoxLayout()
        window_layout.addWidget(group)

        return window_layout
