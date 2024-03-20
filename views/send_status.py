from PyQt6.QtWidgets import (QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QSpinBox,
                             QGroupBox, QComboBox, QCheckBox, QSpacerItem, QSizePolicy)
from ocpp.v16.enums import ChargePointStatus, ChargePointErrorCode
from PyQt6.QtCore import Qt

class StatusNotificationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.compose_window()
        self.btn_send_status.clicked.connect(self.__on_click_btn_send_status)


    def __on_click_btn_send_status(self):
        pass

    def __populate_cmb_err_code(self):
        for value in ChargePointErrorCode:
            self.cmb_err_code.addItem(str(value))

    def __populate_cmb_sts_code(self):
        for value in ChargePointStatus:
            self.cmb_sts_code.addItem(str(value))

    def compose_window(self):
        self.resize(400, 250)
        self.setWindowTitle('Send Status')

        group = QGroupBox('Propiedades')
        self.group_layout = QVBoxLayout()
        self.btn_send_status = QPushButton('Enviar estado')

        # Connector ID
        conn_id_layout = QHBoxLayout()
        self.lbl_conn_id = QLabel('ConnectorId:')
        self.spin_conn_id = QSpinBox()
        self.spin_conn_id.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.spin_conn_id.setFixedWidth(150)
        conn_id_layout.addWidget(self.lbl_conn_id)
        conn_id_layout.addWidget(self.spin_conn_id)
        self.group_layout.addLayout(conn_id_layout)

        # Error code
        err_code_layout = QHBoxLayout()
        self.lbl_err_code = QLabel('ErrorCode:')
        self.cmb_err_code = QComboBox()
        self.__populate_cmb_err_code()
        self.cmb_err_code.setFixedWidth(150)
        err_code_layout.addWidget(self.lbl_err_code)
        err_code_layout.addWidget(self.cmb_err_code)
        self.group_layout.addLayout(err_code_layout)

        # Info
        info_layout = QHBoxLayout()
        self.lbl_info_code = QLabel('Info:')
        self.txt_info_code = QLineEdit()
        self.txt_info_code.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txt_info_code.setFixedWidth(150)
        info_layout.addWidget(self.lbl_info_code)
        info_layout.addWidget(self.txt_info_code)
        self.group_layout.addLayout(info_layout)

        # Status code
        sts_code_layout = QHBoxLayout()
        self.lbl_sts_code = QLabel('StatusCode:')
        self.cmb_sts_code = QComboBox()
        self.__populate_cmb_sts_code()
        self.cmb_sts_code.setFixedWidth(150)
        sts_code_layout.addWidget(self.lbl_sts_code)
        sts_code_layout.addWidget(self.cmb_sts_code)
        self.group_layout.addLayout(sts_code_layout)

        # time stamp
        time_stamp_layout = QHBoxLayout()
        self.lbl_time_stamp = QLabel('TimeStamp:')
        self.ck_time_stamp_id = QCheckBox()
        self.time_spacer = QSpacerItem(190, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        time_stamp_layout.addWidget(self.lbl_time_stamp)
        time_stamp_layout.addSpacerItem(self.time_spacer)
        time_stamp_layout.addWidget(self.ck_time_stamp_id)
        self.group_layout.addLayout(time_stamp_layout)

        # Vendor ID
        vndr_id_layout = QHBoxLayout()
        self.lbl_vndr_id = QLabel('VendorID:')
        self.txt_vndr_id = QLineEdit()
        self.txt_vndr_id.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txt_vndr_id.setFixedWidth(150)
        vndr_id_layout.addWidget(self.lbl_vndr_id)
        vndr_id_layout.addWidget(self.txt_vndr_id)
        self.group_layout.addLayout(vndr_id_layout)

        # Vendor error code
        vndr_err_code_layout = QHBoxLayout()
        self.lbl_vndr_err_code = QLabel('VendorErrorCode:')
        self.txt_vndr_err_code = QLineEdit()
        self.txt_vndr_err_code.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txt_vndr_err_code.setFixedWidth(150)
        vndr_err_code_layout.addWidget(self.lbl_vndr_err_code)
        vndr_err_code_layout.addWidget(self.txt_vndr_err_code)
        self.group_layout.addLayout(vndr_err_code_layout)

        group.setLayout(self.group_layout)

        window_layout = QVBoxLayout()
        window_layout.addWidget(group)
        window_layout.addWidget(self.btn_send_status)

        central_widget = QWidget()
        central_widget.setLayout(window_layout)
        self.setCentralWidget(central_widget)