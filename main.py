import sys
import csv
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFileDialog, QMessageBox,QWidgetAction
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QMainWindow, QTabWidget, QHBoxLayout, QSizePolicy,QToolBar
from PyQt6 import uic, QtCore, QtGui,QtWidgets
from calc.calc import data_plot, calc
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')

"""
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Earthquake Prediction') # название программы

        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(10, 10, 280, 180)
        self.tabs.setMovable(True)


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
        #input_data = self.input_field.text()

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




if __name__ == '__main__':
    app = QApplication(sys.argv)
    #ex = MapWidget(data)
    #ex.show()
    window = MyApp()
    window.show()
    sys.exit(app.exec())
"""

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class Window_2(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(200, 215)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("/Users/themdq/Desktop/Diana/Журавлев/test.ui", self)
        self.path = ''
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Earthquake Prediction')  # название программы
        self.actionOpen.triggered.connect(self.open_file_dialog)
        self.buildPlot.pressed.connect(self.build_plot)



    def open_file_dialog(self):
        # Открываем диалог выбора файла
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        # Устанавливаем выбранный файл в поле ввода
        self.path = file_path
        self.label.setText(self.path)
        #self.input_field.setText(file_path)



    def build_plot(self):
        if self.path == '':
            self.show_warning()
            return
        plot_type = self.plotCombo.currentText()
        data = data_plot(plot_type, self.path)
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(data)
        toolbar = NavigationToolbar2QT(sc, self)
        self.window = Window_2(self)
        self.window.layout = QtWidgets.QVBoxLayout()
        self.window.layout.addWidget(toolbar)
        self.window.layout.addWidget(sc)
        self.window.widget = QtWidgets.QWidget()
        self.window.widget.setLayout(self.window.layout)
        self.window.setCentralWidget(self.window.widget)
        self.window.setWindowTitle(plot_type)
        self.window.show()

    def show_warning(self):
        msg = QMessageBox()
        msg.setWindowTitle("Файл не выбран")
        msg.setText("Файл не выбран! Выберите файл при помощи меню.")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.exec()




app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
