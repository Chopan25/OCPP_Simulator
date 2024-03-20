import sys
import asyncio
import threading
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
import websockets_controller

class WsThread(threading.Thread):
    message_received = asyncio.Queue()

    def __init__(self):
        super().__init__()
        self.url = None
        self.loop = asyncio.new_event_loop()
        self.websocket = None

    def run(self):
        async def ws_handler():
            self.websocket = await websockets.connect(self.url)
            while True:
                message = await self.websocket.recv()
                await self.message_received.put(message)
                print(message)
                window.label_messages.setText(message)

        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(ws_handler())

    def send_message(self, message):
        if self.websocket:
            asyncio.run_coroutine_threadsafe(self.websocket.send(message), self.loop)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label_received = QLabel("Received Messages:")
        self.label_messages = QLabel("")
        self.button_send = QPushButton("Send Message")
        self.button_send.clicked.connect(self.send_ws_message)
        self.button_connect = QPushButton("Connect")
        self.button_connect.clicked.connect(self.connect_ws_server)

        layout = QVBoxLayout()
        layout.addWidget(self.label_received)
        layout.addWidget(self.label_messages)
        layout.addWidget(self.button_send)
        layout.addWidget(self.button_connect)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.ws_thread = WsThread()

    def connect_ws_server(self):
        self.ws_thread.url = "ws://localhost:8765"
        self.ws_thread.start()
        print('connected')

    def send_ws_message(self):
        message = "Hello, WebSocket!"
        self.ws_thread.send_message(message)
        print('message sent')

    def closeEvent(self, event):
        self.ws_thread.loop.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
