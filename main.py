import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFileDialog, QMessageBox
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QMainWindow, QTabWidget, QHBoxLayout, QSizePolicy
from calc import calc
#import csv

import folium
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
import pandas as pd


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Earthquake Prediction') # название программы

        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(10, 10, 280, 180)

        # Создаем первую вкладку
        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1, "Tab 1")
        # Добавляем виджеты на первую вкладку
        layout1 = QVBoxLayout()
        label1 = QLabel("This is tab 1")
        layout1.addWidget(label1)
        self.tab1.setLayout(layout1)
        # Добавляем поле для ввода данных
        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(10, 10, 280, 30)
        layout1.addWidget(self.input_field)
        # Добавляем кнопку для выбора файла
        self.file_button = QPushButton('Выбрать файл', self)
        self.file_button.setGeometry(10, 50, 100, 30)
        self.file_button.clicked.connect(self.open_file_dialog)
        layout1.addWidget(self.file_button)

        # Добавляем кнопку "Рассчитать"
        self.calculate_button = QPushButton('Рассчитать', self)
        self.calculate_button.setGeometry(120, 50, 100, 30)
        self.calculate_button.clicked.connect(self.calculate)
        layout1.addWidget(self.calculate_button)
        self.output_label = QLabel('Вывод:')
        self.output_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout1.addWidget(self.output_label)

        # Создаем вторую вкладку
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2, "Tab 2")
        # Добавляем виджеты на вторую вкладку
        layout2 = QHBoxLayout()
        self.label2 = QLabel("This is tab 2")
        layout2.addWidget(self.label2)
        self.tab2.setLayout(layout2)




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
        res, output_data = calc.calc(result)
        self.label2.setText(str(res))
        print(output_data[0])
        output_data = str(output_data)
        self.output_label.setText(output_data)
        self.output_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # Выводим результат
        #with open('output.csv', 'w', newline='') as file:
            #writer = csv.writer(file)
            #writer.writerows(output_data)


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



class MapWidget(QWidget):
    def __init__(self, data):
        super().__init__()

        # Создаем карту
        map = folium.Map(location=[30, 0], zoom_start=2)

        # Добавляем маркеры на карту
        for index, row in data.iterrows():
            folium.Marker(location=[row['Широта'], row['Долгота']], popup=row['Город'] + ': ' + str(row['Значение'])).add_to(map)

        # Сохраняем карту в виде HTML-страницы
        map.save('map.html')

        # Создаем виджет QWebEngineView и загружаем в него HTML-страницу с картой
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl.fromLocalFile('/Users/themdq/Desktop/Diana/Журавлев/GUI/map.html'))

        # Создаем вертикальный макет и добавляем в него виджет QWebEngineView
        layout = QVBoxLayout()
        layout.addWidget(self.web_view)

        # Устанавливаем макет для виджета
        self.setLayout(layout)

# Создаем DataFrame с данными
data = pd.DataFrame({
    'Город': ['Москва', 'Пекин', 'Нью-Йорк'],
    'Широта': [55.7558, 39.9042, 40.7128],
    'Долгота': [37.6173, 116.4074, -74.0060],
    'Значение': [10, 20, 30]
})


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapWidget(data)
    window = MyApp()
    window.show()
    #ex.show()
    sys.exit(app.exec())
