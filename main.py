import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFileDialog, QMessageBox
from calc import calc

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Earthquake Prediction') # название программы

        # Добавляем поле для ввода данных
        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(10, 10, 280, 30)

        # Добавляем кнопку для выбора файла
        self.file_button = QPushButton('Выбрать файл', self)
        self.file_button.setGeometry(10, 50, 100, 30)
        self.file_button.clicked.connect(self.open_file_dialog)

        # Добавляем кнопку "Рассчитать"
        self.calculate_button = QPushButton('Рассчитать', self)
        self.calculate_button.setGeometry(120, 50, 100, 30)
        self.calculate_button.clicked.connect(self.calculate)

        # Добавляем кнопку "Выход"
        self.exit_button = QPushButton('Выход', self)
        self.exit_button.setGeometry(220, 50, 70, 30)
        self.exit_button.clicked.connect(self.close)

    def open_file_dialog(self):
        # Открываем диалог выбора файла
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        # Устанавливаем выбранный файл в поле ввода
        self.path = file_path
        self.input_field.setText(file_path)

    def calculate(self):
        # Получаем данные из поля ввода
        input_data = self.input_field.text()

        # Рассчитываем результат
        result = self.path
        calc.calc(result)
        # Выводим результат
        print(result)

    def closeEvent(self, event):
        # Создаем диалог подтверждения выхода из программы
        reply = QMessageBox.question(self, 'Подтверждение выхода', 'Вы уверены, что хотите выйти?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # Закрываем приложение
            self.close()
        else:
            # Отменяем закрытие приложения
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec())
