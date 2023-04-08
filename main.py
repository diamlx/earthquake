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

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class WindowPlot(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(400, 300)

class WindowStart(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("/Users/themdq/Desktop/Diana/Журавлев/GUI/ui/open.ui", self)

        self.openButton.clicked.connect(self.open_file_dialog)
        self.actionOpen.triggered.connect(self.open_file_dialog)

    def open_file_dialog(self):
        # Открываем диалог выбора файла
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        # Устанавливаем выбранный файл в поле ввода
        self.path = file_path
        #self.label.setText(self.path)
        #self.input_field.setText(file_path)
        if self.path !='':
            self.wind = MainWindow(self.path)
            self.wind.show()
            self.close()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, path):
        super().__init__()
        uic.loadUi("/Users/themdq/Desktop/Diana/Журавлев/GUI/ui/main.ui", self)
        self.path = path
        self.initUI()

    def initUI(self):
        self.buildPlot.pressed.connect(self.build_plot)
        self.statusBar.showMessage(self.path)

    def build_plot(self):
        if self.path == '':
            self.show_warning()
            return
        plot_type = self.plotCombo.currentText()
        data = data_plot(plot_type, self.path)
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(data)
        toolbar = NavigationToolbar2QT(sc, self)
        self.window = WindowPlot(self)
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

    def calculate(self):
        # Получаем данные из поля ввода
        #input_data = self.input_field.text()
        # Рассчитываем результат
        result = self.path
        res, output_data = calc(result)
        self.label2.setText(str(res))
        print(output_data[0])
        output_data = str(output_data)
        self.output_label.setText(output_data)
        # Выводим результат
        #with open('output.csv', 'w', newline='') as file:
            #writer = csv.writer(file)
            #writer.writerows(output_data)


class PredictWindow(QtWidgets.QMainWindow):
    def __init__(self, path):
        super().__init__()
        uic.loadUi("/Users/themdq/Desktop/Diana/Журавлев/GUI/ui/prediction.ui", self)
        self.path = path
        self.initUI()

    def initUI(self):
        self.buildPlot.pressed.connect(self.build_plot)
        self.statusBar.showMessage('Test')

    def build_plot(self):
        if self.path == '':
            self.show_warning()
            return
        plot_type = self.plotCombo.currentText()
        data = data_plot(plot_type, self.path)
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(data)
        toolbar = NavigationToolbar2QT(sc, self)
        self.window = WindowPlot(self)
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

    def calculate(self):
        # Получаем данные из поля ввода
        #input_data = self.input_field.text()
        # Рассчитываем результат
        result = self.path
        res, output_data = calc(result)
        self.label2.setText(str(res))
        print(output_data[0])
        output_data = str(output_data)
        self.output_label.setText(output_data)
        # Выводим результат
        #with open('output.csv', 'w', newline='') as file:
            #writer = csv.writer(file)
            #writer.writerows(output_data)

app = QtWidgets.QApplication(sys.argv)
window = WindowStart()
window.show()
app.exec()
