from PyQt5 import QtWidgets, QtCore
from uimainwindow import Ui_MainWindow
import mysql.connector
import pandas as pd
import plotly.express as px
from threading import Thread

class mainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)


        self.date_date_to_plot.setDate(QtCore.QDate.currentDate())
        self.btn_generate_reports.clicked.connect(self.plot_hilo)

    def plot_hilo(self):
        self.plotter = Thread(name='plotter', target=self.plot())
        self.plotter.start()

    def plot(self):
        try:

            if str(self.txt_db_host.text()) != '___EXAMPLE___':
                conn = mysql.connector.connect(
                    host=str(self.txt_db_host.text()),
                    user=str(self.txt_db_user.text()),
                    password=str(self.txt_db_password.text()),
                    database=str(self.txt_db_name.text())
                )
            else:
                conn = mysql.connector.connect(
                    host="bpjw2jhdw82qumm9x3v4-mysql.services.clever-cloud.com",
                    user="u5mmyp6f1gmj5qn8",
                    password="iRyoRHLgv587a8lqVXAA",
                    database="bpjw2jhdw82qumm9x3v4"
                )
            print(str(self.txt_db_host.text()),
               str(self.txt_db_user.text()),
               str(self.txt_db_password.text()),
               str(self.txt_db_name.text()))

        except:
            self.error_msg("Error conectando a la base de datos")
            return None


        try:
            c1 = conn.cursor()
            cquery = "SELECT * FROM `sensores` WHERE `dia` = (%s)"
            cvalue = (self.date_date_to_plot.date().toString("dd.MM.yyyy"),)
            print(cvalue)
            c1.execute(cquery, cvalue)
            a = c1.rowcount
            values = []
            for value in c1.fetchall():
              value = list(value)
              value[0] = str('Sensor: ' + value[0])
              values.append(value)

        except:
            self.error_msg("Error al traer informacion de la base de datos")
            return None

        try:
            df = pd.DataFrame(values, columns=['Sensor', 'Fecha', 'Hora', 'Humedad', 'Temperatura', 'Latitud', 'Longitud'])
            df['Latitud'] = df['Latitud'].astype(float)
            df['Longitud'] = df['Longitud'].astype(float)
            print(df)
            print(df.dtypes)
        except:
            self.error_msg("Error el procesar los datos")
            return None

        try:
            fig = px.scatter_mapbox(df, lat="Latitud", lon="Longitud", hover_name="Sensor",
                                    hover_data=['Fecha', 'Hora', 'Humedad',
                                                'Temperatura', 'Latitud',
                                                'Longitud'],
                                    color_discrete_sequence=["fuchsia"], zoom=3, height=900)

            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            fig.show()
        except:
            self.error_msg("Error al mapear datos")
            return None
    def error_msg(self,message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec_()
