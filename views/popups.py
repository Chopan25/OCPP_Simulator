from PyQt6.QtWidgets import QMessageBox

class ErrorPopUp:
    def __init__(self,message):
        # Create and configure the error message box
        error_message = QMessageBox()
        error_message.setIcon(QMessageBox.Icon.Critical)  # Set the icon to Information (i)
        error_message.setWindowTitle("Error")  # Set the window title
        error_message.setText(str(message))  # Set the main text of the message
        error_message.setStandardButtons(QMessageBox.StandardButton.Ok)  # Set the standard Ok button

        # Display the message box
        error_message.exec()

class InformationPopUp:
    def __init__(self,message):
        # Create and configure the error message box
        error_message = QMessageBox()
        error_message.setIcon(QMessageBox.Icon.Information)  # Set the icon to Information (i)
        error_message.setWindowTitle("Info")  # Set the window title
        error_message.setText(str(message))  # Set the main text of the message
        error_message.setStandardButtons(QMessageBox.StandardButton.Ok)  # Set the standard Ok button

        # Display the message box
        error_message.exec()