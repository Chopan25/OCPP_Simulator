import time
from utils import cache_string, get_cached_strings
from PyQt6.QtWidgets import (QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QSpinBox,
                             QGroupBox, QComboBox, QCheckBox, QSpacerItem, QSizePolicy, QCompleter)
from websockets_controller import OCPPThread
from views.send_status import StatusNotificationWindow
from ocpp.v16.enums import ChargePointStatus, ChargePointErrorCode
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


    # other methods
    def close_event(self):
        self.ocpp_thread.join()

    # composers
    def compose_window(self):
        self.setWindowTitle('OCPP Simulator')
        self.resize(800, 600)

        #call all composers
        connections_layout = self.compose_connection()
        button_layout = self.compose_buttons_column()
        status_layout = self.compose_status()

        columns_layout = QHBoxLayout()
        columns_layout.addLayout(button_layout)
        columns_layout.addLayout(status_layout)

        main_layout = QVBoxLayout()
        main_layout.addLayout(connections_layout)
        main_layout.addLayout(columns_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def compose_connection(self):
        self.lbl_url = QLabel('Ingrese los datos de coneccion a su sitema.')
        self.txt_url = QLineEdit()
        self.url_completer = QCompleter(get_cached_strings('urls'))
        self.txt_url.setCompleter(self.url_completer)
        self.txt_url.setPlaceholderText('URL de su sitema central')
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

        return buttons_layout

    def compose_status(self):
        group = QGroupBox('Status Notifications')

        self.btn_send_status = QPushButton("Send Status")
        self.btn_send_status.clicked.connect(self.__on_click_btn_send_status)

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
        self.ck_time_stamp_id = QCheckBox()
        self.time_spacer = QSpacerItem(190, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        time_stamp_layout.addWidget(self.lbl_time_stamp)
        time_stamp_layout.addSpacerItem(self.time_spacer)
        time_stamp_layout.addWidget(self.ck_time_stamp_id)
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

        group.setLayout(group_layout)
        window_layout = QVBoxLayout()
        window_layout.addWidget(group)


        return window_layout